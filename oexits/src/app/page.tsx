"use client";

import { useState } from 'react';
import dynamic from 'next/dynamic';
import Image from 'next/image';
import {
  BarChartIcon,
  AlertTriangleIcon,
  ActivityIcon,
  TrophyIcon,
} from 'lucide-react';

// Use dynamic import to avoid server-side rendering issues with Recharts
const CompPlanAnalysisModal = dynamic(
  () => import('@/components/CompPlanAnalysisModal'),
  { ssr: false }
);

export default function Home() {
  // Your existing state
  const [form, setForm] = useState({
    name: '',
    email: '',
    org: '',
    file: null as File | null,
    consent: false,
  });
  
  // Add this state for modal
  const [showModal, setShowModal] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, type, checked, files } = e.target;
    setForm({
      ...form,
      [name]: type === 'checkbox' ? checked : type === 'file' ? files?.[0] || null : value,
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const data = new FormData();
    Object.entries(form).forEach(([key, value]) => {
      if (value !== null) data.append(key, value as string | Blob);
    });

    const res = await fetch('/api/submit', {
      method: 'POST',
      body: data,
    });

    if (res.ok) {
      alert('Submission received!');
    } else {
      alert('Something went wrong.');
    }
  };

  return (
    <main className="min-h-screen bg-gradient-to-b from-[#6451A0] via-[#4B6CA0] to-[#3E7A9E] text-white font-sans">
      <header className="bg-white text-[#5A369E] flex justify-between items-center px-6 py-4 shadow-md">
        <Image src="/logo.png" alt="ŒXITS Logo" width={144} height={48} />
        <nav className="space-x-6 text-sm font-semibold">
          <a href="#offer">Offer</a>
          <a href="#vendor">Vendor Guide</a>
          <a href="#upload">Upload</a>
          <a href="#contact">Contact</a>
        </nav>
      </header>

      <section className="text-center py-20 px-6">
        <h1 className="text-4xl font-bold mb-4">Free Compensation Plan Assessment</h1>
        <p className="text-lg mb-6 max-w-xl mx-auto">
          Upload your plan for a no-cost, expert-level SPM analysis.
        </p>
        <div className="flex justify-center gap-4">
          <a href="#upload" className="bg-white text-[#5A369E] font-semibold py-2 px-6 rounded shadow">
            Upload My Plan
          </a>
          <button 
            onClick={() => setShowModal(true)} 
            className="bg-transparent border border-white text-white font-semibold py-2 px-6 rounded shadow"
          >
            View Sample Analysis
          </button>
        </div>
      </section>
      
      {/* Modal will be rendered here when showModal is true */}
      {showModal && <CompPlanAnalysisModal onClose={() => setShowModal(false)} />}

      <section className="bg-white py-16 px-6" id="offer">
        <div className="max-w-5xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-[#5A369E] mb-3">What is included in the free assessment</h2>
            <div className="inline-flex items-center bg-gradient-to-r from-[#6451A0]/10 to-[#4B6CA0]/10 px-5 py-2 rounded-full">
              <span className="text-[#5A369E] font-medium">Built by SPM veterans</span>
              <span className="mx-3 text-gray-400">|</span>
              <span className="text-[#4B6CA0] font-medium">Enhanced with GenAI</span>
            </div>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {/* Feature 1: Plan Complexity Score */}
            <div className="bg-gradient-to-br from-white to-purple-50 rounded-xl shadow-md hover:shadow-lg transition-all duration-300 overflow-hidden group">
              <div className="p-6">
                <div className="flex items-start">
                  <div className="h-12 w-12 rounded-lg bg-gradient-to-br from-[#6451A0] to-[#4B6CA0] flex items-center justify-center text-white shadow-md group-hover:scale-110 transition-transform duration-300">
                    <BarChartIcon className="w-6 h-6" />
                  </div>
                  <div className="ml-4">
                    <h3 className="text-xl font-bold text-[#5A369E] mb-2">Plan Complexity Score</h3>
                    <p className="text-gray-600">See how your plan stacks up against industry norms with our proprietary complexity algorithm.</p>
                  </div>
                </div>
                <div className="mt-4 pl-16">
                  <div className="h-2 w-full bg-gray-200 rounded-full overflow-hidden">
                    <div className="h-full bg-gradient-to-r from-[#6451A0] to-[#4B6CA0] w-3/4"></div>
                  </div>
                  <div className="flex justify-between mt-1 text-xs text-gray-500">
                    <span>Simple</span>
                    <span>Complex</span>
                  </div>
                </div>
              </div>
            </div>
            
            {/* Feature 2: Red Flags & Risk Markers */}
            <div className="bg-gradient-to-br from-white to-purple-50 rounded-xl shadow-md hover:shadow-lg transition-all duration-300 overflow-hidden group">
              <div className="p-6">
                <div className="flex items-start">
                  <div className="h-12 w-12 rounded-lg bg-gradient-to-br from-[#6451A0] to-[#4B6CA0] flex items-center justify-center text-white shadow-md group-hover:scale-110 transition-transform duration-300">
                    <AlertTriangleIcon className="w-6 h-6" />
                  </div>
                  <div className="ml-4">
                    <h3 className="text-xl font-bold text-[#5A369E] mb-2">Red Flags & Risk Markers</h3>
                    <p className="text-gray-600">We&apos;ll flag structure issues, over leverage, and confusing logic patterns in your compensation plan.</p>
                  </div>
                </div>
                <div className="mt-4 pl-16 flex space-x-2">
                  <span className="inline-block px-3 py-1 bg-purple-100 text-[#6451A0] rounded-full text-xs font-medium">High leverage</span>
                  <span className="inline-block px-3 py-1 bg-indigo-100 text-[#5A369E] rounded-full text-xs font-medium">Structural</span>
                  <span className="inline-block px-3 py-1 bg-blue-100 text-[#4B6CA0] rounded-full text-xs font-medium">Compliance</span>
                </div>
              </div>
            </div>
            
            {/* Feature 3: Payout Curve Heatmap */}
            <div className="bg-gradient-to-br from-white to-purple-50 rounded-xl shadow-md hover:shadow-lg transition-all duration-300 overflow-hidden group">
              <div className="p-6">
                <div className="flex items-start">
                  <div className="h-12 w-12 rounded-lg bg-gradient-to-br from-[#6451A0] to-[#4B6CA0] flex items-center justify-center text-white shadow-md group-hover:scale-110 transition-transform duration-300">
                    <ActivityIcon className="w-6 h-6" />
                  </div>
                  <div className="ml-4">
                    <h3 className="text-xl font-bold text-[#5A369E] mb-2">Payout Curve Heatmap</h3>
                    <p className="text-gray-600">Visualize incentives by earnings tier with our color-coded performance distribution analysis.</p>
                  </div>
                </div>
                <div className="mt-4 pl-16 flex space-x-1">
                  {[10, 20, 30, 50, 70, 90, 100].map((value, index) => (
                    <div key={index} 
                      className="h-10 flex-1 rounded"
                      style={{
                        backgroundColor: `rgba(100, 81, 160, ${value/100})`,
                        height: `${Math.min(10 + value/2, 40)}px`
                      }}
                    ></div>
                  ))}
                </div>
              </div>
            </div>
            
            {/* Feature 4: Benchmark Comparison */}
            <div className="bg-gradient-to-br from-white to-purple-50 rounded-xl shadow-md hover:shadow-lg transition-all duration-300 overflow-hidden group">
              <div className="p-6">
                <div className="flex items-start">
                  <div className="h-12 w-12 rounded-lg bg-gradient-to-br from-[#6451A0] to-[#4B6CA0] flex items-center justify-center text-white shadow-md group-hover:scale-110 transition-transform duration-300">
                    <TrophyIcon className="w-6 h-6" />
                  </div>
                  <div className="ml-4">
                    <h3 className="text-xl font-bold text-[#5A369E] mb-2">Benchmark Comparison</h3>
                    <p className="text-gray-600">Compare to best practices in your industry with data from our proprietary compensation database.</p>
                  </div>
                </div>
                <div className="mt-4 pl-16">
                  <div className="flex items-center space-x-2 mb-2">
                    <div className="w-2 h-2 rounded-full bg-[#6451A0]"></div>
                    <div className="text-xs text-gray-600 flex-1">Your Plan</div>
                    <div className="w-24 h-2 bg-gray-200 rounded-full overflow-hidden">
                      <div className="h-full bg-[#6451A0] w-3/4"></div>
                    </div>
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="w-2 h-2 rounded-full bg-gray-400"></div>
                    <div className="text-xs text-gray-600 flex-1">Industry Average</div>
                    <div className="w-24 h-2 bg-gray-200 rounded-full overflow-hidden">
                      <div className="h-full bg-gray-400 w-1/2"></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div className="text-center mt-12">
            <a href="#upload" className="inline-block px-6 py-3 bg-gradient-to-r from-[#6451A0] to-[#4B6CA0] text-white font-medium rounded-lg shadow-md hover:shadow-lg transition-all duration-200">
              Get My Free Assessment
            </a>
          </div>
        </div>
      </section>

      <section id="vendor" className="bg-white text-[#333] py-16 px-6">
        <h2 className="text-2xl font-bold text-center mb-4">Download the 2025 SPM Vendor Guide</h2>
        <div className="max-w-4xl mx-auto">
          <div className="flex flex-col md:flex-row items-center bg-gradient-to-br from-purple-50 to-blue-50 rounded-xl overflow-hidden shadow-lg">
            <div className="md:w-2/5 p-6 flex justify-center">
              {/* Stylized document mockup */}
              <div className="relative w-48 h-64">
                <div className="absolute inset-0 bg-white shadow-md rounded-lg transform rotate-3 z-10"></div>
                <div className="absolute inset-0 bg-gradient-to-br from-[#6451A0] to-[#4B6CA0] shadow-lg rounded-lg transform -rotate-2 z-20 flex flex-col items-center justify-center text-white p-4">
                  <div className="border-b border-white/30 w-full mb-3 pb-2 text-center">
                    <h3 className="font-bold text-lg">2025 SPM</h3>
                    <h4 className="text-xl font-bold">VENDOR GUIDE</h4>
                  </div>
                  <div className="text-center mb-4 text-white/90 text-sm">
                    <p>Comprehensive analysis</p>
                    <p>Top 20 vendors reviewed</p>
                    <p>Hidden gems revealed</p>
                  </div>
                  <div className="mt-auto pt-2 border-t border-white/30 w-full text-center">
                    <p className="text-xs">ŒXITS Analysis</p>
                  </div>
                </div>
              </div>
            </div>
            <div className="md:w-3/5 p-6 md:p-8">
              <p className="text-lg mb-4">
                Your insider&apos;s look at the top players, hidden gems, and vendors to avoid.
              </p>
              <ul className="space-y-2 mb-6">
                <li className="flex items-center">
                  <span className="text-purple-600 mr-2">✓</span>
                  <span>Detailed vendor profiles with strengths & weaknesses</span>
                </li>
                <li className="flex items-center">
                  <span className="text-purple-600 mr-2">✓</span>
                  <span>Price vs. value comparison matrix</span>
                </li>
                <li className="flex items-center">
                  <span className="text-purple-600 mr-2">✓</span>
                  <span>Implementation timeline & complexity ratings</span>
                </li>
              </ul>
              <a
                href="/vendor-guide-2025.pdf"
                download
                className="inline-block bg-gradient-to-r from-[#6451A0] to-[#4B6CA0] text-white py-3 px-6 rounded-lg shadow-md hover:shadow-lg transition-all duration-200 font-medium"
              >
                Download the Guide
              </a>
            </div>
          </div>
        </div>
      </section>

      <section id="upload" className="bg-gradient-to-r from-[#6451A0] to-[#4B6CA0] text-white py-16 px-6">
        <h2 className="text-2xl font-bold text-center mb-6">Request Your Free Assessment</h2>
        <form onSubmit={handleSubmit} className="max-w-xl mx-auto space-y-4">
          <input name="name" type="text" placeholder="Name" onChange={handleChange} className="w-full p-3 border rounded" />
          <input name="email" type="email" placeholder="Email Address" onChange={handleChange} className="w-full p-3 border rounded" />
          <input name="org" type="text" placeholder="Organization" onChange={handleChange} className="w-full p-3 border rounded" />
          <input name="file" type="file" accept=".pdf,.docx,.xlsx" onChange={handleChange} className="w-full p-3 border rounded bg-white" />
          <label className="flex items-start space-x-2 text-sm">
            <input name="consent" type="checkbox" onChange={handleChange} />
            <span>I agree to be contacted by ŒXITS for follow-up insights or services.</span>
          </label>
          <button type="submit" className="bg-white text-[#5A369E] hover:bg-gray-100 py-2 px-6 rounded font-medium">
            Request My Free Assessment
          </button>
          <p className="text-xs text-white/80">
            We do not retain, store, or reuse your submitted plan. You will not be contacted unless you opt in.{' '}
            <a href="#" className="underline">View our Privacy Policy</a>.
          </p>
        </form>
      </section>

      <footer id="contact" className="bg-gradient-to-r from-[#6451A0] to-[#4B6CA0] text-white py-6 px-6 text-center">
        <Image src="/white_logo.png" alt="ŒXITS Logo" width={120} height={40} className="mx-auto mb-2" />
        <p className="text-sm">
          hello@oexits.com · <a href="#" className="underline">LinkedIn</a>
        </p>
        <p className="text-xs mt-2">© 2025 ŒXITS. All rights reserved.</p>
      </footer>
    </main>
  );
}