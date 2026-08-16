"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";

export default function AIMonitoring() {
  const [data, setData] = useState<any>(null);
  const router = useRouter();

  useEffect(() => {
    const fetchAIStats = async () => {
      const token = localStorage.getItem("officer_token");
      if (!token) return router.push("/login");

      try {
        const res = await fetch("http://localhost:8000/admin/analytics/ai", {
          headers: { "Authorization": `Bearer ${token}` }
        });
        if (res.ok) {
          setData(await res.json());
        }
      } catch (err) {
        console.error(err);
      }
    };
    fetchAIStats();
  }, [router]);

  if (!data) return <div className="min-h-screen bg-slate-950 p-8 text-white">Loading AI Telemetry...</div>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-200">
      <header className="bg-slate-900 border-b border-slate-800 p-4">
        <div className="container mx-auto flex justify-between items-center">
          <h1 className="text-xl font-bold text-white">RiskLens <span className="text-purple-500">AI Control Center</span></h1>
          <nav className="flex gap-6 text-sm font-medium text-slate-400">
            <Link href="/command-center" className="hover:text-white">Overview</Link>
            <Link href="/live-map" className="hover:text-white">Live Map</Link>
            <Link href="/analytics" className="hover:text-white">Analytics</Link>
            <Link href="/ai-monitoring" className="text-white">AI Monitoring</Link>
          </nav>
        </div>
      </header>

      <main className="container mx-auto py-8 px-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <div className="bg-slate-900 p-6 rounded-xl border border-slate-800">
            <div className="text-slate-400 text-sm font-medium uppercase tracking-wider mb-2">Human Override Rate</div>
            <div className="text-4xl font-bold text-white">{data.override_rate.toFixed(1)}%</div>
            <p className="text-xs text-slate-500 mt-2">Percentage of AI predictions manually corrected by officers.</p>
          </div>
          <div className="bg-slate-900 p-6 rounded-xl border border-slate-800">
            <div className="text-slate-400 text-sm font-medium uppercase tracking-wider mb-2">Low Confidence Flags</div>
            <div className="text-4xl font-bold text-orange-500">{data.low_confidence_rate.toFixed(1)}%</div>
            <p className="text-xs text-slate-500 mt-2">Predictions scoring below the 80% confidence threshold.</p>
          </div>
        </div>

        <div className="bg-slate-900 rounded-xl border border-slate-800 overflow-hidden">
          <div className="p-4 border-b border-slate-800 bg-slate-950/50">
            <h2 className="font-bold text-white">AI Category Accuracy / Agreement</h2>
          </div>
          <table className="w-full text-left border-collapse text-sm">
            <thead>
              <tr className="bg-slate-950 text-slate-400 border-b border-slate-800">
                <th className="p-4 font-medium">Category</th>
                <th className="p-4 font-medium">Agreement Rate</th>
                <th className="p-4 font-medium">Status</th>
              </tr>
            </thead>
            <tbody>
              {data.category_accuracy.map((cat: any, idx: number) => (
                <tr key={idx} className="border-b border-slate-800/50 hover:bg-slate-800/30">
                  <td className="p-4 font-medium">{cat.category}</td>
                  <td className="p-4">
                    <div className="flex items-center gap-3">
                      <span className="w-12 text-right">{cat.accuracy}%</span>
                      <div className="w-48 bg-slate-800 rounded-full h-2">
                        <div 
                          className={`h-2 rounded-full ${cat.accuracy > 90 ? 'bg-green-500' : cat.accuracy > 80 ? 'bg-orange-500' : 'bg-red-500'}`} 
                          style={{ width: `${cat.accuracy}%` }}
                        ></div>
                      </div>
                    </div>
                  </td>
                  <td className="p-4">
                    {cat.accuracy < 80 ? (
                      <span className="text-xs font-bold px-2 py-1 bg-red-500/20 text-red-400 rounded">INVESTIGATE</span>
                    ) : (
                      <span className="text-xs font-bold text-slate-500">STABLE</span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </main>
    </div>
  );
}
