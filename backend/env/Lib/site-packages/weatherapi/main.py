from dataclasses import dataclass
import requests

# Custom errors
class StatusCodeError(Exception):
    pass


@dataclass
class WeatherPoint:
    
    """Point entity to get weather data from.
    
        WeatherPoint is main object in weatherapi, its defined by its latitude and longitude. WeatherPoint methods are
        get_current_weather(), set_key() and get_forecast() # SOON 
        
        Attributes:
            lat: float that represents the latitude of the WeatherPoint.
            lon: float that represents the longitude of the WeatherPoint.
        """
    lat: float
    lon: str

    def _get_data_(self, url):
        """Make a request and reassure that got a correct response (200), otherwise rise an error"""

        r = requests.get(url)

        # Checking response status code
        if r.status_code == 200: # everything its alrighty
            return r

        elif r.status_code in [400, 401, 403]:
            error_code = r.json()["error"]["code"]
            error_message = r.json()["error"]["message"]
            raise StatusCodeError(f"{error_message} - Error code: {error_code}")

        else:
            raise Exception("Can't connect to the API")

    def set_key(self, key:str):
        self.key = key
    
    def get_current_weather(self):
        """Gets current weather of the WeatherPoint coordinate"""
        try:
            self.key
        except:
            raise AttributeError("'key' Attribute not defined. You should define the key attribute throught the set_key() method.")

        # parameters of the api call for current weather
        params = dict(
            key = self.key, # personal key
            q = ",".join([str(self.lat),str(self.lon)]), # coordinates 
            aqi = "yes") # air quality data

        base_url = "http://api.weatherapi.com/v1/current.json?" # base url
        url = [str(key)+"="+str(value) for key, value in params.items()] # the rest of the url
        full_url = base_url + "&".join(url) # concatenating

        # making the request
        r = self._get_data_(full_url)

        rjson = r.json()
        
        # checking if 'location' and 'current' in rjson

        if "location" not in rjson.keys() or "current" not in rjson.keys():
            raise Exception("location and/or current data not found in the request")
        
               
        # setting variables to Point
        self.name = rjson["location"].get("name", None)
        self.region = rjson["location"].get("region", None)
        self.country = rjson["location"].get("country", None)
        self.tz = rjson["location"].get("tz_id", None)
        self.localtime_timestamp = rjson["location"].get("localtime_epoch", None)
        self.localtime = rjson["location"].get("localtime", None)
        self.last_updated = rjson["current"].get("last_updated", None)
        self.temp_c = rjson["current"].get("temp_c", None)
        self.is_day = rjson["current"].get("is_day", None)
        self.condition = rjson["current"]["condition"].get("text", None)
        self.condition_code = rjson["current"]["condition"].get("code", None)
        self.wind_kph = rjson["current"].get("wind_kph", None)
        self.wind_degree = rjson["current"].get("wind_degree", None)
        self.wind_dir = rjson["current"].get("wind_dir", None)
        self.pressure_mb = rjson["current"].get("pressure_mb", None)
        self.precip_mm = rjson["current"].get("precip_mm", None)
        self.humidity = rjson["current"].get("humidity", None)
        self.cloud = rjson["current"].get("cloud", None)
        self.feelslike_c = rjson["current"].get("feelslike_c", None)
        self.visibility_km = rjson["current"].get("vis_km", None)
        self.uv = rjson["current"].get("uv", None)
        self.gust_kph = rjson["current"].get("gust_kph", None)
    