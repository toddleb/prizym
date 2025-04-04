import React, { useState } from 'react';
import SlideLibrary from './slides/Prizym_AIFramework';
import SlideControls from './SlideControls';
import SlideContainer from './SlideContainer';

const RunSlideShow = () => {
  const [currentSlide, setCurrentSlide] = useState(0);

  const handleNext = () => setCurrentSlide(prev => Math.min(prev + 1, SlideLibrary.length - 1));
  const handlePrev = () => setCurrentSlide(prev => Math.max(prev - 1, 0));

  const CurrentSlideComponent = SlideLibrary[currentSlide].component;

  return (
    <div className="w-full h-screen flex flex-col items-center justify-center bg-gray-100 overflow-hidden">
      <div className="w-[1280px] max-h-full overflow-auto">
        <SlideContainer>
          <CurrentSlideComponent />
        </SlideContainer>
      </div>

      <SlideControls
        currentSlide={currentSlide}
        totalSlides={SlideLibrary.length}
        onNext={handleNext}
        onPrev={handlePrev}
      />
    </div>
  );
};

export default RunSlideShow;
