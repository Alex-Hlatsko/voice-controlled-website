from flask import Flask, render_template, jsonify
from objects.home import Home
from objects.index import Index
from objects.sneakers import Sneakers
from objects.sneaker_detail import SneakerDetail
from objects.about import About
from objects.contact import Contact
import requests


app = Flask(__name__)

home_page = Home()
index_page = Index()
sneakers_page = Sneakers()
sneaker_detail_page = SneakerDetail()
about_page = About()
contact_page = Contact()

def parse_data():
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

@app.route('/')
def home():
    return index_page.render()

@app.route('/home')
def index():
    return home_page.render()

@app.route('/sneakers')
def sneakers():
    return sneakers_page.render()

@app.route('/sneakers/<sneaker_id>')
def sneaker_detail(sneaker_id):
    return sneaker_detail_page.render(sneaker_id)

@app.route('/about')
def about():
    return about_page.render()

@app.route('/contact')
def contact():
    return contact_page.render()

@app.route('/process_string_command/<string_command>')
def process_string_command(string_command):
    try:
        if string_command.replace(" ", "").isdigit():
            numeric_command = int(string_command.replace(" ", ""))
            sneakers_data = parse_data()

            sneaker = next((item for item in sneakers_data if item.get("id") == numeric_command), None)

            if sneaker:
                return jsonify({"result": f"Found product with ID: {numeric_command}", "redirect": f"/sneakers/{numeric_command}"})
            else:
                return jsonify({"error": "Product not found"})
        else:
            return jsonify({"error": "Invalid command format"})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/process_command/<command>')
def process_command(command):
    result = None
    
    for page in [home_page, index_page, sneakers_page, sneaker_detail_page, about_page, contact_page]:
        result = page.process_command(command)
        if "redirect" in result:
            break
    
    if result:
        return jsonify(result)
    else:
        return jsonify({"error": "Unknown command"})

if __name__ == '__main__':
    app.run(debug=True)
