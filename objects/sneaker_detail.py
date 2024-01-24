from flask import render_template
from objects.data_parser import DataParser
from commands import voice_commands
from .base import BasePage

class SneakerDetail(BasePage):
    def __init__(self):
        super().__init__()
        self.voice_commands = {
            "home": "/home", 
            "sneakers": "/sneakers", 
            "about us": "/about", 
            "contact": "/contact"
        }
    def __init__(self):
        self.data_parser = DataParser()

    def render(self, sneaker_id):
        sneakers_data = self.data_parser.parse_data()
        sneaker = next((item for item in sneakers_data if str(item["id"]) == sneaker_id), None)

        if sneaker:
            return render_template('sneaker_detail.html', sneaker=sneaker, commands=list(voice_commands.keys()))
        else:
            return render_template('error.html', error_message="Товар не найден")
