from groq import Groq
# from gtts import gTTS
import getpass
# import pyautogui
import pyaudio
import wave
import pyttsx3
import threading
audio = input("would you like audio? (y/n): ")
voiceinput = input("would you like voice input? (y/n): ")
client = Groq(api_key='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')


system_prompt = [{"role": "system", "content": "//Add your code here(what you want to be the chat bot to be)"}]

messages = []

def gpt_response(message):
    global messages

    messages.append({"role": "user", "content": message})


    if len(messages) > 1000:
        messages.pop(0)


    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=system_prompt + messages
    )

    messages.append({"role": "assistant", "content": response.choices[0].message.content})

    return response.choices[0].message.content


while True:
    if voiceinput == 'y':
        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44102, input=True, frames_per_buffer=1024 )

        frames = []

        try:
            while True:
               data = stream.read(1024)
               frames.append(data)
        except KeyboardInterrupt:
            pass

        stream.stop_stream()
        stream.close()
        audio.terminate()
        soundfile = wave.open(rf'C:/Users/{getpass.getuser()}/AppData/Local/Temp/myrecording.wav', 'wb')
        soundfile.setnchannels(1)
        soundfile.setsampwidth(2)
        soundfile.setframerate(44100)
        soundfile.writeframes(b''.join(frames))
        soundfile.close() 
        filename = f'c:/Users/{getpass.getuser()}/AppData/Local/Temp/myrecording.wav'
        with open(filename, "rb") as file:
            transcription = client.audio.transcriptions.create(
            file=(filename, file.read()),
            model="whisper-large-v3",)
            global chat
            chat = transcription.text
            global hi
            hi = transcription.text
            print('You:', chat)
            
    elif voiceinput == 'n':
        chat = input('You: ') 
    print('Bot:', gpt_response(chat))
    mytext = gpt_response(chat)
    def audiooutput(argument):
     engine = pyttsx3.init()
     engine.say(argument)
     engine.runAndWait()
    if audio == "y":
        if voiceinput == 'y':
            audiooutput(hi)
        else:
            thread = threading.Thread(target=audiooutput)
            thread.run()
