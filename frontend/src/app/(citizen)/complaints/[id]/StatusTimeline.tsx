import React from "react";

export default function StatusTimeline({ status, events }: { status: string, events?: any[] }) {
  // A mapping of statuses to display labels
  const steps = [
    { key: "SUBMITTED", label: "Complaint Submitted" },
    { key: "ASSIGNED", label: "Routed to Department" },
    { key: "IN_PROGRESS", label: "Work In Progress" },
    { key: "RESOLVED", label: "Resolution Submitted" },
    { key: "AWAITING_FEEDBACK", label: "Awaiting Your Feedback" },
    { key: "CLOSED", label: "Closed" },
    { key: "REOPENED", label: "Reopened" }
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

  const getStepEvent = (stepKey: string) => {
    if (!events) return null;
    // Find the latest event for this transition
    const matchedEvents = events.filter(e => e.to_status === stepKey);
    if (matchedEvents.length > 0) {
      return matchedEvents[matchedEvents.length - 1]; // Return the most recent one
    }
    return null;
  };

  return (
    <div className="space-y-6">
      {steps.map((step, idx) => {
        const s = getStepStatus(step.key);
        if (s === "pending" && status !== "AWAITING_FEEDBACK" && step.key === "CLOSED") return null;
        if (s === "pending" && step.key === "REOPENED") return null;

        const event = getStepEvent(step.key);

        return (
          <div key={step.key} className="flex gap-4 items-start">
            <div className="flex flex-col items-center">
              <div className={`w-8 h-8 rounded-full flex items-center justify-center font-bold text-sm ${
                s === "completed" ? "bg-risklens-primary text-white shadow-[0_0_10px_rgba(255,107,0,0.4)]" :
                s === "active" ? "bg-orange-500 text-white ring-4 ring-risklens-primary/20" :
                "bg-slate-800 text-slate-500"
              }`}>
                {s === "completed" ? "✓" : s === "active" ? "●" : "○"}
              </div>
              {idx < steps.length - 1 && (
                <div className={`w-1 h-12 mt-2 ${s === "completed" ? "bg-risklens-primary shadow-[0_0_10px_rgba(255,107,0,0.4)]" : "bg-slate-800"}`} />
              )}
            </div>
            <div className="pt-1">
              <h4 className={`font-bold ${s === "pending" ? "text-slate-500" : "text-white"}`}>
                {step.label}
              </h4>
              {event && (
                <p className="text-xs text-slate-400 mt-1">
                  {new Date(event.changed_at).toLocaleString()}
                </p>
              )}
              {s === "active" && !event && <p className="text-sm text-risklens-primary mt-1 font-semibold">Current Status</p>}
            </div>
          </div>
        );
      })}
    </div>
  );
}
