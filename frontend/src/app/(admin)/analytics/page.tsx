"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, LineChart, Line } from 'recharts';

export default function AnalyticsDashboard() {
  const [volumeData, setVolumeData] = useState([
    { name: 'Total', volume: 0 }
  ]);
  const [slaData, setSlaData] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        const token = localStorage.getItem("token") || localStorage.getItem("firebase_token") || localStorage.getItem("officer_token");
        const headers: any = {};
        if (token) headers["Authorization"] = `Bearer ${token}`;

        const res = await fetch("http://localhost:8000/admin/analytics/overview", { headers });
        if (res.ok) {
          const data = await res.json();
          setVolumeData([{ name: 'Total Volume', volume: data.total_volume }]);
          
          if (data.department_performance) {
            const formattedSla = Object.keys(data.department_performance).map(dept => ({
              name: dept,
              resolved_in_sla: data.department_performance[dept].resolved || 0,
              breached: data.department_performance[dept].open || 0 // mapping open to breached for MVP visualization
            }));
            setSlaData(formattedSla);
          }
        }
      } catch (err) {
        console.error("Failed to fetch analytics", err);
      } finally {
        setIsLoading(false);
      }
    };
    fetchAnalytics();
  }, []);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-200">
      <header className="bg-slate-900 border-b border-slate-800 p-4">
        <div className="container mx-auto flex justify-between items-center">
          <h1 className="text-xl font-bold text-white">RiskLens <span className="text-blue-500">Analytics</span></h1>
          <nav className="flex gap-6 text-sm font-medium text-slate-400">
            <Link href="/command-center" className="hover:text-white">Overview</Link>
            <Link href="/live-map" className="hover:text-white">Live Map</Link>
            <Link href="/analytics" className="text-white">Analytics</Link>
            <Link href="/ai-monitoring" className="hover:text-white">AI Monitoring</Link>
          </nav>
        </div>
      </header>

      <main className="container mx-auto py-8 px-4">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          
          {/* Complaint Volume Trend */}
          <div className="bg-slate-900 p-6 rounded-xl border border-slate-800">
            <h2 className="text-lg font-bold text-white mb-6">Weekly Complaint Volume</h2>
            <div className="h-72">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={volumeData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                  <XAxis dataKey="name" stroke="#64748b" />
                  <YAxis stroke="#64748b" />
                  <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#1e293b', color: '#fff' }} />
                  <Line type="monotone" dataKey="volume" stroke="#3b82f6" strokeWidth={3} dot={{ r: 4, fill: '#3b82f6' }} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Department SLA Performance */}
          <div className="bg-slate-900 p-6 rounded-xl border border-slate-800">
            <h2 className="text-lg font-bold text-white mb-6">SLA Compliance by Department</h2>
            <div className="h-72">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={slaData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                  <XAxis dataKey="name" stroke="#64748b" />
                  <YAxis stroke="#64748b" />
                  <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#1e293b', color: '#fff' }} />
                  <Legend />
                  <Bar dataKey="resolved_in_sla" name="Within SLA" stackId="a" fill="#10b981" />
                  <Bar dataKey="breached" name="Breached" stackId="a" fill="#ef4444" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

        </div>
      </main>
    </div>
  );
}
