"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { fetchWithAuth } from "@/lib/api-client";
import ClassificationPreview from "@/components/ClassificationPreview";

export default function ConfirmReport() {
  const [draft, setDraft] = useState<any>(null);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [showOverride, setShowOverride] = useState(false);
  const [finalCategory, setFinalCategory] = useState("");
  const router = useRouter();

  useEffect(() => {
    const saved = sessionStorage.getItem("draftComplaint");
    if (saved) {
      const parsed = JSON.parse(saved);
      setDraft(parsed);
      setFinalCategory(parsed.aiResult.predicted_category);
    } else {
      router.push("/citizen/report");
    }
  }, [router]);

  const handleSubmit = async () => {
    if (!draft) return;
    setSubmitting(true);
    setError("");

    try {
      const formData = new FormData();
      formData.append("analysis_id", draft.aiResult.analysis_id);
      formData.append("category", finalCategory);
      formData.append("description", draft.description);
      formData.append("longitude", draft.location.lng.toString());
      formData.append("latitude", draft.location.lat.toString());
      if (draft.address) formData.append("address", draft.address);
      
      if (draft.fileBase64) {
        // Convert base64 Data URL to Blob
        const res = await fetch(draft.fileBase64);
        const blob = await res.blob();
        formData.append("files", blob, draft.fileName);
      }

      const response = await fetchWithAuth("/complaints/", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Failed to submit complaint");
      }

      const result = await response.json();
      sessionStorage.removeItem("draftComplaint");
      alert(`Complaint submitted successfully! ID: ${result.id}`);
      router.push("/citizen/complaints");
    } catch (err: any) {
      setError(err.message);
      setSubmitting(false);
    }
  };

  if (!draft) return <div className="p-8 text-center">Loading...</div>;

  return (
    <div className="max-w-3xl mx-auto p-6 lg:p-10 risklens-card mt-10">
      <h1 className="text-3xl font-black mb-8 text-risklens-dark border-b border-gray-100 pb-4">
        Confirm <span className="text-risklens-primary">Details</span>
      </h1>
      
      {error && <div className="bg-red-50 text-red-600 p-4 rounded-xl mb-6 border border-red-100 font-medium">{error}</div>}

      <ClassificationPreview 
        predictedCategory={draft.aiResult.predicted_category}
        confidence={draft.aiResult.confidence}
        reasonCodes={draft.aiResult.reason_codes}
        reviewStatus={draft.aiResult.review_status}
        onConfirm={handleSubmit}
        onChangeRequest={() => setShowOverride(true)}
      />

      {showOverride && (
        <div className="bg-white border-2 border-orange-200 p-6 rounded-xl mb-8 shadow-sm">
          <h3 className="font-bold text-gray-800 mb-2">Select Correct Category</h3>
          <p className="text-sm text-gray-600 mb-4">The AI might have made a mistake. Please select the category that best describes your issue.</p>
          <select 
            className="risklens-input mb-4"
            value={finalCategory}
            onChange={(e) => setFinalCategory(e.target.value)}
          >
            <option value="TRAFFIC_JAM">Traffic Jam</option>
            <option value="ROAD_ACCIDENT">Road Accident</option>
            <option value="RASH_DRIVING">Rash Driving</option>
            <option value="ILLEGAL_PARKING">Illegal Parking</option>
            <option value="TRAFFIC_SIGNAL">Traffic Signal Issue</option>
            <option value="POTHOLE">Pothole</option>
            <option value="ROAD_DAMAGE">Road Damage</option>
            <option value="WATERLOGGING">Waterlogging</option>
            <option value="GARBAGE">Garbage / Sanitation</option>
            <option value="STREET_LIGHT">Street Light Issue</option>
            <option value="ENCROACHMENT">Encroachment</option>
            <option value="ROAD_OBSTRUCTION">Road Obstruction</option>
            <option value="OTHER">Other</option>
          </select>
          <div className="flex gap-2">
            <button 
              onClick={() => setShowOverride(false)}
              className="btn-secondary"
            >
              Cancel
            </button>
            <button 
              onClick={handleSubmit}
              className="btn-primary"
              disabled={submitting}
            >
              {submitting ? "Submitting..." : "Submit with Override"}
            </button>
          </div>
        </div>
      )}

      <div className="space-y-4 mb-8">
        <div className="bg-gray-50 p-6 rounded-xl border border-gray-100">
          <p className="text-xs text-gray-500 font-bold uppercase tracking-wider mb-2">Description</p>
          <p className="text-lg whitespace-pre-wrap text-risklens-dark">{draft.description}</p>
        </div>
        
        {draft.address && (
          <div className="bg-gray-50 p-6 rounded-xl border border-gray-100">
            <p className="text-xs text-gray-500 font-bold uppercase tracking-wider mb-2">Address</p>
            <p className="text-lg text-risklens-dark">{draft.address}</p>
          </div>
        )}
        
        <div className="bg-gray-50 p-6 rounded-xl border border-gray-100">
          <p className="text-xs text-gray-500 font-bold uppercase tracking-wider mb-2">Location</p>
          <p className="text-lg font-mono text-risklens-dark">Lat: {draft.location.lat.toFixed(4)}, Lng: {draft.location.lng.toFixed(4)}</p>
        </div>
      </div>

    </div>
  );
}
