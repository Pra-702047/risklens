"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { fetchWithAuth } from "@/lib/api-client";
import Link from "next/link";

export default function OfficerDashboard() {
  const router = useRouter();
  const [complaints, setComplaints] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      router.push("/officer/login");
      return;
    }

    loadComplaints();
  }, [router]);

  const loadComplaints = async () => {
    try {
      const response = await fetchWithAuth("/officer/complaints/");
      if (!response.ok) throw new Error("Failed to load department queue");
      const data = await response.json();
      setComplaints(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case "P0": return "bg-red-500 text-white shadow-[0_0_10px_rgba(239,68,68,0.5)]";
      case "P1": return "bg-risklens-primary text-white shadow-[0_0_10px_rgba(255,107,0,0.5)]";
      case "P2": return "bg-amber-500 text-white";
      default: return "bg-gray-700 text-gray-300";
    }
  };

  if (loading) return <div className="min-h-screen bg-risklens-black flex items-center justify-center"><div className="w-12 h-12 border-4 border-risklens-primary border-t-transparent rounded-full animate-spin"></div></div>;

  return (
    <div className="min-h-screen bg-risklens-black text-slate-100 flex">
      
      {/* Sidebar Command Navigation */}
      <aside className="w-64 bg-risklens-dark border-r border-gray-800 hidden md:flex flex-col">
        <div className="p-6 border-b border-gray-800">
          <h1 className="text-xl font-black mb-1">
            Risk<span className="text-risklens-primary">Lens</span>
          </h1>
          <p className="text-xs text-gray-400 uppercase tracking-widest font-bold">Officer Portal</p>
        </div>
        <nav className="flex-1 p-4 space-y-2">
          <a href="#" className="flex items-center gap-3 px-4 py-3 bg-gray-800/50 text-risklens-primary border-l-2 border-risklens-primary font-bold rounded-r-lg">
            Command Center
          </a>
          <a href="#" className="flex items-center gap-3 px-4 py-3 text-gray-400 hover:text-white hover:bg-gray-800 rounded-lg transition-colors font-medium">
            Live Map
          </a>
          <a href="#" className="flex items-center gap-3 px-4 py-3 text-gray-400 hover:text-white hover:bg-gray-800 rounded-lg transition-colors font-medium">
            SLA Monitoring
          </a>
        </nav>
        <div className="p-4 border-t border-gray-800">
          <button 
            onClick={() => {
              localStorage.removeItem("token");
              router.push("/officer/login");
            }}
            className="w-full flex justify-center items-center gap-2 px-4 py-2 text-sm text-gray-400 hover:text-white hover:bg-gray-800 rounded-lg transition-colors"
          >
            Sign Out
          </button>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 p-8 overflow-y-auto bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] bg-opacity-5">
        <div className="max-w-6xl mx-auto">
          <div className="flex justify-between items-end mb-8 border-b border-gray-800 pb-6">
            <div>
              <h1 className="text-3xl font-black text-white">Assigned Queue</h1>
              <p className="text-gray-400 mt-2 font-medium">Manage and resolve civic incidents routed to your department.</p>
            </div>
            <div className="hidden sm:block text-right">
              <p className="text-2xl font-black text-risklens-primary">{complaints.length}</p>
              <p className="text-xs text-gray-500 uppercase tracking-widest font-bold">Active Cases</p>
            </div>
          </div>

          {error && <div className="bg-red-900/30 text-red-400 p-4 rounded-xl border border-red-800 mb-6 font-medium">{error}</div>}

          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
            {complaints.length === 0 ? (
              <div className="col-span-full text-center p-16 bg-risklens-dark rounded-2xl border border-gray-800">
                <svg className="w-12 h-12 text-gray-600 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" /></svg>
                <p className="text-gray-400 text-lg font-medium">Queue clear. No assigned complaints pending.</p>
              </div>
            ) : (
              complaints.map((c) => (
                <Link href={`/officer/dashboard/${c.id}`} key={c.id}>
                  <div className="bg-risklens-dark border border-gray-800 rounded-2xl p-6 hover:border-risklens-primary transition-all cursor-pointer flex flex-col h-full shadow-lg group">
                    <div className="flex justify-between items-start mb-4">
                      <span className="text-xs font-mono text-gray-500 font-bold tracking-wider">ID: {c.id.split('-')[0]}...</span>
                      <span className={`text-xs font-black px-2.5 py-1 rounded-md ${getPriorityColor(c.priority)}`}>
                        {c.priority || "UNASSIGNED"}
                      </span>
                    </div>
                    
                    <h3 className="font-bold text-xl mb-3 text-white uppercase tracking-tight group-hover:text-risklens-primary transition-colors">{c.category.replace(/_/g, ' ')}</h3>
                    <p className="text-gray-400 text-sm line-clamp-3 mb-6 flex-grow font-medium">
                      {c.description}
                    </p>
                    
                    <div className="flex justify-between items-center mt-auto pt-4 border-t border-gray-800">
                      <span className="text-xs font-bold text-gray-500">{new Date(c.created_at).toLocaleDateString()}</span>
                      <span className={`text-xs font-black uppercase tracking-wider ${c.status === 'RESOLVED' ? 'text-green-500' : 'text-amber-500'}`}>{c.status.replace(/_/g, ' ')}</span>
                    </div>
                  </div>
                </Link>
              ))
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
