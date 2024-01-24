import requests

class DataParser:
    def parse_data(self):
        url = 'https://voice-web-a2514-default-rtdb.europe-west1.firebasedatabase.app/sneakers.json'
        
        try:
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    sneakers_data = [item for item in data if isinstance(item, dict) and item.get("id")]
                    return sneakers_data
                else:
                    raise ValueError("Invalid data format received from the server")
            else:
                raise requests.RequestException(f"Failed to fetch data from the server. Status code: {response.status_code}")
        except (ValueError, requests.RequestException) as e:
            print(f"Error: {e}")
            return None
