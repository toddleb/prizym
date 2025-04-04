import React from 'react';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid,
  Tooltip, Legend, ResponsiveContainer, AreaChart, Area, BarChart, Bar
} from 'recharts';

const ROIAnalysis = () => {
  const roiData = [
    { quarter: 'Q1', investment: 100, returns: 0, cumulative: -100 },
    { quarter: 'Q2', investment: 40, returns: 50, cumulative: -90 },
    { quarter: 'Q3', investment: 30, returns: 80, cumulative: -40 },
    { quarter: 'Q4', investment: 20, returns: 100, cumulative: 40 },
    { quarter: 'Q5', investment: 20, returns: 130, cumulative: 150 },
    { quarter: 'Q6', investment: 20, returns: 150, cumulative: 280 },
    { quarter: 'Q7', investment: 10, returns: 160, cumulative: 430 },
    { quarter: 'Q8', investment: 10, returns: 180, cumulative: 600 },
  ];

  const domainReturns = [
    { name: 'SPM', prizymRevenue: 35, kpmgRevenue: 65 },
    { name: 'Career Planning', prizymRevenue: 65, kpmgRevenue: 35 },
    { name: 'Lead Gen', prizymRevenue: 70, kpmgRevenue: 30 },
    { name: 'Workforce', prizymRevenue: 25, kpmgRevenue: 75 },
  ];

  const valueDrivers = [
    { name: 'Operational Efficiency', value: 35 },
    { name: 'Decision Quality', value: 25 },
    { name: 'Resource Optimization', value: 20 },
    { name: 'Time Savings', value: 15 },
    { name: 'Risk Reduction', value: 5 },
  ];

  return (
    <div className="w-full h-full bg-white p-4 font-sans flex flex-col">
      <h1 className="text-2xl font-bold text-center mb-4">ROI Model Visualization</h1>

      <div className="grid grid-cols-2 grid-rows-2 gap-4 flex-1 min-h-0">
        {/* Investment vs Returns */}
        <div className="border border-gray-300 rounded-lg p-3 bg-gray-50 flex flex-col">
          <h2 className="text-lg font-bold">Investment vs. Returns Timeline</h2>
          <p className="text-xs text-gray-600">Typical implementation ($000s)</p>
          <div className="flex-1 h-[220px]">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={roiData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="quarter" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Area dataKey="investment" stroke="#8884d8" fill="#8884d8" name="Investment" />
                <Area dataKey="returns" stroke="#82ca9d" fill="#82ca9d" name="Returns" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Cumulative ROI */}
        <div className="border border-gray-300 rounded-lg p-3 bg-gray-50 flex flex-col">
          <h2 className="text-lg font-bold">Cumulative ROI</h2>
          <p className="text-xs text-gray-600">Break-even at Q4 ($000s)</p>
          <div className="flex-1 h-[220px]">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={roiData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="quarter" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line dataKey="cumulative" stroke="#ff7300" name="Cumulative ROI" />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Revenue by Domain */}
        <div className="border border-gray-300 rounded-lg p-3 bg-gray-50 flex flex-col">
          <h2 className="text-lg font-bold">Revenue Distribution by Domain</h2>
          <p className="text-xs text-gray-600">Partner share (%)</p>
          <div className="flex-1 h-[220px]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={domainReturns}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="prizymRevenue" stackId="a" fill="#7B3FC4" name="Prizym %" />
                <Bar dataKey="kpmgRevenue" stackId="a" fill="#0073C6" name="KPMG %" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Value Drivers */}
        <div className="border border-gray-300 rounded-lg p-3 bg-gray-50 flex flex-col">
          <h2 className="text-lg font-bold">Value Drivers</h2>
          <p className="text-xs text-gray-600">Key ROI Factors (%)</p>
          <div className="flex-1 h-[220px]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart layout="vertical" data={valueDrivers}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" />
                <YAxis type="category" dataKey="name" width={120} />
                <Tooltip />
                <Legend />
                <Bar dataKey="value" fill="#F57C00" name="Contribution %" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ROIAnalysis;