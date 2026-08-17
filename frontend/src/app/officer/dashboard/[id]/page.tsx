"use client";

import { useEffect, useState, use } from "react";
import { useRouter } from "next/navigation";
import { fetchWithAuth } from "@/lib/api-client";
import Link from "next/link";

export default function OfficerComplaintDetail({ params }: { params: Promise<{ id: string }> }) {
  const router = useRouter();
  const resolvedParams = use(params);
  const complaintId = resolvedParams.id;
  
  const [complaint, setComplaint] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [actionNotes, setActionNotes] = useState("");
  const [actionSubmitting, setActionSubmitting] = useState(false);

  useEffect(() => {
    loadComplaint();
  }, [complaintId]);

  const loadComplaint = async () => {
    try {
      const response = await fetchWithAuth(`/officer/complaints/${complaintId}`);
      if (!response.ok) throw new Error("Failed to load complaint details");
      const data = await response.json();
      setComplaint(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const logAction = async (actionType: string) => {
    setActionSubmitting(true);
    try {
      const queryParams = new URLSearchParams({
        action_type: actionType,
        ...(actionNotes ? { notes: actionNotes } : {})
      });
      
      const response = await fetchWithAuth(`/officer/complaints/${complaintId}/actions?${queryParams.toString()}`, {
        method: "POST"
      });
      
      if (!response.ok) throw new Error("Failed to log action");
      
      // Reload complaint
      await loadComplaint();
      setActionNotes("");
      alert(`Status updated to ${actionType}`);
    } catch (err: any) {
      alert(err.message);
    } finally {
      setActionSubmitting(false);
    }
  };

  if (loading) return <div className="min-h-screen bg-risklens-black flex items-center justify-center"><div className="w-12 h-12 border-4 border-risklens-primary border-t-transparent rounded-full animate-spin"></div></div>;
  if (error) return <div className="min-h-screen bg-risklens-black p-8 text-center text-red-400 font-medium">{error}</div>;
  if (!complaint) return <div className="min-h-screen bg-risklens-black p-8 text-center text-gray-400 font-medium">Incident not found</div>;

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
          <Link href="/officer/dashboard" className="flex items-center gap-3 px-4 py-3 text-gray-400 hover:text-white hover:bg-gray-800 rounded-lg transition-colors font-medium">
            Command Center
          </Link>
          <a href="#" className="flex items-center gap-3 px-4 py-3 text-gray-400 hover:text-white hover:bg-gray-800 rounded-lg transition-colors font-medium">
            Live Map
          </a>
          <a href="#" className="flex items-center gap-3 px-4 py-3 bg-gray-800/50 text-risklens-primary border-l-2 border-risklens-primary font-bold rounded-r-lg">
            Incident Detailing
          </a>
        </nav>
      </aside>

      <main className="flex-1 p-8 overflow-y-auto bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] bg-opacity-5">
        <div className="max-w-5xl mx-auto">
          <Link href="/officer/dashboard" className="text-risklens-primary hover:text-risklens-deep mb-6 inline-flex items-center gap-2 font-bold uppercase tracking-wider text-xs">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" /></svg>
            Return to Command Center
          </Link>
          
          <div className="bg-risklens-dark rounded-2xl p-8 border border-gray-800 shadow-2xl relative overflow-hidden">
            {/* Top right decorative element */}
            <div className="absolute top-0 right-0 w-32 h-32 bg-risklens-primary/5 rounded-bl-full border-b border-l border-risklens-primary/10"></div>

            <div className="flex flex-col md:flex-row justify-between items-start mb-8 relative z-10 border-b border-gray-800 pb-8">
              <div>
                <h1 className="text-3xl font-black text-white mb-2 uppercase tracking-tight">{complaint.category.replace(/_/g, ' ')}</h1>
                <p className="text-risklens-primary font-mono text-sm font-bold bg-orange-900/20 px-3 py-1 rounded-md inline-block border border-orange-900/50">INCIDENT ID: {complaint.id}</p>
              </div>
              <div className="flex items-end gap-3 mt-4 md:mt-0">
                <span className={`px-4 py-1.5 rounded-md font-black text-xs tracking-widest uppercase border ${complaint.status === 'RESOLVED' ? 'bg-green-900/30 text-green-400 border-green-800' : 'bg-amber-900/30 text-amber-400 border-amber-800'}`}>
                  {complaint.status.replace(/_/g, ' ')}
                </span>
                <span className={`px-4 py-1.5 rounded-md font-black text-xs tracking-widest uppercase border ${complaint.priority === 'P0' ? 'bg-red-900/30 text-red-400 border-red-800 shadow-[0_0_15px_rgba(239,68,68,0.2)]' : complaint.priority === 'P1' ? 'bg-orange-900/30 text-orange-400 border-orange-800 shadow-[0_0_15px_rgba(255,107,0,0.2)]' : 'bg-gray-800 text-gray-300 border-gray-700'}`}>
                  {complaint.priority || "UNASSIGNED"}
                </span>
              </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8 relative z-10">
              <div className="lg:col-span-2 space-y-8">
                <div>
                  <h3 className="text-xs font-black text-gray-500 uppercase tracking-widest mb-3 flex items-center gap-2">
                    <svg className="w-4 h-4 text-risklens-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h7" /></svg>
                    Incident Report
                  </h3>
                  <p className="text-lg bg-gray-900/50 p-6 rounded-xl border border-gray-800 font-medium text-gray-300 leading-relaxed shadow-inner">{complaint.description}</p>
                </div>
                
                <div>
                  <h3 className="text-xs font-black text-gray-500 uppercase tracking-widest mb-3 flex items-center gap-2">
                    <svg className="w-4 h-4 text-risklens-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" /><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
                    Geospatial Data
                  </h3>
                  <div className="bg-gray-900/50 p-6 rounded-xl border border-gray-800 shadow-inner">
                    {complaint.address && <p className="mb-3 text-white font-medium">{complaint.address}</p>}
                    <p className="font-mono text-sm text-risklens-primary font-bold bg-black/40 px-3 py-2 rounded border border-gray-800 inline-block">
                      {complaint.latitude}, {complaint.longitude}
                    </p>
                    <a 
                      href={`https://www.google.com/maps/search/?api=1&query=${complaint.latitude},${complaint.longitude}`} 
                      target="_blank" 
                      className="mt-4 flex items-center gap-2 text-sm font-bold text-white bg-gray-800 hover:bg-gray-700 px-4 py-2 rounded-lg w-fit transition-colors border border-gray-700"
                    >
                      <svg className="w-4 h-4 text-blue-400" fill="currentColor" viewBox="0 0 24 24"><path d="M12 0C7.58 0 4 3.58 4 8c0 5.25 7 13 8 16 1-3 8-10.75 8-16 0-4.42-3.58-8-8-8zm0 11c-1.66 0-3-1.34-3-3s1.34-3 3-3 3 1.34 3 3-1.34 3-3 3z"/></svg>
                      Open in Maps
                    </a>
                  </div>
                </div>
              </div>

              <div>
                <h3 className="text-xs font-black text-gray-500 uppercase tracking-widest mb-3 flex items-center gap-2">
                  <svg className="w-4 h-4 text-risklens-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                  Action Console
                </h3>
                <div className="bg-gray-900/80 p-6 rounded-xl border border-gray-800 relative overflow-hidden">
                  <textarea 
                    className="w-full bg-black/50 border border-gray-700 rounded-xl p-4 text-white mb-6 focus:border-risklens-primary outline-none transition-colors font-medium text-sm placeholder-gray-600 resize-none"
                    rows={5}
                    placeholder="Enter operational notes..."
                    value={actionNotes}
                    onChange={(e) => setActionNotes(e.target.value)}
                  ></textarea>
                  
                  <div className="flex flex-col gap-3">
                    <button 
                      disabled={actionSubmitting || complaint.status === 'IN_PROGRESS'}
                      onClick={() => logAction("IN_PROGRESS")}
                      className="bg-amber-600/20 hover:bg-amber-600/40 text-amber-500 border border-amber-600/50 disabled:opacity-30 font-bold py-3.5 rounded-xl transition-all text-sm uppercase tracking-wider"
                    >
                      Set In Progress
                    </button>
                    <button 
                      disabled={actionSubmitting || complaint.status === 'RESOLVED'}
                      onClick={() => logAction("RESOLVED")}
                      className="bg-green-600/20 hover:bg-green-600/40 text-green-500 border border-green-600/50 disabled:opacity-30 font-bold py-3.5 rounded-xl transition-all text-sm uppercase tracking-wider shadow-[0_0_15px_rgba(34,197,94,0.1)] hover:shadow-[0_0_20px_rgba(34,197,94,0.2)]"
                    >
                      Mark Resolved
                    </button>
                  </div>
                </div>
              </div>
            </div>
            
          </div>
        </div>
      </main>
    </div>
  );
}
