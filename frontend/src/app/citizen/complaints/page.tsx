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
        <h1 className="text-3xl font-bold text-gray-800">My Complaints</h1>
        <button 
          onClick={() => router.push("/citizen/report")}
          className="bg-blue-600 text-white px-6 py-2 rounded-lg font-semibold hover:bg-blue-700 transition-colors shadow-sm"
        >
          + New Report
        </button>
      </div>

      {complaints.length === 0 ? (
        <div className="text-center p-12 bg-gray-50 rounded-xl border border-dashed">
          <p className="text-gray-500 mb-4 text-lg">You haven't submitted any complaints yet.</p>
          <button 
            onClick={() => router.push("/citizen/report")}
            className="text-blue-600 font-semibold hover:underline"
          >
            Submit your first report now
          </button>
        </div>
      ) : (
        <div className="grid gap-4">
          {complaints.map((c) => (
            <div key={c.id} className="bg-white p-5 rounded-lg shadow-sm border hover:shadow-md transition-shadow">
              <div className="flex justify-between items-start mb-2">
                <span className="font-mono text-sm text-blue-600 font-bold">{c.id}</span>
                <span className="bg-yellow-100 text-yellow-800 text-xs px-2 py-1 rounded-full font-bold uppercase">
                  {c.status}
                </span>
              </div>
              <h3 className="text-lg font-bold text-gray-800 mb-1">{c.category}</h3>
              <p className="text-gray-600 line-clamp-2 text-sm">{c.description}</p>
              <div className="mt-4 text-xs text-gray-400">
                Submitted on: {new Date(c.created_at).toLocaleDateString()}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
