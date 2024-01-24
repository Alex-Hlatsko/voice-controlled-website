from .base import BasePage
from flask import render_template
from commands import voice_commands

class Home(BasePage):
    def __init__(self):
        super().__init__()
        self.voice_commands = {
            "home": "/home", 
            "sneakers": "/sneakers", 
            "about us": "/about", 
            "contact": "/contact"
        }
    def render(self):
        return render_template('home.html', commands=list(voice_commands.keys()))
