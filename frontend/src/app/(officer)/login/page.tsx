"use client";

import { useState } from "react";
import { signInWithEmailAndPassword } from "firebase/auth";
import { auth } from "@/lib/firebase/config";
import { useRouter } from "next/navigation";

export default function OfficerLogin() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const router = useRouter();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      // 1. Firebase Auth
      const userCredential = await signInWithEmailAndPassword(auth, email, password);
      const token = await userCredential.user.getIdToken();
      
      // 2. Fetch officer profile to verify RBAC
      const res = await fetch("http://localhost:8000/users/me/officer", {
        headers: {
          "Authorization": `Bearer ${token}`
        }
      });
      
      if (!res.ok) {
        throw new Error("Access Denied. You are not an authorized officer.");
      }
      
      // Save token (in real app, use HTTP-only cookies)
      localStorage.setItem("officer_token", token);
      
      router.push("/dashboard");
    } catch (err: any) {
      setError(err.message || "Failed to login");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-900 text-white">
      <div className="w-full max-w-md p-8 rounded-xl bg-slate-800 border border-slate-700">
        <div className="text-center mb-8">
          <h1 className="text-2xl font-bold text-red-500 mb-2">RiskLens Authority Portal</h1>
          <p className="text-slate-400">Restricted Access</p>
        </div>

        {error && (
          <div className="mb-6 p-4 rounded bg-red-900/50 border border-red-500 text-red-200">
            {error}
          </div>
        )}

        <form onSubmit={handleLogin} className="space-y-6">
          <div>
            <label className="block text-sm font-medium mb-2">Official Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-lg p-3 text-white focus:border-red-500 outline-none"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-2">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-lg p-3 text-white focus:border-red-500 outline-none"
              required
            />
          </div>
          <button
            type="submit"
            className="w-full py-3 rounded-lg font-bold bg-red-600 hover:bg-red-700 transition-colors"
          >
            Authenticate
          </button>
        </form>
      </div>
    </div>
  );
}
