import os
import cv2
import numpy as np
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, accuracy_score
from tensorflow.keras.applications import DenseNet121
from tensorflow.keras.models import Model
import json

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
dataset_dir = os.path.join(base_dir, 'dataset', 'train')
model_dir = os.path.join(base_dir, 'model')
os.makedirs(model_dir, exist_ok=True)

# 1. Feature Extractor Setup (DenseNet121 without top layers)
base_model = DenseNet121(weights='imagenet', include_top=False, input_shape=(224, 224, 3), pooling='avg')

def load_data_and_extract_features(dataset_path):
    features = []
    labels = []
    class_names = sorted(os.listdir(dataset_path))
    class_mapping = {i: name for i, name in enumerate(class_names)}
    
    for label_idx, class_name in class_mapping.items():
        class_path = os.path.join(dataset_path, class_name)
        if not os.path.isdir(class_path): continue
        for img_name in os.listdir(class_path):
            img_path = os.path.join(class_path, img_name)
            img = cv2.imread(img_path)
            if img is None: continue
            
            # Preprocess
            img = cv2.resize(img, (224, 224))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = img / 255.0  # Normalize
            
            # Apply Gaussian Blur (Noise reduction)
            img = cv2.GaussianBlur(img, (5, 5), 0)
            
            # Extract Feature
            img_expanded = np.expand_dims(img, axis=0)
            feature = base_model.predict(img_expanded, verbose=0)
            
            features.append(feature.flatten())
            labels.append(label_idx)
            
    return np.array(features), np.array(labels), class_mapping

print("Extracting features from dataset using DenseNet121...")
X, y, class_mapping = load_data_and_extract_features(dataset_dir)

# Save class mapping
with open(os.path.join(model_dir, 'ml_class_mapping.json'), 'w') as f:
    json.dump(class_mapping, f)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 2. Train Random Forest
print("Training Random Forest Classifier...")
rf_clf = RandomForestClassifier(n_estimators=100, random_state=42)
rf_clf.fit(X_train, y_train)

rf_preds = rf_clf.predict(X_test)
print("Random Forest Accuracy:", accuracy_score(y_test, rf_preds))
print("Random Forest Report:\n", classification_report(y_test, rf_preds, target_names=list(class_mapping.values())))

# Save model
rf_path = os.path.join(model_dir, 'rf_model.pkl')
with open(rf_path, 'wb') as f:
    pickle.dump(rf_clf, f)
print(f"Saved RF model to {rf_path}")

# 3. Train Decision Tree
print("\nTraining Decision Tree Classifier...")
dt_clf = DecisionTreeClassifier(random_state=42)
dt_clf.fit(X_train, y_train)

dt_preds = dt_clf.predict(X_test)
print("Decision Tree Accuracy:", accuracy_score(y_test, dt_preds))
print("Decision Tree Report:\n", classification_report(y_test, dt_preds, target_names=list(class_mapping.values())))

dt_path = os.path.join(model_dir, 'dt_model.pkl')
with open(dt_path, 'wb') as f:
    pickle.dump(dt_clf, f)
print(f"Saved DT model to {dt_path}")

print("Hybrid model training complete.")
