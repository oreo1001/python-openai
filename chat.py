from io import BytesIO
from flask import request, jsonify
from flask_restx import Resource, Api, Namespace, fields
import openai
from pydub import AudioSegment
import time

Chat = Namespace(
    name="Chat",
    description="Chatgpt를 작성하기 위해 사용하는 API.",
)


@Chat.route('')
class ChatSimple(Resource):
    def get(self):
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

        return {'result': result}
    
    def post(self):
        print('post 호출됨')
        print(request.files)
        audio_file = request.files['audioBlob']
        
        now = time.time()
        
        # Decode blob data to bytes
        bytes_data = audio_file.read()
        
        # Write bytes data to temporary file with .mp3 extension
        with open("temp.mp3", "wb") as f:
            f.write(bytes_data)
        
        # # Convert temporary file to mp3 using pydub library
        # sound = AudioSegment.from_file("temp.mp3", format="mp3")
        
        audio = open("./temp.mp3", "rb")
        print('audio open complete')
        
        transcript = openai.Audio.transcribe(
            "whisper-1", audio)
        
        print(transcript['text'])
        
        hi = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "assistant", "content": transcript['text']},
            ]
        )
        
        print(hi)
        result = hi['choices'][0]['message']['content']
        print(result)
        
        print(time.time() - now)
        #

        return {'result': result}
