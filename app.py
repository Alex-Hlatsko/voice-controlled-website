# app.py

from flask import Flask, render_template, jsonify
import speech_recognition as sr

app = Flask(__name__)

recognizer = sr.Recognizer()

# Dictionary to map command names to URLs
voice_commands = {"home": "/", "sneakers": "/sneakers", "about us": "/about", "contact": "/contact"}

@app.route('/')
def index():
    return render_template('index.html', commands=list(voice_commands.keys()))

@app.route('/sneakers')
def sneakers():
    return render_template('sneakers.html', commands=list(voice_commands.keys()))

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
