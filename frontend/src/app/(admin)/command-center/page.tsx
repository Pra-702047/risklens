"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";

export default function CommandCenter() {
  const [data, setData] = useState<any>(null);
  const router = useRouter();

  useEffect(() => {
    const fetchOverview = async () => {
      const token = localStorage.getItem("officer_token");
      if (!token) return router.push("/login");

      try {
        const res = await fetch("http://localhost:8000/admin/analytics/overview", {
          headers: { "Authorization": `Bearer ${token}` }
        });
        if (res.ok) {
          setData(await res.json());
        }
      } catch (err) {
        console.error(err);
      }
    };
    fetchOverview();
  }, [router]);

  if (!data) return <div className="min-h-screen bg-slate-950 p-8 text-white">Loading Command Center...</div>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-200">
      <header className="bg-slate-900 border-b border-slate-800 p-4">
        <div className="container mx-auto flex justify-between items-center">
          <h1 className="text-xl font-bold text-white">RiskLens <span className="text-blue-500">Command Center</span></h1>
          <nav className="flex gap-6 text-sm font-medium text-slate-400">
            <Link href="/command-center" className="text-white">Overview</Link>
            <Link href="/live-map" className="hover:text-white">Live Map</Link>
            <Link href="/analytics" className="hover:text-white">Analytics</Link>
            <Link href="/ai-monitoring" className="hover:text-white">AI Monitoring</Link>
          </nav>
        </div>
      </header>

      <main className="container mx-auto py-8 px-4">
        {/* Top KPIs */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-slate-900 p-6 rounded-xl border border-slate-800">
            <div className="text-slate-400 text-sm font-medium uppercase tracking-wider mb-2">Open Issues</div>
            <div className="text-4xl font-bold text-white">{data.open_complaints}</div>
          </div>
          <div className="bg-slate-900 p-6 rounded-xl border border-red-900/50 relative overflow-hidden">
            <div className="absolute top-0 right-0 w-16 h-16 bg-red-500/10 rounded-bl-full" />
            <div className="text-slate-400 text-sm font-medium uppercase tracking-wider mb-2">P0 / P1 Critical</div>
            <div className="text-4xl font-bold text-red-500">{data.critical_complaints}</div>
          </div>
          <div className="bg-slate-900 p-6 rounded-xl border border-orange-900/50">
            <div className="text-slate-400 text-sm font-medium uppercase tracking-wider mb-2">SLA Risk</div>
            <div className="text-4xl font-bold text-orange-500">{data.sla_risk}</div>
          </div>
          <div className="bg-slate-900 p-6 rounded-xl border border-rose-900/50">
            <div className="text-slate-400 text-sm font-medium uppercase tracking-wider mb-2">SLA Breached</div>
            <div className="text-4xl font-bold text-rose-600">{data.sla_breached}</div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          {/* Active Critical Incidents */}
          <div className="lg:col-span-2 bg-slate-900 rounded-xl border border-slate-800 overflow-hidden">
            <div className="p-4 border-b border-slate-800 bg-slate-950/50">
              <h2 className="font-bold text-white">Active Critical Exceptions (P0/P1)</h2>
            </div>
            <table className="w-full text-left border-collapse text-sm">
              <tbody>
                <tr className="border-b border-slate-800/50 hover:bg-slate-800/30">
                  <td className="p-4"><span className="px-2 py-1 bg-red-500/20 text-red-400 rounded text-xs font-bold">P0</span></td>
                  <td className="p-4 font-medium">Major Accident</td>
                  <td className="p-4 text-slate-400">Traffic Police</td>
                  <td className="p-4 text-orange-400 font-medium">SLA: 12m</td>
                </tr>
                <tr className="border-b border-slate-800/50 hover:bg-slate-800/30">
                  <td className="p-4"><span className="px-2 py-1 bg-red-500/20 text-red-400 rounded text-xs font-bold">P0</span></td>
                  <td className="p-4 font-medium">Road Collapse</td>
                  <td className="p-4 text-slate-400">PWD</td>
                  <td className="p-4 text-rose-500 font-medium">BREACHED</td>
                </tr>
              </tbody>
            </table>
          </div>

          {/* Department Workload */}
          <div className="bg-slate-900 rounded-xl border border-slate-800 overflow-hidden">
            <div className="p-4 border-b border-slate-800 bg-slate-950/50">
              <h2 className="font-bold text-white">Department Workload</h2>
            </div>
            <div className="p-6 space-y-6">
              <div>
                <div className="flex justify-between text-sm mb-2">
                  <span>Traffic Police</span>
                  <span className="text-slate-400">142</span>
                </div>
                <div className="w-full bg-slate-800 rounded-full h-2">
                  <div className="bg-blue-500 h-2 rounded-full" style={{ width: "85%" }}></div>
                </div>
              </div>
              <div>
                <div className="flex justify-between text-sm mb-2">
                  <span>NMC / Municipal</span>
                  <span className="text-slate-400">89</span>
                </div>
                <div className="w-full bg-slate-800 rounded-full h-2">
                  <div className="bg-indigo-500 h-2 rounded-full" style={{ width: "65%" }}></div>
                </div>
              </div>
              <div>
                <div className="flex justify-between text-sm mb-2">
                  <span>PWD (Roads)</span>
                  <span className="text-slate-400">34</span>
                </div>
                <div className="w-full bg-slate-800 rounded-full h-2">
                  <div className="bg-emerald-500 h-2 rounded-full" style={{ width: "30%" }}></div>
                </div>
              </div>
            </div>
          </div>

        </div>
      </main>
    </div>
  );
}
