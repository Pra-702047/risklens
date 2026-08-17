"use client";

import { useEffect, useState } from "react";
import dynamic from "next/dynamic";
import Link from "next/link";
import "leaflet/dist/leaflet.css";

// Dynamically import map components to avoid SSR issues with Leaflet
const MapContainer = dynamic(() => import("react-leaflet").then((mod) => mod.MapContainer), { ssr: false });
const TileLayer = dynamic(() => import("react-leaflet").then((mod) => mod.TileLayer), { ssr: false });
const Marker = dynamic(() => import("react-leaflet").then((mod) => mod.Marker), { ssr: false });
const Popup = dynamic(() => import("react-leaflet").then((mod) => mod.Popup), { ssr: false });

export default function LiveMap() {
  const [geoData, setGeoData] = useState<any>(null);

  useEffect(() => {
    const fetchGeoData = async () => {
      try {
        const token = localStorage.getItem("token") || localStorage.getItem("firebase_token");
        const headers: any = {};
        if (token) headers["Authorization"] = `Bearer ${token}`;
        
        const res = await fetch("http://localhost:8000/geo/incidents", { headers });
        if (res.ok) {
          const data = await res.json();
          setGeoData(data);
        }
      } catch (err) {
        console.error("Failed to load map data:", err);
      }
    };
    
    fetchGeoData();
    // Poll every 30 seconds for live updates
    const interval = setInterval(fetchGeoData, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="h-screen flex flex-col bg-slate-950 text-slate-200">
      <header className="bg-slate-900 border-b border-slate-800 p-4 shrink-0">
        <div className="container mx-auto flex justify-between items-center">
          <h1 className="text-xl font-bold text-white">RiskLens <span className="text-blue-500">Live Map</span></h1>
          <nav className="flex gap-6 text-sm font-medium text-slate-400">
            <Link href="/command-center" className="hover:text-white">Overview</Link>
            <Link href="/live-map" className="text-white">Live Map</Link>
            <Link href="/analytics" className="hover:text-white">Analytics</Link>
          </nav>
        </div>
      </header>

      <main className="flex-1 relative">
        {geoData && typeof window !== 'undefined' ? (
          <MapContainer 
            center={[21.1458, 79.0882]} 
            zoom={13} 
            className="w-full h-full z-0"
          >
            <TileLayer
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
              url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
            />
            {geoData.features.map((f: any, idx: number) => {
              // Note: Leaflet expects [lat, lng], GeoJSON is [lng, lat]
              const position: [number, number] = [f.geometry.coordinates[1], f.geometry.coordinates[0]];
              return (
                <Marker key={idx} position={position}>
                  <Popup>
                    <div className="font-sans text-sm">
                      <strong className="text-red-600 block mb-1">{f.properties.priority} - {f.properties.category}</strong>
                      Status: {f.properties.status}<br/>
                      ID: {f.properties.id}
                    </div>
                  </Popup>
                </Marker>
              );
            })}
          </MapContainer>
        ) : (
          <div className="w-full h-full flex items-center justify-center">Loading Map...</div>
        )}

        {/* Floating Legend / Filters */}
        <div className="absolute top-4 right-4 bg-slate-900/90 backdrop-blur border border-slate-800 p-4 rounded-xl z-10 w-64 shadow-2xl">
          <h3 className="font-bold text-white mb-3 text-sm">Map Layers</h3>
          <div className="space-y-2 text-sm text-slate-300">
            <label className="flex items-center gap-2">
              <input type="checkbox" defaultChecked className="accent-blue-500" /> Active Complaints
            </label>
            <label className="flex items-center gap-2">
              <input type="checkbox" defaultChecked className="accent-red-500" /> P0 / P1 Critical
            </label>
            <label className="flex items-center gap-2">
              <input type="checkbox" defaultChecked className="accent-orange-500" /> Incident Clusters
            </label>
            <label className="flex items-center gap-2">
              <input type="checkbox" className="accent-purple-500" /> Heatmap (Density)
            </label>
          </div>
        </div>
      </main>
    </div>
  );
}
