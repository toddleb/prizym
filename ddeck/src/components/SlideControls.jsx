import React from 'react';
import { ChevronUp, ChevronDown } from 'lucide-react';

const SlideControls = ({ currentSlide, totalSlides, onNext, onPrev }) => (
  <div className="flex flex-col items-center space-y-2 fixed bottom-4 right-4">
    <button
      className="p-2 bg-gray-200 hover:bg-gray-300 rounded-full disabled:opacity-50"
      onClick={onPrev}
      disabled={currentSlide === 0}
    >
      <ChevronUp size={24} />
    </button>
    <span className="text-xs font-medium">
      Slide {currentSlide + 1} / {totalSlides}
    </span>
    <button
      className="p-2 bg-gray-200 hover:bg-gray-300 rounded-full disabled:opacity-50"
      onClick={onNext}
      disabled={currentSlide === totalSlides - 1}
    >
      <ChevronDown size={24} />
    </button>
  </div>
);

export default SlideControls;
