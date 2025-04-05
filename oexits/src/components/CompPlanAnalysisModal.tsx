import React, { useRef, useEffect } from 'react';
import { X } from 'lucide-react';
import CompPlanAnalysis from './CompPlanAnalysis';

interface CompPlanAnalysisModalProps {
  onClose: () => void;
}

const CompPlanAnalysisModal: React.FC<CompPlanAnalysisModalProps> = ({ onClose }) => {
  const modalRef = useRef<HTMLDivElement>(null);
  
  // Handle ESC key press to close modal
  useEffect(() => {
    const handleEsc = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    window.addEventListener('keydown', handleEsc);
    return () => window.removeEventListener('keydown', handleEsc);
  }, [onClose]);

  // Handle clicking outside the modal to close
  const handleBackdropClick = (e: React.MouseEvent) => {
    if (modalRef.current && !modalRef.current.contains(e.target as Node)) {
      onClose();
    }
  };

  return (
    <div 
      className="fixed inset-0 z-50 overflow-auto bg-black/50 flex items-center justify-center p-4 animate-fadeIn" 
      onClick={handleBackdropClick}
    >
      <div 
        ref={modalRef} 
        className="bg-white rounded-lg shadow-xl w-full max-w-6xl max-h-[90vh] overflow-hidden"
      >
        {/* Header - Updated with gradient that matches main background */}
        <div className="flex justify-between items-center border-b p-4 bg-gradient-to-r from-[#6451A0] to-[#4B6CA0] text-white">
          <h2 className="text-xl font-bold">Sample Compensation Plan Analysis</h2>
          <button 
            onClick={onClose} 
            className="text-white hover:bg-white/20 rounded-full p-1 transition-colors"
            aria-label="Close modal"
          >
            <X className="w-6 h-6" />
          </button>
        </div>
        
        {/* Content */}
        <div className="overflow-y-auto max-h-[calc(90vh-8rem)]">
          {/* Import the detailed analysis component */}
          <CompPlanAnalysis />
        </div>
        
        {/* Footer */}
        <div className="border-t p-4 bg-gray-50 flex justify-between items-center">
          <p className="text-sm text-gray-500">
            This is a sample analysis. Upload your plan to receive a customized assessment.
          </p>
          <a 
            href="#upload" 
            onClick={onClose} 
            className="bg-gradient-to-r from-[#6451A0] to-[#4B6CA0] text-white py-2 px-4 rounded text-sm font-medium"
          >
            Upload My Plan
          </a>
        </div>
      </div>
    </div>
  );
};

export default CompPlanAnalysisModal;
