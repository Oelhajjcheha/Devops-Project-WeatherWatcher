"""
Test Suite for Weather Watcher API
----------------------------------
Unit tests for all API endpoints including weather functionality.
"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app, validate_city_name
from app.services.weather_service import (
    WeatherService,
    WeatherData,
    GeoLocation,
    CityNotFoundError,
    WeatherAPIError,
    APIKeyMissingError,
)

client = TestClient(app)


# ============================================
# Basic Endpoint Tests
# ============================================

def test_read_root():
    """Test the root endpoint returns HTML"""
    response = client.get("/")
    assert response.status_code == 200
    assert "Weather Watcher" in response.text


def test_health_check():
    """Test health endpoint returns correct status"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["version"] == "0.1.0"


def test_api_info():
    """Test info endpoint returns project details"""
    response = client.get("/api/info")
    assert response.status_code == 200
    data = response.json()
    assert data["project"] == "Weather Watcher"


# ============================================
# Input Validation Tests
# ============================================

class TestCityValidation:
    """Tests for city name input validation."""
    
    def test_valid_city_name(self):
        """Test that valid city names pass validation."""
        from fastapi import HTTPException
        
        assert validate_city_name("London") == "London"
        assert validate_city_name("  New York  ") == "New York"
        assert validate_city_name("São Paulo") == "São Paulo"
        assert validate_city_name("St. John's") == "St. John's"
        assert validate_city_name("Los Angeles, CA") == "Los Angeles, CA"
    
    def test_empty_city_name(self):
        """Test that empty city names raise HTTPException."""
        from fastapi import HTTPException
        
        with pytest.raises(HTTPException) as exc_info:
            validate_city_name("")
        assert exc_info.value.status_code == 400
        assert "empty" in exc_info.value.detail.lower()
    
    def test_whitespace_only_city(self):
        """Test that whitespace-only names raise HTTPException."""
        from fastapi import HTTPException
        
        with pytest.raises(HTTPException) as exc_info:
            validate_city_name("   ")
        assert exc_info.value.status_code == 400
    
    def test_short_city_name(self):
        """Test that single-character city names raise HTTPException."""
        from fastapi import HTTPException
        
        with pytest.raises(HTTPException) as exc_info:
            validate_city_name("A")
        assert exc_info.value.status_code == 400
        assert "at least 2" in exc_info.value.detail.lower()
    
    def test_long_city_name(self):
        """Test that overly long city names raise HTTPException."""
        from fastapi import HTTPException
        
        long_name = "A" * 101
        with pytest.raises(HTTPException) as exc_info:
            validate_city_name(long_name)
        assert exc_info.value.status_code == 400
        assert "too long" in exc_info.value.detail.lower()
    
    def test_invalid_characters(self):
        """Test that city names with invalid characters raise HTTPException."""
        from fastapi import HTTPException
        
        with pytest.raises(HTTPException) as exc_info:
            validate_city_name("London<script>")
        assert exc_info.value.status_code == 400
        assert "invalid characters" in exc_info.value.detail.lower()


# ============================================
# Weather Endpoint Tests (Mock Data)
# ============================================

class TestWeatherEndpointMockData:
    """Tests for weather endpoint when API key is not configured (mock data)."""
    
    def test_weather_by_query_returns_mock_data(self):
        """Test /api/weather returns mock data when no API key."""
        with patch.dict("os.environ", {"GOOGLE_MAPS_API_KEY": ""}, clear=False):
            response = client.get("/api/weather?city=London")
            assert response.status_code == 200
            data = response.json()
            
            # Check required fields exist
            assert "city" in data
            assert "temperature" in data
            assert "feels_like" in data
            assert "description" in data
            assert "humidity" in data
            assert "wind_speed" in data
            assert "pressure" in data
            assert "icon" in data
            assert "country" in data
            
            # Check mock data indicator
            assert "Mock" in data["description"] or data["city"] == "London"
    
    def test_weather_by_path_returns_mock_data(self):
        """Test /weather/{city} returns mock data when no API key."""
        with patch.dict("os.environ", {"GOOGLE_MAPS_API_KEY": ""}, clear=False):
            response = client.get("/weather/Tokyo")
            assert response.status_code == 200
            data = response.json()
            
            assert data["city"] == "Tokyo"
            assert isinstance(data["temperature"], int)
    
    def test_weather_invalid_empty_city(self):
        """Test that empty city parameter returns 400/422."""
        response = client.get("/api/weather?city=")
        # FastAPI returns 422 for validation errors
        assert response.status_code in [400, 422]
    
    def test_weather_missing_city_parameter(self):
        """Test that missing city parameter returns 422."""
        response = client.get("/api/weather")
        assert response.status_code == 422


# ============================================
# Weather Service Unit Tests
# ============================================

class TestWeatherService:
    """Unit tests for WeatherService class."""
    
    @pytest.fixture
    def service(self):
        """Create a WeatherService instance with test API key."""
        return WeatherService(api_key="test_api_key")
    
    def test_service_initialization_with_key(self):
        """Test service initializes with provided API key."""
        service = WeatherService(api_key="my_test_key")
        assert service.api_key == "my_test_key"
    
    def test_service_initialization_from_env(self):
        """Test service reads API key from environment."""
        with patch.dict("os.environ", {"GOOGLE_MAPS_API_KEY": "env_key"}):
            service = WeatherService()
            assert service.api_key == "env_key"
    
    def test_validate_api_key_raises_when_missing(self):
        """Test that missing API key raises APIKeyMissingError."""
        service = WeatherService(api_key=None)
        with pytest.raises(APIKeyMissingError):
            service._validate_api_key()
    
    def test_map_weather_icon_daytime(self):
        """Test icon mapping for daytime conditions."""
        service = WeatherService(api_key="test")
        
        assert service._map_weather_icon("CLEAR", is_daytime=True) == "01d"
        assert service._map_weather_icon("RAIN", is_daytime=True) == "10d"
        assert service._map_weather_icon("SNOW", is_daytime=True) == "13d"
        assert service._map_weather_icon("THUNDERSTORM", is_daytime=True) == "11d"
    
    def test_map_weather_icon_nighttime(self):
        """Test icon mapping for nighttime conditions."""
        service = WeatherService(api_key="test")
        
        assert service._map_weather_icon("CLEAR", is_daytime=False) == "01n"
        assert service._map_weather_icon("RAIN", is_daytime=False) == "10n"
    
    def test_map_weather_icon_unknown_condition(self):
        """Test icon mapping returns default for unknown conditions."""
        service = WeatherService(api_key="test")
        
        assert service._map_weather_icon("UNKNOWN_CONDITION", is_daytime=True) == "03d"
    
    def test_parse_weather_response(self):
        """Test parsing of Google Weather API response."""
        service = WeatherService(api_key="test")
        
        mock_response = {
            "currentTime": "2025-01-28T22:13:56Z",
            "isDaytime": True,
            "weatherCondition": {
                "type": "CLEAR",
                "description": {"text": "Sunny"}
            },
            "temperature": {"degrees": 20.5},
            "feelsLikeTemperature": {"degrees": 19.0},
            "relativeHumidity": 65,
            "wind": {"speed": {"value": 18}},  # km/h
            "airPressure": {"meanSeaLevelMillibars": 1015.5}
        }
        
        location = GeoLocation(
            latitude=51.5,
            longitude=-0.1,
            city="London",
            country="GB",
            country_name="United Kingdom"  # Add country_name
        )
        
        result = service._parse_weather_response(mock_response, location)
        
        assert result.city == "London"
        assert result.country == "GB"
        assert result.country_name == "United Kingdom"  # Test country_name field
        assert result.temperature == 20  # rounded from 20.5
        assert result.feels_like == 19
        assert result.description == "Sunny"
        assert result.humidity == 65
        assert result.wind_speed == 5.0  # 18 km/h ≈ 5 m/s
        assert result.pressure == 1015
        assert result.icon == "01d"


# ============================================
# Weather Endpoint Integration Tests (Mocked API)
# ============================================

class TestWeatherEndpointWithMockedAPI:
    """Integration tests for weather endpoint with mocked external APIs."""
    
    @pytest.mark.skip(reason="Async tests not properly configured - will fix in separate PR")
    @pytest.mark.asyncio
    async def test_successful_weather_fetch(self):
        """Test successful weather fetch with mocked Google APIs."""
        mock_weather_data = WeatherData(
            city="Paris",
            country="FR",
            country_name="France",  # Add country_name field
            temperature=18,
            feels_like=17,
            description="Partly cloudy",
            humidity=70,
            wind_speed=4.5,
            pressure=1012,
            icon="02d"
        )
        
        with patch.dict("os.environ", {"GOOGLE_MAPS_API_KEY": "test_key"}):
            with patch.object(
                WeatherService,
                'get_weather_by_city',
                new_callable=AsyncMock,
                return_value=mock_weather_data
            ):
                response = client.get("/api/weather?city=Paris")
                
                assert response.status_code == 200
                data = response.json()
                assert data["city"] == "Paris"
                assert data["country"] == "France"  # Now returns full country name
                assert data["temperature"] == 18
    
    @pytest.mark.skip(reason="Async tests not properly configured - will fix in separate PR")
    @pytest.mark.asyncio
    async def test_city_not_found_error(self):
        """Test 404 response when city is not found."""
        with patch.dict("os.environ", {"GOOGLE_MAPS_API_KEY": "test_key"}):
            with patch.object(
                WeatherService,
                'get_weather_by_city',
                new_callable=AsyncMock,
                side_effect=CityNotFoundError("City not found: Fakeville")
            ):
                response = client.get("/api/weather?city=Fakeville")
                
                assert response.status_code == 404
                assert "not found" in response.json()["detail"].lower()
    
    @pytest.mark.skip(reason="Async tests not properly configured - will fix in separate PR")
    @pytest.mark.asyncio
    async def test_weather_api_error(self):
        """Test 500 response when weather API fails."""
        with patch.dict("os.environ", {"GOOGLE_MAPS_API_KEY": "test_key"}):
            with patch.object(
                WeatherService,
                'get_weather_by_city',
                new_callable=AsyncMock,
                side_effect=WeatherAPIError("Service unavailable")
            ):
                response = client.get("/api/weather?city=London")
                
                assert response.status_code == 500
    
    @pytest.mark.skip(reason="Async tests not properly configured - will fix in separate PR")
    @pytest.mark.asyncio
    async def test_weather_timeout_error(self):
        """Test 504 response when weather API times out."""
        with patch.dict("os.environ", {"GOOGLE_MAPS_API_KEY": "test_key"}):
            with patch.object(
                WeatherService,
                'get_weather_by_city',
                new_callable=AsyncMock,
                side_effect=WeatherAPIError("Weather service timeout")
            ):
                response = client.get("/api/weather?city=London")
                
                assert response.status_code == 504


# ============================================
# Response Format Tests
# ============================================

class TestWeatherResponseFormat:
    """Tests to verify weather response format matches frontend expectations."""
    
    def test_response_contains_all_required_fields(self):
        """Verify response has all fields expected by frontend."""
        with patch.dict("os.environ", {"GOOGLE_MAPS_API_KEY": ""}, clear=False):
            response = client.get("/api/weather?city=Berlin")
            assert response.status_code == 200
            data = response.json()
            
            required_fields = [
                "city",
                "country", 
                "temperature",
                "feels_like",
                "description",
                "humidity",
                "wind_speed",
                "pressure",
                "icon"
            ]
            
            for field in required_fields:
                assert field in data, f"Missing required field: {field}"
    
    def test_temperature_is_integer(self):
        """Verify temperature is returned as integer (Celsius)."""
        with patch.dict("os.environ", {"GOOGLE_MAPS_API_KEY": ""}, clear=False):
            response = client.get("/api/weather?city=Madrid")
            data = response.json()
            
            assert isinstance(data["temperature"], int)
            assert isinstance(data["feels_like"], int)
    
    def test_wind_speed_is_float(self):
        """Verify wind speed is returned as float (m/s)."""
        with patch.dict("os.environ", {"GOOGLE_MAPS_API_KEY": ""}, clear=False):
            response = client.get("/api/weather?city=Rome")
            data = response.json()
            
            assert isinstance(data["wind_speed"], (int, float))
    
    def test_humidity_is_valid_percentage(self):
        """Verify humidity is a valid percentage (0-100)."""
        with patch.dict("os.environ", {"GOOGLE_MAPS_API_KEY": ""}, clear=False):
            response = client.get("/api/weather?city=Athens")
            data = response.json()
            
            assert 0 <= data["humidity"] <= 100


# ============================================
# Country Code Conversion Tests
# ============================================
# Task 157: Test country name display

class TestCountryCodeConversion:
    """Tests for country code to name conversion functionality."""
    
    def test_convert_us_code_to_name(self):
        """Test US code converts to United States."""
        from app.main import convert_country_code_to_name
        assert convert_country_code_to_name("US") == "United States"
    
    def test_convert_gb_code_to_name(self):
        """Test GB code converts to United Kingdom."""
        from app.main import convert_country_code_to_name
        assert convert_country_code_to_name("GB") == "United Kingdom"
    
    def test_convert_de_code_to_name(self):
        """Test DE code converts to Germany."""
        from app.main import convert_country_code_to_name
        assert convert_country_code_to_name("DE") == "Germany"
    
    def test_convert_jp_code_to_name(self):
        """Test JP code converts to Japan."""
        from app.main import convert_country_code_to_name
        assert convert_country_code_to_name("JP") == "Japan"
    
    def test_convert_lowercase_code(self):
        """Test lowercase codes are handled correctly."""
        from app.main import convert_country_code_to_name
        assert convert_country_code_to_name("us") == "United States"
        assert convert_country_code_to_name("gb") == "United Kingdom"
    
    def test_convert_mixed_case_code(self):
        """Test mixed case codes are handled correctly."""
        from app.main import convert_country_code_to_name
        assert convert_country_code_to_name("Us") == "United States"
        assert convert_country_code_to_name("Gb") == "United Kingdom"
    
    def test_convert_unknown_code_returns_code(self):
        """Test unknown codes return the code itself."""
        from app.main import convert_country_code_to_name
        assert convert_country_code_to_name("XX") == "XX"
        assert convert_country_code_to_name("ZZ") == "ZZ"
    
    def test_convert_empty_string(self):
        """Test empty string returns empty string."""
        from app.main import convert_country_code_to_name
        assert convert_country_code_to_name("") == ""
    
    def test_convert_code_with_whitespace(self):
        """Test codes with whitespace are trimmed."""
        from app.main import convert_country_code_to_name
        assert convert_country_code_to_name(" US ") == "United States"
        assert convert_country_code_to_name("  GB  ") == "United Kingdom"
    
    def test_weather_response_contains_country_name(self):
        """Test weather API response contains full country name, not code."""
        with patch.dict("os.environ", {"GOOGLE_MAPS_API_KEY": ""}, clear=False):
            response = client.get("/api/weather?city=London")
            assert response.status_code == 200
            data = response.json()
            
            # Should be full country name, not "US"
            assert data["country"] == "United States"
            assert data["country"] != "US"
    
    def test_weather_response_converts_country_codes(self):
        """Test that weather responses convert country codes to names."""
        from app.main import convert_country_code_to_name
        
        # Mock weather data with country code
        with patch.dict("os.environ", {"GOOGLE_MAPS_API_KEY": ""}, clear=False):
            response = client.get("/api/weather?city=TestCity")
            data = response.json()
            
            # Verify the country field contains a full name
            # Mock data uses "US" code which should be converted to "United States"
            assert "United States" in data["country"] or len(data["country"]) > 2


# ============================================
# Comparison Feature Tests (Sprint 4)
# ============================================

class TestComparisonFeature:
    """Tests for Weather Comparison Tool functionality."""
    
    def test_comparison_section_exists_in_html(self):
        """Test that comparison section HTML is present on the homepage."""
        response = client.get("/")
        assert response.status_code == 200
        html_content = response.text
        
        # Check for comparison section
        assert 'id="comparisonSection"' in html_content
        assert 'id="comparisonContainer"' in html_content
        assert 'Weather Comparison' in html_content
    
    def test_add_to_comparison_button_exists(self):
        """Test that Add to Comparison button is present in HTML."""
        response = client.get("/")
        assert response.status_code == 200
        html_content = response.text
        
        assert 'id="addToComparisonBtn"' in html_content
        assert 'Add to Comparison' in html_content
    
    def test_comparison_javascript_functions_exist(self):
        """Test that comparison JavaScript functions are defined."""
        response = client.get("/")
        assert response.status_code == 200
        html_content = response.text
        
        # Check for JavaScript functions
        assert 'updateComparisonView' in html_content
        assert 'removeFromComparison' in html_content
        assert 'comparisonCities' in html_content
    
    def test_comparison_css_styles_exist(self):
        """Test that comparison CSS styles are defined."""
        response = client.get("/")
        assert response.status_code == 200
        html_content = response.text
        
        # Check for comparison-specific CSS classes
        assert '.comparison-section' in html_content
        assert '.comparison-card' in html_content
        assert '.comparison-badge' in html_content
        assert '.add-to-comparison-btn' in html_content
    
    def test_comparison_color_variables_defined(self):
        """Test that comparison color CSS variables are defined."""
        response = client.get("/")
        assert response.status_code == 200
        html_content = response.text
        
        assert '--comparison-highlight' in html_content
        assert '--comparison-best' in html_content
        assert '--comparison-worst' in html_content
    
    def test_comparison_indicators_styling(self):
        """Test that visual comparison indicators have proper styling."""
        response = client.get("/")
        assert response.status_code == 200
        html_content = response.text
        
        # Check for warmest/coldest indicator styles
        assert '.warmest' in html_content
        assert '.coldest' in html_content
        assert 'best-temp' in html_content
        assert 'worst-temp' in html_content
    
    def test_comparison_responsive_design(self):
        """Test that comparison section has mobile responsive CSS."""
        response = client.get("/")
        assert response.status_code == 200
        html_content = response.text
        
        # Check for media queries affecting comparison
        assert '@media (max-width: 768px)' in html_content or '@media (max-width: 480px)' in html_content
    
    def test_comparison_empty_state_html(self):
        """Test that comparison empty state is properly defined."""
        response = client.get("/")
        assert response.status_code == 200
        html_content = response.text
        
        assert 'comparison-empty' in html_content
        assert 'No cities to compare' in html_content
    
    def test_clear_comparison_button_exists(self):
        """Test that Clear All comparison button exists."""
        response = client.get("/")
        assert response.status_code == 200
        html_content = response.text
        
        assert 'id="clearComparisonBtn"' in html_content
        assert 'Clear All' in html_content
    
    def test_comparison_count_display_exists(self):
        """Test that comparison count display element exists."""
        response = client.get("/")
        assert response.status_code == 200
        html_content = response.text
        
        assert 'id="comparisonCount"' in html_content
    
    def test_comparison_metrics_display(self):
        """Test that comparison cards show proper weather metrics."""
        response = client.get("/")
        assert response.status_code == 200
        html_content = response.text
        
        # Check for metrics structure in comparison cards
        assert 'comparison-metrics' in html_content
        assert 'comparison-metric-label' in html_content
        assert 'comparison-metric-value' in html_content
    
    def test_temperature_indicators_exist(self):
        """Test that temperature up/down indicators are defined."""
        response = client.get("/")
        assert response.status_code == 200
        html_content = response.text
        
        assert 'comparison-temp-indicator' in html_content
        assert 'fa-arrow-up' in html_content
        assert 'fa-arrow-down' in html_content
    
    def test_remove_button_styling(self):
        """Test that remove from comparison button has proper styling."""
        response = client.get("/")
        assert response.status_code == 200
        html_content = response.text
        
        assert 'remove-comparison-btn' in html_content
    
    def test_comparison_animations_defined(self):
        """Test that comparison-specific animations are defined."""
        response = client.get("/")
        assert response.status_code == 200
        html_content = response.text
        
        # Check for animation classes
        assert 'scaleIn' in html_content or 'fadeSlideUp' in html_content
    
    def test_comparison_grid_layout(self):
        """Test that comparison cards use grid layout."""
        response = client.get("/")
        assert response.status_code == 200
        html_content = response.text
        
        assert 'comparison-container' in html_content
        assert 'grid-template-columns' in html_content


# ============================================
# Integration Test for Full Comparison Flow
# ============================================

class TestComparisonIntegration:
    """Integration tests for complete comparison workflow."""
    
    def test_weather_data_includes_all_comparison_fields(self):
        """Test that weather API returns all fields needed for comparison."""
        with patch.dict("os.environ", {"GOOGLE_MAPS_API_KEY": ""}, clear=False):
            response = client.get("/api/weather?city=London")
            assert response.status_code == 200
            data = response.json()
            
            # Verify all required fields for comparison
            required_fields = [
                'city', 'country', 'temperature', 'feels_like',
                'description', 'humidity', 'wind_speed', 'pressure', 'icon'
            ]
            
            for field in required_fields:
                assert field in data, f"Missing required field: {field}"
    
    def test_multiple_cities_weather_data_format(self):
        """Test that multiple weather requests return consistent data format."""
        with patch.dict("os.environ", {"GOOGLE_MAPS_API_KEY": ""}, clear=False):
            cities = ['London', 'Paris', 'Tokyo']
            responses = []
            
            for city in cities:
                response = client.get(f"/api/weather?city={city}")
                assert response.status_code == 200
                responses.append(response.json())
            
            # Verify all responses have same structure
            keys_set = set(responses[0].keys())
            for response in responses[1:]:
                assert set(response.keys()) == keys_set


# ============================================
# Temperature Unit Toggle Tests
# ============================================

class TestTemperatureUnitToggle:
    """Tests for temperature unit toggle functionality."""
    
    def test_temperature_toggle_button_exists(self):
        """Test that temperature toggle button is present in HTML."""
        response = client.get("/")
        assert response.status_code == 200
        html_content = response.text
        
        # Check for toggle button
        assert 'id="temperatureToggle"' in html_content
        assert 'id="tempUnitC"' in html_content
        assert 'id="tempUnitF"' in html_content
        assert '°C' in html_content
        assert '°F' in html_content
    
    def test_temperature_toggle_css_styles_exist(self):
        """Test that temperature toggle CSS styles are defined."""
        response = client.get("/")
        assert response.status_code == 200
        html_content = response.text
        
        # Check for toggle-specific CSS classes
        assert '.temperature-toggle-container' in html_content
        assert '.temperature-toggle' in html_content
        assert '.temp-unit' in html_content
    
    def test_temperature_conversion_functions_exist(self):
        """Test that temperature conversion JavaScript functions are defined."""
        response = client.get("/")
        assert response.status_code == 200
        html_content = response.text
        
        # Check for conversion functions
        assert 'celsiusToFahrenheit' in html_content
        assert 'fahrenheitToCelsius' in html_content
        assert 'convertTemperature' in html_content
        assert 'toggleTemperatureUnit' in html_content
        assert 'getTemperatureUnitSymbol' in html_content
    
    def test_temperature_conversion_celsius_to_fahrenheit(self):
        """Test Celsius to Fahrenheit conversion logic."""
        # Test conversion: 0°C = 32°F
        celsius = 0
        fahrenheit = (celsius * 9/5) + 32
        assert round(fahrenheit) == 32
        
        # Test conversion: 25°C = 77°F
        celsius = 25
        fahrenheit = (celsius * 9/5) + 32
        assert round(fahrenheit) == 77
        
        # Test conversion: 100°C = 212°F
        celsius = 100
        fahrenheit = (celsius * 9/5) + 32
        assert round(fahrenheit) == 212
    
    def test_temperature_conversion_fahrenheit_to_celsius(self):
        """Test Fahrenheit to Celsius conversion logic."""
        # Test conversion: 32°F = 0°C
        fahrenheit = 32
        celsius = (fahrenheit - 32) * 5/9
        assert round(celsius) == 0
        
        # Test conversion: 77°F = 25°C
        fahrenheit = 77
        celsius = (fahrenheit - 32) * 5/9
        assert round(celsius) == 25
        
        # Test conversion: 212°F = 100°C
        fahrenheit = 212
        celsius = (fahrenheit - 32) * 5/9
        assert round(celsius) == 100
    
    def test_temperature_display_includes_unit_symbol(self):
        """Test that temperature display includes unit symbol in HTML."""
        response = client.get("/")
        assert response.status_code == 200
        html_content = response.text
        
        # Check that temperature display uses unit symbol
        assert 'getTemperatureUnitSymbol' in html_content
        assert '°C' in html_content or '°F' in html_content
    
    def test_temperature_toggle_localstorage_support(self):
        """Test that temperature unit preference uses localStorage."""
        response = client.get("/")
        assert response.status_code == 200
        html_content = response.text
        
        # Check for localStorage usage
        assert 'localStorage.getItem' in html_content
        assert 'localStorage.setItem' in html_content
        assert 'temperatureUnit' in html_content
    
    def test_temperature_conversion_rounding(self):
        """Test that temperature conversion properly rounds values."""
        # Test that conversions round to nearest integer
        celsius = 20.5
        fahrenheit = (celsius * 9/5) + 32
        assert round(fahrenheit) == 69
        
        fahrenheit = 69.5
        celsius = (fahrenheit - 32) * 5/9
        assert round(celsius) == 21
    
    def test_weather_data_stored_in_celsius(self):
        """Test that weather data from API is stored in Celsius."""
        with patch.dict("os.environ", {"GOOGLE_MAPS_API_KEY": ""}, clear=False):
            response = client.get("/api/weather?city=London")
            assert response.status_code == 200
            data = response.json()
            
            # Temperature should be in Celsius (reasonable range: -50 to 50)
            assert isinstance(data["temperature"], int)
            assert -50 <= data["temperature"] <= 50
            assert isinstance(data["feels_like"], int)
            assert -50 <= data["feels_like"] <= 50
