from flask import Flask, render_template

app = Flask(__name__)

voice_commands = ["open web", "show info", "hello"]

@app.route('/')
def index():
    return render_template('index.html', commands=voice_commands)

if __name__ == '__main__':
    app.run(debug=True)
