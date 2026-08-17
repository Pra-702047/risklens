import { auth } from "./config";
import { 
  createUserWithEmailAndPassword, 
  signInWithEmailAndPassword, 
  signOut, 
  onAuthStateChanged,
  User
} from "firebase/auth";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// Optional env var to switch between firebase and local auth
const AUTH_PROVIDER = process.env.NEXT_PUBLIC_AUTH_PROVIDER || "local";

export const registerUser = async (email: string, password: string): Promise<any> => {
  if (AUTH_PROVIDER === "local") {
    const res = await fetch(`${API_BASE_URL}/users/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password, role: "CITIZEN" })
    });
    if (!res.ok) throw new Error(await res.text());
    return await res.json();
  }
  const userCredential = await createUserWithEmailAndPassword(auth, email, password);
  return userCredential.user;
};

export const loginUser = async (email: string, password: string): Promise<any> => {
  if (AUTH_PROVIDER === "local") {
    const res = await fetch(`${API_BASE_URL}/users/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username: email, password })
    });
    if (!res.ok) throw new Error("Invalid credentials");
    const data = await res.json();
    if (typeof window !== "undefined") {
      localStorage.setItem("token", data.access_token);
      localStorage.setItem("user_role", data.role);
    }
    return { email, role: data.role };
  }
  const userCredential = await signInWithEmailAndPassword(auth, email, password);
  return userCredential.user;
};

export const logoutUser = async (): Promise<void> => {
  if (typeof window !== "undefined") {
    localStorage.removeItem("token");
    localStorage.removeItem("user_role");
  }
  if (AUTH_PROVIDER !== "local") {
    await signOut(auth);
  }
};

export const getIdToken = async (forceRefresh = false): Promise<string | null> => {
  if (typeof window !== "undefined") {
    const localToken = localStorage.getItem("token");
    if (localToken) return localToken;
  }
  const user = auth.currentUser;
  if (user) {
    return await user.getIdToken(forceRefresh);
  }
  return null;
};

export const listenToAuthState = (callback: (user: any | null) => void) => {
  if (AUTH_PROVIDER === "local") {
    if (typeof window !== "undefined") {
      const token = localStorage.getItem("token");
      if (token) {
        callback({ uid: "local_user" }); // mock user presence
        return () => {};
      }
    }
    callback(null);
    return () => {};
  }
  return onAuthStateChanged(auth, callback);
};

export const getCurrentUser = (): any | null => {
  if (AUTH_PROVIDER === "local") {
    if (typeof window !== "undefined" && localStorage.getItem("token")) {
      return { uid: "local_user" };
    }
    return null;
  }
  return auth.currentUser;
};
