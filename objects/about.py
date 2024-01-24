from flask import render_template
from commands import voice_commands
from .base import BasePage

class About(BasePage):
    def __init__(self):
        super().__init__()
        self.voice_commands = {
            "home": "/home", 
            "sneakers": "/sneakers", 
            "about us": "/about", 
            "contact": "/contact"
        }
    def render(self):
        return render_template('about.html', commands=list(voice_commands.keys()))
