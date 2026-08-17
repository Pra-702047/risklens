"use client";

import { useState } from "react";
import { loginUser } from "@/lib/firebase/auth";
import { useRouter } from "next/navigation";
import Link from "next/link";

export default function CitizenLogin() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const router = useRouter();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await loginUser(email, password);
      router.push("/citizen/complaints");
    } catch (err: any) {
      setError(err.message);
    }
  };

  return (
    <div className="flex h-[calc(100vh-64px)] items-center justify-center bg-gray-50 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] bg-opacity-10">
      <div className="w-full max-w-md risklens-card">
        <h1 className="text-3xl font-black mb-6 text-center text-risklens-dark">
          Citizen <span className="text-risklens-primary">Login</span>
        </h1>
        {error && <p className="text-red-500 text-sm mb-4 bg-red-50 p-3 rounded-xl border border-red-100">{error}</p>}
        <form onSubmit={handleLogin} className="space-y-5">
          <div>
            <label className="block text-sm font-bold text-gray-700 mb-1">Email</label>
            <input 
              type="email" 
              className="risklens-input" 
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div>
            <label className="block text-sm font-bold text-gray-700 mb-1">Password</label>
            <input 
              type="password" 
              className="risklens-input" 
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <button 
            type="submit" 
            className="w-full btn-primary"
          >
            Login to RiskLens
          </button>
        </form>
        
        <div className="mt-8 text-center text-sm text-gray-600 border-t pt-6">
          Don't have an account?{" "}
          <Link href="/citizen/register" className="text-risklens-primary font-bold hover:text-risklens-deep transition-colors">
            Sign up here
          </Link>
        </div>
      </div>
    </div>
  );
}

