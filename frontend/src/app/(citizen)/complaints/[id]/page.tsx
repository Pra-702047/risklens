"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import StatusTimeline from "./StatusTimeline";

export default function CitizenComplaintDetails({ params }: { params: { id: string } }) {
  const [complaint, setComplaint] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  
  // Feedback Form State
  const [rating, setRating] = useState(0);
  const [resolutionAccepted, setResolutionAccepted] = useState<boolean | null>(null);
  const [comment, setComment] = useState("");
  const [feedbackLoading, setFeedbackLoading] = useState(false);

  const router = useRouter();

  useEffect(() => {
    const fetchComplaint = async () => {
      const token = localStorage.getItem("firebase_token");
      if (!token) return router.push("/login");

      try {
        const res = await fetch(`http://localhost:8000/complaints/${params.id}`, {
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

  const submitFeedback = async () => {
    if (rating === 0 || resolutionAccepted === null) {
      alert("Please provide a rating and acceptance decision.");
      return;
    }
    
    setFeedbackLoading(true);
    const token = localStorage.getItem("firebase_token");
    try {
      const res = await fetch(`http://localhost:8000/complaints/${params.id}/feedback`, {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          rating,
          resolution_accepted: resolutionAccepted,
          comment
        })
      });
      
      if (res.ok) {
        const data = await res.json();
        setComplaint({ ...complaint, status: data.new_status });
        alert("Feedback submitted successfully!");
      } else {
        alert("Failed to submit feedback.");
      }
    } catch (err) {
      console.error(err);
    } finally {
      setFeedbackLoading(false);
    }
  };

  if (loading) return <div className="min-h-screen bg-slate-950 p-8 text-white">Loading...</div>;
  if (!complaint) return <div className="min-h-screen bg-slate-950 p-8 text-white">Complaint not found.</div>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-200 py-8">
      <div className="container mx-auto px-4 max-w-4xl">
        <Link href="/complaints" className="text-sm text-blue-400 hover:text-blue-300 mb-6 inline-block">
          &larr; Back to My Complaints
        </Link>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Timeline Sidebar */}
          <div className="md:col-span-1 bg-slate-900 p-6 rounded-xl border border-slate-800 h-fit">
            <h2 className="text-lg font-bold text-white mb-6">Tracking</h2>
            <StatusTimeline status={complaint.status} events={complaint.status_history} />
          </div>

          {/* Main Details */}
          <div className="md:col-span-2 space-y-6">
            
            <div className="bg-slate-900 p-6 rounded-xl border border-slate-800">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h1 className="text-2xl font-bold text-white mb-1">{complaint.category}</h1>
                  <p className="text-slate-400 text-sm">{complaint.address}</p>
                </div>
                <div className="bg-slate-800 px-3 py-1 rounded text-sm text-slate-300">
                  ID: {complaint.id.split("-")[0]}
                </div>
              </div>
              
              <div className="mt-6">
                <h3 className="text-sm font-medium text-slate-400 mb-2">Your Description</h3>
                <p className="bg-slate-950 p-4 rounded text-slate-300 leading-relaxed border border-slate-800">
                  {complaint.description}
                </p>
              </div>
            </div>

            {/* Resolution & Feedback Panel */}
            {complaint.status === "AWAITING_FEEDBACK" && (
              <div className="bg-blue-900/20 p-6 rounded-xl border border-blue-800/50">
                <h2 className="text-xl font-bold text-blue-400 mb-6">Resolution Review</h2>
                
                <div className="mb-8">
                  <h3 className="text-white font-medium mb-2">Officer Notes</h3>
                  <p className="text-slate-300 bg-slate-900 p-4 rounded border border-slate-700 italic">
                    "Issue has been addressed on-site." {/* Mocking officer note for MVP */}
                  </p>
                </div>

                <div className="border-t border-blue-800/30 pt-6">
                  <h3 className="text-white font-bold mb-4">Was this issue resolved?</h3>
                  
                  {/* Rating */}
                  <div className="mb-6">
                    <p className="text-sm text-slate-400 mb-2">Rate the service (1-5)</p>
                    <div className="flex gap-2">
                      {[1, 2, 3, 4, 5].map(star => (
                        <button
                          key={star}
                          onClick={() => setRating(star)}
                          className={`text-2xl ${rating >= star ? "text-yellow-400" : "text-slate-600"}`}
                        >
                          ★
                        </button>
                      ))}
                    </div>
                  </div>

                  {/* Acceptance */}
                  <div className="mb-6">
                    <div className="flex gap-4">
                      <button 
                        onClick={() => setResolutionAccepted(true)}
                        className={`flex-1 py-3 rounded-lg font-bold border ${
                          resolutionAccepted === true 
                          ? "bg-green-600 border-green-500 text-white" 
                          : "bg-slate-900 border-slate-700 text-slate-400 hover:border-green-500 hover:text-green-400"
                        }`}
                      >
                        Yes, issue resolved
                      </button>
                      <button 
                        onClick={() => setResolutionAccepted(false)}
                        className={`flex-1 py-3 rounded-lg font-bold border ${
                          resolutionAccepted === false 
                          ? "bg-red-600 border-red-500 text-white" 
                          : "bg-slate-900 border-slate-700 text-slate-400 hover:border-red-500 hover:text-red-400"
                        }`}
                      >
                        No, issue still exists
                      </button>
                    </div>
                  </div>

                  {/* Comment */}
                  <div className="mb-6">
                    <textarea 
                      placeholder="Add an optional comment..."
                      value={comment}
                      onChange={(e) => setComment(e.target.value)}
                      className="w-full bg-slate-900 border border-slate-700 rounded-lg p-3 text-white focus:border-blue-500 outline-none h-24"
                    />
                  </div>

                  <button 
                    onClick={submitFeedback}
                    disabled={feedbackLoading}
                    className="w-full py-4 rounded-lg font-bold bg-blue-600 hover:bg-blue-700 text-white transition-colors"
                  >
                    {feedbackLoading ? "Submitting..." : "Submit Feedback"}
                  </button>
                </div>
              </div>
            )}

            {complaint.status === "REOPEN_LIMIT_REACHED" && (
              <div className="bg-red-900/20 p-6 rounded-xl border border-red-800/50">
                <h2 className="text-lg font-bold text-red-500 mb-2">Escalated to Supervisor</h2>
                <p className="text-slate-300 text-sm">
                  This complaint has reached the maximum number of reopen requests and is currently under administrative review by a supervisor.
                </p>
              </div>
            )}

          </div>
        </div>
      </div>
    </div>
  );
}
