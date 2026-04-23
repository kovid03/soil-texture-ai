from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import tensorflow as tf
import numpy as np
import cv2
import json
import os
import base64
from gradcam import make_gradcam_heatmap, overlay_gradcam
from recommendations import get_recommendations

app = FastAPI(title="Soil Texture Classification API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Paths — relative to project root so it works anywhere
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
MODEL_PATH = os.path.join(BASE_DIR, 'model', 'soil_densenet.keras')
MAPPING_PATH = os.path.join(BASE_DIR, 'model', 'class_mapping.json')

# Load Model
model = None
class_mapping = {'0': 'Clay', '1': 'Loam', '2': 'Loamy Sand', '3': 'Sandy', '4': 'Sandy Loam'}

try:
    model = tf.keras.models.load_model(MODEL_PATH)
    print("Model loaded successfully.")

    with open(MAPPING_PATH, 'r') as f:
        class_mapping = json.load(f)
    print("Class mapping loaded:", class_mapping)
except Exception as e:
    print(f"Warning: Could not load model or mapping: {e}")
    print("Server will run but predictions will not work until model is placed in /model/")


def preprocess_image(img_bytes):
    """Convert raw bytes to a preprocessed 224x224 numpy array."""
    nparr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if img is None:
        raise ValueError("Invalid image file")

    original_img = img.copy()

    # Resize, convert BGR->RGB, normalize
    img = cv2.resize(img, (224, 224))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img / 255.0
    img_expanded = np.expand_dims(img, axis=0)

    return img_expanded, original_img


@app.get("/")
def read_root():
    return {"message": "Soil Texture Classification API is running!"}


@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_loaded": model is not None,
        "classes": list(class_mapping.values())
    }


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if not model:
        return {"error": "Model not loaded on server. Place soil_densenet.keras in /model/"}

    contents = await file.read()

    try:
        img_array, original_img = preprocess_image(contents)
    except Exception as e:
        return {"error": str(e)}

    # Predict
    preds = model.predict(img_array)
    pred_idx = np.argmax(preds[0])
    confidence = float(np.max(preds[0]))

    soil_type = class_mapping.get(str(pred_idx), "Unknown")

    # Recommendations
    recs = get_recommendations(soil_type)

    # Grad-CAM — find last conv layer
    last_conv_layer = 'conv5_block16_concat'  # DenseNet121 default
    try:
        for layer in reversed(model.layers):
            try:
                shape = layer.output.shape
            except Exception:
                continue
            if len(shape) == 4:
                last_conv_layer = layer.name
                break
    except Exception:
        pass

    cam_b64 = None
    try:
        heatmap = make_gradcam_heatmap(
            img_array.astype(np.float32), model, last_conv_layer
        )
        orig_resized = cv2.resize(original_img, (224, 224))
        cam_img = overlay_gradcam(orig_resized, heatmap)
        _, buffer = cv2.imencode('.jpg', cam_img)
        cam_b64 = base64.b64encode(buffer).decode('utf-8')
    except Exception as e:
        print(f"GradCAM error: {e}")

    return {
        "soil_type": soil_type,
        "confidence": confidence,
        "recommendations": recs,
        "gradcam_image": cam_b64
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
