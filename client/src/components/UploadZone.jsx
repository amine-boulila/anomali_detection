import { useRef, useState } from "react";

function UploadZone({ disabled, file, onFileSelect, previewUrl }) {
  const inputRef = useRef(null);
  const [isDragging, setIsDragging] = useState(false);

  const openFilePicker = () => {
    if (!disabled) {
      inputRef.current?.click();
    }
  };

  const handleDrop = (event) => {
    event.preventDefault();
    setIsDragging(false);

    const droppedFile = event.dataTransfer.files?.[0];
    onFileSelect(droppedFile);
  };

  return (
    <div className="upload-block">
      <button
        className={`upload-zone ${isDragging ? "dragging" : ""}`}
        disabled={disabled}
        onClick={openFilePicker}
        onDragEnter={(event) => {
          event.preventDefault();
          setIsDragging(true);
        }}
        onDragLeave={(event) => {
          event.preventDefault();
          setIsDragging(false);
        }}
        onDragOver={(event) => event.preventDefault()}
        onDrop={handleDrop}
        type="button"
      >
        <span className="upload-icon">📷</span>
        <span className="upload-title">Drag and drop your image here</span>
        <span className="upload-text">or click to browse files</span>
        <span className="upload-hint">Accepted formats: JPG, PNG, BMP, WEBP</span>
      </button>

      <input
        accept="image/*"
        className="hidden-input"
        disabled={disabled}
        onChange={(event) => onFileSelect(event.target.files?.[0])}
        ref={inputRef}
        type="file"
      />

      {file ? <p className="file-name">Selected file: {file.name}</p> : null}

      {previewUrl ? (
        <div className="preview-card">
          <img alt="Selected plant preview" className="preview-image" src={previewUrl} />
        </div>
      ) : null}
    </div>
  );
}

export default UploadZone;
