import pandas as pd
import pickle
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

# Load data
df = pd.read_csv('synthetic_respiratory_data.csv')

# Store encoders
feature_encoders = {}

# Encode categorical features
for col in ['gender', 'fever', 'cough', 'shortness_of_breath', 'chest_pain', 'fatigue', 'voice_pitch']:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    feature_encoders[col] = le

# Encode target
disease_encoder = LabelEncoder()
df['diagnosis'] = disease_encoder.fit_transform(df['diagnosis'])

# Features and target
X = df.drop(columns=['diagnosis'])
y = df['diagnosis']

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Save model and encoders
with open('symptom_model.pkl', 'wb') as f:
    pickle.dump(model, f)

with open('disease_encoder_symptoms.pkl', 'wb') as f:
    pickle.dump(disease_encoder, f)

with open('symptoms_feature_encoder.pkl', 'wb') as f:
    pickle.dump(feature_encoders, f)

print("✅ Trained and saved symptom_model.pkl, disease_encoder_symptoms.pkl, and symptoms_feature_encoder.pkl")
