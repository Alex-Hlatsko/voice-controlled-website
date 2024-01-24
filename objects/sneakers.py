# objects/sneakers.py

from flask import render_template, jsonify
from commands import voice_commands
from .base import BasePage
from .data_parser import DataParser

class Sneakers(BasePage):
    def __init__(self):
        super().__init__()
        self.voice_commands = {
            "home": "/home",
            "sneakers": "/sneakers",
            "about us": "/about",
            "contact": "/contact"
        }
        self.data_parser = DataParser()

    def render(self):
        sneakers_data = self.data_parser.parse_data()
        if sneakers_data:
            return render_template('sneakers.html', sneakers_data=sneakers_data, commands=list(voice_commands.keys()))
        else:
            return jsonify({"error": "Error"})
