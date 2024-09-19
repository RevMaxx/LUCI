import os
import requests
from google.cloud import speech
from deepgram import Deepgram
import asyncio

class Transcriber:
    def __init__(self, service_name, api_key, voice_id):
        self.service_name = service_name.lower()
        self.api_key = api_key
        self.voice_id = voice_id
    
    async def transcribe(self, audio_file):
        if self.service_name == "deepgram":
            return await self.transcribe_deepgram(audio_file)
        elif self.service_name == "google":
            return self.transcribe_google(audio_file)
        else:
            raise ValueError(f"Unsupported service: {self.service_name}")

    # Deepgram transcription
    async def transcribe_deepgram(self, audio_file):
        dg = Deepgram(self.api_key)
        with open(audio_file, 'rb') as audio:
            response = await dg.transcription.prerecorded({'buffer': audio}, {'model': 'nova', 'language': 'en'})
        return response

    # Google Speech-to-Text transcription
    def transcribe_google(self, audio_file):
        client = speech.SpeechClient()
        with open(audio_file, 'rb') as audio:
            audio_content = audio.read()
        audio = speech.RecognitionAudio(content=audio_content)
        config = speech.RecognitionConfig(language_code="en-US")
        response = client.recognize(config=config, audio=audio)
        transcripts = [result.alternatives[0].transcript for result in response.results]
        return transcripts
