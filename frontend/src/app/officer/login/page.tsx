"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { loginUser } from "@/lib/firebase/auth";

export default function OfficerLogin() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      await loginUser(email, password);
      router.push("/officer/dashboard");
    } catch (err: any) {
      setError(err.message || "Invalid credentials");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-risklens-black text-white bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] bg-opacity-10">
      <div className="bg-risklens-dark p-8 rounded-2xl shadow-2xl max-w-md w-full border border-gray-800">
        <div className="text-center mb-8">
          <div className="w-16 h-16 mx-auto bg-risklens-primary rounded-full flex items-center justify-center mb-4 shadow-[0_0_20px_rgba(255,107,0,0.4)]">
            <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 11c0 3.517-1.009 6.799-2.753 9.571m-3.44-2.04l.054-.09A13.916 13.916 0 008 11a4 4 0 118 0c0 1.017-.07 2.019-.203 3m-2.118 6.844A21.88 21.88 0 0015.171 17m3.839 1.132c.645-2.266.99-4.659.99-7.132A8 8 0 008 4.07M3 15.364c.64-1.319 1-2.8 1-4.364 0-1.457.39-2.823 1.07-4" /></svg>
          </div>
          <h1 className="text-3xl font-black mb-1">
            Risk<span className="text-risklens-primary">Lens</span> Command
          </h1>
          <p className="text-gray-400 text-sm tracking-widest uppercase">Secure Officer Portal</p>
        </div>

        {error && <p className="text-red-400 text-sm mb-4 bg-red-900/50 p-3 rounded-xl border border-red-800 text-center">{error}</p>}
        
        <form onSubmit={handleLogin} className="space-y-4">
          <div>
            <label className="block text-sm font-bold text-gray-400 mb-1">Officer Email</label>
            <input 
              type="email" 
              className="w-full bg-gray-800 border border-gray-700 rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-risklens-primary" 
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              placeholder="traffic@risklens.local"
            />
          </div>
          <div>
            <label className="block text-sm font-bold text-gray-400 mb-1">Password</label>
            <input 
              type="password" 
              className="w-full bg-gray-800 border border-gray-700 rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-risklens-primary" 
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              placeholder="••••••••"
            />
          </div>
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-risklens-primary hover:bg-risklens-deep text-white py-4 rounded-xl font-bold transition-colors shadow-lg shadow-orange-900/20 disabled:opacity-50 mt-4"
          >
            {loading ? "Authenticating..." : "Access System"}
          </button>
        </form>
      </div>
    </div>
  );
}
