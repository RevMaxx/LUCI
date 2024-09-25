import speech_recognition as sr
from Luci.Models.model import ChatModel
import os
import threading
import time

class VoiceDocumentationAgent:
    def __init__(self, model_name=None, api_key=None, sys_prompt=None, method='call_gpt', stop_word='stop'):
        self.model_name = model_name or os.environ.get('MODEL_NAME')
        if not self.model_name:
            raise ValueError("Model name is not set. Please provide a valid model name.")

        self.api_key = api_key or os.environ.get('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("API key is not set. Please provide a valid API key.")

        self.sys_prompt = sys_prompt or "You are an advanced medical AI assistant specialized in clinical documentation."
        self.method = method  # The method to call from ChatModel
        self.stop_word = stop_word.lower()  # The word to stop recording

    def transcribe_speech(self):
        """
        Continuously captures audio from the microphone and returns the transcribed text
        when the stop word is said. Prints live transcription every 10 seconds.
        """
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()

        print(f"Please speak now. Say '{self.stop_word}' to stop recording.")

        transcription = ""
        last_print_time = time.time()
        stop_recording = False

        def callback(recognizer, audio):
            nonlocal transcription, stop_recording, last_print_time
            try:
                # Using Google's speech recognition engine
                text = recognizer.recognize_google(audio)
                transcription += " " + text
                print(f"\nInterim Transcription:\n{text}\n")

                # Check for the stop word
                if self.stop_word in text.lower():
                    stop_recording = True
            except sr.UnknownValueError:
                print("Speech Recognition could not understand audio.")
            except sr.RequestError as e:
                print(f"Could not request results from Speech Recognition service; {e}")

        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            print("Listening...")

        # Start listening in the background
        stop_listening = recognizer.listen_in_background(microphone, callback)

        # Keep the program running until the stop word is detected
        try:
            while not stop_recording:
                time.sleep(0.1)
                # Print live transcription every 10 seconds
                if time.time() - last_print_time >= 10:
                    print(f"\nLive Transcription (Last 10 seconds):\n{transcription}\n")
                    last_print_time = time.time()
        except KeyboardInterrupt:
            print("Recording stopped by user.")
        finally:
            stop_listening(wait_for_stop=False)

        # Remove the stop word from the transcription
        transcription = transcription.lower().replace(self.stop_word, "")
        return transcription.strip()

    def format_to_soap(self, note_text, **kwargs):
        """
        Uses ChatModel to format the transcribed text into a SOAP note.
        """
        prompt = f"""
        Format the following clinical note into a structured SOAP (Subjective, Objective, Assessment, Plan) note:

        Clinical Note:
        \"\"\"
        {note_text}
        \"\"\"

        Structured SOAP Note:
        """

        # Instantiate the ChatModel
        chat_model = ChatModel(
            model_name=self.model_name,
            api_key=self.api_key,
            prompt=prompt,
            SysPrompt=self.sys_prompt
        )

        # Call the selected method with any additional arguments
        if hasattr(chat_model, self.method):
            method_to_call = getattr(chat_model, self.method)
            response = method_to_call(**kwargs)
            # Ensure response is a string
            if isinstance(response, dict) and 'content' in response:
                return response['content']
            elif hasattr(response, 'content'):
                return response.content
            else:
                return str(response)
        else:
            raise ValueError(f"The method '{self.method}' is not available in ChatModel.")

    def save_soap_note_to_file(self, soap_note, filename="soap_note.txt"):
        """
        Saves the SOAP note to a text file.
        """
        if not isinstance(soap_note, str):
            soap_note = str(soap_note)
        with open(filename, "w", encoding='utf-8') as file:
            file.write(soap_note)
        print(f"\nSOAP note saved to {filename}")

    def run(self, **kwargs):
        """
        Runs the voice documentation agent.
        """
        transcription = self.transcribe_speech()
        if transcription:
            print("\nFinal Transcription:\n")
            print(transcription)
            soap_note = self.format_to_soap(transcription, **kwargs)
            print("\nGenerated SOAP Note:\n")
            print(soap_note)
            self.save_soap_note_to_file(soap_note)
        else:
            print("No transcription available. Exiting.")
