import os
import numpy as np
import pandas as pd
import librosa
import pickle
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# === Load all models and encoders ===
AUDIO_MODEL_PATH = 'audio_models.pkl'
AUDIO_ENCODER_PATH = 'disease_encoder_audios.pkl'
SYMPTOM_MODEL_PATH = 'symptom_model.pkl'
SYMPTOM_ENCODER_PATH = 'disease_encoder_symptoms.pkl'
SYMPTOM_FEATURE_ENCODERS_PATH = 'symptoms_feature_encoder.pkl'

with open(AUDIO_MODEL_PATH, 'rb') as f:
    audio_model = pickle.load(f)
with open(AUDIO_ENCODER_PATH, 'rb') as f:
    audio_encoder = pickle.load(f)
with open(SYMPTOM_MODEL_PATH, 'rb') as f:
    symptom_model = pickle.load(f)
with open(SYMPTOM_ENCODER_PATH, 'rb') as f:
    symptom_encoder = pickle.load(f)
with open(SYMPTOM_FEATURE_ENCODERS_PATH, 'rb') as f:
    symptom_feature_encoders = pickle.load(f)  # Dict of LabelEncoders or OneHotEncoders

# === Helper: Extract audio features ===
def extract_audio_features(file_path):
    try:
        y, sr = librosa.load(file_path, sr=22050)
        features = {
            'duration': librosa.get_duration(y=y, sr=sr),
            'rms': librosa.feature.rms(y=y).mean(),
            'zero_crossing_rate': librosa.feature.zero_crossing_rate(y=y).mean(),
            'spectral_centroid': librosa.feature.spectral_centroid(y=y, sr=sr).mean(),
            'spectral_bandwidth': librosa.feature.spectral_bandwidth(y=y, sr=sr).mean(),
        }
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        for i in range(13):
            features[f'mfcc_{i+1}_mean'] = mfccs[i].mean()

        # Add placeholders for crackles/wheezes to match training data (assume 0)
        features['has_crackles'] = 0
        features['has_wheezes'] = 0

        return pd.DataFrame([features])
    except Exception as e:
        print(f"Audio processing error: {e}")
        return pd.DataFrame()


# === Helper: Process symptoms ===
def process_symptoms(symptoms):
    # Create a full feature row with default values
    all_features = {col: 0 for col in symptom_feature_encoders.keys()}
    all_features.update(symptoms)  # Overwrite with actual input

    df = pd.DataFrame([all_features])

    for col, encoder in symptom_feature_encoders.items():
        if col in df.columns:
            try:
                df[col] = encoder.transform(df[col])
            except Exception as e:
                print(f"[WARN] Encoding issue for {col}: {e}")
                df[col] = 0  # fallback if transformation fails
    return df

# === Route: Analyze audio and symptoms ===
@app.route('/api/analyze', methods=['POST'])
def analyze():
    try:
        audio_file = request.files.get('audio')
        symptoms = request.form.to_dict()

        # === Audio prediction ===
        audio_path = 'temp_audio.wav'
        audio_disease = "Could not process audio"
        if audio_file:
            audio_file.save(audio_path)
            audio_features = extract_audio_features(audio_path)
            os.remove(audio_path)

            if not audio_features.empty:
                try:
                    model_features = list(audio_model.feature_names_in_)
                    print("[DEBUG] Model expects audio features:", model_features)
                    print("[DEBUG] Audio features extracted:", list(audio_features.columns))

                    audio_features = audio_features.reindex(columns=model_features, fill_value=0)
                    audio_pred = audio_model.predict(audio_features)
                    audio_disease = audio_encoder.inverse_transform(audio_pred)[0]
                except Exception as e:
                    print(f"Audio prediction error: {e}")

        # === Symptom prediction ===
        symptom_disease = "Insufficient symptom data"
        try:
            symptoms_df = process_symptoms(symptoms)
            if not symptoms_df.empty:
                print("[DEBUG] Symptom features:", symptoms_df.columns.tolist())
                symptom_pred = symptom_model.predict(symptoms_df)
                symptom_disease = symptom_encoder.inverse_transform(symptom_pred)[0]
        except Exception as e:
            print(f"Symptom prediction error: {e}")

        return jsonify({
            'prediction_from_audio': audio_disease,
            'prediction_from_symptoms': symptom_disease
        })

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

# === Run ===
if __name__ == '__main__':
    app.run(debug=True, port=5000)
