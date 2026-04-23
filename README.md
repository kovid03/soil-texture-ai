# 🌱 Soil Texture Classification — AI-Powered System

An end-to-end AI system that classifies soil images into **Clay, Loam, Sandy, Loamy Sand, Sandy Loam** using a DenseNet121 deep learning model. It provides confidence scores, Grad-CAM visual explanations, and crop/fertilizer recommendations.

> **Dataset Source:** [Phantom-fs/Soil-Classification-Dataset](https://github.com/Phantom-fs/Soil-Classification-Dataset) (555 real soil images used for training)

---

## ✨ Features

| Feature | Description |
|---|---|
| 🧠 **DenseNet121** | Fine-tuned on 555 real soil images — **96.4% validation accuracy** |
| 🔬 **Grad-CAM** | Visual heatmap showing exactly which regions the model focuses on |
| 🌾 **Crop Recommendations** | Rule-based engine suggests suitable crops for the detected soil type |
| 🧪 **Fertilizer Suggestions** | Recommends fertilizers based on soil class |
| 🌐 **Multilingual UI** | English & Hindi support with one-click toggle |
| 🎨 **Modern UI** | Dark mode, glassmorphism, Framer Motion animations |
| 🔀 **Hybrid ML Models** | Random Forest + Decision Tree classifiers (DenseNet feature extraction) |

---

## 📁 Project Structure

```
├── backend/                  # FastAPI server
│   ├── main.py              # API endpoints (/predict, /health)
│   ├── gradcam.py           # Grad-CAM visualization
│   └── recommendations.py   # Crop & fertilizer rules
├── frontend/                 # Next.js + Tailwind CSS app
│   └── src/app/page.tsx     # Main UI component
├── model/                    # Trained model files (generated)
│   ├── soil_densenet.keras  # DenseNet121 model
│   └── class_mapping.json   # Class index mapping
├── dataset/                  # Dataset scripts
│   ├── download_real_data.py # Downloads 555 real soil images
│   └── generate_dummy_data.py
├── notebooks/                # Training scripts
│   ├── train_densenet.py    # DenseNet121 training
│   └── train_ml.py          # Random Forest + Decision Tree
├── requirements.txt
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- npm

### 1. Clone & Setup

```bash
git clone https://github.com/YOUR_USERNAME/soil-texture-ai.git
cd soil-texture-ai

# Python environment
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Download Dataset

```bash
python3 dataset/download_real_data.py
```

This downloads **555 real soil images** from the [Soil-Classification-Dataset](https://github.com/Phantom-fs/Soil-Classification-Dataset) repository into `dataset/train/` with 5 classes.

### 3. Train the Model

```bash
python3 notebooks/train_densenet.py
```

This fine-tunes DenseNet121 on the downloaded dataset. The trained model is saved to `model/soil_densenet.keras`.

**Optional — train hybrid ML models:**
```bash
python3 notebooks/train_ml.py
```

### 4. Run the Backend

```bash
cd backend
uvicorn main:app --reload --port 8000
```

API will be available at `http://localhost:8000`.

### 5. Run the Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend will be available at `http://localhost:3000`.

### 6. Test It!

Open `http://localhost:3000`, upload any soil image, and get instant classification with Grad-CAM visualization and crop recommendations!

---

## 🔌 API Reference

| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | Health check |
| `/health` | GET | Detailed status (model loaded, classes) |
| `/predict` | POST | Upload image, returns classification |

### POST `/predict` — Example Response

```json
{
  "soil_type": "Clay",
  "confidence": 0.993,
  "recommendations": {
    "crops": ["Rice", "Broccoli", "Cabbage", "Cauliflower"],
    "fertilizers": ["Organic compost", "Gypsum", "Slow-release Nitrogen"]
  },
  "gradcam_image": "<base64 JPEG>"
}
```

---

## 📊 Model Performance

| Metric | Value |
|---|---|
| Architecture | DenseNet121 (fine-tuned) |
| Training Images | 555 (real soil photos) |
| Validation Accuracy | **96.4%** |
| Optimizer | Adam (lr=0.0001) |
| Loss | Categorical Crossentropy |
| Data Augmentation | Rotation, flip, zoom, brightness, shear |

### Soil Classes

| Class | Description | Source Mapping |
|---|---|---|
| Clay | Dark, sticky soil | Black Soil |
| Loam | Rich, balanced soil | Alluvial + Mountain Soil |
| Sandy | Light, loose soil | Red + Arid Soil |
| Loamy Sand | Sandy with some loam | Yellow Soil |
| Sandy Loam | Loam with sand mix | Laterite Soil |

---

## ☁️ Deployment

### Backend (Render)
1. Push code to GitHub
2. Create a new Web Service on [Render](https://render.com)
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`

### Frontend (Vercel)
1. Connect your GitHub repo to [Vercel](https://vercel.com)
2. Set root directory to `frontend/`
3. Update the API URL in `page.tsx` to point to your deployed backend

---

## 📜 License

This project uses the soil dataset under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/). The dataset was created by [Phantom-fs](https://github.com/Phantom-fs/Soil-Classification-Dataset).

---

## 🙏 Credits

- **Dataset**: [Phantom-fs/Soil-Classification-Dataset](https://github.com/Phantom-fs/Soil-Classification-Dataset)
- **Model**: DenseNet121 (pre-trained on ImageNet)
- **Frontend**: Next.js, Tailwind CSS, Framer Motion, Lucide Icons
- **Backend**: FastAPI, TensorFlow, OpenCV
