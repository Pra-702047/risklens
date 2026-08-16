"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { fetchWithAuth } from "@/lib/api-client";

export default function ReportComplaint() {
  const [description, setDescription] = useState("");
  const [address, setAddress] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [location, setLocation] = useState<{lat: number, lng: number} | null>(null);
  const [locating, setLocating] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);
  const router = useRouter();

  const getGPS = () => {
    setLocating(true);
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setLocation({
            lat: position.coords.latitude,
            lng: position.coords.longitude
          });
          setLocating(false);
        },
        (error) => {
          alert("Error getting location: " + error.message);
          setLocating(false);
        }
      );
    } else {
      alert("Geolocation is not supported by this browser.");
      setLocating(false);
    }
  };

  const handleAnalyze = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!location) {
      alert("Please capture your GPS location first.");
      return;
    }
    
    setAnalyzing(true);
    
    try {
      const formData = new FormData();
      formData.append("description", description);
      // We skip actual file upload to AI for MVP text analysis, but we attach it if future-proofed
      if (file) {
         // Not uploading file to /analyze in this MVP to save complexity,
         // the backend route accepts it but ignores it for Gemini text model.
      }
      
      const res = await fetchWithAuth("/complaints/analyze", {
        method: "POST",
        body: formData,
      });
      
      if (!res.ok) throw new Error("Analysis failed");
      
      const aiResult = await res.json();
      
      // Store draft
      sessionStorage.setItem("draftComplaint", JSON.stringify({
        description, address, location, aiResult
      }));
      
      router.push("/citizen/report/confirm");
    } catch (err: any) {
      alert("Error analyzing complaint: " + err.message);
      setAnalyzing(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6 bg-white shadow-lg mt-10 rounded-xl">
      <h1 className="text-3xl font-bold mb-6 text-gray-800 border-b pb-4">Report an Issue</h1>
      
      <form onSubmit={handleAnalyze} className="space-y-6">
        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-2">Description</label>
          <textarea 
            rows={4}
            className="w-full rounded-md border-gray-300 shadow-sm p-3 border focus:ring-2 focus:ring-blue-500"
            placeholder="Describe the issue in detail..."
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            required
          />
        </div>

        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-2">Address / Landmark (Optional)</label>
          <input 
            type="text"
            className="w-full rounded-md border-gray-300 shadow-sm p-3 border focus:ring-2 focus:ring-blue-500"
            placeholder="e.g. Near City Center Mall"
            value={address}
            onChange={(e) => setAddress(e.target.value)}
          />
        </div>

        <div className="bg-gray-50 p-4 rounded-lg border">
          <label className="block text-sm font-semibold text-gray-700 mb-2">GPS Location</label>
          <div className="flex items-center gap-4">
            <button 
              type="button"
              onClick={getGPS}
              className="bg-blue-100 text-blue-700 px-4 py-2 rounded-md font-medium hover:bg-blue-200 transition-colors"
            >
              {locating ? "Locating..." : "Capture Location"}
            </button>
            {location && (
              <span className="text-sm text-green-600 font-mono">
                {location.lat.toFixed(4)}, {location.lng.toFixed(4)}
              </span>
            )}
          </div>
        </div>

        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-2">Evidence (Image/Video/Audio)</label>
          <input 
            type="file" 
            accept="image/*,video/*,audio/*"
            onChange={(e) => setFile(e.target.files ? e.target.files[0] : null)}
            className="w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
          />
        </div>

        <div className="pt-4">
          <button 
            type="submit" 
            disabled={analyzing}
            className="w-full bg-blue-600 text-white p-4 rounded-lg font-bold text-lg hover:bg-blue-700 transition-all shadow-md disabled:bg-blue-400"
          >
            {analyzing ? "AI is Analyzing..." : "Analyze & Proceed"}
          </button>
        </div>
      </form>
    </div>
  );
}
