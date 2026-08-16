"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, LineChart, Line } from 'recharts';

export default function AnalyticsDashboard() {
  // Mock Data for MVP
  const volumeData = [
    { name: 'Mon', volume: 120 },
    { name: 'Tue', volume: 150 },
    { name: 'Wed', volume: 180 },
    { name: 'Thu', volume: 140 },
    { name: 'Fri', volume: 200 },
    { name: 'Sat', volume: 250 },
    { name: 'Sun', volume: 190 },
  ];

  const slaData = [
    { name: 'Traffic', resolved_in_sla: 85, breached: 15 },
    { name: 'NMC', resolved_in_sla: 60, breached: 40 },
    { name: 'PWD', resolved_in_sla: 90, breached: 10 },
  ];

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
