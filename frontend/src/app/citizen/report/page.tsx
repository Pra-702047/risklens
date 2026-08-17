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
    <div className="w-full max-w-3xl mx-auto px-4 py-12">
      <div className="mb-10 text-center">
        <h1 className="text-4xl md:text-5xl font-black mb-4 text-risklens-dark tracking-tight">
          Report an <span className="text-transparent bg-clip-text bg-gradient-to-r from-risklens-primary to-orange-400">Issue</span>
        </h1>
        <p className="text-lg text-gray-500 max-w-xl mx-auto">
          Help us identify and resolve problems in your community. Provide details, location, and evidence for faster resolution.
        </p>
      </div>
      
      <div className="bg-white rounded-3xl shadow-xl shadow-gray-200/50 border border-gray-100 overflow-hidden">
        <form onSubmit={handleAnalyze} className="p-8 md:p-12 space-y-8">
          
          <div className="space-y-6">
            <div>
              <label className="block text-sm font-bold text-gray-900 mb-2">Description</label>
              <textarea 
                rows={5}
                className="w-full rounded-2xl border border-gray-200 shadow-sm p-5 text-gray-800 bg-gray-50/50 hover:bg-gray-50 focus:bg-white focus:ring-4 focus:ring-risklens-primary/20 focus:border-risklens-primary transition-all outline-none resize-y text-base"
                placeholder="Please describe the issue in as much detail as possible..."
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                required
              />
            </div>

            <div>
              <label className="block text-sm font-bold text-gray-900 mb-2">Address / Landmark <span className="text-gray-400 font-normal">(Optional)</span></label>
              <input 
                type="text"
                className="w-full rounded-2xl border border-gray-200 shadow-sm p-5 text-gray-800 bg-gray-50/50 hover:bg-gray-50 focus:bg-white focus:ring-4 focus:ring-risklens-primary/20 focus:border-risklens-primary transition-all outline-none text-base"
                placeholder="e.g. Near City Center Mall, opposite to the park"
                value={address}
                onChange={(e) => setAddress(e.target.value)}
              />
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 pt-6 border-t border-gray-100">
            {/* Location Section */}
            <div>
              <label className="block text-sm font-bold text-gray-900 mb-2">
                GPS Location <span className="text-red-500">*</span>
              </label>
              <p className="text-xs text-gray-500 mb-4">Required to pinpoint the exact issue location for responders.</p>
              
              <div className="flex flex-col gap-3">
                <button 
                  type="button"
                  onClick={getGPS}
                  className={`flex items-center justify-center gap-3 px-6 py-4 rounded-2xl font-bold transition-all border-2 ${
                    location 
                      ? "bg-green-50 border-green-200 text-green-700 hover:bg-green-100" 
                      : "bg-white border-gray-200 text-gray-800 hover:border-risklens-primary hover:text-risklens-primary shadow-sm"
                  }`}
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" /><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
                  {locating ? "Locating..." : location ? "Location Captured" : "Capture Location"}
                </button>
                
                {location && (
                  <div className="flex items-center gap-2 text-sm text-green-700 font-medium px-2">
                    <span className="relative flex h-2.5 w-2.5">
                      <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                      <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-green-500"></span>
                    </span>
                    {location.lat.toFixed(5)}, {location.lng.toFixed(5)}
                  </div>
                )}
              </div>
            </div>

            {/* Evidence Section */}
            <div>
              <label className="block text-sm font-bold text-gray-900 mb-2">Evidence <span className="text-gray-400 font-normal">(Optional)</span></label>
              <p className="text-xs text-gray-500 mb-4">Upload an image, video, or audio recording of the issue.</p>
              
              <div className="relative group">
                <input 
                  type="file" 
                  accept="image/*,video/*,audio/*"
                  onChange={(e) => setFile(e.target.files ? e.target.files[0] : null)}
                  className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
                />
                <div className={`flex flex-col items-center justify-center p-6 border-2 border-dashed rounded-2xl transition-all text-center h-full min-h-[120px] ${
                  file ? "border-risklens-primary bg-orange-50/50" : "border-gray-300 bg-gray-50/50 group-hover:border-risklens-primary group-hover:bg-orange-50/20"
                }`}>
                  {file ? (
                    <div className="flex flex-col items-center gap-2">
                      <svg className="w-8 h-8 text-risklens-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      <span className="text-sm font-semibold text-gray-900 break-all px-4">{file.name}</span>
                      <span className="text-xs text-gray-500">Click to replace</span>
                    </div>
                  ) : (
                    <div className="flex flex-col items-center gap-2">
                      <svg className="w-8 h-8 text-gray-400 group-hover:text-risklens-primary transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
                      </svg>
                      <span className="text-sm font-medium text-gray-600"><span className="text-risklens-primary font-bold">Click to upload</span> or drag and drop</span>
                      <span className="text-xs text-gray-400">SVG, PNG, JPG or MP4 (max. 10MB)</span>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>

          <div className="pt-8 mt-8 border-t border-gray-100">
            <button 
              type="submit" 
              disabled={analyzing}
              className="w-full relative overflow-hidden group bg-risklens-dark hover:bg-black text-white text-lg font-bold py-5 px-8 rounded-2xl flex items-center justify-center gap-3 transition-all shadow-lg shadow-gray-200 hover:shadow-xl disabled:opacity-70 disabled:cursor-not-allowed transform hover:-translate-y-0.5"
            >
              <div className="absolute inset-0 w-full h-full bg-gradient-to-r from-risklens-primary to-orange-500 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
              
              <span className="relative flex items-center gap-2">
                {analyzing ? (
                  <>
                    <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                    AI is Analyzing Evidence...
                  </>
                ) : (
                  <>
                    Analyze & Proceed
                    <svg className="w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 5l7 7m0 0l-7 7m7-7H3" /></svg>
                  </>
                )}
              </span>
            </button>
            <p className="text-center text-xs text-gray-400 mt-4">
              By submitting, you agree to our Terms of Service and Privacy Policy.
            </p>
          </div>
        </form>
      </div>
    </div>
  );
}
