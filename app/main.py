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


# -----------------------------------------------
# Country Code to Name Mapping Dictionary
# -----------------------------------------------
# Task 154: Create country code mapping dictionary
# NOTE: This is only used as fallback for mock data when API key is not set.
# Real weather data uses full country names directly from Google Geocoding API.
COUNTRY_CODE_MAP = {
    "US": "United States",
    "GB": "United Kingdom",
    "CA": "Canada",
    "AU": "Australia",
    "DE": "Germany",
    "FR": "France",
    "IT": "Italy",
    "ES": "Spain",
    "NL": "Netherlands",
    "BE": "Belgium",
    "CH": "Switzerland",
    "AT": "Austria",
    "PT": "Portugal",
    "IE": "Ireland",
    "SE": "Sweden",
    "NO": "Norway",
    "DK": "Denmark",
    "FI": "Finland",
    "PL": "Poland",
    "CZ": "Czech Republic",
    "GR": "Greece",
    "TR": "Turkey",
    "RU": "Russia",
    "UA": "Ukraine",
    "RO": "Romania",
    "BG": "Bulgaria",
    "HR": "Croatia",
    "RS": "Serbia",
    "JP": "Japan",
    "CN": "China",
    "KR": "South Korea",
    "IN": "India",
    "ID": "Indonesia",
    "TH": "Thailand",
    "VN": "Vietnam",
    "MY": "Malaysia",
    "SG": "Singapore",
    "PH": "Philippines",
    "NZ": "New Zealand",
    "BR": "Brazil",
    "MX": "Mexico",
    "AR": "Argentina",
    "CL": "Chile",
    "CO": "Colombia",
    "PE": "Peru",
    "VE": "Venezuela",
    "ZA": "South Africa",
    "EG": "Egypt",
    "MA": "Morocco",
    "NG": "Nigeria",
    "KE": "Kenya",
    "AE": "United Arab Emirates",
    "SA": "Saudi Arabia",
    "IL": "Israel",
    "QA": "Qatar",
    "KW": "Kuwait",
}


# -----------------------------------------------
# Country Name Conversion Function
# -----------------------------------------------
# Task 155: Implement country name conversion function
def convert_country_code_to_name(country_code: str) -> str:
    """
    Convert ISO 3166-1 alpha-2 country code to full country name.
    
    Args:
        country_code: Two-letter country code (e.g., "US", "GB")
        
    Returns:
        Full country name (e.g., "United States", "United Kingdom")
        If code not found, returns the original code.
    
    Examples:
        >>> convert_country_code_to_name("US")
        'United States'
        >>> convert_country_code_to_name("GB")
        'United Kingdom'
        >>> convert_country_code_to_name("XX")
        'XX'
    """
    if not country_code:
        return ""
    
    # Convert to uppercase for case-insensitive lookup
    code = country_code.strip().upper()
    
    # Return full name if found, otherwise return the code itself
    return COUNTRY_CODE_MAP.get(code, code)

    
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
        
        <!-- Google Fonts - Distinctive typography -->
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
        
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
               DARK THEME COLOR PALETTE - REFINED
               ============================================ */
            :root {
                --bg-primary: #06080d;
                --bg-secondary: #0c1017;
                --bg-card: #111827;
                --bg-card-hover: #1a2234;
                --text-primary: #f0f4f8;
                --text-secondary: #94a3b8;
                --text-muted: #64748b;
                --accent-primary: #38bdf8;
                --accent-secondary: #818cf8;
                --accent-gradient: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
                --success: #22c55e;
                --success-glow: rgba(34, 197, 94, 0.3);
                --error: #f43f5e;
                --error-glow: rgba(244, 63, 94, 0.3);
                --warning: #f59e0b;
                --border: rgba(148, 163, 184, 0.1);
                --border-hover: rgba(148, 163, 184, 0.2);
                --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.3);
                --shadow-md: 0 8px 32px rgba(0, 0, 0, 0.4);
                --shadow-lg: 0 16px 64px rgba(0, 0, 0, 0.5);
                --shadow-glow: 0 0 40px rgba(56, 189, 248, 0.15);
                
                /* Skeleton loading colors */
                --skeleton-base: #1e293b;
                --skeleton-shine: #334155;
                
                /* Comparison tool colors */
                --comparison-highlight: #fbbf24;
                --comparison-highlight-glow: rgba(251, 191, 36, 0.3);
                --comparison-best: #10b981;
                --comparison-worst: #ef4444;
            }
            
            /* ============================================
               BODY & BACKGROUND
               ============================================ */
            body {
                font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif;
                background: var(--bg-primary);
                color: var(--text-primary);
                min-height: 100vh;
                padding: 24px;
                position: relative;
                overflow-x: hidden;
                line-height: 1.6;
            }
            
            /* Animated gradient background overlay */
            body::before {
                content: '';
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: 
                    radial-gradient(ellipse 80% 50% at 20% 40%, rgba(56, 189, 248, 0.08) 0%, transparent 50%),
                    radial-gradient(ellipse 60% 40% at 80% 60%, rgba(129, 140, 248, 0.06) 0%, transparent 50%),
                    radial-gradient(ellipse 40% 30% at 40% 80%, rgba(192, 132, 252, 0.04) 0%, transparent 50%);
                animation: ambientGlow 20s ease-in-out infinite;
                z-index: 0;
                pointer-events: none;
            }
            
            /* Smooth ambient glow animation */
            @keyframes ambientGlow {
                0%, 100% { 
                    opacity: 1; 
                    transform: scale(1);
                }
                50% { 
                    opacity: 0.8; 
                    transform: scale(1.02);
                }
            }
            
            /* ============================================
               MAIN CONTAINER
               ============================================ */
            .container {
                max-width: 720px;
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
                margin-bottom: 48px;
                animation: fadeSlideDown 0.8s cubic-bezier(0.16, 1, 0.3, 1);
            }
            
            h1 {
                color: var(--text-primary);
                font-size: clamp(2rem, 5vw, 3rem);
                font-weight: 700;
                margin-bottom: 8px;
                letter-spacing: -0.03em;
                display: inline-flex;
                align-items: center;
                gap: 16px;
            }
            
            h1 i {
                background: var(--accent-gradient);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                filter: drop-shadow(0 0 20px rgba(56, 189, 248, 0.4));
            }
            
            .subtitle {
                color: var(--text-secondary);
                font-size: 1.1rem;
                font-weight: 400;
                opacity: 0;
                animation: fadeSlideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) 0.2s forwards;
            }
            
            /* Temperature Unit Toggle */
            .temperature-toggle-container {
                margin-top: 20px;
                display: flex;
                justify-content: center;
                opacity: 0;
                animation: fadeSlideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) 0.4s forwards;
            }
            
            .temperature-toggle {
                display: flex;
                align-items: center;
                background: var(--bg-card);
                border: 1px solid var(--border);
                border-radius: 12px;
                padding: 4px;
                gap: 0;
                cursor: pointer;
                transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
                box-shadow: var(--shadow-sm);
                position: relative;
            }
            
            .temperature-toggle:hover {
                box-shadow: var(--shadow-md);
                border-color: var(--accent);
            }
            
            .temperature-toggle:focus {
                outline: 2px solid var(--accent);
                outline-offset: 2px;
            }
            
            .temp-unit {
                padding: 8px 16px;
                font-size: 0.95rem;
                font-weight: 600;
                color: var(--text-secondary);
                transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
                border-radius: 8px;
                user-select: none;
                position: relative;
                z-index: 1;
            }
            
            .temp-unit.active {
                color: var(--text-primary);
                background: var(--accent-gradient);
                box-shadow: var(--shadow-sm);
            }
            
            .temp-unit:not(.active):hover {
                color: var(--text-primary);
            }
            
            /* ============================================
               ANIMATIONS - CORE
               ============================================ */
            @keyframes fadeSlideDown {
                from {
                    opacity: 0;
                    transform: translateY(-20px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            @keyframes fadeSlideUp {
                from {
                    opacity: 0;
                    transform: translateY(20px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
            
            @keyframes scaleIn {
                from {
                    opacity: 0;
                    transform: scale(0.95);
                }
                to {
                    opacity: 1;
                    transform: scale(1);
                }
            }
            
            @keyframes pulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.5; }
            }
            
            /* Shimmer animation for skeleton loading */
            @keyframes shimmer {
                0% {
                    background-position: -200% 0;
                }
                100% {
                    background-position: 200% 0;
                }
            }
            
            /* Success checkmark animation */
            @keyframes checkmark {
                0% {
                    stroke-dashoffset: 100;
                }
                100% {
                    stroke-dashoffset: 0;
                }
            }
            
            /* Bounce animation */
            @keyframes bounce {
                0%, 100% { transform: translateY(0); }
                50% { transform: translateY(-6px); }
            }
            
            /* Ripple effect */
            @keyframes ripple {
                0% {
                    transform: scale(0);
                    opacity: 0.6;
                }
                100% {
                    transform: scale(2.5);
                    opacity: 0;
                }
            }
            
            /* Spin animation */
            @keyframes spin {
                to { transform: rotate(360deg); }
            }
            
            /* Float animation */
            @keyframes float {
                0%, 100% { transform: translateY(0) rotate(0deg); }
                25% { transform: translateY(-5px) rotate(2deg); }
                75% { transform: translateY(5px) rotate(-2deg); }
            }
            
            /* Progress bar animation */
            @keyframes progressPulse {
                0%, 100% { box-shadow: 0 0 0 0 rgba(56, 189, 248, 0.4); }
                50% { box-shadow: 0 0 0 8px rgba(56, 189, 248, 0); }
            }
            
            /* ============================================
               SEARCH FORM SECTION
               ============================================ */
            .search-section {
                background: var(--bg-card);
                padding: 32px;
                border-radius: 24px;
                border: 1px solid var(--border);
                box-shadow: var(--shadow-md);
                margin-bottom: 24px;
                backdrop-filter: blur(20px);
                opacity: 0;
                animation: fadeSlideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) 0.1s forwards;
                position: relative;
                z-index: 100;
                /* Removed overflow:hidden to allow dropdown to show */
            }
            
            /* Subtle gradient border effect - using box-shadow instead */
            .search-section::before {
                content: '';
                position: absolute;
                top: 0;
                left: 50%;
                transform: translateX(-50%);
                width: 60%;
                height: 1px;
                background: linear-gradient(90deg, transparent, var(--accent-primary), transparent);
                opacity: 0.5;
                border-radius: 24px 24px 0 0;
            }
            
            .search-form {
                display: flex;
                gap: 12px;
            }
            
            .autocomplete-wrapper {
                position: relative;
                flex: 1;
            }
            
            .search-input {
                width: 100%;
                padding: 16px 20px;
                background: var(--bg-secondary);
                border: 2px solid var(--border);
                border-radius: 16px;
                color: var(--text-primary);
                font-family: 'Outfit', sans-serif;
                font-size: 1rem;
                font-weight: 400;
                outline: none;
                transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            }
            
            .search-input:focus {
                border-color: var(--accent-primary);
                box-shadow: 0 0 0 4px rgba(56, 189, 248, 0.15), var(--shadow-glow);
                background: var(--bg-card);
            }
            
            .search-input::placeholder {
                color: var(--text-muted);
            }
            
            /* Search Button with loading states */
            .search-button {
                padding: 16px 28px;
                background: var(--accent-gradient);
                border: none;
                border-radius: 16px;
                color: white;
                font-family: 'Outfit', sans-serif;
                font-size: 1rem;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 10px;
                min-width: 140px;
                position: relative;
                overflow: hidden;
            }
            
            .search-button::before {
                content: '';
                position: absolute;
                inset: 0;
                background: linear-gradient(135deg, rgba(255,255,255,0.2) 0%, transparent 50%);
                opacity: 0;
                transition: opacity 0.3s ease;
            }
            
            .search-button:hover:not(:disabled)::before {
                opacity: 1;
            }
            
            .search-button:hover:not(:disabled) {
                transform: translateY(-2px);
                box-shadow: 0 8px 32px rgba(56, 189, 248, 0.4);
            }
            
            .search-button:active:not(:disabled) {
                transform: translateY(0);
            }
            
            .search-button:disabled {
                opacity: 0.7;
                cursor: not-allowed;
                transform: none;
            }
            
            /* Button loading state */
            .search-button.loading .button-text {
                opacity: 0;
            }
            
            .search-button.loading .button-spinner {
                opacity: 1;
            }
            
            .button-spinner {
                position: absolute;
                width: 20px;
                height: 20px;
                border: 2px solid rgba(255,255,255,0.3);
                border-top-color: white;
                border-radius: 50%;
                animation: spin 0.8s linear infinite;
                opacity: 0;
                transition: opacity 0.2s ease;
            }
            
            /* Ripple effect on click */
            .search-button .ripple {
                position: absolute;
                border-radius: 50%;
                background: rgba(255, 255, 255, 0.4);
                transform: scale(0);
                animation: ripple 0.6s ease-out;
                pointer-events: none;
            }
            
            /* ============================================
               AUTOCOMPLETE DROPDOWN
               ============================================ */
            .autocomplete-wrapper {
                position: relative;
                flex: 1;
                z-index: 1000;
            }
            
            .autocomplete-dropdown {
                position: absolute;
                top: calc(100% + 8px);
                left: 0;
                right: 0;
                background: var(--bg-card);
                border: 1px solid var(--border-hover);
                border-radius: 16px;
                max-height: 320px;
                overflow-y: auto;
                z-index: 10000;
                box-shadow: var(--shadow-lg), 0 0 0 1px rgba(56, 189, 248, 0.1);
                display: none;
                opacity: 0;
                transform: translateY(-10px);
            }
            
            .autocomplete-dropdown.show {
                display: block;
                animation: dropdownReveal 0.25s cubic-bezier(0.16, 1, 0.3, 1) forwards;
            }
            
            .autocomplete-dropdown.hiding {
                animation: dropdownHide 0.2s cubic-bezier(0.16, 1, 0.3, 1) forwards;
            }
            
            @keyframes dropdownReveal {
                from {
                    opacity: 0;
                    transform: translateY(-10px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            @keyframes dropdownHide {
                from {
                    opacity: 1;
                    transform: translateY(0);
                }
                to {
                    opacity: 0;
                    transform: translateY(-10px);
                }
            }
            
            .autocomplete-item {
                padding: 14px 20px;
                cursor: pointer;
                transition: all 0.2s ease;
                color: var(--text-primary);
                font-size: 0.95rem;
                display: flex;
                align-items: center;
                gap: 12px;
                border-bottom: 1px solid var(--border);
            }
            
            .autocomplete-item:last-child {
                border-bottom: none;
            }
            
            .autocomplete-item:hover,
            .autocomplete-item.active {
                background: var(--bg-card-hover);
            }
            
            .autocomplete-item i {
                color: var(--accent-primary);
                font-size: 0.9rem;
                width: 20px;
                text-align: center;
            }
            
            .autocomplete-loading,
            .autocomplete-empty {
                padding: 20px;
                text-align: center;
                color: var(--text-secondary);
                font-size: 0.9rem;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 10px;
            }
            
            .autocomplete-loading i {
                color: var(--accent-primary);
            }
            
            /* ============================================
               SKELETON LOADING STATES
               ============================================ */
            .skeleton {
                background: linear-gradient(
                    90deg,
                    var(--skeleton-base) 0%,
                    var(--skeleton-shine) 50%,
                    var(--skeleton-base) 100%
                );
                background-size: 200% 100%;
                animation: shimmer 1.5s ease-in-out infinite;
                border-radius: 8px;
            }
            
            .skeleton-text {
                height: 1em;
                border-radius: 6px;
            }
            
            .skeleton-text-lg {
                height: 2.5em;
                border-radius: 8px;
            }
            
            .skeleton-text-xl {
                height: 4em;
                border-radius: 12px;
            }
            
            .skeleton-circle {
                border-radius: 50%;
            }
            
            .skeleton-card {
                padding: 20px;
                border-radius: 12px;
            }
            
            /* Weather Display Skeleton */
            .weather-skeleton {
                background: var(--bg-card);
                padding: 40px;
                border-radius: 24px;
                border: 1px solid var(--border);
                box-shadow: var(--shadow-md);
                display: none;
            }
            
            .weather-skeleton.show {
                display: block;
                animation: fadeIn 0.3s ease;
            }
            
            .weather-skeleton-header {
                display: flex;
                justify-content: space-between;
                align-items: flex-start;
                margin-bottom: 32px;
            }
            
            .weather-skeleton-location {
                flex: 1;
            }
            
            .weather-skeleton-city {
                width: 180px;
                height: 32px;
                margin-bottom: 12px;
            }
            
            .weather-skeleton-country {
                width: 120px;
                height: 20px;
            }
            
            .weather-skeleton-icon {
                width: 80px;
                height: 80px;
            }
            
            .weather-skeleton-main {
                text-align: center;
                margin-bottom: 32px;
            }
            
            .weather-skeleton-temp {
                width: 140px;
                height: 64px;
                margin: 0 auto 16px;
            }
            
            .weather-skeleton-desc {
                width: 200px;
                height: 24px;
                margin: 0 auto 12px;
            }
            
            .weather-skeleton-feels {
                width: 150px;
                height: 18px;
                margin: 0 auto;
            }
            
            .weather-skeleton-details {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 20px;
            }
            
            .weather-skeleton-detail {
                height: 100px;
                border-radius: 16px;
            }
            
            /* ============================================
               LOADING OVERLAY - ENHANCED
               ============================================ */
            .loading-overlay {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(6, 8, 13, 0.8);
                backdrop-filter: blur(8px);
                display: none;
                align-items: center;
                justify-content: center;
                z-index: 9999;
                opacity: 0;
                transition: opacity 0.3s ease;
            }
            
            .loading-overlay.show {
                display: flex;
                animation: fadeIn 0.3s ease forwards;
            }
            
            .loading-content {
                text-align: center;
                animation: scaleIn 0.4s cubic-bezier(0.16, 1, 0.3, 1);
            }
            
            /* Modern spinner */
            .modern-spinner {
                width: 64px;
                height: 64px;
                margin: 0 auto 24px;
                position: relative;
            }
            
            .modern-spinner::before,
            .modern-spinner::after {
                content: '';
                position: absolute;
                border-radius: 50%;
            }
            
            .modern-spinner::before {
                inset: 0;
                border: 3px solid var(--border);
            }
            
            .modern-spinner::after {
                inset: 0;
                border: 3px solid transparent;
                border-top-color: var(--accent-primary);
                animation: spin 0.8s linear infinite;
            }
            
            /* Weather icon animation in loader */
            .loading-weather-icon {
                font-size: 2rem;
                color: var(--accent-primary);
                animation: float 2s ease-in-out infinite;
                margin-bottom: 16px;
            }
            
            .loading-text {
                color: var(--text-primary);
                font-size: 1.1rem;
                font-weight: 500;
                margin-bottom: 8px;
            }
            
            .loading-subtext {
                color: var(--text-secondary);
                font-size: 0.9rem;
            }
            
            /* Progress bar */
            .loading-progress {
                width: 200px;
                height: 4px;
                background: var(--border);
                border-radius: 2px;
                margin: 20px auto 0;
                overflow: hidden;
            }
            
            .loading-progress-bar {
                height: 100%;
                background: var(--accent-gradient);
                border-radius: 2px;
                width: 0%;
                transition: width 0.3s ease;
                animation: progressPulse 1.5s ease-in-out infinite;
            }
            
            /* ============================================
               INLINE LOADING STATE
               ============================================ */
            .loading-inline {
                display: none;
                text-align: center;
                padding: 60px 40px;
                background: var(--bg-card);
                border-radius: 24px;
                border: 1px solid var(--border);
                box-shadow: var(--shadow-md);
            }
            
            .loading-inline.show {
                display: block;
                animation: fadeSlideUp 0.4s cubic-bezier(0.16, 1, 0.3, 1);
            }
            
            .loading-dots {
                display: flex;
                justify-content: center;
                gap: 8px;
                margin-bottom: 20px;
            }
            
            .loading-dot {
                width: 12px;
                height: 12px;
                background: var(--accent-primary);
                border-radius: 50%;
                animation: bounce 1.4s ease-in-out infinite;
            }
            
            .loading-dot:nth-child(1) { animation-delay: 0s; }
            .loading-dot:nth-child(2) { animation-delay: 0.2s; }
            .loading-dot:nth-child(3) { animation-delay: 0.4s; }
            
            /* ============================================
               WEATHER DISPLAY SECTION - ENHANCED
               ============================================ */
            .weather-display {
                background: var(--bg-card);
                padding: 40px;
                border-radius: 24px;
                border: 1px solid var(--border);
                box-shadow: var(--shadow-md);
                backdrop-filter: blur(20px);
                display: none;
                position: relative;
                overflow: hidden;
            }
            
            .weather-display::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 1px;
                background: linear-gradient(90deg, transparent, var(--success), transparent);
                opacity: 0;
                transition: opacity 0.5s ease;
            }
            
            .weather-display.show {
                display: block;
            }
            
            .weather-display.show::before {
                opacity: 0.6;
            }
            
            /* Staggered reveal animation */
            .weather-display.reveal .weather-header {
                animation: fadeSlideUp 0.5s cubic-bezier(0.16, 1, 0.3, 1) 0s forwards;
            }
            
            .weather-display.reveal .weather-main {
                animation: fadeSlideUp 0.5s cubic-bezier(0.16, 1, 0.3, 1) 0.1s forwards;
            }
            
            .weather-display.reveal .weather-details {
                animation: fadeSlideUp 0.5s cubic-bezier(0.16, 1, 0.3, 1) 0.2s forwards;
            }
            
            .weather-display.reveal .weather-header,
            .weather-display.reveal .weather-main,
            .weather-display.reveal .weather-details {
                opacity: 0;
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
                letter-spacing: -0.02em;
            }
            
            .weather-country {
                font-size: 1rem;
                color: var(--text-secondary);
                display: flex;
                align-items: center;
                gap: 6px;
            }
            
            .weather-country i {
                font-size: 0.8rem;
            }
            
            .weather-icon {
                font-size: 5rem;
                line-height: 1;
                background: var(--accent-gradient);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                filter: drop-shadow(0 4px 20px rgba(56, 189, 248, 0.3));
                transition: transform 0.3s ease;
            }
            
            .weather-display.reveal .weather-icon {
                animation: iconPop 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) 0.3s forwards;
                transform: scale(0);
            }
            
            @keyframes iconPop {
                to { transform: scale(1); }
            }
            
            .weather-main {
                text-align: center;
                margin-bottom: 32px;
            }
            
            .weather-temp {
                font-size: 4.5rem;
                font-weight: 800;
                color: var(--text-primary);
                margin-bottom: 8px;
                line-height: 1;
                letter-spacing: -0.04em;
                font-family: 'JetBrains Mono', monospace;
            }
            
            .weather-description {
                font-size: 1.25rem;
                color: var(--text-secondary);
                text-transform: capitalize;
                margin-bottom: 12px;
                font-weight: 500;
            }
            
            .weather-feels-like {
                font-size: 0.95rem;
                color: var(--text-muted);
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 6px;
            }
            
            .weather-feels-like i {
                color: var(--accent-secondary);
            }
            
            .weather-details {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 16px;
            }
            
            .weather-detail-item {
                display: flex;
                flex-direction: column;
                align-items: center;
                padding: 24px 16px;
                background: var(--bg-secondary);
                border-radius: 16px;
                border: 1px solid var(--border);
                transition: all 0.3s ease;
            }
            
            .weather-detail-item:hover {
                background: var(--bg-card-hover);
                border-color: var(--border-hover);
                transform: translateY(-2px);
            }
            
            .weather-detail-icon {
                font-size: 1.5rem;
                margin-bottom: 12px;
                background: var(--accent-gradient);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }
            
            .weather-detail-label {
                font-size: 0.8rem;
                color: var(--text-muted);
                margin-bottom: 6px;
                text-transform: uppercase;
                letter-spacing: 0.1em;
                font-weight: 500;
            }
            
            .weather-detail-value {
                font-size: 1.5rem;
                font-weight: 700;
                color: var(--text-primary);
                font-family: 'JetBrains Mono', monospace;
            }
            
            /* ============================================
               ERROR MESSAGE - ENHANCED
               ============================================ */
            .error-message {
                display: none;
                background: linear-gradient(135deg, rgba(244, 63, 94, 0.1) 0%, rgba(244, 63, 94, 0.05) 100%);
                border: 1px solid var(--error);
                border-radius: 16px;
                padding: 24px;
                margin-bottom: 24px;
                text-align: center;
            }
            
            .error-message.show {
                display: block;
                animation: shake 0.5s cubic-bezier(0.36, 0.07, 0.19, 0.97);
            }
            
            @keyframes shake {
                0%, 100% { transform: translateX(0); }
                10%, 30%, 50%, 70%, 90% { transform: translateX(-4px); }
                20%, 40%, 60%, 80% { transform: translateX(4px); }
            }
            
            .error-icon {
                font-size: 2.5rem;
                color: var(--error);
                margin-bottom: 12px;
                animation: pulse 2s ease-in-out infinite;
            }
            
            .error-title {
                font-size: 1.1rem;
                font-weight: 600;
                color: var(--error);
                margin-bottom: 8px;
            }
            
            .error-text {
                color: var(--text-secondary);
                font-size: 0.95rem;
                margin-bottom: 16px;
            }
            
            .retry-button {
                padding: 12px 24px;
                background: var(--error);
                border: none;
                border-radius: 10px;
                color: white;
                font-family: 'Outfit', sans-serif;
                font-size: 0.95rem;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
                display: inline-flex;
                align-items: center;
                gap: 8px;
            }
            
            .retry-button:hover {
                background: #e11d48;
                transform: translateY(-2px);
                box-shadow: 0 8px 24px var(--error-glow);
            }
            
            /* ============================================
               5-DAY FORECAST SECTION - FULL WIDTH
               ============================================ */
            .forecast-section {
                margin-top: 24px;
                display: none;
                width: 100vw;
                position: relative;
                left: 50%;
                transform: translateX(-50%);
                padding: 0 24px;
                box-sizing: border-box;
            }
            
            .forecast-section.show {
                display: block;
            }
            
            .forecast-title {
                font-size: 1.25rem;
                color: var(--text-primary);
                margin-bottom: 20px;
                display: flex;
                align-items: center;
                gap: 12px;
                font-weight: 600;
                opacity: 0;
                animation: fadeSlideUp 0.5s cubic-bezier(0.16, 1, 0.3, 1) 0.3s forwards;
                max-width: 1200px;
                margin-left: auto;
                margin-right: auto;
            }
            
            .forecast-title i {
                color: var(--accent-primary);
            }
            
            .forecast-container {
                display: grid;
                grid-template-columns: repeat(5, 1fr);
                gap: 16px;
                max-width: 1200px;
                margin: 0 auto;
            }
            
            .forecast-card {
                background: var(--bg-card);
                border: 1px solid var(--border);
                border-radius: 20px;
                padding: 20px 16px;
                text-align: center;
                transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
                opacity: 0;
                transform: translateY(20px);
            }
            
            .forecast-card.reveal {
                animation: cardReveal 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards;
            }
            
            @keyframes cardReveal {
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            .forecast-card:hover {
                transform: translateY(-4px);
                border-color: var(--accent-primary);
                box-shadow: var(--shadow-glow);
            }
            
            .forecast-day {
                font-size: 0.9rem;
                color: var(--text-secondary);
                font-weight: 600;
                margin-bottom: 4px;
            }
            
            .forecast-date {
                font-size: 0.75rem;
                color: var(--text-muted);
                margin-bottom: 12px;
            }
            
            .forecast-icon {
                font-size: 2rem;
                margin: 8px 0;
                background: var(--accent-gradient);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }
            
            .forecast-temps {
                margin: 12px 0 8px;
            }
            
            .forecast-temp-high {
                font-size: 1.25rem;
                font-weight: 700;
                color: var(--text-primary);
                font-family: 'JetBrains Mono', monospace;
            }
            
            .forecast-temp-low {
                font-size: 1rem;
                color: var(--text-muted);
                margin-left: 4px;
                font-family: 'JetBrains Mono', monospace;
            }
            
            .forecast-description {
                font-size: 0.8rem;
                color: var(--text-secondary);
                margin-top: 8px;
                line-height: 1.3;
            }
            
            /* Forecast skeleton */
            .forecast-skeleton {
                display: none;
                margin-top: 24px;
                width: 100vw;
                position: relative;
                left: 50%;
                transform: translateX(-50%);
                padding: 0 24px;
                box-sizing: border-box;
            }
            
            .forecast-skeleton.show {
                display: block;
                animation: fadeIn 0.3s ease;
            }
            
            .forecast-skeleton-title {
                width: 180px;
                height: 24px;
                margin-bottom: 20px;
                max-width: 1200px;
                margin-left: auto;
                margin-right: auto;
            }
            
            .forecast-skeleton-container {
                display: grid;
                grid-template-columns: repeat(5, 1fr);
                gap: 16px;
                max-width: 1200px;
                margin: 0 auto;
            }
            
            .forecast-skeleton-card {
                height: 180px;
                border-radius: 20px;
            }
            
            /* ============================================
               COMPARISON TOOL SECTION
               ============================================ */
            .comparison-section {
                margin-top: 40px;
                display: none;
            }
            
            .comparison-section.show {
                display: block;
                animation: fadeSlideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1);
            }
            
            .comparison-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 24px;
            }
            
            .comparison-title {
                font-size: 1.5rem;
                font-weight: 700;
                color: var(--text-primary);
                display: flex;
                align-items: center;
                gap: 12px;
            }
            
            .comparison-title i {
                background: var(--accent-gradient);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }
            
            .comparison-count {
                background: var(--bg-secondary);
                padding: 6px 14px;
                border-radius: 12px;
                font-size: 0.85rem;
                font-weight: 600;
                color: var(--accent-primary);
                border: 1px solid var(--border);
            }
            
            .comparison-actions {
                display: flex;
                gap: 12px;
            }
            
            .clear-comparison-btn {
                padding: 10px 18px;
                background: var(--bg-secondary);
                border: 1px solid var(--border);
                border-radius: 12px;
                color: var(--text-secondary);
                font-size: 0.9rem;
                font-weight: 500;
                cursor: pointer;
                transition: all 0.3s ease;
                display: flex;
                align-items: center;
                gap: 8px;
            }
            
            .clear-comparison-btn:hover {
                background: var(--bg-card-hover);
                border-color: var(--error);
                color: var(--error);
                transform: translateY(-2px);
            }
            
            .add-to-comparison-btn {
                background: var(--comparison-highlight);
                color: #000;
                padding: 12px 20px;
                border: none;
                border-radius: 12px;
                font-size: 0.95rem;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
                display: flex;
                align-items: center;
                gap: 8px;
                margin-top: 16px;
                width: 100%;
                justify-content: center;
                position: relative;
                overflow: hidden;
            }
            
            .add-to-comparison-btn::before {
                content: '';
                position: absolute;
                inset: 0;
                background: linear-gradient(135deg, rgba(255,255,255,0.3) 0%, transparent 50%);
                opacity: 0;
                transition: opacity 0.3s ease;
            }
            
            .add-to-comparison-btn:hover::before {
                opacity: 1;
            }
            
            .add-to-comparison-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 24px var(--comparison-highlight-glow);
            }
            
            .add-to-comparison-btn:disabled {
                opacity: 0.5;
                cursor: not-allowed;
                transform: none;
            }
            
            .add-to-comparison-btn.added {
                background: var(--success);
                color: white;
            }
            
            .add-to-comparison-btn.added i {
                animation: checkmark 0.5s ease;
            }
            
            .comparison-container {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
                gap: 20px;
            }
            
            .comparison-card {
                background: var(--bg-card);
                border: 2px solid var(--border);
                border-radius: 20px;
                padding: 24px;
                position: relative;
                transition: all 0.3s ease;
                animation: scaleIn 0.4s cubic-bezier(0.16, 1, 0.3, 1);
            }
            
            .comparison-card:hover {
                border-color: var(--comparison-highlight);
                box-shadow: 0 8px 32px var(--comparison-highlight-glow);
                transform: translateY(-4px);
            }
            
            .comparison-card.best-temp {
                border-color: var(--comparison-best);
                background: linear-gradient(135deg, var(--bg-card) 0%, rgba(16, 185, 129, 0.05) 100%);
            }
            
            .comparison-card.worst-temp {
                border-color: var(--comparison-worst);
                background: linear-gradient(135deg, var(--bg-card) 0%, rgba(239, 68, 68, 0.05) 100%);
            }
            
            .comparison-badge {
                position: absolute;
                top: 12px;
                right: 12px;
                padding: 4px 10px;
                border-radius: 8px;
                font-size: 0.75rem;
                font-weight: 600;
                display: flex;
                align-items: center;
                gap: 4px;
            }
            
            .comparison-badge.warmest {
                background: var(--comparison-best);
                color: white;
            }
            
            .comparison-badge.coldest {
                background: var(--comparison-worst);
                color: white;
            }
            
            .comparison-card-header {
                display: flex;
                justify-content: space-between;
                align-items: flex-start;
                margin-bottom: 20px;
                padding-right: 60px;
            }
            
            .comparison-location {
                flex: 1;
            }
            
            .comparison-city {
                font-size: 1.25rem;
                font-weight: 700;
                color: var(--text-primary);
                margin-bottom: 4px;
            }
            
            .comparison-country {
                font-size: 0.85rem;
                color: var(--text-secondary);
                display: flex;
                align-items: center;
                gap: 6px;
            }
            
            .comparison-icon {
                font-size: 3rem;
                background: var(--accent-gradient);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }
            
            .comparison-temp {
                font-size: 2.5rem;
                font-weight: 800;
                color: var(--text-primary);
                font-family: 'JetBrains Mono', monospace;
                margin: 12px 0;
                position: relative;
            }
            
            .comparison-temp-indicator {
                position: absolute;
                right: -30px;
                top: 50%;
                transform: translateY(-50%);
                font-size: 1.5rem;
            }
            
            .comparison-temp-indicator.up {
                color: var(--comparison-worst);
            }
            
            .comparison-temp-indicator.down {
                color: var(--comparison-best);
            }
            
            .comparison-description {
                font-size: 0.9rem;
                color: var(--text-secondary);
                margin-bottom: 16px;
                text-transform: capitalize;
            }
            
            .comparison-metrics {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 12px;
                margin-top: 16px;
                padding-top: 16px;
                border-top: 1px solid var(--border);
            }
            
            .comparison-metric {
                text-align: center;
            }
            
            .comparison-metric-label {
                font-size: 0.75rem;
                color: var(--text-muted);
                margin-bottom: 4px;
                display: block;
            }
            
            .comparison-metric-value {
                font-size: 0.95rem;
                font-weight: 600;
                color: var(--text-primary);
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 4px;
            }
            
            .comparison-metric i {
                color: var(--accent-primary);
                font-size: 0.85rem;
            }
            
            .remove-comparison-btn {
                position: absolute;
                top: 12px;
                left: 12px;
                width: 32px;
                height: 32px;
                background: var(--bg-secondary);
                border: 1px solid var(--border);
                border-radius: 8px;
                color: var(--text-muted);
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                transition: all 0.3s ease;
                z-index: 10;
            }
            
            .remove-comparison-btn:hover {
                background: var(--error);
                border-color: var(--error);
                color: white;
                transform: scale(1.1);
            }
            
            .comparison-empty {
                text-align: center;
                padding: 60px 40px;
                background: var(--bg-card);
                border: 2px dashed var(--border);
                border-radius: 20px;
                color: var(--text-secondary);
            }
            
            .comparison-empty i {
                font-size: 3rem;
                color: var(--text-muted);
                margin-bottom: 16px;
                opacity: 0.5;
            }
            
            .comparison-empty-title {
                font-size: 1.1rem;
                font-weight: 600;
                color: var(--text-primary);
                margin-bottom: 8px;
            }
            
            .comparison-empty-text {
                font-size: 0.9rem;
            }
            
            /* ============================================
               SUCCESS INDICATOR
               ============================================ */
            .success-indicator {
                position: fixed;
                top: 24px;
                right: 24px;
                background: var(--success);
                color: white;
                padding: 12px 20px;
                border-radius: 12px;
                display: flex;
                align-items: center;
                gap: 10px;
                font-weight: 500;
                box-shadow: 0 8px 32px var(--success-glow);
                opacity: 0;
                transform: translateX(100%);
                transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
                z-index: 9999;
            }
            
            .success-indicator.show {
                opacity: 1;
                transform: translateX(0);
            }
            
            .success-indicator i {
                font-size: 1.1rem;
            }
            
            /* ============================================
               RESPONSIVE DESIGN
               ============================================ */
            @media (max-width: 768px) {
                body {
                    padding: 16px;
                }
                
                .container {
                    max-width: 100%;
                }
                
                header {
                    margin-bottom: 32px;
                }
                
                h1 {
                    font-size: 1.75rem;
                    gap: 12px;
                }
                
                .search-section {
                    padding: 24px;
                    border-radius: 20px;
                }
                
                .search-form {
                    flex-direction: column;
                }
                
                .search-button {
                    width: 100%;
                }
                
                .weather-display {
                    padding: 32px 24px;
                    border-radius: 20px;
                }
                
                .weather-header {
                    flex-direction: column;
                    align-items: center;
                    text-align: center;
                    gap: 16px;
                }
                
                .weather-country {
                    justify-content: center;
                }
                
                .weather-temp {
                    font-size: 3.5rem;
                }
                
                .weather-icon {
                    font-size: 4rem;
                }
                
                .weather-details {
                    grid-template-columns: repeat(3, 1fr);
                    gap: 12px;
                }
                
                .weather-detail-item {
                    padding: 16px 12px;
                }
                
                .weather-detail-value {
                    font-size: 1.25rem;
                }
                
                .forecast-container {
                    grid-template-columns: repeat(5, 1fr);
                    gap: 12px;
                }
                
                .forecast-card {
                    padding: 16px 8px;
                    border-radius: 16px;
                }
                
                .forecast-icon {
                    font-size: 1.5rem;
                }
                
                .forecast-skeleton-container {
                    grid-template-columns: repeat(5, 1fr);
                    gap: 8px;
                }
                
                .forecast-section {
                    padding: 0 16px;
                }
                
                .comparison-container {
                    grid-template-columns: 1fr;
                }
                
                .comparison-header {
                    flex-direction: column;
                    gap: 16px;
                    align-items: stretch;
                }
                
                .comparison-actions {
                    width: 100%;
                }
                
                .clear-comparison-btn {
                    flex: 1;
                    justify-content: center;
                }
            }
            
            @media (max-width: 480px) {
                .weather-details {
                    grid-template-columns: 1fr;
                }
                
                .forecast-container {
                    grid-template-columns: repeat(2, 1fr);
                }
                
                .forecast-skeleton-container {
                    grid-template-columns: repeat(2, 1fr);
                }
                
                .weather-skeleton-details {
                    grid-template-columns: 1fr;
                }
                
                .comparison-card-header {
                    padding-right: 0;
                }
                
                .comparison-temp {
                    font-size: 2rem;
                }
                
                .comparison-metrics {
                    grid-template-columns: 1fr;
                    gap: 8px;
                }
            }
        </style>
    </head>
    <body>
        <!-- Success indicator toast -->
        <div class="success-indicator" id="successIndicator">
            <i class="fas fa-check-circle"></i>
            <span>Weather loaded successfully</span>
        </div>
        
        <!-- Main container -->
        <div class="container">
            <!-- Header section -->
            <header>
                <h1><i class="fas fa-cloud-sun"></i> Weather Watcher</h1>
                <p class="subtitle">Real-time weather at your fingertips</p>
                <!-- Temperature Unit Toggle -->
                <div class="temperature-toggle-container">
                    <button class="temperature-toggle" id="temperatureToggle" aria-label="Toggle temperature unit">
                        <span class="temp-unit active" id="tempUnitC">°C</span>
                        <span class="temp-unit" id="tempUnitF">°F</span>
                    </button>
                </div>
            </header>
            
            <!-- Search form section -->
            <section class="search-section" aria-label="Search for weather">
                <form class="search-form" id="weatherForm" role="search">
                    <div class="autocomplete-wrapper">
                        <input
                            type="text"
                            class="search-input"
                            id="cityInput"
                            placeholder="Search any city worldwide..."
                            aria-label="City name"
                            required
                            autocomplete="off"
                        >
                        <div id="autocompleteDropdown" class="autocomplete-dropdown"></div>
                    </div>
                    <button type="submit" class="search-button" id="searchButton" aria-label="Search weather">
                        <span class="button-text">
                            <i class="fas fa-search" aria-hidden="true"></i>
                            Search
                        </span>
                        <div class="button-spinner"></div>
                    </button>
                </form>
            </section>
            
            <!-- Error message container -->
            <div class="error-message" id="errorMessage" role="alert" aria-live="polite">
                <div class="error-icon"><i class="fas fa-exclamation-triangle"></i></div>
                <div class="error-title">Unable to fetch weather</div>
                <div class="error-text" id="errorText"></div>
                <button class="retry-button" id="retryButton">
                    <i class="fas fa-redo"></i>
                    Try Again
                </button>
            </div>
            
            <!-- Inline loading state with skeleton -->
            <div class="loading-inline" id="loadingInline">
                <div class="loading-dots">
                    <div class="loading-dot"></div>
                    <div class="loading-dot"></div>
                    <div class="loading-dot"></div>
                </div>
                <div class="loading-weather-icon">
                    <i class="fas fa-cloud-sun-rain"></i>
                </div>
                <div class="loading-text">Fetching weather data...</div>
                <div class="loading-subtext" id="loadingSubtext">Locating city coordinates</div>
                <div class="loading-progress">
                    <div class="loading-progress-bar" id="loadingProgressBar"></div>
                </div>
            </div>
            
            <!-- Weather skeleton loader -->
            <div class="weather-skeleton" id="weatherSkeleton">
                <div class="weather-skeleton-header">
                    <div class="weather-skeleton-location">
                        <div class="skeleton weather-skeleton-city"></div>
                        <div class="skeleton weather-skeleton-country"></div>
                    </div>
                    <div class="skeleton weather-skeleton-icon skeleton-circle"></div>
                </div>
                <div class="weather-skeleton-main">
                    <div class="skeleton weather-skeleton-temp"></div>
                    <div class="skeleton weather-skeleton-desc"></div>
                    <div class="skeleton weather-skeleton-feels"></div>
                </div>
                <div class="weather-skeleton-details">
                    <div class="skeleton weather-skeleton-detail"></div>
                    <div class="skeleton weather-skeleton-detail"></div>
                    <div class="skeleton weather-skeleton-detail"></div>
                </div>
            </div>
            
            <!-- Weather display section -->
            <section class="weather-display" id="weatherDisplay" aria-label="Weather information">
                <div class="weather-header">
                    <div class="weather-location">
                        <h2 class="weather-city" id="weatherCity"></h2>
                        <p class="weather-country" id="weatherCountry">
                            <i class="fas fa-map-marker-alt"></i>
                            <span id="weatherCountryText"></span>
                        </p>
                    </div>
                    <div class="weather-icon" id="weatherIcon" aria-hidden="true"></div>
                </div>
                
                <div class="weather-main">
                    <div class="weather-temp" id="weatherTemp"></div>
                    <p class="weather-description" id="weatherDescription"></p>
                    <p class="weather-feels-like" id="weatherFeelsLike">
                        <i class="fas fa-temperature-low"></i>
                        <span id="weatherFeelsLikeText"></span>
                    </p>
                </div>
                
                <div class="weather-details" role="list">
                    <div class="weather-detail-item" role="listitem">
                        <i class="fas fa-tint weather-detail-icon" aria-hidden="true"></i>
                        <span class="weather-detail-label">Humidity</span>
                        <span class="weather-detail-value" id="weatherHumidity"></span>
                    </div>
                    <div class="weather-detail-item" role="listitem">
                        <i class="fas fa-wind weather-detail-icon" aria-hidden="true"></i>
                        <span class="weather-detail-label">Wind</span>
                        <span class="weather-detail-value" id="weatherWind"></span>
                    </div>
                    <div class="weather-detail-item" role="listitem">
                        <i class="fas fa-compress-arrows-alt weather-detail-icon" aria-hidden="true"></i>
                        <span class="weather-detail-label">Pressure</span>
                        <span class="weather-detail-value" id="weatherPressure"></span>
                    </div>
                </div>
                
                <!-- Add to Comparison Button -->
                <button class="add-to-comparison-btn" id="addToComparisonBtn">
                    <i class="fas fa-plus"></i>
                    <span id="addToComparisonText">Add to Comparison</span>
                </button>
            </section>
            
            <!-- Forecast skeleton -->
            <div class="forecast-skeleton" id="forecastSkeleton">
                <div class="skeleton forecast-skeleton-title"></div>
                <div class="forecast-skeleton-container">
                    <div class="skeleton forecast-skeleton-card"></div>
                    <div class="skeleton forecast-skeleton-card"></div>
                    <div class="skeleton forecast-skeleton-card"></div>
                    <div class="skeleton forecast-skeleton-card"></div>
                    <div class="skeleton forecast-skeleton-card"></div>
                </div>
            </div>
            
            <!-- 5-Day Forecast Section -->
            <section class="forecast-section" id="forecastSection">
                <h2 class="forecast-title">
                    <i class="fas fa-calendar-week"></i> 5-Day Forecast
                </h2>
                <div class="forecast-container" id="forecastContainer"></div>
            </section>
            
            <!-- Weather Comparison Section -->
            <section class="comparison-section" id="comparisonSection">
                <div class="comparison-header">
                    <div>
                        <h2 class="comparison-title">
                            <i class="fas fa-balance-scale"></i>
                            Weather Comparison
                        </h2>
                        <span class="comparison-count" id="comparisonCount">0 cities</span>
                    </div>
                    <div class="comparison-actions">
                        <button class="clear-comparison-btn" id="clearComparisonBtn">
                            <i class="fas fa-trash"></i>
                            Clear All
                        </button>
                    </div>
                </div>
                <div class="comparison-container" id="comparisonContainer">
                    <div class="comparison-empty">
                        <i class="fas fa-cloud-sun"></i>
                        <div class="comparison-empty-title">No cities to compare</div>
                        <div class="comparison-empty-text">Search for a city and click "Add to Comparison" to start comparing weather data</div>
                    </div>
                </div>
            </section>
        </div>
        
        <!-- JavaScript -->
        <script>
        document.addEventListener('DOMContentLoaded', () => {
            // ============================================
            // DOM ELEMENTS
            // ============================================
            const cityInput = document.getElementById('cityInput');
            const searchButton = document.getElementById('searchButton');
            const autocompleteDropdown = document.getElementById('autocompleteDropdown');
            const weatherForm = document.getElementById('weatherForm');
            const weatherDisplay = document.getElementById('weatherDisplay');
            const loadingInline = document.getElementById('loadingInline');
            const loadingSubtext = document.getElementById('loadingSubtext');
            const loadingProgressBar = document.getElementById('loadingProgressBar');
            const weatherSkeleton = document.getElementById('weatherSkeleton');
            const errorMessage = document.getElementById('errorMessage');
            const errorText = document.getElementById('errorText');
            const retryButton = document.getElementById('retryButton');
            const successIndicator = document.getElementById('successIndicator');
            const forecastSection = document.getElementById('forecastSection');
            const forecastContainer = document.getElementById('forecastContainer');
            const forecastSkeleton = document.getElementById('forecastSkeleton');
            
            // Weather display elements
            const weatherCity = document.getElementById('weatherCity');
            const weatherCountryText = document.getElementById('weatherCountryText');
            const weatherIcon = document.getElementById('weatherIcon');
            const weatherTemp = document.getElementById('weatherTemp');
            const weatherDescription = document.getElementById('weatherDescription');
            const weatherFeelsLikeText = document.getElementById('weatherFeelsLikeText');
            const weatherHumidity = document.getElementById('weatherHumidity');
            const weatherWind = document.getElementById('weatherWind');
            const weatherPressure = document.getElementById('weatherPressure');
            
            // Comparison elements
            const addToComparisonBtn = document.getElementById('addToComparisonBtn');
            const addToComparisonText = document.getElementById('addToComparisonText');
            const comparisonSection = document.getElementById('comparisonSection');
            const comparisonContainer = document.getElementById('comparisonContainer');
            const comparisonCount = document.getElementById('comparisonCount');
            const clearComparisonBtn = document.getElementById('clearComparisonBtn');
            
            // State
            let autocompleteTimeout = null;
            let selectedIndex = -1;
            let currentCity = '';
            let loadingInterval = null;
            let currentWeatherData = null;
            let comparisonCities = [];
            
            // Temperature unit management
            const temperatureToggle = document.getElementById('temperatureToggle');
            const tempUnitC = document.getElementById('tempUnitC');
            const tempUnitF = document.getElementById('tempUnitF');
            
            // Get unit from localStorage or default to Celsius
            let temperatureUnit = localStorage.getItem('temperatureUnit') || 'C';
            
            // Initialize toggle state
            function initializeTemperatureToggle() {
                if (temperatureUnit === 'F') {
                    tempUnitC.classList.remove('active');
                    tempUnitF.classList.add('active');
                } else {
                    tempUnitC.classList.add('active');
                    tempUnitF.classList.remove('active');
                }
            }
            
            // Temperature conversion functions
            function celsiusToFahrenheit(celsius) {
                return Math.round((celsius * 9/5) + 32);
            }
            
            function fahrenheitToCelsius(fahrenheit) {
                return Math.round((fahrenheit - 32) * 5/9);
            }
            
            // Convert temperature based on current unit
            function convertTemperature(celsius) {
                if (temperatureUnit === 'F') {
                    return celsiusToFahrenheit(celsius);
                }
                return celsius;
            }
            
            // Get temperature unit symbol
            function getTemperatureUnitSymbol() {
                return temperatureUnit === 'F' ? '°F' : '°C';
            }
            
            // Toggle temperature unit
            function toggleTemperatureUnit() {
                temperatureUnit = temperatureUnit === 'C' ? 'F' : 'C';
                localStorage.setItem('temperatureUnit', temperatureUnit);
                
                // Update toggle button appearance
                if (temperatureUnit === 'F') {
                    tempUnitC.classList.remove('active');
                    tempUnitF.classList.add('active');
                } else {
                    tempUnitC.classList.add('active');
                    tempUnitF.classList.remove('active');
                }
                
                // Update all displayed temperatures
                if (currentWeatherData) {
                    displayWeather(currentWeatherData);
                }
                
                // Update forecast if displayed
                if (forecastSection.classList.contains('show')) {
                    const city = currentCity || currentWeatherData?.city;
                    if (city) {
                        fetchForecast(city);
                    }
                }
                
                // Update comparison view if there are cities
                if (comparisonCities.length > 0) {
                    updateComparisonView();
                }
            }
            
            // Initialize on page load
            initializeTemperatureToggle();
            
            // Add event listener for toggle button
            temperatureToggle.addEventListener('click', toggleTemperatureUnit);
            
            // ============================================
            // WEATHER ICON MAPPING
            // ============================================
            const weatherIconMap = {
                '01d': 'fa-sun',
                '01n': 'fa-moon',
                '02d': 'fa-cloud-sun',
                '02n': 'fa-cloud-moon',
                '03d': 'fa-cloud',
                '03n': 'fa-cloud',
                '04d': 'fa-cloud',
                '04n': 'fa-cloud',
                '09d': 'fa-cloud-rain',
                '09n': 'fa-cloud-rain',
                '10d': 'fa-cloud-sun-rain',
                '10n': 'fa-cloud-moon-rain',
                '11d': 'fa-bolt',
                '11n': 'fa-bolt',
                '13d': 'fa-snowflake',
                '13n': 'fa-snowflake',
                '50d': 'fa-smog',
                '50n': 'fa-smog'
            };
            
            function getWeatherIcon(iconCode) {
                const iconClass = weatherIconMap[iconCode] || 'fa-cloud';
                return `<i class="fas ${iconClass}"></i>`;
            }
            
            // ============================================
            // LOADING STATE MANAGEMENT
            // ============================================
            const loadingMessages = [
                'Locating city coordinates',
                'Connecting to weather service',
                'Fetching current conditions',
                'Processing weather data',
                'Almost there...'
            ];
            
            function showLoadingState() {
                // Hide other states
                weatherDisplay.classList.remove('show', 'reveal');
                forecastSection.classList.remove('show');
                errorMessage.classList.remove('show');
                
                // Show loading
                loadingInline.classList.add('show');
                
                // Add loading class to button
                searchButton.classList.add('loading');
                searchButton.disabled = true;
                
                // Animate progress bar and messages
                let progress = 0;
                let messageIndex = 0;
                
                loadingProgressBar.style.width = '0%';
                loadingSubtext.textContent = loadingMessages[0];
                
                loadingInterval = setInterval(() => {
                    progress += Math.random() * 15 + 5;
                    if (progress > 90) progress = 90;
                    loadingProgressBar.style.width = `${progress}%`;
                    
                    // Update message
                    const newIndex = Math.min(Math.floor(progress / 20), loadingMessages.length - 1);
                    if (newIndex !== messageIndex) {
                        messageIndex = newIndex;
                        loadingSubtext.style.opacity = '0';
                        setTimeout(() => {
                            loadingSubtext.textContent = loadingMessages[messageIndex];
                            loadingSubtext.style.opacity = '1';
                        }, 150);
                    }
                }, 300);
            }
            
            function showSkeletonState() {
                loadingInline.classList.remove('show');
                weatherSkeleton.classList.add('show');
                forecastSkeleton.classList.add('show');
            }
            
            function hideLoadingState() {
                // Clear interval
                if (loadingInterval) {
                    clearInterval(loadingInterval);
                    loadingInterval = null;
                }
                
                // Complete progress bar
                loadingProgressBar.style.width = '100%';
                
                // Delay hiding for smooth transition
                setTimeout(() => {
                    loadingInline.classList.remove('show');
                    weatherSkeleton.classList.remove('show');
                    forecastSkeleton.classList.remove('show');
                    searchButton.classList.remove('loading');
                    searchButton.disabled = false;
                }, 200);
            }
            
            function showSuccessToast() {
                successIndicator.classList.add('show');
                setTimeout(() => {
                    successIndicator.classList.remove('show');
                }, 3000);
            }
            
            function showError(message) {
                hideLoadingState();
                errorText.textContent = message;
                errorMessage.classList.add('show');
                weatherDisplay.classList.remove('show');
                forecastSection.classList.remove('show');
            }
            
            function hideError() {
                errorMessage.classList.remove('show');
            }
            
            // ============================================
            // AUTOCOMPLETE FUNCTIONALITY
            // ============================================
            function handleAutocomplete() {
                const query = cityInput.value.trim();
                if (autocompleteTimeout) clearTimeout(autocompleteTimeout);
                if (query.length < 2) {
                    hideAutocomplete();
                    return;
                }
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
                if (suggestions.length === 0) {
                    showAutocompleteEmpty();
                    return;
                }
                
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
                autocompleteDropdown.innerHTML = '<div class="autocomplete-loading"><i class="fas fa-circle-notch fa-spin"></i> Searching cities...</div>';
                autocompleteDropdown.classList.add('show');
            }
            
            function showAutocompleteEmpty() {
                autocompleteDropdown.innerHTML = '<div class="autocomplete-empty"><i class="fas fa-search"></i> No cities found</div>';
                autocompleteDropdown.classList.add('show');
            }
            
            function hideAutocomplete() {
                if (!autocompleteDropdown.classList.contains('show')) return;
                
                // Add hiding animation
                autocompleteDropdown.classList.add('hiding');
                
                // Remove classes after animation completes
                setTimeout(() => {
                    autocompleteDropdown.classList.remove('show', 'hiding');
                    autocompleteDropdown.innerHTML = '';
                    selectedIndex = -1;
                }, 200);
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
                // Don't trigger autocomplete on focus - wait for user to type
                // This prevents the jarring jump when clicking back into the search box
            });
            
            // ============================================
            // WEATHER FETCH
            // ============================================
            async function fetchWeather(city, retryCount = 0) {
                try {
                    showLoadingState();
                    hideError();
                    hideAutocomplete();
                    currentCity = city;
                    
                    // Simulate slight delay for better UX (shows loading states)
                    await new Promise(resolve => setTimeout(resolve, 500));
                    
                    // Show skeleton after initial loading animation
                    showSkeletonState();
                    
                    const response = await fetch(`/api/weather?city=${encodeURIComponent(city)}`);
                    
                    if (!response.ok) {
                        const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }));
                        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
                    }
                    
                    const data = await response.json();
                    
                    // Hide loading and display weather
                    hideLoadingState();
                    displayWeather(data);
                    showSuccessToast();
                    
                    // Fetch forecast
                    fetchForecast(data.city);
                    
                } catch (error) {
                    console.error('Weather fetch error:', error);
                    
                    let errorMsg = 'Failed to fetch weather data. ';
                    
                    if (error.message.includes('404') || error.message.includes('not found')) {
                        errorMsg = `City "${city}" not found. Please check the spelling and try again.`;
                    } else if (error.message.includes('timeout')) {
                        errorMsg = 'Request timed out. The weather service is taking too long to respond.';
                    } else if (error.message.includes('network') || error.message.includes('Failed to fetch')) {
                        errorMsg = 'Network error. Please check your internet connection.';
                    } else {
                        errorMsg += error.message;
                    }
                    
                    showError(errorMsg);
                    
                    if (retryCount < 2) {
                        retryButton.onclick = () => fetchWeather(city, retryCount + 1);
                        retryButton.style.display = 'inline-flex';
                    } else {
                        retryButton.style.display = 'none';
                    }
                }
            }
            
            // ============================================
            // DISPLAY WEATHER DATA
            // ============================================
            function displayWeather(data) {
                // Store current weather data for comparison
                currentWeatherData = data;
                
                // Convert temperatures based on selected unit
                const displayTemp = convertTemperature(data.temperature);
                const displayFeelsLike = convertTemperature(data.feels_like);
                const unitSymbol = getTemperatureUnitSymbol();
                
                weatherCity.textContent = data.city;
                weatherCountryText.textContent = data.country || '';
                weatherIcon.innerHTML = getWeatherIcon(data.icon);
                weatherTemp.textContent = `${displayTemp}${unitSymbol}`;
                weatherDescription.textContent = data.description;
                weatherFeelsLikeText.textContent = `Feels like ${displayFeelsLike}${unitSymbol}`;
                weatherHumidity.textContent = `${data.humidity}%`;
                weatherWind.textContent = `${data.wind_speed} m/s`;
                weatherPressure.textContent = `${data.pressure} hPa`;
                
                // Show with staggered reveal animation
                weatherDisplay.classList.add('show', 'reveal');
                cityInput.blur();
                
                // Enable/update add to comparison button
                const existingCity = comparisonCities.find(c => 
                    c.city.toLowerCase() === data.city.toLowerCase()
                );
                
                if (existingCity) {
                    addToComparisonBtn.classList.add('added');
                    addToComparisonText.textContent = 'Already Added';
                    addToComparisonBtn.querySelector('i').className = 'fas fa-check';
                } else {
                    addToComparisonBtn.classList.remove('added');
                    addToComparisonText.textContent = 'Add to Comparison';
                    addToComparisonBtn.querySelector('i').className = 'fas fa-plus';
                }
            }
            
            // ============================================
            // FORECAST FETCH & DISPLAY
            // ============================================
            async function fetchForecast(city) {
                try {
                    forecastSkeleton.classList.add('show');
                    
                    const response = await fetch(`/api/forecast?city=${encodeURIComponent(city)}`);
                    
                    if (!response.ok) {
                        throw new Error('Failed to fetch forecast');
                    }
                    
                    const data = await response.json();
                    
                    forecastSkeleton.classList.remove('show');
                    displayForecast(data.forecasts);
                    
                } catch (error) {
                    console.error('Forecast fetch error:', error);
                    forecastSkeleton.classList.remove('show');
                    forecastSection.classList.remove('show');
                }
            }
            
            function displayForecast(forecasts) {
                if (!forecasts || forecasts.length === 0) {
                    forecastSection.classList.remove('show');
                    return;
                }
                
                forecastContainer.innerHTML = '';
                
                const unitSymbol = getTemperatureUnitSymbol();
                
                forecasts.forEach((forecast, index) => {
                    const card = document.createElement('div');
                    card.className = 'forecast-card';
                    
                    // Add staggered reveal animation
                    setTimeout(() => {
                        card.classList.add('reveal');
                    }, index * 100);
                    
                    const date = new Date(forecast.date);
                    const dayName = date.toLocaleDateString('en-US', { weekday: 'short' });
                    const monthDay = date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
                    
                    const icon = getWeatherIcon(forecast.icon);
                    
                    // Convert forecast temperatures
                    const displayTempMax = convertTemperature(forecast.temp_max);
                    const displayTempMin = convertTemperature(forecast.temp_min);
                    
                    card.innerHTML = `
                        <div class="forecast-day">${dayName}</div>
                        <div class="forecast-date">${monthDay}</div>
                        <div class="forecast-icon">${icon}</div>
                        <div class="forecast-temps">
                            <span class="forecast-temp-high">${displayTempMax}${unitSymbol}</span>
                            <span class="forecast-temp-low">${displayTempMin}${unitSymbol}</span>
                        </div>
                        <div class="forecast-description">${forecast.description}</div>
                    `;
                    
                    forecastContainer.appendChild(card);
                });
                
                forecastSection.classList.add('show');
            }
            
            // ============================================
            // COMPARISON TOOL FUNCTIONS
            // ============================================
            
            // Add to comparison button handler
            addToComparisonBtn.addEventListener('click', () => {
                if (!currentWeatherData) return;
                
                // Check if city already exists in comparison
                const existingCity = comparisonCities.find(c => 
                    c.city.toLowerCase() === currentWeatherData.city.toLowerCase()
                );
                
                if (existingCity) {
                    showError('This city is already in the comparison list.');
                    return;
                }
                
                // Limit to 5 cities
                if (comparisonCities.length >= 5) {
                    showError('Maximum 5 cities can be compared at once.');
                    return;
                }
                
                // Add city to comparison
                comparisonCities.push({...currentWeatherData});
                updateComparisonView();
                
                // Show success feedback
                addToComparisonBtn.classList.add('added');
                addToComparisonText.textContent = 'Added!';
                const icon = addToComparisonBtn.querySelector('i');
                icon.className = 'fas fa-check';
                
                setTimeout(() => {
                    addToComparisonBtn.classList.remove('added');
                    addToComparisonText.textContent = 'Add to Comparison';
                    icon.className = 'fas fa-plus';
                }, 2000);
            });
            
            // Clear all comparison button handler
            clearComparisonBtn.addEventListener('click', () => {
                if (comparisonCities.length === 0) return;
                
                if (confirm('Are you sure you want to clear all cities from comparison?')) {
                    comparisonCities = [];
                    updateComparisonView();
                }
            });
            
            // Update comparison view
            function updateComparisonView() {
                // Update count
                comparisonCount.textContent = `${comparisonCities.length} ${comparisonCities.length === 1 ? 'city' : 'cities'}`;
                
                // Show/hide section
                if (comparisonCities.length > 0) {
                    comparisonSection.classList.add('show');
                } else {
                    comparisonSection.classList.remove('show');
                }
                
                // Clear container
                comparisonContainer.innerHTML = '';
                
                if (comparisonCities.length === 0) {
                    comparisonContainer.innerHTML = `
                        <div class="comparison-empty">
                            <i class="fas fa-cloud-sun"></i>
                            <div class="comparison-empty-title">No cities to compare</div>
                            <div class="comparison-empty-text">Search for a city and click "Add to Comparison" to start comparing weather data</div>
                        </div>
                    `;
                    return;
                }
                
                // Find warmest and coldest (using Celsius values for comparison logic)
                const temps = comparisonCities.map(c => c.temperature);
                const maxTemp = Math.max(...temps);
                const minTemp = Math.min(...temps);
                const avgTemp = temps.reduce((a, b) => a + b, 0) / temps.length;
                
                const unitSymbol = getTemperatureUnitSymbol();
                
                // Render comparison cards
                comparisonCities.forEach((city, index) => {
                    const card = document.createElement('div');
                    card.className = 'comparison-card';
                    
                    // Convert temperature for display
                    const displayTemp = convertTemperature(city.temperature);
                    
                    // Add best/worst temp classes (using Celsius for comparison)
                    if (city.temperature === maxTemp && comparisonCities.length > 1) {
                        card.classList.add('best-temp');
                    }
                    if (city.temperature === minTemp && comparisonCities.length > 1) {
                        card.classList.add('worst-temp');
                    }
                    
                    // Get weather icon
                    const iconClass = weatherIconMap[city.icon] || 'fa-cloud';
                    
                    // Temperature indicator (using Celsius for comparison)
                    let tempIndicator = '';
                    if (comparisonCities.length > 1) {
                        if (city.temperature > avgTemp) {
                            tempIndicator = '<i class="fas fa-arrow-up comparison-temp-indicator up"></i>';
                        } else if (city.temperature < avgTemp) {
                            tempIndicator = '<i class="fas fa-arrow-down comparison-temp-indicator down"></i>';
                        }
                    }
                    
                    // Badge for warmest/coldest
                    let badge = '';
                    if (city.temperature === maxTemp && comparisonCities.length > 1) {
                        badge = '<div class="comparison-badge warmest"><i class="fas fa-fire"></i> Warmest</div>';
                    } else if (city.temperature === minTemp && comparisonCities.length > 1) {
                        badge = '<div class="comparison-badge coldest"><i class="fas fa-snowflake"></i> Coldest</div>';
                    }
                    
                    card.innerHTML = `
                        <button class="remove-comparison-btn" onclick="removeFromComparison(${index})" title="Remove from comparison">
                            <i class="fas fa-times"></i>
                        </button>
                        ${badge}
                        <div class="comparison-card-header">
                            <div class="comparison-location">
                                <div class="comparison-city">${city.city}</div>
                                <div class="comparison-country">
                                    <i class="fas fa-map-marker-alt"></i>
                                    ${city.country}
                                </div>
                            </div>
                        </div>
                        <div class="comparison-icon"><i class="fas ${iconClass}"></i></div>
                        <div class="comparison-temp">
                            ${displayTemp}${unitSymbol}
                            ${tempIndicator}
                        </div>
                        <div class="comparison-description">${city.description}</div>
                        <div class="comparison-metrics">
                            <div class="comparison-metric">
                                <span class="comparison-metric-label">Humidity</span>
                                <div class="comparison-metric-value">
                                    <i class="fas fa-tint"></i>
                                    ${city.humidity}%
                                </div>
                            </div>
                            <div class="comparison-metric">
                                <span class="comparison-metric-label">Wind</span>
                                <div class="comparison-metric-value">
                                    <i class="fas fa-wind"></i>
                                    ${city.wind_speed} m/s
                                </div>
                            </div>
                            <div class="comparison-metric">
                                <span class="comparison-metric-label">Pressure</span>
                                <div class="comparison-metric-value">
                                    <i class="fas fa-compress-arrows-alt"></i>
                                    ${city.pressure} hPa
                                </div>
                            </div>
                        </div>
                    `;
                    
                    comparisonContainer.appendChild(card);
                });
            }
            
            // Global function to remove from comparison (called from inline onclick)
            window.removeFromComparison = function(index) {
                comparisonCities.splice(index, 1);
                updateComparisonView();
            };
            
            // ============================================
            // FORM SUBMISSION
            // ============================================
            weatherForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                
                const city = cityInput.value.trim();
                
                if (!city) {
                    showError('Please enter a city name.');
                    return;
                }
                
                await fetchWeather(city);
            });
            
            // Button ripple effect
            searchButton.addEventListener('click', function(e) {
                const rect = this.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                
                const ripple = document.createElement('span');
                ripple.className = 'ripple';
                ripple.style.left = `${x}px`;
                ripple.style.top = `${y}px`;
                
                this.appendChild(ripple);
                
                setTimeout(() => ripple.remove(), 600);
            });
            
        }); // End DOMContentLoaded
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
    country: str = Field(..., description="Country name (converted from ISO 3166-1 alpha-2 code)")
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
                "country": "United Kingdom",
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
            "country": convert_country_code_to_name("US"),  # Fallback for mock data only
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
        
        # Return weather data with full country name from Google's API
        return {
            "city": weather_data.city,
            "country": weather_data.country_name,  # Use full name directly from Google
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

# -----------------------------------------------
# Weather Forecast Endpoint
# -----------------------------------------------
@app.get(
    "/api/forecast",
    summary="Get 5-day weather forecast",
    description="Get weather forecast for the next 5 days for a given city.",
)
async def get_forecast(
    city: str = Query(
        ...,
        min_length=2,
        max_length=100,
        description="City name",
        example="Madrid"
    )
):
    """
    Get 5-day weather forecast for a city using OpenWeatherMap API.
    
    Returns forecast data for the next 5 days including:
    - Date
    - High/low temperatures
    - Weather condition description
    - Weather icon code
    """
    # Validate city name
    city = validate_city_name(city)
    
    # Get OpenWeatherMap API key
    openweather_key = os.getenv("OPENWEATHER_API_KEY")
    
    if not openweather_key:
        logger.error("OPENWEATHER_API_KEY not configured")
        raise HTTPException(
            status_code=503,
            detail="Forecast service not configured. Please set OPENWEATHER_API_KEY."
        )
    
    try:
        # Fetch forecast directly from OpenWeatherMap API
        url = "https://api.openweathermap.org/data/2.5/forecast"
        params = {
            "q": city,
            "appid": openweather_key,
            "units": "metric",
            "cnt": 40  # 5 days × 8 data points per day (3-hour intervals)
        }
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)
            
            if response.status_code == 404:
                raise HTTPException(
                    status_code=404,
                    detail=f"City not found: {city}"
                )
            
            response.raise_for_status()
            data = response.json()
            
            if data.get("cod") != "200":
                raise HTTPException(
                    status_code=500,
                    detail=f"Weather API error: {data.get('message', 'Unknown error')}"
                )
            
            # Parse forecast data - group by day and get min/max temps
            daily_data = {}
            
            for item in data.get("list", []):
                dt_txt = item.get("dt_txt", "")
                if not dt_txt:
                    continue
                
                date = dt_txt.split(" ")[0]
                
                if date not in daily_data:
                    daily_data[date] = {
                        "temps": [],
                        "descriptions": [],
                        "icons": []
                    }
                
                # Collect temperature data
                temp = item.get("main", {}).get("temp", 0)
                daily_data[date]["temps"].append(temp)
                
                # Prefer midday weather data (12:00-15:00) for description
                hour = dt_txt.split(" ")[1] if " " in dt_txt else ""
                if hour in ["12:00:00", "15:00:00", "09:00:00"]:
                    weather_info = item.get("weather", [{}])[0]
                    daily_data[date]["descriptions"].append(
                        weather_info.get("description", "").capitalize()
                    )
                    daily_data[date]["icons"].append(
                        weather_info.get("icon", "01d")
                    )
            
            # Build forecast response for first 5 days
            forecasts = []
            for date in sorted(daily_data.keys())[:5]:
                day = daily_data[date]
                
                if not day["temps"]:
                    continue
                
                description = day["descriptions"][0] if day["descriptions"] else "Clear"
                icon = day["icons"][0] if day["icons"] else "01d"
                
                forecasts.append({
                    "date": date,
                    "temp_max": round(max(day["temps"])),
                    "temp_min": round(min(day["temps"])),
                    "description": description,
                    "icon": icon,
                })
            
            logger.info(f"Successfully fetched forecast for: {city}")
            
            return {
                "city": city.title(),
                "forecasts": forecasts
            }
            
    except HTTPException:
        raise
    except httpx.TimeoutException:
        logger.error(f"Forecast timeout for city: {city}")
        raise HTTPException(
            status_code=504,
            detail="Forecast service timeout. Please try again."
        )
    except httpx.HTTPStatusError as e:
        logger.error(f"Forecast HTTP error for {city}: {e.response.status_code}")
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch forecast data"
        )
    except Exception as e:
        logger.error(f"Unexpected error fetching forecast for {city}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred"
        )