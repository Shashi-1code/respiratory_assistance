import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# Load dataset
df = pd.read_csv('respiratory_features_with_cycles.csv')

# Drop unnecessary columns
df = df.drop(columns=['patient_id', 'filename', 'cycle_num'])

# Separate features and target
X = df.drop(columns=['disease'])
y = df['disease']

# Encode the target
disease_encoder = LabelEncoder()
y_encoded = disease_encoder.fit_transform(y)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y_encoded)

# Save the model
with open('audio_models.pkl', 'wb') as f:
    pickle.dump(model, f)

# Save the encoder
with open('disease_encoder_audios.pkl', 'wb') as f:
    pickle.dump(disease_encoder, f)

print("Model and encoder saved successfully.")
