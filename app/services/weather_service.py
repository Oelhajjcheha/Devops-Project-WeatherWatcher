"""
Weather Service Module
----------------------
Interfaces with Google Maps Weather API to fetch real-time weather data.

The Google Weather API requires latitude/longitude coordinates, so this service:
1. Uses Google Geocoding API to convert city names to coordinates
2. Fetches current weather conditions from Google Weather API
3. Maps the response to frontend-compatible format
"""

import os
import logging
from typing import Optional
from dataclasses import dataclass
import httpx

logger = logging.getLogger(__name__)


# -----------------------------------------------
# Data Classes for Weather Response
# -----------------------------------------------
@dataclass
class WeatherData:
    """Structured weather data returned to the frontend."""
    city: str
    country: str
    temperature: int
    feels_like: int
    description: str
    humidity: int
    wind_speed: float
    pressure: int
    icon: str


@dataclass
class GeoLocation:
    """Geographic coordinates from geocoding."""
    latitude: float
    longitude: float
    city: str
    country: str


# -----------------------------------------------
# Weather Icon Mapping
# -----------------------------------------------
# Maps Google Weather condition types to OpenWeatherMap-style icon codes
# (Frontend already has icon mapping for these codes)
WEATHER_ICON_MAP = {
    "CLEAR": "01d",
    "MOSTLY_CLEAR": "01d",
    "PARTLY_CLOUDY": "02d",
    "MOSTLY_CLOUDY": "03d",
    "CLOUDY": "04d",
    "OVERCAST": "04d",
    "LIGHT_RAIN": "09d",
    "RAIN": "10d",
    "HEAVY_RAIN": "10d",
    "RAIN_SHOWERS": "09d",
    "SCATTERED_SHOWERS": "09d",
    "DRIZZLE": "09d",
    "LIGHT_SNOW": "13d",
    "SNOW": "13d",
    "HEAVY_SNOW": "13d",
    "SNOW_SHOWERS": "13d",
    "FLURRIES": "13d",
    "THUNDERSTORM": "11d",
    "THUNDERSTORMS": "11d",
    "ISOLATED_THUNDERSTORMS": "11d",
    "SCATTERED_THUNDERSTORMS": "11d",
    "FOG": "50d",
    "HAZE": "50d",
    "MIST": "50d",
    "SMOKE": "50d",
    "DUST": "50d",
    "WINDY": "50d",
    "HAIL": "13d",
    "SLEET": "13d",
    "FREEZING_RAIN": "13d",
}


# -----------------------------------------------
# Custom Exceptions
# -----------------------------------------------
class WeatherServiceError(Exception):
    """Base exception for weather service errors."""
    pass


class CityNotFoundError(WeatherServiceError):
    """Raised when a city cannot be geocoded."""
    pass


class WeatherAPIError(WeatherServiceError):
    """Raised when the weather API call fails."""
    pass


class APIKeyMissingError(WeatherServiceError):
    """Raised when the Google Maps API key is not configured."""
    pass


# -----------------------------------------------
# Weather Service Class
# -----------------------------------------------
class WeatherService:
    """
    Service for fetching weather data from Google Maps Weather API.
    
    Usage:
        service = WeatherService()
        weather = await service.get_weather_by_city("London")
    """
    
    GEOCODING_BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json"
    WEATHER_BASE_URL = "https://weather.googleapis.com/v1/currentConditions:lookup"
    
    def __init__(self, api_key: Optional[str] = None, timeout: float = 10.0):
        """
        Initialize the weather service.
        
        Args:
            api_key: Google Maps API key. If not provided, reads from 
                     GOOGLE_MAPS_API_KEY environment variable.
            timeout: HTTP request timeout in seconds.
        """
        self.api_key = api_key or os.getenv("GOOGLE_MAPS_API_KEY")
        self.timeout = timeout
    
    def _validate_api_key(self) -> None:
        """Ensure API key is available."""
        if not self.api_key:
            raise APIKeyMissingError(
                "Google Maps API key not configured. "
                "Set GOOGLE_MAPS_API_KEY environment variable."
            )
    
    async def _geocode_city(self, city: str) -> GeoLocation:
        """
        Convert a city name to geographic coordinates using Google Geocoding API.
        
        Args:
            city: City name (e.g., "London", "New York, NY")
            
        Returns:
            GeoLocation with latitude, longitude, and formatted city/country
            
        Raises:
            CityNotFoundError: If the city cannot be found
            WeatherAPIError: If the geocoding API call fails
        """
        params = {
            "address": city,
            "key": self.api_key,
        }
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(self.GEOCODING_BASE_URL, params=params)
                response.raise_for_status()
                data = response.json()
                
                if data.get("status") == "ZERO_RESULTS" or not data.get("results"):
                    raise CityNotFoundError(f"City not found: {city}")
                
                if data.get("status") != "OK":
                    logger.error(f"Geocoding API error: {data.get('status')}")
                    raise WeatherAPIError(f"Geocoding failed: {data.get('status')}")
                
                result = data["results"][0]
                location = result["geometry"]["location"]
                
                # Extract city and country from address components
                city_name = city.title()
                country_code = ""
                
                for component in result.get("address_components", []):
                    types = component.get("types", [])
                    if "locality" in types:
                        city_name = component["long_name"]
                    elif "administrative_area_level_1" in types and not city_name:
                        city_name = component["long_name"]
                    elif "country" in types:
                        country_code = component["short_name"]
                
                return GeoLocation(
                    latitude=location["lat"],
                    longitude=location["lng"],
                    city=city_name,
                    country=country_code,
                )
                
        except httpx.TimeoutException:
            logger.error(f"Geocoding timeout for city: {city}")
            raise WeatherAPIError("Geocoding service timeout")
        except httpx.HTTPStatusError as e:
            logger.error(f"Geocoding HTTP error: {e.response.status_code}")
            raise WeatherAPIError(f"Geocoding service error: {e.response.status_code}")
        except CityNotFoundError:
            raise
        except Exception as e:
            logger.error(f"Unexpected geocoding error: {str(e)}")
            raise WeatherAPIError(f"Failed to geocode city: {str(e)}")
    
    async def _fetch_weather(self, lat: float, lng: float) -> dict:
        """
        Fetch current weather conditions from Google Weather API.
        
        Args:
            lat: Latitude
            lng: Longitude
            
        Returns:
            Raw weather data dictionary from Google Weather API
            
        Raises:
            WeatherAPIError: If the weather API call fails
        """
        params = {
            "key": self.api_key,
            "location.latitude": lat,
            "location.longitude": lng,
            "unitsSystem": "METRIC",  # Use Celsius
        }
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(self.WEATHER_BASE_URL, params=params)
                response.raise_for_status()
                return response.json()
                
        except httpx.TimeoutException:
            logger.error(f"Weather API timeout for coordinates: {lat}, {lng}")
            raise WeatherAPIError("Weather service timeout")
        except httpx.HTTPStatusError as e:
            logger.error(f"Weather API HTTP error: {e.response.status_code}")
            if e.response.status_code == 403:
                raise WeatherAPIError("Weather API access denied. Check API key permissions.")
            raise WeatherAPIError(f"Weather service error: {e.response.status_code}")
        except Exception as e:
            logger.error(f"Unexpected weather API error: {str(e)}")
            raise WeatherAPIError(f"Failed to fetch weather: {str(e)}")
    
    def _map_weather_icon(self, condition_type: str, is_daytime: bool = True) -> str:
        """
        Map Google Weather condition type to OpenWeatherMap-style icon code.
        
        Args:
            condition_type: Google Weather condition type (e.g., "CLEAR", "RAIN")
            is_daytime: Whether it's currently daytime
            
        Returns:
            Icon code like "01d" (clear day) or "10n" (rain night)
        """
        base_icon = WEATHER_ICON_MAP.get(condition_type, "03d")
        
        # Replace 'd' with 'n' for nighttime
        if not is_daytime:
            return base_icon.replace("d", "n")
        
        return base_icon
    
    def _parse_weather_response(
        self, 
        weather_data: dict, 
        location: GeoLocation
    ) -> WeatherData:
        """
        Parse Google Weather API response into frontend-compatible format.
        
        Args:
            weather_data: Raw response from Google Weather API
            location: Geocoded location data
            
        Returns:
            WeatherData instance ready for frontend consumption
        """
        # Extract weather condition
        weather_condition = weather_data.get("weatherCondition", {})
        condition_type = weather_condition.get("type", "CLOUDY")
        description_obj = weather_condition.get("description", {})
        description = description_obj.get("text", "Unknown")
        
        # Extract temperature (already in Celsius due to unitsSystem=METRIC)
        temperature = weather_data.get("temperature", {}).get("degrees", 0)
        feels_like = weather_data.get("feelsLikeTemperature", {}).get("degrees", 0)
        
        # Extract other weather data
        humidity = weather_data.get("relativeHumidity", 0)
        
        # Wind speed (convert from km/h to m/s for consistency with frontend)
        wind_data = weather_data.get("wind", {}).get("speed", {})
        wind_speed_kmh = wind_data.get("value", 0)
        wind_speed_ms = round(wind_speed_kmh / 3.6, 1)  # km/h to m/s
        
        # Pressure
        pressure = int(weather_data.get("airPressure", {}).get("meanSeaLevelMillibars", 1013))
        
        # Determine if daytime for icon selection
        is_daytime = weather_data.get("isDaytime", True)
        icon = self._map_weather_icon(condition_type, is_daytime)
        
        return WeatherData(
            city=location.city,
            country=location.country,
            temperature=round(temperature),
            feels_like=round(feels_like),
            description=description,
            humidity=humidity,
            wind_speed=wind_speed_ms,
            pressure=pressure,
            icon=icon,
        )
    
    async def get_weather_by_city(self, city: str) -> WeatherData:
        """
        Get current weather conditions for a city.
        
        This is the main public method that:
        1. Validates the API key
        2. Geocodes the city name to coordinates
        3. Fetches weather data for those coordinates
        4. Returns formatted weather data
        
        Args:
            city: City name (e.g., "London", "Tokyo", "New York")
            
        Returns:
            WeatherData with current conditions
            
        Raises:
            APIKeyMissingError: If API key is not configured
            CityNotFoundError: If city cannot be found
            WeatherAPIError: If weather fetch fails
        """
        self._validate_api_key()
        
        logger.info(f"Fetching weather for city: {city}")
        
        # Step 1: Geocode city to coordinates
        location = await self._geocode_city(city)
        logger.info(f"Geocoded {city} to: {location.latitude}, {location.longitude}")
        
        # Step 2: Fetch weather for coordinates
        weather_data = await self._fetch_weather(location.latitude, location.longitude)
        
        # Step 3: Parse and return formatted data
        return self._parse_weather_response(weather_data, location)
    
    async def get_forecast_by_city(self, city: str) -> list:
        """
        Get 5-day weather forecast for a city.
        
        Args:
            city: City name (e.g., "London", "Madrid")
            
        Returns:
            List of forecast data for next 5 days
            
        Raises:
            CityNotFoundError: If the city cannot be found
            WeatherAPIError: If the API call fails
        """
        self._validate_api_key()
        
        # First, geocode the city to get coordinates
        geo_location = await self._geocode_city(city)
        
        # Fetch forecast data from Google Weather API
        forecast_data = await self._fetch_forecast(
            geo_location.latitude,
            geo_location.longitude
        )
        
        # Parse and format forecast data
        forecasts = []
        
        # Google Weather API returns daily data
        if "days" in forecast_data:
            for day_data in forecast_data["days"][:5]:  # Get first 5 days
                date = day_data.get("date", "")
                
                # Get condition info
                condition = day_data.get("conditions", {})
                condition_type = condition.get("conditionCode", "UNKNOWN")
                description = condition.get("conditionDescription", "Unknown")
                
                # Get temperature data
                temp_data = day_data.get("temperature", {})
                temp_max = temp_data.get("max", {}).get("value", 0)
                temp_min = temp_data.get("min", {}).get("value", 0)
                
                # Convert to Celsius and round
                temp_max_c = round(temp_max)
                temp_min_c = round(temp_min)
                
                # Map to icon
                icon = self._map_weather_icon(condition_type)
                
                forecasts.append({
                    "date": date,
                    "temp_max": temp_max_c,
                    "temp_min": temp_min_c,
                    "description": description,
                    "icon": icon,
                })
        
        return forecasts
    
    async def _fetch_forecast(self, lat: float, lng: float) -> dict:
        """
        Fetch weather forecast from Google Weather API.
        
        Args:
            lat: Latitude
            lng: Longitude
            
        Returns:
            Raw forecast data dictionary
            
        Raises:
            WeatherAPIError: If the API call fails
        """
        url = "https://weather.googleapis.com/v1/forecast:lookup"
        
        params = {
            "key": self.api_key,
            "location.latitude": lat,
            "location.longitude": lng,
            "unitsSystem": "METRIC",
        }
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                return response.json()
                
        except httpx.TimeoutException:
            logger.error(f"Forecast API timeout for coordinates: {lat}, {lng}")
            raise WeatherAPIError("Forecast service timeout")
        except httpx.HTTPStatusError as e:
            logger.error(f"Forecast API HTTP error: {e.response.status_code}")
            raise WeatherAPIError(f"Forecast service error: {e.response.status_code}")
        except Exception as e:
            logger.error(f"Unexpected forecast API error: {str(e)}")
            raise WeatherAPIError(f"Failed to fetch forecast: {str(e)}")

    async def get_weather_by_coordinates(
        self, 
        latitude: float, 
        longitude: float,
        city_name: str = "Unknown",
        country_code: str = ""
    ) -> WeatherData:
        """
        Get current weather conditions for specific coordinates.
        
        Args:
            latitude: Location latitude
            longitude: Location longitude
            city_name: Optional city name for display
            country_code: Optional country code for display
            
        Returns:
            WeatherData with current conditions
        """
        self._validate_api_key()
        
        location = GeoLocation(
            latitude=latitude,
            longitude=longitude,
            city=city_name,
            country=country_code,
        )
        
        weather_data = await self._fetch_weather(latitude, longitude)
        return self._parse_weather_response(weather_data, location)


# -----------------------------------------------
# Module-level convenience function
# -----------------------------------------------
async def get_weather(city: str, api_key: Optional[str] = None) -> WeatherData:
    """
    Convenience function to fetch weather for a city.
    
    Args:
        city: City name
        api_key: Optional API key (uses environment variable if not provided)
        
    Returns:
        WeatherData instance
    """
    service = WeatherService(api_key=api_key)
    return await service.get_weather_by_city(city)
