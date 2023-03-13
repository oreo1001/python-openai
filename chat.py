from io import BytesIO
from flask import request, jsonify
from flask_restx import Resource, Api, Namespace, fields
import openai
import time
from flask import send_file
#from pydub import AudioSegment
#from gtts import gTTS

Chat = Namespace(
    name="Chat",
    description="Chatgpt를 작성하기 위해 사용하는 API.",
)


@Chat.route('/TTS')
class ChatSimple(Resource):
    def post(self):
        text = request.json.get('text')
        tts = gTTS(text=text, lang='ko')
        date_string = str(time.time())
        filename = "voice"+date_string+".mp3"
        tts.save(filename)
        return send_file(filename, mimetype='audio/mpeg', as_attachment=True)


@Chat.route('/askGPT')
class ChatSimple(Resource):
    def post(self):
        text = request.json.get('text')
        
        prompt1 = "You can transform into an American citizen who is my spoken English teacher and improver. Create your backstory and temperament, and with appropriate characteristics and responses, you will immerse yourself into the persona fully you will be that persona in our conversation, responding in the first person."
        prompt2 = "\nPlease proceed with the class by following the following rules."
        prompt3 = "\n1. I will speak to you in English and you will reply to me in English to practice my spoken English."
        prompt4 = "\n2. The class is conducted by having a normal conversation in English."
        prompt5 = "\n3. I want you to [respond to my answer]."
        prompt6 = "\n4. I want you to ask me a [question] in your reply."
        prompt7 = "\n5. I want you to strictly [correct my grammar] mistakes, typos, and factual errors."
        prompt8 = "\n6. I want you to keep your reply neat, limiting the reply to 100 words."
        prompt9 = "\n7. Sometimes I want you to ask me to make a sentence using certain words. But it shouldn't be too frequent."
        prompt10 = "\n8. Your reply is divided into [response to my answer], [grammar correction], and [question]."
        prompt11 = "\n9. Your reply should separate [response to my answer], [grammar correction], and [question] and print them out. (Take the following output format as an example.)"
        prompt12 = "\n[response to my answer]: Great! As a native English speaker from America, I'll be able to help you with that."
        prompt13 = "\n[grammar correction]: To make your sentence grammatically correct, you could say, \"I want to speak American English\" or \"I want to speak English like Americans do\"."
        prompt14 = "\n[question]: Are there any specific situations or contexts in which you want to improve your spoken English skills? For example, do you want to feel more confident speaking English at work, in social settings, or while traveling?"
        prompt15 = "\nRemember, I want you to strictly correct my grammar mistakes, typos, and factual errors."
        prompt16 = "Now let’s start practicing, you could ask me a question first."    
        prompt = prompt1+prompt2+prompt3+prompt4 + \
            prompt5+prompt6+prompt7+prompt8+prompt9 + \
            prompt10+prompt11+prompt12+prompt13+prompt14+prompt15+prompt16

        print(text)

        if (text == 'JungwonJungmo'): 
            hi = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant"},
                    {"role": "user", "content": prompt}
                ]
            )
        else:
            hi = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant"},
                    {"role": "user", "content": prompt},
                    {"role": "user", "content": text}
                ]
            )
        print(hi)
        result = hi['choices'][0]['message']['content']

        return {'result': result}


@Chat.route('/transcribe')
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

        return {'transcribe': transcript, 'result': result}

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

        result = transcript['text']

        print(result)

        print(time.time() - now)
        #

        return {'result': result}
