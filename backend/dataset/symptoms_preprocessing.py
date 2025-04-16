import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

# Load the data
df = pd.read_csv('synthetic_respiratory_data.csv')

# Encode categorical features
categorical_cols = ['gender', 'fever', 'cough', 'shortness_of_breath', 'chest_pain', 'fatigue', 'voice_pitch']
encoders = {}

for col in categorical_cols:
    encoders[col] = LabelEncoder()
    df[col] = encoders[col].fit_transform(df[col])

# Encode target (diagnosis)
label_encoder = LabelEncoder()
df['diagnosis'] = label_encoder.fit_transform(df['diagnosis'])

# Features and target
X = df.drop('diagnosis', axis=1)
y = df['diagnosis']

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train classifier
clf = RandomForestClassifier(random_state=42)
clf.fit(X_train, y_train)

# Evaluate
y_pred = clf.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred, target_names=label_encoder.classes_))

# Save model and encoders
joblib.dump(clf, 'symptom_model.pkl')
joblib.dump(label_encoder, 'disease_encoder_symptoms.pkl')
joblib.dump(encoders, 'symptom_feature_encoders.pkl')
