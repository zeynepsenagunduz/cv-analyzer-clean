import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
export default function CardForCourses({ title, link }) {
  return (
    <div className="w-full bg-gradient-to-r from-orange-50 to-amber-50 border-2 border-orange-200 flex flex-col justify-center items-center text-xl p-6 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-200 transform hover:scale-[1.01]">
      <div className="w-full flex justify-between items-center">
        <div className="flex items-center gap-3 flex-1">
          <svg className="w-8 h-8 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
          </svg>
          <span className="text-gray-800 font-semibold">{title}</span>
        </div>
        <button
          onClick={() => {
            window.open(link, '_blank');
          }}
          type="submit"
          className="flex items-center gap-2 text-white bg-gradient-to-r from-orange-500 to-orange-600 hover:from-orange-600 hover:to-orange-700 focus:ring-4 focus:outline-none focus:ring-orange-300 font-semibold rounded-xl text-sm px-6 py-3 shadow-lg hover:shadow-xl transition-all duration-200 transform hover:scale-105"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
          </svg>
          Kursa Git
        </button>
      </div>
    </div>
  );
}
