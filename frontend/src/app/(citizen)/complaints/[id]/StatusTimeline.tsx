import React from "react";

export default function StatusTimeline({ status, events }: { status: string, events?: any[] }) {
  // A mapping of statuses to display labels
  const steps = [
    { key: "SUBMITTED", label: "Complaint Submitted" },
    { key: "ROUTED", label: "Routed to Department" },
    { key: "ACKNOWLEDGE", label: "Officer Assigned" },
    { key: "IN_PROGRESS", label: "Work In Progress" },
    { key: "RESOLVED", label: "Resolution Submitted" },
    { key: "AWAITING_FEEDBACK", label: "Awaiting Your Feedback" },
    { key: "CLOSED", label: "Closed" }
  ];

  // Logic to determine if a step is completed, active, or pending
  const getStepStatus = (stepKey: string) => {
    if (status === stepKey) return "active";
    if (status === "CLOSED" || status === "REOPEN_LIMIT_REACHED") return "completed";
    
    const currentIndex = steps.findIndex(s => s.key === status);
    const stepIndex = steps.findIndex(s => s.key === stepKey);
    
    // Exception cases
    if (status === "REOPENED" && stepIndex <= 3) return "completed";
    if (status === "REOPENED" && stepKey === "IN_PROGRESS") return "active";
    
    if (currentIndex > stepIndex) return "completed";
    return "pending";
  };

  return (
    <div className="space-y-6">
      {steps.map((step, idx) => {
        const s = getStepStatus(step.key);
        if (s === "pending" && status !== "AWAITING_FEEDBACK" && step.key === "CLOSED") return null;

        return (
          <div key={step.key} className="flex gap-4 items-start">
            <div className="flex flex-col items-center">
              <div className={`w-8 h-8 rounded-full flex items-center justify-center font-bold text-sm ${
                s === "completed" ? "bg-green-500 text-white" :
                s === "active" ? "bg-blue-500 text-white ring-4 ring-blue-500/20" :
                "bg-slate-800 text-slate-500"
              }`}>
                {s === "completed" ? "✓" : s === "active" ? "●" : "○"}
              </div>
              {idx < steps.length - 1 && (
                <div className={`w-1 h-12 mt-2 ${s === "completed" ? "bg-green-500" : "bg-slate-800"}`} />
              )}
            </div>
            <div className="pt-1">
              <h4 className={`font-bold ${s === "pending" ? "text-slate-500" : "text-white"}`}>
                {step.label}
              </h4>
              {/* Optional: map events timestamp here if we have timeline data */}
              {s === "active" && <p className="text-sm text-slate-400 mt-1">Current Status</p>}
            </div>
          </div>
        );
      })}
    </div>
  );
}
