const API_BASE = "http://localhost:5000/api";

// 1. Health Status Function (Moved outside for scope clarity)
export const getHealthStatus = async () => {
  const response = await fetch(`${API_BASE}/health`);
  if (!response.ok) {
    throw new Error("Health check failed");
  }
  return response.json();
};

// 2. Upload PDFs Function
export const uploadPDFs = async (files) => {
  const formData = new FormData();

  // Ensure files is an array-like object before iterating
  Array.from(files).forEach((file) => {
    formData.append("pdfs", file); // Must match backend 'pdfs' field
  });

  const response = await fetch(`${API_BASE}/upload/analyze`, {
    method: "POST",
    body: formData,
    // Note: Do NOT set 'Content-Type' header;
    // Browser sets it automatically with the boundary for FormData.
  });

  const data = await response.json();

  if (!response.ok) {
    console.error("Backend error:", data);
    throw new Error(data?.message || "Upload failed");
  }

  return data;
};