# Plant Disease Image Classification App

This project is a full-stack web app for classifying plant leaf diseases with two saved models:

- a classical Machine Learning model
- a Deep Learning model

The frontend is built with React inside `client/`.
The backend is built with FastAPI inside `server/`.

Note: the repository already contained an empty `serveur/` folder. It was left untouched, and the working FastAPI backend was created in `server/` to match your requested structure.

## Project Structure

```text
platforme/
├── client/
│   ├── .env.example
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│       ├── App.jsx
│       ├── main.jsx
│       ├── components/
│       ├── services/
│       └── styles/
├── models/
│   ├── best_ml_model.joblib
│   ├── dl_metadata.json
│   ├── label_encoder.joblib
│   ├── ml_metadata.json
│   ├── projet-image-avec-tenserflow.ipynb
│   └── tensorflow_leaf_disease_model.keras
├── server/
│   ├── .env.example
│   ├── main.py
│   ├── requirements.txt
│   └── app/
│       ├── config.py
│       ├── models_loader/
│       ├── routes/
│       ├── schemas/
│       ├── services/
│       └── utils/
└── serveur/
```

## Backend Features

- `GET /health` to check API status and model files
- `POST /predict` to classify an uploaded image with the ML model
- CORS enabled for the React frontend
- validation for image file type
- modular code split into routes, services, utilities, and model loaders

Expected prediction response:

```json
{
  "model": "ml",
  "predicted_class": "Tomato___Late_blight",
  "confidence": 0.91
}
```

## Frontend Features

- themed UI for "Plant Disease Detection using AI"
- drag-and-drop style upload area
- image preview
- ML model selection support in the backend right now
- prediction button
- loading state
- friendly error messages
- styled result card with healthy vs disease color feedback

## How to Run the Backend

1. Open a terminal in the project root.
2. Create and activate a virtual environment.
3. Install the backend dependencies:

```bash
cd server
pip install -r requirements.txt
```

This installs the ML-only backend dependencies.

If you also want Deep Learning support later, install:

```bash
cd server
pip install -r requirements-dl.txt
```

4. Optional: copy `.env.example` to `.env` and adjust values if needed.
5. Start the FastAPI server:

```bash
uvicorn main:app --reload
```

6. Open `http://127.0.0.1:8000/docs` for the Swagger UI.

## How to Run the Frontend

1. Open another terminal in the project root.
2. Install the frontend dependencies:

```bash
cd client
npm install
```

3. Optional: copy `.env.example` to `.env` and set the API URL if your backend is not running on port 8000.
4. Start the React development server:

```bash
npm run dev
```

5. Open the local URL shown by Vite, usually `http://localhost:5173`.

## Backend Endpoints

### `GET /health`

Returns a simple status object and checks whether the saved model files exist.

### `POST /predict`

Send a `multipart/form-data` request with:

- `file`: plant image
- `model_type`: `ml`

## Exact Places to Customize

These are the exact files and sections you may want to adapt for your own saved models:

1. `server/app/config.py`
   Update filenames if your saved artifacts change.

2. `server/app/utils/image_processing.py`
   Update preprocessing or handcrafted feature extraction if you retrain the ML model differently.
   Important functions:
   - `hsv_segmentation`
   - `preprocess_image_for_ml`
   - `extract_ml_feature_vector`
   - `preprocess_image_for_dl`

3. `server/app/models_loader/dl_loader.py`
   This file is kept for later, but the DL path is commented out in the current backend.

4. `server/app/models_loader/ml_loader.py`
   Update label decoding if the saved ML model returns labels in a different format.

5. `models/ml_metadata.json`
   Confirm `feature_vector_length` and class names stay aligned with your saved ML model.

6. `models/dl_metadata.json`
   Confirm the `class_names` order and `image_size` match the saved `.keras` model.

## Notes About the Current Implementation

- The ML preprocessing and feature extraction were matched to the notebook already present in `models/projet-image-avec-tenserflow.ipynb`.
- The ML feature vector currently uses:
  - HSV histogram features
  - GLCM texture features
  - contour shape features
- The DL loader files are kept for later reuse, but the API currently exposes the ML path only and comments out the DL registry path.
- Clear `TODO` comments were added only where future customization may be needed.
- You can run the ML API without TensorFlow installed. TensorFlow is only needed when you want to use the `dl` model type.
