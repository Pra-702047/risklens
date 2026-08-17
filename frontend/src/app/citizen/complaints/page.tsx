"use client";

import { useEffect, useState } from "react";
import { fetchWithAuth } from "@/lib/api-client";
import { useRouter } from "next/navigation";

export default function MyComplaints() {
  const [complaints, setComplaints] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const fetchComplaints = async () => {
      try {
        const res = await fetchWithAuth("/complaints/");
        if (res.ok) {
          const data = await res.json();
          setComplaints(data);
        }
      } catch (err) {
        console.error("Failed to fetch complaints", err);
      } finally {
        setLoading(false);
      }
    };
    
    fetchComplaints();
  }, []);

  if (loading) return <div className="p-8 text-center text-lg">Loading your complaints...</div>;

  return (
    <div className="max-w-4xl mx-auto p-6 mt-8">
      <div className="flex justify-between items-center mb-8 border-b pb-4">
        <h1 className="text-3xl font-black text-risklens-dark">My <span className="text-risklens-primary">Complaints</span></h1>
        <button 
          onClick={() => router.push("/citizen/report")}
          className="btn-primary"
        >
          + New Report
        </button>
      </div>

      {complaints.length === 0 ? (
        <div className="text-center p-16 risklens-card border-dashed">
          <svg className="w-16 h-16 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 13h6m-3-3v6m5 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
          <p className="text-gray-500 mb-6 text-lg font-medium">You haven't submitted any complaints yet.</p>
          <button 
            onClick={() => router.push("/citizen/report")}
            className="btn-primary"
          >
            Submit your first report now
          </button>
        </div>
      ) : (
        <div className="grid gap-6">
          {complaints.map((c) => (
            <div key={c.id} className="risklens-card cursor-pointer">
              <div className="flex flex-col sm:flex-row sm:justify-between sm:items-start mb-4 gap-2">
                <div>
                  <span className="font-mono text-xs text-risklens-primary font-bold bg-orange-50 px-2 py-1 rounded-md mb-2 inline-block border border-orange-100">ID: {c.id}</span>
                  <h3 className="text-xl font-bold text-gray-800 uppercase tracking-tight">{c.category.replace(/_/g, ' ')}</h3>
                </div>
                <span className={`text-xs px-3 py-1.5 rounded-full font-bold uppercase ${c.status === 'RESOLVED' ? 'bg-green-100 text-green-800' : 'bg-amber-100 text-amber-800'}`}>
                  {c.status.replace(/_/g, ' ')}
                </span>
              </div>
              <p className="text-gray-600 line-clamp-2 text-sm font-medium mb-6">{c.description}</p>
              
              {/* Progress Timeline Mockup */}
              <div className="relative pt-2 mb-4">
                <div className="overflow-hidden h-2 mb-4 text-xs flex rounded-full bg-gray-100">
                  <div style={{ width: c.status === 'RESOLVED' ? '100%' : c.status === 'IN_PROGRESS' ? '75%' : '25%' }} className="shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center bg-risklens-primary transition-all duration-500"></div>
                </div>
                <div className="flex justify-between text-xs font-bold text-gray-400 uppercase tracking-wider">
                  <span className={c.status ? 'text-risklens-primary' : ''}>Reported</span>
                  <span className={c.status === 'ASSIGNED' || c.status === 'IN_PROGRESS' || c.status === 'RESOLVED' ? 'text-risklens-primary' : ''}>Assigned</span>
                  <span className={c.status === 'RESOLVED' ? 'text-risklens-primary' : ''}>Resolved</span>
                </div>
              </div>

              <div className="mt-4 pt-4 border-t border-gray-100 text-xs font-bold text-gray-400 flex justify-between items-center">
                <span>Submitted: {new Date(c.created_at).toLocaleDateString()}</span>
                <span className="text-risklens-primary hover:underline">View Details →</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
