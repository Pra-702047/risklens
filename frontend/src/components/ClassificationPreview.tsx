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
    <div className="border border-blue-200 bg-blue-50 p-6 rounded-xl shadow-sm mb-8">
      <div className="flex justify-between items-start mb-4">
        <div>
          <h2 className="text-sm font-semibold text-blue-600 uppercase tracking-wide mb-1">AI Suggested Category</h2>
          <div className="text-2xl font-bold text-gray-900 flex items-center gap-3">
            🟠 {predictedCategory.replace(/_/g, ' ')}
            {getConfidenceBadge()}
          </div>
        </div>
      </div>

      <div className="mb-6">
        <h3 className="text-sm font-semibold text-gray-700 mb-2">Why?</h3>
        <ul className="list-disc list-inside text-sm text-gray-600 space-y-1">
          {reasonCodes && reasonCodes.length > 0 ? (
            reasonCodes.map((code, idx) => (
              <li key={idx}>{code.replace(/_/g, ' ').toLowerCase()}</li>
            ))
          ) : (
            <li>No specific reasons provided.</li>
          )}
        </ul>
      </div>
      
      {reviewStatus === "HUMAN_REVIEW" && (
        <div className="bg-orange-100 text-orange-800 p-3 rounded-md text-sm mb-6 border border-orange-200">
          <strong>Note:</strong> The AI is not fully confident in this classification. Please review carefully.
        </div>
      )}

      <div className="flex gap-4 items-center border-t border-blue-200 pt-4">
        <span className="font-semibold text-gray-700 mr-2">Is this correct?</span>
        <button 
          onClick={onConfirm}
          className="bg-blue-600 text-white px-6 py-2 rounded-lg font-bold hover:bg-blue-700 transition-colors shadow-sm"
        >
          ✓ Yes, Correct
        </button>
        <button 
          onClick={onChangeRequest}
          className="bg-white border border-gray-300 text-gray-700 px-6 py-2 rounded-lg font-bold hover:bg-gray-50 transition-colors"
        >
          Change
        </button>
      </div>
    </div>
  );
}
