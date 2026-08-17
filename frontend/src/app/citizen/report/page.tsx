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
      
      const res = await fetchWithAuth("/complaints/analyze", {
        method: "POST",
        body: formData,
      });
      
      if (!res.ok) throw new Error("Analysis failed");
      
      const aiResult = await res.json();
      
      // Handle file conversion to base64
      let fileBase64 = null;
      let fileName = null;
      let fileType = null;
      
      if (file) {
        const reader = new FileReader();
        fileBase64 = await new Promise((resolve) => {
          reader.onload = () => resolve(reader.result);
          reader.readAsDataURL(file);
        });
        fileName = file.name;
        fileType = file.type;
      }
      
      // Store draft
      sessionStorage.setItem("draftComplaint", JSON.stringify({
        description, address, location, aiResult, fileBase64, fileName, fileType
      }));
      
      router.push("/citizen/report/confirm");
    } catch (err: any) {
      alert("Error analyzing complaint: " + err.message);
      setAnalyzing(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6 lg:p-10 risklens-card mt-10">
      <h1 className="text-3xl font-black mb-8 text-risklens-dark border-b border-gray-100 pb-4">
        Report an <span className="text-risklens-primary">Issue</span>
      </h1>
      
      <form onSubmit={handleAnalyze} className="space-y-8">
        <div>
          <label className="block text-sm font-bold text-gray-700 mb-2">Description</label>
          <textarea 
            rows={4}
            className="risklens-input"
            placeholder="Describe the issue in detail..."
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            required
          />
        </div>

        <div>
          <label className="block text-sm font-bold text-gray-700 mb-2">Address / Landmark (Optional)</label>
          <input 
            type="text"
            className="risklens-input"
            placeholder="e.g. Near City Center Mall"
            value={address}
            onChange={(e) => setAddress(e.target.value)}
          />
        </div>

        <div className="bg-orange-50 p-6 rounded-xl border border-orange-100">
          <label className="block text-sm font-bold text-gray-700 mb-3">GPS Location <span className="text-red-500">*</span></label>
          <div className="flex flex-col sm:flex-row sm:items-center gap-4">
            <button 
              type="button"
              onClick={getGPS}
              className="btn-secondary flex items-center justify-center gap-2"
            >
              <svg className="w-5 h-5 text-risklens-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" /><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
              {locating ? "Locating..." : "Capture Location"}
            </button>
            {location && (
              <span className="text-sm text-green-600 font-bold bg-green-50 px-3 py-1.5 rounded-full border border-green-100 flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
                {location.lat.toFixed(4)}, {location.lng.toFixed(4)}
              </span>
            )}
          </div>
        </div>

        <div>
          <label className="block text-sm font-bold text-gray-700 mb-2">Evidence (Image/Video/Audio)</label>
          <input 
            type="file" 
            accept="image/*,video/*,audio/*"
            onChange={(e) => setFile(e.target.files ? e.target.files[0] : null)}
            className="w-full text-sm text-gray-500 file:mr-4 file:py-3 file:px-6 file:rounded-xl file:border-0 file:text-sm file:font-bold file:bg-gray-100 file:text-risklens-dark hover:file:bg-gray-200 transition-colors cursor-pointer border border-dashed border-gray-300 rounded-xl p-2"
          />
        </div>

        <div className="pt-6 border-t border-gray-100">
          <button 
            type="submit" 
            disabled={analyzing}
            className="w-full btn-primary text-lg py-4 flex items-center justify-center gap-2"
          >
            {analyzing ? (
              <>
                <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                AI is Analyzing...
              </>
            ) : "Analyze & Proceed"}
          </button>
        </div>
      </form>
    </div>
  );
}
