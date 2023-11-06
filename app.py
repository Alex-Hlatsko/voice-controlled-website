from flask import Flask, render_template, jsonify
import time
import speech_recognition as sr

app = Flask(__name__)

recognizer = sr.Recognizer()

voice_commands = ["открой сайт", "покажи информацию", "привет"]

@app.route('/')
def index():
    return render_template('index.html', commands=voice_commands)

@app.route('/listen')
def listen():
    return render_template('listen.html')

@app.route('/listen_now', methods=['GET', 'POST'])
def listen_now():
    timer = 10
    audio = None
    with sr.Microphone() as source:
        print("Скажите что-нибудь...")
        for i in range(timer):
            audio = recognizer.listen(source, timeout=1)
            if audio:
                break

    if audio:
        try:
            command = recognizer.recognize_google(audio, language="ru-RU")
            print(f"Вы сказали: {command}")
            return jsonify({"result": f"Вы сказали: {command}"})
        except sr.UnknownValueError:
            return jsonify({"error": "Речь не распознана"})
        except sr.RequestError as e:
            return jsonify({"error": f"Ошибка при запросе к сервису распознавания: {e}"})
    else:
        return jsonify({"error": "Тайм-аут распознавания"})

if __name__ == '__main__':
    app.run(debug=True)
