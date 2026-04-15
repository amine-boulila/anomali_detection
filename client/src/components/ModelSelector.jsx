const MODEL_OPTIONS = [
  {
    value: "ml",
    label: "Machine Learning",
    description: "Handcrafted features with the saved ML model",
  },
];

function ModelSelector({ disabled, modelType, onChange }) {
  return (
    <div className="model-selector">
      <h3 className="selector-title">Choose Prediction Model</h3>

      <div className="toggle-group">
        {MODEL_OPTIONS.map((option) => (
          <label
            className={`toggle-card ${modelType === option.value ? "selected" : ""}`}
            key={option.value}
          >
            <input
              checked={modelType === option.value}
              disabled={disabled}
              name="model-type"
              onChange={() => onChange(option.value)}
              type="radio"
              value={option.value}
            />
            <span className="toggle-label">{option.label}</span>
            <span className="toggle-description">{option.description}</span>
          </label>
        ))}
      </div>
    </div>
  );
}

export default ModelSelector;
