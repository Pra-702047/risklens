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
    <div className="max-w-2xl mx-auto p-6 bg-white shadow-lg mt-10 rounded-xl">
      <h1 className="text-3xl font-bold mb-6 text-gray-800 border-b pb-4">Confirm Details</h1>
      
      {error && <div className="bg-red-50 text-red-600 p-4 rounded-md mb-6">{error}</div>}

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
            className="w-full rounded-md border-gray-300 shadow-sm p-3 border focus:ring-2 focus:ring-blue-500 mb-4"
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
              className="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg font-medium transition-colors"
            >
              Cancel
            </button>
            <button 
              onClick={handleSubmit}
              className="bg-orange-500 text-white px-6 py-2 rounded-lg font-bold hover:bg-orange-600 transition-colors shadow-sm"
              disabled={submitting}
            >
              {submitting ? "Submitting..." : "Submit with Override"}
            </button>
          </div>
        </div>
      )}

      <div className="space-y-4 mb-8">
        <div className="bg-gray-50 p-4 rounded-lg">
          <p className="text-sm text-gray-500 font-semibold uppercase">Description</p>
          <p className="text-lg whitespace-pre-wrap">{draft.description}</p>
        </div>
        
        {draft.address && (
          <div className="bg-gray-50 p-4 rounded-lg">
            <p className="text-sm text-gray-500 font-semibold uppercase">Address</p>
            <p className="text-lg">{draft.address}</p>
          </div>
        )}
        
        <div className="bg-gray-50 p-4 rounded-lg">
          <p className="text-sm text-gray-500 font-semibold uppercase">Location</p>
          <p className="text-lg font-mono">Lat: {draft.location.lat.toFixed(4)}, Lng: {draft.location.lng.toFixed(4)}</p>
        </div>
      </div>

    </div>
  );
}
