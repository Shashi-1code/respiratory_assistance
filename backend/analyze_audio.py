from pydub import AudioSegment
import speech_recognition as sr
import librosa
import os

def convert_webm_to_wav(input_path, output_path):
    audio = AudioSegment.from_file(input_path, format="webm")
    audio.export(output_path, format="wav")
    return output_path

def transcribe_audio(file_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio = recognizer.record(source)
    return recognizer.recognize_google(audio)

def analyze_pitch(file_path):
    y, sr_ = librosa.load(file_path)
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr_)
    pitch_values = pitches[magnitudes > 0]
    avg_pitch = float(pitch_values.mean()) if pitch_values.size > 0 else 0.0

    # Simplified categorization logic (adjust as needed)
    if avg_pitch > 200:
        return "high"
    elif avg_pitch < 100:
        return "low"
    else:
        return "normal"

def generate_response(transcript, pitch_info):
    if not transcript:
        return "Sorry, I couldn't hear you clearly."

    if pitch_info == "high":
        return "You might be experiencing breathlessness. Consider consulting a doctor if symptoms persist."
    elif pitch_info == "low":
        return "Your tone sounds calm. If you're experiencing any discomfort, monitor your symptoms."
    else:
        return "Everything sounds normal, but continue to take care of your respiratory health."
