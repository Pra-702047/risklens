import React from 'react';

interface ClassificationPreviewProps {
  predictedCategory: string;
  confidence: number;
  reasonCodes: string[];
  reviewStatus: string;
  onConfirm: () => void;
  onChangeRequest: () => void;
}

export default function ClassificationPreview({
  predictedCategory,
  confidence,
  reasonCodes,
  reviewStatus,
  onConfirm,
  onChangeRequest
}: ClassificationPreviewProps) {
  
  const getConfidenceBadge = () => {
    if (confidence >= 0.8) return <span className="bg-green-100 text-green-800 text-xs px-2 py-1 rounded-full font-bold uppercase">High Confidence</span>;
    if (confidence >= 0.6) return <span className="bg-yellow-100 text-yellow-800 text-xs px-2 py-1 rounded-full font-bold uppercase">Medium Confidence</span>;
    return <span className="bg-red-100 text-red-800 text-xs px-2 py-1 rounded-full font-bold uppercase">Low Confidence</span>;
  };

  return (
    <div className="border border-orange-100 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] bg-orange-50/30 p-8 rounded-2xl shadow-sm mb-8 relative overflow-hidden">
      {/* Decorative AI Radar rings */}
      <div className="absolute -top-24 -right-24 w-64 h-64 border-[1px] border-orange-200 rounded-full opacity-50"></div>
      <div className="absolute -top-12 -right-12 w-40 h-40 border-[1px] border-orange-300 rounded-full opacity-50"></div>
      
      <div className="relative z-10 flex justify-between items-start mb-6">
        <div>
          <h2 className="text-xs font-black text-risklens-primary uppercase tracking-widest mb-2 flex items-center gap-2">
            <svg className="w-4 h-4 animate-spin-slow" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 10l-2 1m0 0l-2-1m2 1v2.5M20 7l-2 1m2-1l-2-1m2 1v2.5M14 4l-2-1-2 1M4 7l2-1M4 7l2 1M4 7v2.5M12 21l-2-1m2 1l2-1m-2 1v-2.5M6 18l2-1v-2.5M18 18l-2-1v-2.5" /></svg>
            AI Categorization Analysis
          </h2>
          <div className="text-3xl font-black text-risklens-dark flex items-center gap-4">
            {predictedCategory.replace(/_/g, ' ')}
            {getConfidenceBadge()}
          </div>
        </div>
      </div>

      <div className="relative z-10 mb-8 bg-white/60 p-4 rounded-xl border border-white">
        <h3 className="text-xs font-bold text-gray-500 uppercase tracking-wider mb-2">Detection Factors</h3>
        <ul className="list-disc list-inside text-sm text-gray-700 space-y-1 font-medium">
          {reasonCodes && reasonCodes.length > 0 ? (
            reasonCodes.map((code, idx) => (
              <li key={idx}>{code.replace(/_/g, ' ').toLowerCase()}</li>
            ))
          ) : (
            <li>No specific reasons extracted.</li>
          )}
        </ul>
      </div>
      
      {reviewStatus === "HUMAN_REVIEW" && (
        <div className="relative z-10 bg-amber-50 text-amber-800 p-4 rounded-xl text-sm mb-6 border border-amber-200 font-medium flex gap-3 items-start">
          <svg className="w-5 h-5 text-amber-600 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
          <div>
            <strong>Manual Override Recommended:</strong> The AI confidence score is below the operational threshold. Please verify the category.
          </div>
        </div>
      )}

      <div className="relative z-10 flex gap-4 items-center border-t border-orange-100 pt-6">
        <span className="font-bold text-gray-700 mr-2">Is this correct?</span>
        <button 
          onClick={onConfirm}
          className="btn-primary"
        >
          ✓ Yes, Correct
        </button>
        <button 
          onClick={onChangeRequest}
          className="btn-secondary"
        >
          Change Category
        </button>
      </div>
    </div>
  );
}
