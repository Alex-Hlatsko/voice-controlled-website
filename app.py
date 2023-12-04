from flask import Flask, render_template, jsonify
import speech_recognition as sr
import requests

app = Flask(__name__)

recognizer = sr.Recognizer()

from commands import voice_commands;

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
    return render_template('index.html', commands=list(voice_commands.keys()))

@app.route('/home')
def index():
    return render_template('home.html', commands=list(voice_commands.keys()))

@app.route('/sneakers')
def sneakers():
    sneakers_data = parse_data()
    if sneakers_data:
        return render_template('sneakers.html', sneakers_data=sneakers_data, commands=list(voice_commands.keys()))
    else:
        return jsonify({"error": "Error"})
        
@app.route('/process_string_command/<string_command>')
def process_string_command(string_command):
    # Проверяем, состоит ли строка только из цифр
    if string_command.isdigit():
        # Преобразуем строку в число и затем в строку
        numeric_command = str(int(string_command))
        sneakers_data = parse_data()

        # Ищем товар с указанным ID в спарсенных данных
        sneaker = next((item for item in sneakers_data if str(item["id"]) == numeric_command), None)

        if sneaker:
            return jsonify({"result": f"Found product with ID: {numeric_command}", "redirect": f"/sneakers/{numeric_command}"})
        else:
            return jsonify({"error": "Product not found"})
    else:
        return jsonify({"error": "Invalid command format"})
    
@app.route('/sneakers/<sneaker_id>')
def sneaker_detail(sneaker_id):
    sneakers_data = parse_data()
    
    sneaker = next((item for item in sneakers_data if str(item["id"]) == sneaker_id), None)

    if sneaker:
        return render_template('sneaker_detail.html', sneaker=sneaker, commands=list(voice_commands.keys()))
    else:
        return render_template('error.html', error_message="Товар не найден")

@app.route('/about')
def about():
    return render_template('about.html', commands=list(voice_commands.keys()))

@app.route('/contact')
def contact():
    return render_template('contact.html', commands=list(voice_commands.keys()))

@app.route('/process_command/<command>')
def process_command(command):
    if command in voice_commands:
        return jsonify({"result": f"You said: {command}", "redirect": voice_commands[command]})
    else:
        return jsonify({"error": "Unknown command"})

if __name__ == '__main__':
    app.run(debug=True)