import React, { useEffect, useState, useRef } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  PointElement,
  LineElement,
} from 'chart.js';
import { Bar, Doughnut, Line } from 'react-chartjs-2';

// Register ChartJS components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  PointElement,
  LineElement
);

export default function AnalyticsDashboard() {
  const [loading, setLoading] = useState(true);
  const [overview, setOverview] = useState(null);
  const [trends, setTrends] = useState(null);
  
  useEffect(() => {
    if (!window.localStorage.getItem('userData')) {
      window.location.href = '/login';
    }
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async () => {
    try {
      // Fetch overview data
      const overviewRes = await fetch('http://localhost:8000/api/analytics/overview');
      const overviewData = await overviewRes.json();
      
      // Fetch skill trends
      const trendsRes = await fetch('http://localhost:8000/api/analytics/skill-trends');
      const trendsData = await trendsRes.json();
      
      setOverview(overviewData);
      setTrends(trendsData);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching analytics:', error);
      setLoading(false);
    }
  };

  const clearLocalStorage = () => {
    window.localStorage.clear();
  };

  // Chart data preparation
  const getTopSkillsChartData = () => {
    if (!overview?.top_skills) return null;
    
    const top10 = overview.top_skills.slice(0, 10);
    
    return {
      labels: top10.map(s => s.skill),
      datasets: [
        {
          label: 'CV Sayısı',
          data: top10.map(s => s.count),
          backgroundColor: 'rgba(59, 130, 246, 0.8)',
          borderColor: 'rgba(59, 130, 246, 1)',
          borderWidth: 2,
        },
      ],
    };
  };

  const getTrendingSkillsChartData = () => {
    if (!trends?.trending_skills) return null;
    
    const top10 = trends.trending_skills.slice(0, 10);
    
    return {
      labels: top10.map(s => s.skill),
      datasets: [
        {
          label: 'Talep',
          data: top10.map(s => s.demand),
          backgroundColor: [
            'rgba(255, 99, 132, 0.8)',
            'rgba(54, 162, 235, 0.8)',
            'rgba(255, 206, 86, 0.8)',
            'rgba(75, 192, 192, 0.8)',
            'rgba(153, 102, 255, 0.8)',
            'rgba(255, 159, 64, 0.8)',
            'rgba(199, 199, 199, 0.8)',
            'rgba(83, 102, 255, 0.8)',
            'rgba(255, 99, 255, 0.8)',
            'rgba(99, 255, 132, 0.8)',
          ],
          borderWidth: 2,
        },
      ],
    };
  };

  const getCategoryDistributionData = () => {
    if (!trends?.trending_skills) return null;
    
    const categories = {};
    trends.trending_skills.forEach(skill => {
      const cat = skill.category || 'other';
      categories[cat] = (categories[cat] || 0) + skill.demand;
    });
    
    return {
      labels: Object.keys(categories).map(k => k.charAt(0).toUpperCase() + k.slice(1)),
      datasets: [
        {
          label: 'Kategori Dağılımı',
          data: Object.values(categories),
          backgroundColor: [
            'rgba(59, 130, 246, 0.8)',
            'rgba(16, 185, 129, 0.8)',
            'rgba(245, 158, 11, 0.8)',
            'rgba(239, 68, 68, 0.8)',
            'rgba(139, 92, 246, 0.8)',
            'rgba(236, 72, 153, 0.8)',
          ],
          borderWidth: 2,
        },
      ],
    };
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
        labels: {
          font: {
            size: 12,
            weight: 'bold',
          },
        },
      },
      title: {
        display: false,
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          precision: 0,
        },
      },
    },
  };

  const doughnutOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'right',
        labels: {
          font: {
            size: 11,
          },
          padding: 10,
        },
      },
    },
  };

  if (loading) {
    return (
      <div className="w-screen h-screen flex justify-center items-center bg-gradient-to-br from-gray-50 to-gray-100">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600 text-xl">Analytics Yükleniyor...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="w-screen h-screen flex justify-start items-center bg-gradient-to-br from-gray-50 to-gray-100">
      {/* Sidebar */}
      <div className="sidebar w-64 h-full flex flex-col justify-start items-center text-white pt-9 text-2xl bg-gradient-to-b from-blue-700 to-blue-900 shadow-2xl">
        <div className="flex items-center gap-2 mb-8">
          <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
          <span className="font-bold">ANALYTİCS</span>
        </div>
        
        <div className="flex flex-col gap-4 w-full px-4 mt-8">
          <button
            onClick={() => {
              const userData = JSON.parse(window.localStorage.getItem('userData'));
              const role = userData?.role;
              if (role === 'headhunter') {
                window.location.href = '/dashboard/headhunter';
              } else {
                window.location.href = '/dashboard/user';
              }
            }}
            className="w-full bg-white/10 hover:bg-white/20 rounded-xl px-4 py-3 text-sm font-semibold transition-all duration-200 text-left flex items-center gap-2"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
            </svg>
            Ana Sayfa
          </button>
          
          <button
            className="w-full bg-white/30 rounded-xl px-4 py-3 text-sm font-semibold text-left flex items-center gap-2"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
            Analytics
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div className="w-full h-full flex flex-col">
        {/* Navbar */}
        <div className="navbar w-full h-20 flex justify-between items-center pr-8 pl-8 bg-white shadow-md border-b border-gray-200">
          <span className="text-xl font-semibold text-gray-700">📊 Analytics Dashboard</span>
          
          <div className="flex justify-center items-center gap-6">
            <button
              onClick={() => {
                clearLocalStorage();
                window.location.href = '/login';
              }}
              className="flex items-center gap-2 text-white bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 focus:ring-4 focus:outline-none focus:ring-red-300 font-semibold rounded-xl text-sm px-6 py-3 shadow-lg hover:shadow-xl transition-all duration-200 transform hover:scale-105"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
              Çıkış
            </button>
            <div className="w-12 h-12 rounded-full bg-gradient-to-br from-blue-400 to-purple-500 flex items-center justify-center shadow-lg">
              <img className="w-10 h-10 rounded-full object-cover" src="../../public/user.png" alt="User" />
            </div>
          </div>
        </div>

        {/* Main Content Area */}
        <div className="main w-full flex-1 flex flex-col justify-start items-start bg-gradient-to-br from-gray-50 to-gray-100 overflow-y-auto p-8">
          
          {/* Stats Grid */}
          <div className="w-full max-w-7xl mx-auto mb-8">
            <h2 className="text-3xl font-bold text-gray-800 mb-6 flex items-center gap-3">
              <svg className="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
              Genel İstatistikler
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {/* Total CVs */}
              <div className="bg-white rounded-2xl shadow-lg p-6 hover:shadow-xl transition-all duration-200 transform hover:scale-105">
                <div className="flex items-center justify-between mb-4">
                  <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-blue-400 to-blue-600 flex items-center justify-center">
                    <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                  </div>
                </div>
                <h3 className="text-gray-600 text-sm font-semibold uppercase tracking-wide mb-2">Toplam CV</h3>
                <p className="text-4xl font-bold text-gray-800">{overview?.total_cvs || 0}</p>
              </div>

              {/* Total Jobs */}
              <div className="bg-white rounded-2xl shadow-lg p-6 hover:shadow-xl transition-all duration-200 transform hover:scale-105">
                <div className="flex items-center justify-between mb-4">
                  <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-green-400 to-green-600 flex items-center justify-center">
                    <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                    </svg>
                  </div>
                </div>
                <h3 className="text-gray-600 text-sm font-semibold uppercase tracking-wide mb-2">Toplam İş İlanı</h3>
                <p className="text-4xl font-bold text-gray-800">{overview?.total_jobs || 0}</p>
              </div>

              {/* Total Matches */}
              <div className="bg-white rounded-2xl shadow-lg p-6 hover:shadow-xl transition-all duration-200 transform hover:scale-105">
                <div className="flex items-center justify-between mb-4">
                  <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-purple-400 to-purple-600 flex items-center justify-center">
                    <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                    </svg>
                  </div>
                </div>
                <h3 className="text-gray-600 text-sm font-semibold uppercase tracking-wide mb-2">Toplam Eşleşme</h3>
                <p className="text-4xl font-bold text-gray-800">{overview?.total_matches || 0}</p>
              </div>

              {/* Average Score */}
              <div className="bg-white rounded-2xl shadow-lg p-6 hover:shadow-xl transition-all duration-200 transform hover:scale-105">
                <div className="flex items-center justify-between mb-4">
                  <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-orange-400 to-orange-600 flex items-center justify-center">
                    <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
                    </svg>
                  </div>
                </div>
                <h3 className="text-gray-600 text-sm font-semibold uppercase tracking-wide mb-2">Ortalama Skor</h3>
                <p className="text-4xl font-bold text-gray-800">{overview?.avg_match_score || 0}%</p>
              </div>
            </div>
          </div>

          {/* Charts Grid */}
          <div className="w-full max-w-7xl mx-auto mb-8">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Bar Chart - Top Skills in CVs */}
              <div className="bg-white rounded-2xl shadow-lg p-6">
                <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
                  <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                  CV'lerde En Popüler Beceriler
                </h3>
                <div className="h-80">
                  {getTopSkillsChartData() && (
                    <Bar data={getTopSkillsChartData()} options={chartOptions} />
                  )}
                </div>
              </div>

              {/* Doughnut Chart - Trending Skills */}
              <div className="bg-white rounded-2xl shadow-lg p-6">
                <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
                  <svg className="w-6 h-6 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 18.657A8 8 0 016.343 7.343S7 9 9 10c0-2 .5-5 2.986-7C14 5 16.09 5.777 17.656 7.343A7.975 7.975 0 0120 13a7.975 7.975 0 01-2.343 5.657z" />
                  </svg>
                  En Çok Aranan Beceriler
                </h3>
                <div className="h-80">
                  {getTrendingSkillsChartData() && (
                    <Doughnut data={getTrendingSkillsChartData()} options={doughnutOptions} />
                  )}
                </div>
              </div>

              {/* Category Distribution */}
              <div className="bg-white rounded-2xl shadow-lg p-6 lg:col-span-2">
                <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
                  <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z" />
                  </svg>
                  Kategori Dağılımı
                </h3>
                <div className="h-64">
                  {getCategoryDistributionData() && (
                    <Bar 
                      data={getCategoryDistributionData()} 
                      options={{
                        ...chartOptions,
                        indexAxis: 'y',
                      }} 
                    />
                  )}
                </div>
              </div>
            </div>
          </div>
          
        </div>
      </div>
    </div>
  );
}
