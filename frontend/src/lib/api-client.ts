import { getIdToken } from "./firebase/auth";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export const fetchWithAuth = async (endpoint: string, options: RequestInit = {}) => {
  let token = null;
  
  if (typeof window !== "undefined") {
    token = localStorage.getItem("token");
  }
  
  if (!token) {
    token = await getIdToken();
  }
  
  const headers = new Headers(options.headers);
  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }
  
  if (!(options.body instanceof FormData)) {
    headers.set("Content-Type", "application/json");
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  return response;
};
