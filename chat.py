from flask import request, jsonify
from flask_restx import Resource, Api, Namespace, fields
import openai

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
