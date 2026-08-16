"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";

export default function IncidentDetails({ params }: { params: { id: string } }) {
  const [complaint, setComplaint] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState(false);
  const router = useRouter();

  useEffect(() => {
    const fetchComplaint = async () => {
      const token = localStorage.getItem("officer_token");
      if (!token) return router.push("/login");

      try {
        const res = await fetch(`http://localhost:8000/officer/complaints/${params.id}`, {
          headers: { "Authorization": `Bearer ${token}` }
        });
        
        if (res.ok) {
          setComplaint(await res.json());
        }
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchComplaint();
  }, [params.id, router]);

  const handleAction = async (action: string) => {
    setActionLoading(true);
    try {
      const token = localStorage.getItem("officer_token");
      
      // If action is ACKNOWLEDGE, we must first claim it via POST /claim.
      // But for simplicity in MVP, let's assume /claim API covers ACKNOWLEDGE, 
      // or we just call the action API directly if claim was skipped.
      // A more robust UI would have a specific "Claim Issue" button first.
      
      if (action === "ACKNOWLEDGE") {
        await fetch(`http://localhost:8000/officer/complaints/${params.id}/claim`, {
          method: "POST",
          headers: { "Authorization": `Bearer ${token}` }
        });
      }

      const res = await fetch(`http://localhost:8000/officer/complaints/${params.id}/actions?action_type=${action}`, {
        method: "POST",
        headers: { "Authorization": `Bearer ${token}` }
      });
      
      if (res.ok) {
        // Optimistically update
        setComplaint({ ...complaint, status: action });
      } else {
        const errData = await res.json();
        alert(errData.detail || "Failed to update action");
      }
    } catch (err) {
      console.error(err);
    } finally {
      setActionLoading(false);
    }
  };

  if (loading) return <div className="min-h-screen bg-slate-950 text-white p-8">Loading...</div>;
  if (!complaint) return <div className="min-h-screen bg-slate-950 text-white p-8">Complaint not found.</div>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-200 py-8">
      <div className="container mx-auto px-4 max-w-5xl">
        <Link href="/dashboard" className="text-sm text-blue-400 hover:text-blue-300 mb-6 inline-block">
          &larr; Back to Dashboard
        </Link>
        
        {/* Header Strip */}
        <div className={`p-4 rounded-t-xl font-bold flex justify-between items-center ${
          complaint.priority === "P0" ? "bg-red-600 text-white" :
          complaint.priority === "P1" ? "bg-orange-600 text-white" :
          "bg-slate-800 text-white"
        }`}>
          <div className="flex items-center gap-3">
            <span className="text-xl">{complaint.priority || "P3"} Criticality</span>
            <span className="bg-black/20 px-2 py-1 rounded text-xs">{complaint.id}</span>
          </div>
          <div className="text-sm">
            Status: <span className="uppercase">{complaint.status}</span>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-6">
          
          {/* Main Details */}
          <div className="md:col-span-2 space-y-6">
            <div className="bg-slate-900 p-6 rounded-xl border border-slate-800">
              <h2 className="text-lg font-bold text-white mb-4">Incident Details</h2>
              <div className="grid grid-cols-2 gap-4 mb-6">
                <div>
                  <div className="text-sm text-slate-400 mb-1">Category</div>
                  <div className="font-medium">{complaint.category}</div>
                </div>
                <div>
                  <div className="text-sm text-slate-400 mb-1">Location</div>
                  <div className="font-medium text-sm">{complaint.address}</div>
                </div>
              </div>
              <div>
                <div className="text-sm text-slate-400 mb-2">Citizen Description</div>
                <p className="p-4 bg-slate-950 rounded border border-slate-800 text-slate-300 text-sm leading-relaxed">
                  {complaint.description}
                </p>
              </div>
            </div>

            <div className="bg-slate-900 p-6 rounded-xl border border-slate-800">
              <h2 className="text-lg font-bold text-white mb-4">Evidence</h2>
              <div className="p-8 border-2 border-dashed border-slate-800 rounded flex flex-col items-center justify-center text-slate-500">
                <span>[Upload Before/After Photos UI Here]</span>
                <button className="mt-4 px-4 py-2 bg-slate-800 rounded text-sm hover:bg-slate-700">Attach Evidence</button>
              </div>
            </div>
          </div>

          {/* Action Panel */}
          <div className="space-y-6">
            <div className="bg-slate-900 p-6 rounded-xl border border-slate-800">
              <h2 className="text-lg font-bold text-white mb-4">Field Actions</h2>
              
              <div className="space-y-3">
                <button 
                  onClick={() => handleAction("ACKNOWLEDGE")}
                  disabled={actionLoading || complaint.status !== "SUBMITTED"}
                  className="w-full py-3 rounded font-medium bg-blue-600 hover:bg-blue-700 disabled:opacity-50 disabled:bg-slate-800 disabled:text-slate-500 transition-colors"
                >
                  Acknowledge Issue
                </button>
                <button 
                  onClick={() => handleAction("IN_PROGRESS")}
                  disabled={actionLoading || !["ACKNOWLEDGE", "REOPENED"].includes(complaint.status)}
                  className="w-full py-3 rounded font-medium bg-amber-600 hover:bg-amber-700 disabled:opacity-50 disabled:bg-slate-800 disabled:text-slate-500 transition-colors"
                >
                  Mark In Progress
                </button>
                <button 
                  onClick={() => handleAction("ON_SITE")}
                  disabled={actionLoading || complaint.status !== "IN_PROGRESS"}
                  className="w-full py-3 rounded font-medium bg-purple-600 hover:bg-purple-700 disabled:opacity-50 disabled:bg-slate-800 disabled:text-slate-500 transition-colors"
                >
                  Report On Site
                </button>
                <button 
                  onClick={() => handleAction("RESOLVED")}
                  disabled={actionLoading || !["IN_PROGRESS", "ON_SITE", "ACTION_TAKEN"].includes(complaint.status)}
                  className="w-full py-3 rounded font-medium bg-emerald-600 hover:bg-emerald-700 disabled:opacity-50 disabled:bg-slate-800 disabled:text-slate-500 transition-colors"
                >
                  Mark Resolved
                </button>
              </div>
            </div>

          </div>
        </div>
      </div>
    </div>
  );
}
