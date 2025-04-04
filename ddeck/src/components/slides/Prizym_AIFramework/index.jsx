import React from 'react';

import CoverSlide from './CoverSlide';
import LensFramework from './LensFramework';
import TechArch from './TechArch';
import TechStack from './TechStack';
import TechRoadmap from './TechRoadmap';
import G2M from './G2M';
import CompetitiveLandscape from './CompetitiveLandscape';
import Commercialization from './Commercialization';
import ProjectGovernance from './ProjectGovernance';
import ProjectRoadmap from './ProjectRoadmap';
import ROIAnalysis from './ROIAnalysis';
import RiskManagement from './RiskManagement';
import ProjectAnalysis from './ProjectAnalysis';
import DomainDeepDive from './DomainDeepDive';
import PerformanceAnalysis from './PerformanceAnalysis';
import RealTimeAnalysis from './RealTimeAnalysis';
import PlanAnalysis from './PlanAnalysis';

const SlideLibrary = [
  { name: 'CoverSlide', component: () => <CoverSlide slideNumber={1} /> },
  { name: 'LensFramework', component: () => <LensFramework slideNumber={2} /> },
  { name: 'TechArch', component: () => <TechArch slideNumber={3} /> },
  { name: 'TechStack', component: () => <TechStack slideNumber={4} /> },
  { name: 'TechRoadmap', component: () => <TechRoadmap slideNumber={5} /> },
  { name: 'G2M', component: () => <G2M slideNumber={6} /> },
  { name: 'CompetitiveLandscape', component: () => <CompetitiveLandscape slideNumber={7} /> },
  { name: 'Commercialization', component: () => <Commercialization slideNumber={8} /> },
  { name: 'ProjectGovernance', component: () => <ProjectGovernance slideNumber={9} /> },
  { name: 'ProjectRoadmap', component: () => <ProjectRoadmap slideNumber={10} /> },
  { name: 'ROIAnalysis', component: () => <ROIAnalysis slideNumber={11} /> },
  { name: 'RiskManagement', component: () => <RiskManagement slideNumber={12} /> },
  { name: 'ProjectAnalysis', component: () => <ProjectAnalysis slideNumber={13} /> },
  { name: 'DomainDeepDive', component: () => <DomainDeepDive slideNumber={14} /> },
  { name: 'PerformanceAnalysis', component: () => <PerformanceAnalysis slideNumber={15} /> },
  { name: 'RealTimeAnalysis', component: () => <RealTimeAnalysis slideNumber={16} /> },
  { name: 'PlanAnalysis', component: () => <PlanAnalysis slideNumber={17} /> },
];

export default SlideLibrary;
