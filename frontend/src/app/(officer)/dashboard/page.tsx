"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";

export default function OfficerDashboard() {
  const [complaints, setComplaints] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filterStatus, setFilterStatus] = useState("ALL");
  const [filterPriority, setFilterPriority] = useState("ALL");
  const router = useRouter();

  const filteredComplaints = complaints.filter((c: any) => {
    if (filterStatus !== "ALL" && c.status !== filterStatus) return false;
    if (filterPriority !== "ALL" && c.priority !== filterPriority) return false;
    return true;
  });

  useEffect(() => {
    const fetchQueue = async () => {
      const token = localStorage.getItem("officer_token");
      if (!token) {
        router.push("/login");
        return;
      }

      try {
        const res = await fetch("http://localhost:8000/officer/complaints/", {
          headers: {
            "Authorization": `Bearer ${token}`
          }
        });
        
        if (res.ok) {
          const data = await res.json();
          setComplaints(data);
        } else if (res.status === 401 || res.status === 403) {
          router.push("/login");
        }
      } catch (err) {
        console.error("Failed to fetch queue", err);
      } finally {
        setLoading(false);
      }
    };

    fetchQueue();
  }, [router]);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-200">
      <header className="bg-slate-900 border-b border-slate-800 p-4">
        <div className="container mx-auto flex justify-between items-center">
          <h1 className="text-xl font-bold text-white">RiskLens <span className="text-red-500">Operations</span></h1>
          <div className="flex gap-4">
            <span className="text-sm text-slate-400">Department Queue</span>
            <button 
              onClick={() => { localStorage.removeItem("officer_token"); router.push("/login"); }}
              className="text-sm text-slate-400 hover:text-white"
            >
              Logout
            </button>
          </div>
        </div>
      </header>

      <main className="container mx-auto py-8 px-4">
        {/* KPIs */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-slate-900 p-6 rounded-xl border border-slate-800">
            <div className="text-slate-400 text-sm font-medium mb-1">Open Issues</div>
            <div className="text-3xl font-bold text-white">{complaints.length}</div>
          </div>
          <div className="bg-slate-900 p-6 rounded-xl border border-slate-800">
            <div className="text-slate-400 text-sm font-medium mb-1">P0 / P1 Critical</div>
            <div className="text-3xl font-bold text-red-500">
              {complaints.filter((c: any) => c.priority === "P0" || c.priority === "P1").length}
            </div>
          </div>
          <div className="bg-slate-900 p-6 rounded-xl border border-slate-800">
            <div className="text-slate-400 text-sm font-medium mb-1">SLA Risk</div>
            <div className="text-3xl font-bold text-orange-500">0</div>
          </div>
          <div className="bg-slate-900 p-6 rounded-xl border border-slate-800">
            <div className="text-slate-400 text-sm font-medium mb-1">SLA Breached</div>
            <div className="text-3xl font-bold text-rose-600">0</div>
          </div>
        </div>

        {/* Filters */}
        <div className="flex gap-4 mb-4">
          <select 
            className="bg-slate-800 text-white border border-slate-700 rounded-md p-2 text-sm"
            onChange={(e) => setFilterStatus(e.target.value)}
            value={filterStatus}
          >
            <option value="ALL">All Statuses</option>
            <option value="ASSIGNED">Assigned</option>
            <option value="IN_PROGRESS">In Progress</option>
            <option value="RESOLVED">Resolved</option>
          </select>

          <select 
            className="bg-slate-800 text-white border border-slate-700 rounded-md p-2 text-sm"
            onChange={(e) => setFilterPriority(e.target.value)}
            value={filterPriority}
          >
            <option value="ALL">All Priorities</option>
            <option value="P0">P0 - Critical</option>
            <option value="P1">P1 - High</option>
            <option value="P2">P2 - Medium</option>
            <option value="P3">P3 - Low</option>
          </select>
        </div>

        {/* Data Table */}
        <div className="bg-slate-900 rounded-xl border border-slate-800 overflow-hidden">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-slate-950 border-b border-slate-800 text-sm font-medium text-slate-400">
                <th className="p-4">Priority</th>
                <th className="p-4">Category</th>
                <th className="p-4">Location</th>
                <th className="p-4">Status</th>
                <th className="p-4">Action</th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr><td colSpan={5} className="p-8 text-center text-slate-500">Loading queue...</td></tr>
              ) : filteredComplaints.length === 0 ? (
                <tr><td colSpan={5} className="p-8 text-center text-slate-500">No complaints match the selected filters.</td></tr>
              ) : (
                filteredComplaints.map((c: any) => (
                  <tr key={c.id} className="border-b border-slate-800 hover:bg-slate-800/50 transition-colors">
                    <td className="p-4">
                      <span className={`px-2 py-1 rounded text-xs font-bold ${
                        c.priority === "P0" ? "bg-red-500/20 text-red-400" :
                        c.priority === "P1" ? "bg-orange-500/20 text-orange-400" :
                        "bg-slate-700 text-slate-300"
                      }`}>
                        {c.priority || "P3"}
                      </span>
                    </td>
                    <td className="p-4 font-medium">
                      {c.category === "UNKNOWN" || !c.category ? (
                        <span className="text-yellow-500 flex items-center gap-1">
                          <span className="w-2 h-2 rounded-full bg-yellow-500"></span> Uncategorized
                        </span>
                      ) : (
                        c.category
                      )}
                    </td>
                    <td className="p-4 text-sm text-slate-400 truncate max-w-xs">{c.address}</td>
                    <td className="p-4">
                      <span className="text-xs uppercase font-medium text-slate-400">{c.status}</span>
                    </td>
                    <td className="p-4">
                      <Link href={`/incidents/${c.id}`} className="text-sm font-medium text-blue-400 hover:text-blue-300">
                        View Details →
                      </Link>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </main>
    </div>
  );
}
