import pyttsx3
import speech_recognition as sr

def set_tts_language(engine, language):
    """TTS 엔진 언어 설정"""
    voices = engine.getProperty('voices')
    if language == 'ko':  # 한국어
        engine.setProperty('voice', voices[0].id)  # 보통 한국어 음성을 voices[0]로 설정
    elif language == 'en':  # 영어
        engine.setProperty('voice', voices[1].id)
    else:
        print(f"Unsupported language: {language}. Defaulting to {voices[0].name}")

def get_audio_input():
    """음성 입력을 텍스트로 변환"""
    r = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("Listening...")
            audio = r.listen(source)
        # Google Speech Recognition으로 텍스트 변환
        text = r.recognize_google(audio, language='ko')
        print(f"Recognized Text: {text}")
        return text
    except sr.UnknownValueError:
        print("Could not understand the audio.")
        return None
    except sr.RequestError as e:
        print(f"Request error: {e}")
        return None

def text_to_speech(text):
    """텍스트를 음성으로 변환"""
    if text:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()