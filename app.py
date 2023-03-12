import os

import openai
from flask import Flask, redirect, render_template, request, url_for, jsonify
from flask_cors import CORS
from flask_restx import Resource, Api
from todo import Todo
from auth import Auth
from chat import Chat
import time
from flask import send_file

app = Flask(__name__)
CORS(app, supports_credentials=True)
#CORS(app, resources={r'*': {'origins': 'https://hwangtoemat.github.io'}})

api = Api(
    app,
    version='0.1',
    title="test Server",
    description="Todo API Server!",
    terms_url="/",
    contact="ohsimon77@naver.com",
    license=""
)
openai.api_key = os.getenv("OPENAI_API_KEY")

api.add_namespace(Todo, '/todos')
api.add_namespace(Auth, '/auth')
api.add_namespace(Chat, '/chat')

'''
@app.route("/chat", methods=['get'])
def chat():
    """음성파일로 채팅의 답변을 받습니다."""
    audio_file = open("./녹음.m4a", "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    # return {"result": transcript}

    hi = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "assistant", "content": transcript['text']},
        ]
    )
    result = hi['choices'][0]['message']['content']
    return result
'''


@app.route("/speak", methods=['post'])
def speak():
    text1 = "안녕하세요, 저는 IML 이에요."
    tts = gTTS(text=text1, lang='ko')
    date_string = str(time.time())
    filename = "voice"+date_string+".mp3"
    tts.save(filename)
    return send_file(filename)


@app.route("/receive", methods=['post'])
def form():
    files = request.files
    #file = files.get('file')
    print(files)
    '''
    with open(os.path.abspath(f'audios/{file}'), 'wb') as f:
        f.write(file.content)
    '''
    response = jsonify("File received and saved!")
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


@app.route("/animal", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        animal = request.form["animal"]
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(animal),
            temperature=0.6,
        )
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("index.html", result=result)


def generate_prompt(animal):
    return """Suggest three names for an animal that is a superhero.

Animal: Cat
Names: Captain Sharpclaw, Agent Fluffball, The Incredible Feline
Animal: Dog
Names: Ruff the Protector, Wonder Canine, Sir Barks-a-Lot
Animal: {}
Names:""".format(
        animal.capitalize()
    )
