import requests
import json
import os
import yaml
from datetime import datetime

class DynamicApiClient:
    def __init__(self, base_url="", config_path="config.yml", output_dir="data_files"):
        self.base_url = base_url
        self.output_dir = output_dir
        self.config = self._load_config(config_path)
        
        # If base_url is not provided, try to get it from config
        if not self.base_url and self.config:
            self.base_url = self.config.get('server', {}).get('base_url', "")
        
        # If output_dir is provided in config, use it
        if self.config:
            self.output_dir = self.config.get('server', {}).get('output_dir', self.output_dir)

    def _load_config(self, config_path):
        """Loads configuration from a YAML file."""
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    return yaml.safe_load(f)
            except yaml.YAMLError as e:
                print(f"Error parsing config file: {e}")
        return {}

    def get_header(self, key, default=None):
        """Gets a header value from config."""
        return self.config.get('headers', {}).get(key, default)

    def get_secret(self, key, default=None):
        """Gets a secret value from config."""
        return self.config.get('secrets', {}).get(key, default)

    def make_request(self, method, endpoint, params=None, data=None, headers=None):
        """
        Makes a dynamic REST API call.
        :param method: GET, POST, etc.
        :param endpoint: API endpoint (will be appended to base_url)
        :param params: URL parameters for GET requests
        :param data: JSON body for POST requests
        :param headers: Optional headers (will be merged with default headers from config)
        :return: Response object
        """
        url = f"{self.base_url}{endpoint}" if self.base_url and not endpoint.startswith("http") else endpoint
        
        # Merge default headers from config with provided headers
        combined_headers = self.config.get('headers', {}).copy()
        if headers:
            combined_headers.update(headers)
        
        try:
            response = requests.request(
                method=method.upper(),
                url=url,
                params=params,
                json=data,
                headers=combined_headers
            )
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"Error during request to {url}: {e}")
            return None

    def save_to_json(self, response, filename=None):
        """
        Saves the API response to a local JSON file.
        :param response: requests.Response object
        :param filename: Optional filename, defaults to timestamp-based name
        """
        if response is None:
            print("No response to save.")
            return

        try:
            data = response.json()
        except ValueError:
            print("Response is not in JSON format.")
            return

        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"response_{timestamp}.json"
        
        # If filename is just a name (no path), use output_dir
        if not os.path.isabs(filename) and os.path.dirname(filename) == '':
            filename = os.path.join(self.output_dir, filename)
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(filename), exist_ok=True) if os.path.dirname(filename) else None

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        
        print(f"Data saved to {filename}")
        return filename
