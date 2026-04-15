import { useEffect, useState } from "react";
import AppHeader from "./components/AppHeader";
import LoadingSpinner from "./components/LoadingSpinner";
import ModelSelector from "./components/ModelSelector";
import ResultCard from "./components/ResultCard";
import UploadZone from "./components/UploadZone";
import { predictPlantDisease } from "./services/api";

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState("");
  const [modelType, setModelType] = useState("ml");
  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (!selectedFile) {
      setPreviewUrl("");
      return undefined;
    }

    const localUrl = URL.createObjectURL(selectedFile);
    setPreviewUrl(localUrl);

    return () => URL.revokeObjectURL(localUrl);
  }, [selectedFile]);

  const handleFileSelect = (file) => {
    if (!file) {
      return;
    }

    if (!file.type.startsWith("image/")) {
      setError("Please choose a valid image file.");
      return;
    }

    setSelectedFile(file);
    setPrediction(null);
    setError("");
  };

  const handlePredict = async () => {
    if (!selectedFile) {
      setError("Please upload an image before running prediction.");
      return;
    }

    setIsLoading(true);
    setError("");
    setPrediction(null);

    try {
      const result = await predictPlantDisease({
        file: selectedFile,
        modelType,
      });
      setPrediction(result);
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="page-shell">
      <div className="page-glow page-glow-left" />
      <div className="page-glow page-glow-right" />

      <main className="app-layout">
        <AppHeader />

        <section className="main-card">
          <div className="card-grid">
            <div className="panel">
              <h2 className="panel-title">Upload Plant Leaf Image</h2>
              <p className="panel-text">
                Drop a leaf image below or browse from your computer, then choose
                the model you want to test.
              </p>

              <UploadZone
                disabled={isLoading}
                file={selectedFile}
                onFileSelect={handleFileSelect}
                previewUrl={previewUrl}
              />

              <ModelSelector
                disabled={isLoading}
                modelType={modelType}
                onChange={setModelType}
              />

              <button
                className="predict-button"
                disabled={!selectedFile || isLoading}
                onClick={handlePredict}
                type="button"
              >
                {isLoading ? "Predicting..." : "Predict Disease"}
              </button>

              {error ? <div className="message-banner error-banner">{error}</div> : null}
            </div>

            <div className="panel result-panel">
              <h2 className="panel-title">Prediction Result</h2>
              <p className="panel-text">
                The selected model will return the predicted class and its confidence
                score here.
              </p>

              {isLoading ? <LoadingSpinner /> : null}

              {!isLoading && prediction ? (
                <ResultCard prediction={prediction} />
              ) : null}

              {!isLoading && !prediction ? (
                <div className="result-placeholder">
                  <span className="placeholder-icon">🌱</span>
                  <p>No prediction yet. Upload an image and click predict.</p>
                </div>
              ) : null}
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;
