class BasePage:
    def __init__(self):
        self.voice_commands = {}

    def process_command(self, command):
        if command in self.voice_commands:
            return {"result": f"You said: {command}", "redirect": self.voice_commands[command]}
        else:
            return {"error": "Unknown command"}
