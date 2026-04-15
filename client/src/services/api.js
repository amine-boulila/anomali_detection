const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL?.replace(/\/$/, "") || "http://127.0.0.1:8000";

export async function predictPlantDisease({ file, modelType }) {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("model_type", modelType);

  const response = await fetch(`${API_BASE_URL}/predict`, {
    method: "POST",
    body: formData,
  });

  let payload = null;
  try {
    payload = await response.json();
  } catch (error) {
    payload = null;
  }

  if (!response.ok) {
    throw new Error(payload?.detail || "Prediction request failed.");
  }

  return payload;
}
