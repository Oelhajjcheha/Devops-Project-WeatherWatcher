import os
import re
import logging
from fastapi import FastAPI, HTTPException, Query, Path
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import httpx

# Load environment variables from .env file (for local development)
from dotenv import load_dotenv
load_dotenv()

# Import weather service
from app.services.weather_service import (
    WeatherService,
    WeatherData,
    CityNotFoundError,
    WeatherAPIError,
    APIKeyMissingError,
)

# -----------------------------------------------
# Application Insights (OpenCensus)
# -----------------------------------------------
from opencensus.ext.azure.log_exporter import AzureLogHandler
from opencensus.ext.azure.trace_exporter import AzureExporter
from opencensus.trace.samplers import ProbabilitySampler
from opencensus.trace.tracer import Tracer


# -----------------------------------------------
# Application Insights Setup
# -----------------------------------------------
conn_str = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")

if conn_str:
    # ENABLE Application Insights (Azure)
    logger = logging.getLogger(__name__)
    logger.addHandler(AzureLogHandler(connection_string=conn_str))
    logger.setLevel(logging.INFO)

    tracer = Tracer(
        exporter=AzureExporter(connection_string=conn_str),
        sampler=ProbabilitySampler(1.0)
    )
else:
    # DISABLE Insights during tests (GitHub Actions)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    
# -------------------------------------------
# Custom Telemetry Helper
# -------------------------------------------
def track_weather_search(logger, city: str, success: bool, temperature: int = None):
    """
    Sends custom telemetry about weather searches.
    """
    logger.info(
        "Weather search executed",
        extra={
            "custom_dimensions": {
                "city": city,
                "success": success,
                "temperature": temperature
            }
        }
    )

# -----------------------------------------------
# FastAPI App
# -----------------------------------------------
app = FastAPI(title="Weather Watcher", version="0.1.0")

# Enable CORS for frontend API calls
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <!-- Meta tags for SEO and mobile optimization -->
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="description" content="Weather Watcher - Get real-time weather information for any city">
        <meta name="keywords" content="weather, forecast, temperature, humidity">
        <title>Weather Watcher - Real-Time Weather Forecast</title>
        
        <!-- Font Awesome CDN for weather icons -->
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" 
              integrity="sha512-iecdLmaskl7CVkqkXNQ/ZH/XLlvWZOJyj7Yy7tcenmpD1ypASozpmT/E0iPtmFIB46ZmdtAc9eNBvH0H/ZpiBw==" 
              crossorigin="anonymous" referrerpolicy="no-referrer" />
        
        <style>
            /* ============================================
               RESET & BASE STYLES
               ============================================ */
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            /* Smooth scrolling and font rendering */
            html {
                scroll-behavior: smooth;
                -webkit-font-smoothing: antialiased;
                -moz-osx-font-smoothing: grayscale;
            }
            
            /* ============================================
               DARK THEME COLOR PALETTE
               ============================================ */
            :root {
                --bg-primary: #0a0a0f;
                --bg-secondary: #12121a;
                --bg-card: #1a1a24;
                --text-primary: #e8e8f0;
                --text-secondary: #a0a0b0;
                --accent-primary: #4a9eff;
                --accent-secondary: #6b8eff;
                --success: #10d876;
                --error: #ff4757;
                --border: #2a2a3a;
                --shadow: rgba(0, 0, 0, 0.5);
            }
            
            /* ============================================
               BODY & BACKGROUND
               ============================================ */
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 
                             'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
                background: var(--bg-primary);
                color: var(--text-primary);
                min-height: 100vh;
                padding: 20px;
                position: relative;
                overflow-x: hidden;
            }
            
            /* Animated gradient background overlay */
            body::before {
                content: '';
                position: fixed;
                top: -50%;
                left: -50%;
                width: 200%;
                height: 200%;
                background: radial-gradient(circle at 20% 50%, rgba(74, 158, 255, 0.08) 0%, transparent 50%),
                            radial-gradient(circle at 80% 80%, rgba(107, 142, 255, 0.06) 0%, transparent 50%);
                animation: gradientShift 20s ease infinite;
                z-index: 0;
                pointer-events: none;
            }
            
            /* Smooth gradient animation */
            @keyframes gradientShift {
                0%, 100% { transform: translate(0, 0) rotate(0deg); }
                50% { transform: translate(-5%, -5%) rotate(180deg); }
            }
            
            /* ============================================
               MAIN CONTAINER
               ============================================ */
            .container {
                max-width: 700px;
                width: 100%;
                margin: 0 auto;
                position: relative;
                z-index: 1;
            }
            
            /* ============================================
               HEADER SECTION
               ============================================ */
            header {
                text-align: center;
                margin-bottom: 40px;
                animation: fadeInUp 0.6s ease;
            }
            
            h1 {
                color: var(--text-primary);
                font-size: 2.5rem;
                font-weight: 700;
                margin-bottom: 8px;
                letter-spacing: -0.02em;
                background: linear-gradient(135deg, var(--text-primary) 0%, var(--accent-primary) 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }
            
            /* Fade in animation */
            @keyframes fadeInUp {
                from {
                    opacity: 0;
                    transform: translateY(10px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            /* ============================================
               SEARCH FORM SECTION
               ============================================ */
            .search-section {
                background: var(--bg-card);
                padding: 32px;
                border-radius: 20px;
                border: 1px solid var(--border);
                box-shadow: 0 20px 60px var(--shadow),
                            0 0 0 1px rgba(255, 255, 255, 0.02) inset;
                margin-bottom: 24px;
                backdrop-filter: blur(10px);
                animation: fadeInUp 0.6s ease 0.1s both;
            }
            
            .search-form {
                display: flex;
                gap: 12px;
            }
            
            .search-input {
                flex: 1;
                padding: 14px 20px;
                background: var(--bg-secondary);
                border: 1px solid var(--border);
                border-radius: 12px;
                color: var(--text-primary);
                font-size: 1rem;
                outline: none;
                transition: all 0.3s ease;
            }
            
            .search-input:focus {
                border-color: var(--accent-primary);
                box-shadow: 0 0 0 3px rgba(74, 158, 255, 0.1);
            }
            
            .search-input::placeholder {
                color: var(--text-secondary);
            }
            
            .search-button {
                padding: 14px 32px;
                background: linear-gradient(135deg, var(--accent-primary) 0%, var(--accent-secondary) 100%);
                border: none;
                border-radius: 12px;
                color: white;
                font-size: 1rem;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
                display: flex;
                align-items: center;
                gap: 8px;
            }
            
            .search-button:hover:not(:disabled) {
                transform: translateY(-2px);
                box-shadow: 0 8px 20px rgba(74, 158, 255, 0.3);
            }
            
            .search-button:disabled {
                opacity: 0.6;
                cursor: not-allowed;
            }
            
            /* ============================================
               WEATHER DISPLAY SECTION
               ============================================ */
            .weather-display {
                background: var(--bg-card);
                padding: 40px;
                border-radius: 20px;
                border: 1px solid var(--border);
                box-shadow: 0 20px 60px var(--shadow),
                            0 0 0 1px rgba(255, 255, 255, 0.02) inset;
                backdrop-filter: blur(10px);
                display: none;
                animation: fadeInUp 0.6s ease;
            }
            
            .weather-display.show {
                display: block;
            }
            
            .weather-header {
                display: flex;
                justify-content: space-between;
                align-items: flex-start;
                margin-bottom: 32px;
            }
            
            .weather-location {
                flex: 1;
            }
            
            .weather-city {
                font-size: 2rem;
                font-weight: 700;
                color: var(--text-primary);
                margin-bottom: 4px;
            }
            
            .weather-country {
                font-size: 1rem;
                color: var(--text-secondary);
            }
            
            .weather-icon {
                font-size: 5rem;
                color: var(--accent-primary);
                line-height: 1;
            }
            
            .weather-main {
                text-align: center;
                margin-bottom: 32px;
            }
            
            .weather-temp {
                font-size: 4rem;
                font-weight: 700;
                color: var(--text-primary);
                margin-bottom: 8px;
                line-height: 1;
            }
            
            .weather-description {
                font-size: 1.2rem;
                color: var(--text-secondary);
                text-transform: capitalize;
                margin-bottom: 16px;
            }
            
            .weather-feels-like {
                font-size: 0.9rem;
                color: var(--text-secondary);
            }
            
            .weather-details {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
                gap: 20px;
                margin-top: 32px;
            }
            
            .weather-detail-item {
                display: flex;
                flex-direction: column;
                align-items: center;
                padding: 20px;
                background: var(--bg-secondary);
                border-radius: 12px;
                border: 1px solid var(--border);
            }
            
            .weather-detail-label {
                font-size: 0.85rem;
                color: var(--text-secondary);
                margin-bottom: 8px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            
            .weather-detail-value {
                font-size: 1.5rem;
                font-weight: 600;
                color: var(--text-primary);
            }
            
            .weather-detail-icon {
                font-size: 1.5rem;
                color: var(--accent-primary);
                margin-bottom: 8px;
            }
            
            /* ============================================
               LOADING ANIMATION
               ============================================ */
            .loading {
                display: none;
                text-align: center;
                padding: 40px;
                animation: fadeInUp 0.6s ease;
            }
            
            .loading.show {
                display: block;
            }
            
            .spinner {
                width: 50px;
                height: 50px;
                border: 4px solid var(--border);
                border-top-color: var(--accent-primary);
                border-radius: 50%;
                margin: 0 auto 20px;
                animation: spin 1s linear infinite;
            }
            
            @keyframes spin {
                to { transform: rotate(360deg); }
            }
            
            .loading-text {
                color: var(--text-secondary);
                font-size: 1rem;
            }
            
            /* ============================================
               ERROR MESSAGE
               ============================================ */
            .error-message {
                display: none;
                background: rgba(255, 71, 87, 0.1);
                border: 1px solid var(--error);
                border-radius: 12px;
                padding: 20px;
                margin-bottom: 24px;
                color: var(--error);
                text-align: center;
                animation: fadeInUp 0.6s ease;
            }
            
            .error-message.show {
                display: block;
            }
            
            .error-message i {
                margin-right: 8px;
            }
            
            .retry-button {
                margin-top: 12px;
                padding: 8px 20px;
                background: var(--error);
                border: none;
                border-radius: 8px;
                color: white;
                font-size: 0.9rem;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
            }
            
            .retry-button:hover {
                background: #ff3838;
                transform: translateY(-1px);
            }
            
            /* ============================================
               RESPONSIVE DESIGN - TABLET
               ============================================ */
            @media (max-width: 768px) {
                .container {
                    max-width: 100%;
                }
                
                h1 {
                    font-size: 2rem;
                }
                
                .search-section {
                    padding: 24px;
                }
                
                .weather-display {
                    padding: 32px 24px;
                }
                
                .weather-temp {
                    font-size: 3rem;
                }
                
                .weather-icon {
                    font-size: 4rem;
                }
            }
            
            /* ============================================
               RESPONSIVE DESIGN - MOBILE
               ============================================ */
            @media (max-width: 640px) {
                body {
                    padding: 12px;
                }
                
                header {
                    margin-bottom: 24px;
                }
                
                h1 {
                    font-size: 1.75rem;
                }
                
                .search-section {
                    padding: 20px;
                    border-radius: 16px;
                }
                
                .search-form {
                    flex-direction: column;
                }
                
                .search-button {
                    width: 100%;
                    justify-content: center;
                }
                
                .weather-display {
                    padding: 24px 20px;
                    border-radius: 16px;
                }
                
                .weather-header {
                    flex-direction: column;
                    align-items: center;
                    text-align: center;
                    margin-bottom: 24px;
                }
                
                .weather-city {
                    font-size: 1.5rem;
                }
                
                .weather-temp {
                    font-size: 2.5rem;
                }
                
                .weather-icon {
                    font-size: 3.5rem;
                }
                
                .weather-details {
                    grid-template-columns: repeat(2, 1fr);
                    gap: 12px;
                }
                
                .weather-detail-item {
                    padding: 16px;
                }
                
                .weather-detail-value {
                    font-size: 1.25rem;
                }
            }
            
            /* ============================================
               SMOOTH TRANSITIONS
               ============================================ */
            * {
                transition: color 0.2s ease, background-color 0.2s ease;
            }
            /* Autocomplete Dropdown */
.autocomplete-wrapper {
    position: relative;
    flex: 1;
}

.autocomplete-dropdown {
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-top: none;
    border-radius: 0 0 12px 12px;
    max-height: 300px;
    overflow-y: auto;
    z-index: 1000;
    box-shadow: 0 8px 24px var(--shadow);
    margin-top: -12px;
    padding-top: 12px;
    display: none;
}

.autocomplete-dropdown.show {
    display: block;
    animation: slideDown 0.2s ease;
}

@keyframes slideDown {
    from { opacity: 0; transform: translateY(-10px); }
    to { opacity: 1; transform: translateY(0); }
}

.autocomplete-item {
    padding: 12px 20px;
    cursor: pointer;
    transition: background 0.2s ease;
    color: var(--text-primary);
    font-size: 0.95rem;
    display: flex;
    align-items: center;
    gap: 8px;
}

.autocomplete-item:hover,
.autocomplete-item.active {
    background: var(--bg-secondary);
}

.autocomplete-item i {
    color: var(--text-secondary);
    font-size: 0.9rem;
}

.autocomplete-loading,
.autocomplete-empty {
    padding: 12px 20px;
    text-align: center;
    color: var(--text-secondary);
    font-size: 0.9rem;
}

        </style>
        </style>
        </style>
    </head>
    <body>
        <!-- Main container for semantic structure -->
        <div class="container">
            <!-- Header section with title -->
            <header>
                <h1><i class="fas fa-cloud-sun"></i> Weather Watcher</h1>
            </header>
            
            <!-- Search form section -->
<section class="search-section" aria-label="Search for weather">
    <form class="search-form" id="weatherForm" role="search">
        <div class="autocomplete-wrapper">
            <input
                type="text"
                class="search-input"
                id="cityInput"
                placeholder="Enter city name (e.g., Madrid, Tokyo, New York...)"
                aria-label="City name"
                required
                autocomplete="off"
            >
            <div id="autocompleteDropdown" class="autocomplete-dropdown"></div>
        </div>
        <button type="submit" class="search-button" id="searchButton" aria-label="Search weather">
            <i class="fas fa-search" aria-hidden="true"></i>
            <span>Search</span>
        </button>
    </form>
</section>
            
            <!-- Error message container -->
            <div class="error-message" id="errorMessage" role="alert" aria-live="polite">
                <i class="fas fa-exclamation-circle"></i>
                <span id="errorText"></span>
                <button class="retry-button" id="retryButton" style="display: none;">Retry</button>
            </div>
            
            <!-- Loading animation container -->
            <div class="loading" id="loading" aria-live="polite" aria-busy="true">
                <div class="spinner" aria-hidden="true"></div>
                <p class="loading-text">Fetching weather data...</p>
            </div>
            
            <!-- Weather display section -->
            <section class="weather-display" id="weatherDisplay" aria-label="Weather information">
                <div class="weather-header">
                    <div class="weather-location">
                        <h2 class="weather-city" id="weatherCity"></h2>
                        <p class="weather-country" id="weatherCountry"></p>
                    </div>
                    <div class="weather-icon" id="weatherIcon" aria-hidden="true"></div>
                </div>
                
                <div class="weather-main">
                    <div class="weather-temp" id="weatherTemp"></div>
                    <p class="weather-description" id="weatherDescription"></p>
                    <p class="weather-feels-like" id="weatherFeelsLike"></p>
                </div>
                
                <div class="weather-details" role="list">
                    <div class="weather-detail-item" role="listitem">
                        <i class="fas fa-tint weather-detail-icon" aria-hidden="true"></i>
                        <span class="weather-detail-label">Humidity</span>
                        <span class="weather-detail-value" id="weatherHumidity"></span>
                    </div>
                    <div class="weather-detail-item" role="listitem">
                        <i class="fas fa-wind weather-detail-icon" aria-hidden="true"></i>
                        <span class="weather-detail-label">Wind Speed</span>
                        <span class="weather-detail-value" id="weatherWind"></span>
                    </div>
                    <div class="weather-detail-item" role="listitem">
                        <i class="fas fa-compress-arrows-alt weather-detail-icon" aria-hidden="true"></i>
                        <span class="weather-detail-label">Pressure</span>
                        <span class="weather-detail-value" id="weatherPressure"></span>
                    </div>
                </div>
            </section>
        </div>
        
        <!-- JavaScript for weather functionality -->
        <script>
        // ===================================================
// AUTOCOMPLETE FUNCTIONALITY
// ===================================================
let autocompleteTimeout = null;
let selectedIndex = -1;

const cityInput = document.getElementById('cityInput');
const searchButton = document.getElementById('searchButton');
const autocompleteDropdown = document.getElementById('autocompleteDropdown');
const weatherForm = document.getElementById('weatherForm');

function handleAutocomplete() {
    const query = cityInput.value.trim();
    if (autocompleteTimeout) clearTimeout(autocompleteTimeout);
    if (query.length < 2) { hideAutocomplete(); return; }
    autocompleteTimeout = setTimeout(() => fetchAutocomplete(query), 300);
}

async function fetchAutocomplete(query) {
    try {
        showAutocompleteLoading();
        const response = await fetch(`/api/cities/autocomplete?query=${encodeURIComponent(query)}`);
        if (!response.ok) throw new Error('Failed');
        const data = await response.json();
        displayAutocomplete(data.suggestions || []);
    } catch (error) {
        console.error('Autocomplete error:', error);
        hideAutocomplete();
    }
}

function displayAutocomplete(suggestions) {
    if (suggestions.length === 0) { showAutocompleteEmpty(); return; }
    autocompleteDropdown.innerHTML = '';
    selectedIndex = -1;
    suggestions.forEach((suggestion, index) => {
        const item = document.createElement('div');
        item.className = 'autocomplete-item';
        item.innerHTML = `<i class="fas fa-map-marker-alt"></i><span>${suggestion.display}</span>`;
        item.addEventListener('click', () => selectSuggestion(suggestion));
        item.dataset.city = suggestion.city;
        item.dataset.index = index;
        autocompleteDropdown.appendChild(item);
    });
    autocompleteDropdown.classList.add('show');
}

function showAutocompleteLoading() {
    autocompleteDropdown.innerHTML = '<div class="autocomplete-loading"><i class="fas fa-spinner fa-spin"></i> Searching...</div>';
    autocompleteDropdown.classList.add('show');
}

function showAutocompleteEmpty() {
    autocompleteDropdown.innerHTML = '<div class="autocomplete-empty"><i class="fas fa-search"></i> No cities found</div>';
    autocompleteDropdown.classList.add('show');
}

function hideAutocomplete() {
    autocompleteDropdown.classList.remove('show');
    selectedIndex = -1;
}

function selectSuggestion(suggestion) {
    cityInput.value = suggestion.city;
    hideAutocomplete();
    weatherForm.dispatchEvent(new Event('submit'));
}

// Keyboard navigation
cityInput.addEventListener('keydown', (e) => {
    const items = autocompleteDropdown.querySelectorAll('.autocomplete-item');
    if (!items.length) return;
    if (e.key === 'ArrowDown') {
        e.preventDefault();
        selectedIndex = (selectedIndex + 1) % items.length;
        updateSelection(items);
    } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        selectedIndex = selectedIndex <= 0 ? items.length - 1 : selectedIndex - 1;
        updateSelection(items);
    } else if (e.key === 'Enter') {
        if (selectedIndex >= 0 && items[selectedIndex]) {
            e.preventDefault();
            cityInput.value = items[selectedIndex].dataset.city;
            hideAutocomplete();
            weatherForm.dispatchEvent(new Event('submit'));
        }
    } else if (e.key === 'Escape') {
        hideAutocomplete();
    }
});

function updateSelection(items) {
    items.forEach((item, index) => {
        if (index === selectedIndex) {
            item.classList.add('active');
            item.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
        } else {
            item.classList.remove('active');
        }
    });
}

document.addEventListener('click', (e) => {
    if (!e.target.closest('.autocomplete-wrapper')) hideAutocomplete();
});

cityInput.addEventListener('input', handleAutocomplete);
cityInput.addEventListener('focus', () => {
    if (cityInput.value.trim().length >= 2) handleAutocomplete();
});
            // ============================================
            // WEATHER ICON MAPPING
            // Maps OpenWeatherMap icon codes to Font Awesome icons
            // ============================================
            const weatherIconMap = {
                '01d': 'fa-sun',           // Clear sky (day)
                '01n': 'fa-moon',          // Clear sky (night)
                '02d': 'fa-cloud-sun',     // Few clouds (day)
                '02n': 'fa-cloud-moon',    // Few clouds (night)
                '03d': 'fa-cloud',         // Scattered clouds
                '03n': 'fa-cloud',
                '04d': 'fa-cloud',         // Broken clouds
                '04n': 'fa-cloud',
                '09d': 'fa-cloud-rain',    // Shower rain
                '09n': 'fa-cloud-rain',
                '10d': 'fa-cloud-sun-rain', // Rain (day)
                '10n': 'fa-cloud-moon-rain', // Rain (night)
                '11d': 'fa-bolt',          // Thunderstorm
                '11n': 'fa-bolt',
                '13d': 'fa-snowflake',     // Snow
                '13n': 'fa-snowflake',
                '50d': 'fa-smog',          // Mist
                '50n': 'fa-smog'
            };
            
            // ============================================
            // DOM ELEMENTS
            // Get references to all interactive elements
            // ============================================
            const weatherForm = document.getElementById('weatherForm');
            const cityInput = document.getElementById('cityInput');
            const searchButton = document.getElementById('searchButton');
            const weatherDisplay = document.getElementById('weatherDisplay');
            const loading = document.getElementById('loading');
            const errorMessage = document.getElementById('errorMessage');
            const errorText = document.getElementById('errorText');
            const retryButton = document.getElementById('retryButton');
            
            // Weather display elements
            const weatherCity = document.getElementById('weatherCity');
            const weatherCountry = document.getElementById('weatherCountry');
            const weatherIcon = document.getElementById('weatherIcon');
            const weatherTemp = document.getElementById('weatherTemp');
            const weatherDescription = document.getElementById('weatherDescription');
            const weatherFeelsLike = document.getElementById('weatherFeelsLike');
            const weatherHumidity = document.getElementById('weatherHumidity');
            const weatherWind = document.getElementById('weatherWind');
            const weatherPressure = document.getElementById('weatherPressure');
            
            // ============================================
            // UTILITY FUNCTIONS
            // Helper functions for UI state management
            // ============================================
            
            // Show loading state
            function showLoading() {
                loading.classList.add('show');
                weatherDisplay.classList.remove('show');
                errorMessage.classList.remove('show');
                searchButton.disabled = true;
            }
            
            // Hide loading state
            function hideLoading() {
                loading.classList.remove('show');
                searchButton.disabled = false;
            }
            
            // Show error message
            function showError(message, showRetry = false) {
                errorText.textContent = message;
                errorMessage.classList.add('show');
                weatherDisplay.classList.remove('show');
                retryButton.style.display = showRetry ? 'block' : 'none';
                hideLoading();
            }
            
            // Hide error message
            function hideError() {
                errorMessage.classList.remove('show');
            }
            
            // Get Font Awesome icon class from weather icon code
            function getWeatherIcon(iconCode) {
                const iconClass = weatherIconMap[iconCode] || 'fa-cloud';
                return `<i class="fas ${iconClass}"></i>`;
            }
            
            // ============================================
            // API CALL FUNCTION
            // Fetches weather data from backend API
            // ============================================
            async function fetchWeather(city, retryCount = 0) {
                try {
                    showLoading();
                    hideError();
                    
                    // Make API request to backend
                    const response = await fetch(`/api/weather?city=${encodeURIComponent(city)}`);
                    
                    // Handle HTTP errors
                    if (!response.ok) {
                        const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }));
                        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
                    }
                    
                    // Parse JSON response
                    const data = await response.json();
                    
                    // Display weather data
                    displayWeather(data);
                    hideLoading();
                    hideError();
                    
                } catch (error) {
                    console.error('Weather fetch error:', error);
                    
                    // Show user-friendly error message
                    let errorMsg = 'Failed to fetch weather data. ';
                    
                    if (error.message.includes('404') || error.message.includes('not found')) {
                        errorMsg = 'City not found. Please check the spelling and try again.';
                    } else if (error.message.includes('timeout')) {
                        errorMsg = 'Request timed out. The weather service is taking too long to respond.';
                    } else if (error.message.includes('network') || error.message.includes('Failed to fetch')) {
                        errorMsg = 'Network error. Please check your internet connection.';
                    } else {
                        errorMsg += error.message;
                    }
                    
                    // Show retry button for retryable errors
                    const showRetry = retryCount < 2 && !error.message.includes('404');
                    showError(errorMsg, showRetry);
                    
                    // Store city for retry functionality
                    if (showRetry) {
                        retryButton.onclick = () => fetchWeather(city, retryCount + 1);
                    }
                }
            }
            
            // ============================================
            // DISPLAY WEATHER DATA
            // Updates DOM with weather information
            // ============================================
            function displayWeather(data) {
                // Update location
                weatherCity.textContent = data.city;
                weatherCountry.textContent = data.country || '';
                
                // Update weather icon
                weatherIcon.innerHTML = getWeatherIcon(data.icon);
                
                // Update temperature and description
                weatherTemp.textContent = `${data.temperature}°C`;
                weatherDescription.textContent = data.description;
                weatherFeelsLike.textContent = `Feels like ${data.feels_like}°C`;
                
                // Update weather details
                weatherHumidity.textContent = `${data.humidity}%`;
                weatherWind.textContent = `${data.wind_speed} m/s`;
                weatherPressure.textContent = `${data.pressure} hPa`;
                
                // Show weather display with animation
                weatherDisplay.classList.add('show');
            }
            
            // ============================================
            // FORM SUBMISSION HANDLER
            // Handles search form submission
            // ============================================
            weatherForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                
                // Get city name from input
                const city = cityInput.value.trim();
                
                // Validate input
                if (!city) {
                    showError('Please enter a city name.', false);
                    return;
                }
                
                // Fetch weather data
                await fetchWeather(city);
            });
            
            // ============================================
            // ENTER KEY HANDLER
            // Allows submitting form with Enter key
            // ============================================
            cityInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    weatherForm.dispatchEvent(new Event('submit'));
                }
            });
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "version": "0.1.0",
        "sprint": 1
    }


@app.get("/api/info")
def get_info():
    track_weather_search(logger, city="N/A", success=True)

    return {
        "project": "Weather Watcher",
        "sprint": 1,
        "tech_stack": ["FastAPI", "Azure App Service", "Azure DevOps"]
    }



@app.get("/api/debug")
def debug_config():
    """
    Debug endpoint to check if environment variables are loaded.
    Shows if API key is configured (without revealing the actual key).
    """
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    app_insights = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")
    
    return {
        "google_maps_api_key_configured": bool(api_key and len(api_key) > 10),
        "google_maps_api_key_length": len(api_key) if api_key else 0,
        "google_maps_api_key_preview": f"{api_key[:8]}..." if api_key and len(api_key) > 8 else "NOT SET",
        "app_insights_configured": bool(app_insights),
        "environment": os.getenv("ENVIRONMENT", "production"),
        "dotenv_loaded": True,  # If this endpoint works, dotenv was loaded
    }


# -----------------------------------------------
# Pydantic Models for API Response
# -----------------------------------------------
class WeatherResponse(BaseModel):
    """Response model for weather data."""
    city: str = Field(..., description="City name")
    country: str = Field(..., description="Country code (ISO 3166-1 alpha-2)")
    temperature: int = Field(..., description="Temperature in Celsius")
    feels_like: int = Field(..., description="Feels like temperature in Celsius")
    description: str = Field(..., description="Weather condition description")
    humidity: int = Field(..., ge=0, le=100, description="Relative humidity percentage")
    wind_speed: float = Field(..., ge=0, description="Wind speed in m/s")
    pressure: int = Field(..., description="Atmospheric pressure in hPa")
    icon: str = Field(..., description="Weather icon code")

    class Config:
        json_schema_extra = {
            "example": {
                "city": "London",
                "country": "GB",
                "temperature": 15,
                "feels_like": 14,
                "description": "Partly cloudy",
                "humidity": 72,
                "wind_speed": 4.2,
                "pressure": 1015,
                "icon": "02d"
            }
        }


# -----------------------------------------------
# Input Validation Helper
# -----------------------------------------------
def validate_city_name(city: str) -> str:
    """
    Validate and sanitize city name input.
    
    Args:
        city: Raw city name input
        
    Returns:
        Sanitized city name
        
    Raises:
        HTTPException: If city name is invalid
    """
    if not city or not city.strip():
        raise HTTPException(
            status_code=400,
            detail="City name cannot be empty"
        )
    
    # Strip whitespace and limit length
    city = city.strip()
    
    if len(city) < 2:
        raise HTTPException(
            status_code=400,
            detail="City name must be at least 2 characters"
        )
    
    if len(city) > 100:
        raise HTTPException(
            status_code=400,
            detail="City name too long (max 100 characters)"
        )
    
    # Allow letters, spaces, hyphens, commas, periods, and apostrophes
    # This covers names like "St. John's", "New York, NY", "São Paulo"
    if not re.match(r"^[\w\s\-,.'À-ÿ]+$", city, re.UNICODE):
        raise HTTPException(
            status_code=400,
            detail="City name contains invalid characters"
        )
    
    return city


# -----------------------------------------------
# Weather Service Instance
# -----------------------------------------------
weather_service = WeatherService()


# -----------------------------------------------
# Weather API Endpoints
# -----------------------------------------------
@app.get(
    "/weather/{city}",
    response_model=WeatherResponse,
    summary="Get weather by city (path parameter)",
    description="Fetch current weather data for a city using Google Weather API.",
    responses={
        200: {"description": "Weather data retrieved successfully"},
        400: {"description": "Invalid city name"},
        404: {"description": "City not found"},
        500: {"description": "Weather service error"},
        503: {"description": "Google Weather API not configured"},
        504: {"description": "Weather service timeout"},
    }
)
async def get_weather_by_path(
    city: str = Path(
        ...,
        min_length=2,
        max_length=100,
        description="City name (e.g., 'London', 'New York', 'Tokyo')",
        example="London"
    )
):
    """
    Fetch current weather data for a city.
    
    This endpoint uses the Google Maps Weather API to retrieve real-time
    weather conditions for the specified city.
    
    **Example cities:**
    - London
    - New York
    - Tokyo
    - Paris
    - Sydney
    """
    return await _fetch_weather_for_city(city)


@app.get(
    "/api/weather",
    response_model=WeatherResponse,
    summary="Get weather by city (query parameter)",
    description="Fetch current weather data for a city using Google Weather API.",
    responses={
        200: {"description": "Weather data retrieved successfully"},
        400: {"description": "Invalid city name"},
        404: {"description": "City not found"},
        500: {"description": "Weather service error"},
        503: {"description": "Google Weather API not configured"},
        504: {"description": "Weather service timeout"},
    }
)
async def get_weather_by_query(
    city: str = Query(
        ...,
        min_length=2,
        max_length=100,
        description="City name",
        example="London"
    )
):
    """
    Fetch current weather data for a city (query parameter version).
    
    This endpoint is the same as /weather/{city} but uses a query parameter
    for backward compatibility with the existing frontend.
    """
    return await _fetch_weather_for_city(city)


async def _fetch_weather_for_city(city: str) -> dict:
    """
    Internal function to fetch weather data for a city.
    
    Handles both path and query parameter endpoints to avoid code duplication.
    """
    # Validate input
    city = validate_city_name(city)
    
    # Check if API key is configured
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    
    if not api_key:
        # Return mock data for development/testing when API key is not set
        logger.warning(f"GOOGLE_MAPS_API_KEY not set. Returning mock data for: {city}")
        return {
            "city": city.title(),
            "country": "US",
            "temperature": 22,
            "feels_like": 24,
            "description": "Clear sky (Mock Data)",
            "humidity": 65,
            "wind_speed": 3.5,
            "pressure": 1013,
            "icon": "01d"
        }
    
    try:
        # Fetch weather using the service
        weather_data = await weather_service.get_weather_by_city(city)
        
        track_weather_search(logger, city=city, success=True, temperature=weather_data.temperature)

        logger.info(f"Successfully fetched weather for: {city}")
        
        return {
            "city": weather_data.city,
            "country": weather_data.country,
            "temperature": weather_data.temperature,
            "feels_like": weather_data.feels_like,
            "description": weather_data.description,
            "humidity": weather_data.humidity,
            "wind_speed": weather_data.wind_speed,
            "pressure": weather_data.pressure,
            "icon": weather_data.icon,
        }
        
    except CityNotFoundError as e:
        logger.warning(f"City not found: {city}")
        track_weather_search(logger, city=city, success=False)
        raise HTTPException(
            status_code=404,
            detail=f"City not found: {city}. Please check the spelling and try again."
        )
    
    except APIKeyMissingError as e:
        logger.error("Google Maps API key not configured")
        raise HTTPException(
            status_code=503,
            detail="Weather service not configured. Please set GOOGLE_MAPS_API_KEY."
        )
    
    except WeatherAPIError as e:
        logger.error(f"Weather API error for {city}: {str(e)}")
        track_weather_search(logger, city=city, success=False)
        if "timeout" in str(e).lower():
            raise HTTPException(
                status_code=504,
                detail="Weather service is taking too long to respond. Please try again."
            )
        
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch weather data. Please try again later."
        )
    
    except Exception as e:
        logger.error(f"Unexpected error fetching weather for {city}: {str(e)}")
        track_weather_search(logger, city=city, success=False)
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred. Please try again."
        )


# -----------------------------------------------
# City Autocomplete Endpoint
# -----------------------------------------------
@app.get(
    "/api/cities/autocomplete",
    summary="City autocomplete suggestions",
    description="Get city suggestions as user types for autocomplete functionality.",
)
async def autocomplete_cities(
    query: str = Query(
        ...,
        min_length=2,
        max_length=100,
        description="Search query (minimum 2 characters)",
        example="Mad"
    )
):
    """Get city autocomplete suggestions using Google Places API."""
    
    if not query or len(query.strip()) < 2:
        raise HTTPException(status_code=400, detail="Query must be at least 2 characters")
    
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    
    if not api_key:
        logger.warning("GOOGLE_MAPS_API_KEY not set for autocomplete")

        # ⭐ ADD THIS CUSTOM TELEMETRY ⭐
        logger.info(
            "Autocomplete executed",
            extra={
                "custom_dimensions": {
                    "query": query,
                    "success": True,
                    "source": "mock"
                }
            }
        )

        return {
            "suggestions": [
                {
                    "city": f"{query.title()}",
                    "country": "Mock",
                    "display": f"{query.title()}, Mock"
                }
            ]
        }
    
    try:
        url = "https://maps.googleapis.com/maps/api/place/autocomplete/json"
        params = {"input": query, "types": "(cities)", "key": api_key}
        
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") != "OK":
                return {"suggestions": []}
            
            suggestions = []
            for prediction in data.get("predictions", [])[:10]:
                description = prediction.get("description", "")
                parts = [part.strip() for part in description.split(",")]
                
                if len(parts) >= 2:
                    suggestions.append({
                        "city": parts[0],
                        "country": parts[-1],
                        "display": description
                    })
                                        
# telemetry for successful real autocomplete
logger.info(
    "Autocomplete executed",
    extra={
        "custom_dimensions": {
            "query": query,
            "success": True,
            "source": "google",
            "count": len(suggestions)
        }
    }
)

return {"suggestions": suggestions}

            
    except Exception as e:
        logger.error(f"Autocomplete error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch suggestions")
