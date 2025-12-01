import os
import logging
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import httpx

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
                    <input 
                        type="text" 
                        class="search-input" 
                        id="cityInput" 
                        placeholder="Enter city name..." 
                        aria-label="City name"
                        required
                        autocomplete="off"
                    >
                    <button type="submit" class="search-button" id="searchButton" aria-label="Search weather">
                        <i class="fas fa-search"></i>
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
    return {
        "project": "Weather Watcher",
        "sprint": 1,
        "tech_stack": ["FastAPI", "Azure App Service", "Azure DevOps", "GitHub Actions"]
    }


# -----------------------------------------------
# Weather API Endpoint
# -----------------------------------------------
@app.get("/api/weather")
async def get_weather(city: str = Query(..., description="City name")):
    """
    Fetch weather data for a given city.
    Uses OpenWeatherMap API if API key is available, otherwise returns mock data.
    """
    # Get API key from environment variable
    api_key = os.getenv("OPENWEATHER_API_KEY")
    
    # If no API key, return mock data for development
    if not api_key:
        logger.info(f"Using mock weather data for city: {city}")
        return {
            "city": city.title(),
            "temperature": 22,
            "feels_like": 24,
            "description": "clear sky",
            "humidity": 65,
            "wind_speed": 3.5,
            "pressure": 1013,
            "icon": "01d",
            "country": "US"
        }
    
    # Use real OpenWeatherMap API
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": api_key,
            "units": "metric"
        }
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            return {
                "city": data["name"],
                "temperature": round(data["main"]["temp"]),
                "feels_like": round(data["main"]["feels_like"]),
                "description": data["weather"][0]["description"],
                "humidity": data["main"]["humidity"],
                "wind_speed": round(data["wind"]["speed"], 1),
                "pressure": data["main"]["pressure"],
                "icon": data["weather"][0]["icon"],
                "country": data["sys"]["country"]
            }
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(status_code=404, detail="City not found")
        raise HTTPException(status_code=500, detail="Weather service error")
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Weather service timeout")
    except Exception as e:
        logger.error(f"Weather API error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch weather data")
