function formatConfidence(confidence) {
  const safeConfidence = Number.isFinite(confidence) ? confidence : 0;
  return `${(safeConfidence * 100).toFixed(2)}%`;
}

function ResultCard({ prediction }) {
  const isHealthy = prediction.predicted_class.toLowerCase().includes("healthy");

  return (
    <article className={`result-card ${isHealthy ? "healthy" : "disease"}`}>
      <div className="result-badge">{isHealthy ? "Healthy Leaf" : "Disease Detected"}</div>

      <div className="result-row">
        <span className="result-label">Predicted Class</span>
        <strong className="result-value">{prediction.predicted_class}</strong>
      </div>

      <div className="result-row">
        <span className="result-label">Confidence Score</span>
        <strong className="result-value">{formatConfidence(prediction.confidence)}</strong>
      </div>

      <div className="result-row">
        <span className="result-label">Model Used</span>
        <strong className="result-value">{prediction.model.toUpperCase()}</strong>
      </div>
    </article>
  );
}

export default ResultCard;
