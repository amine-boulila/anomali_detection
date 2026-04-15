function LoadingSpinner() {
  return (
    <div className="loading-box" role="status">
      <div className="spinner" />
      <p>Analyzing leaf image with AI...</p>
    </div>
  );
}

export default LoadingSpinner;
