import React, { useEffect, useState } from 'react';

export default function HeadHunterApplications() {
  const [loading, setLoading] = useState(true);
  const [topFive, setTopFive] = useState([]);
  const [applications, setApplications] = useState([]);
  const [userData, setUserData] = useState(null);

  useEffect(() => {
    const user = window.localStorage.getItem('userData');
    if (!user) {
      window.location.href = '/login';
      return;
    }
    
    const parsedUser = JSON.parse(user);
    setUserData(parsedUser);
    fetchApplications(parsedUser.userid);
  }, []);

  const fetchApplications = async (userid) => {
    try {
      const response = await fetch(`http://localhost:8000/api/headhunter/applications/${userid}`);
      const data = await response.json();
      setTopFive(data.top_five || []);
      setApplications(data.applications || []);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching applications:', error);
      setLoading(false);
    }
  };

  const clearLocalStorage = () => {
    window.localStorage.clear();
  };

  const navigateToPDF = (userid) => {
    window.open(`http://localhost:8000/static/cvs/${userid}.pdf`, '_blank');
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('tr-TR', { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (loading) {
    return (
      <div className="w-screen h-screen flex justify-center items-center bg-gradient-to-br from-gray-50 to-gray-100">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600 text-xl">Başvurular Yükleniyor...</p>
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
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <span className="font-bold">BAŞVURULAR</span>
        </div>
        
        <div className="flex flex-col gap-4 w-full px-4 mt-8">
          <button
            onClick={() => window.location.href = '/dashboard/headhunter'}
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
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            Başvurular
          </button>

          <button
            onClick={() => window.location.href = '/headhunter/profile'}
            className="w-full bg-white/10 hover:bg-white/20 rounded-xl px-4 py-3 text-sm font-semibold transition-all duration-200 text-left flex items-center gap-2"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
            Profilim
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div className="w-full h-full flex flex-col">
        {/* Navbar */}
        <div className="navbar w-full h-20 flex justify-between items-center pr-8 pl-8 bg-white shadow-md border-b border-gray-200">
          <span className="text-xl font-semibold text-gray-700">📊 İş İlanıma Gelen Başvurular</span>
          
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
          
          {/* Top 5 Section */}
          <div className="w-full max-w-5xl mx-auto mb-8">
            <h2 className="text-3xl font-bold text-gray-800 mb-2 flex items-center gap-3">
              <svg className="w-9 h-9 text-yellow-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
              </svg>
              Algoritma Önerisi - En İyi 5 Aday
            </h2>
            <p className="text-gray-600 mb-6">İş ilanınıza en çok eşleşen adaylar (başvuru durumu ile)</p>
            
            {topFive.length === 0 ? (
              <div className="bg-white rounded-2xl shadow-lg p-8 text-center">
                <p className="text-gray-600">Henüz hiç aday yok</p>
              </div>
            ) : (
              <div className="space-y-4">
                {topFive.map((candidate, index) => (
                  <div
                    key={index}
                    className="w-full p-6 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-200 transform hover:scale-[1.01] bg-gradient-to-r from-yellow-50 via-amber-50 to-orange-50 border-2 border-yellow-400"
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-4 flex-1">
                        {/* Rank Badge */}
                        <div className="w-12 h-12 rounded-full bg-gradient-to-br from-yellow-400 to-orange-500 flex items-center justify-center text-white text-xl font-bold shadow-lg">
                          {index + 1}
                        </div>

                        {/* Avatar */}
                        <div className="w-16 h-16 rounded-full flex items-center justify-center text-white text-2xl font-bold shadow-lg bg-gradient-to-br from-yellow-400 to-orange-500">
                          {candidate.username?.charAt(0).toUpperCase() || 'U'}
                        </div>

                        {/* User Info */}
                        <div className="flex-1">
                          <div className="flex items-center gap-2 mb-1">
                            <h3 className="text-xl font-bold text-gray-800">{candidate.username}</h3>
                            {candidate.has_applied ? (
                              <span className="bg-green-500 text-white text-xs font-bold px-3 py-1 rounded-full shadow-md flex items-center gap-1">
                                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                                </svg>
                                BAŞVURDU
                              </span>
                            ) : (
                              <span className="bg-red-500 text-white text-xs font-bold px-3 py-1 rounded-full shadow-md flex items-center gap-1">
                                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                                </svg>
                                BAŞVURMADI
                              </span>
                            )}
                          </div>
                          <p className="text-gray-600 flex items-center gap-2">
                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                            </svg>
                            {candidate.email}
                          </p>
                        </div>
                      </div>

                      {/* Score & CV Button */}
                      <div className="flex items-center gap-4">
                        <div className="text-center">
                          <p className="text-sm text-gray-600 font-semibold mb-1">Eşleşme</p>
                          <div className="text-3xl font-bold px-6 py-2 rounded-xl shadow-md bg-gradient-to-r from-yellow-400 to-orange-500 text-white">
                            {candidate.point}%
                          </div>
                        </div>

                        <button
                          onClick={() => navigateToPDF(candidate.userid)}
                          className="flex items-center gap-2 text-white bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 focus:ring-4 focus:outline-none focus:ring-green-300 font-semibold rounded-xl text-sm px-6 py-3 shadow-lg hover:shadow-xl transition-all duration-200 transform hover:scale-105"
                        >
                          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                          </svg>
                          CV Görüntüle
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* All Applications Section */}
          <div className="w-full max-w-5xl mx-auto mb-8">
            <h2 className="text-3xl font-bold text-gray-800 mb-2 flex items-center gap-3">
              <svg className="w-9 h-9 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              Tüm Başvurular ({applications.length} kişi)
            </h2>
            <p className="text-gray-600 mb-6">Başvuru tarihine göre sıralanmış</p>
            
            {applications.length === 0 ? (
              <div className="bg-white rounded-2xl shadow-lg p-8 text-center">
                <svg className="w-16 h-16 mx-auto text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
                </svg>
                <p className="text-gray-600 text-lg">Henüz başvuru yok</p>
              </div>
            ) : (
              <div className="space-y-4">
                {applications.map((app, index) => (
                  <div
                    key={index}
                    className="w-full p-6 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-200 transform hover:scale-[1.01] bg-white border-2 border-gray-200"
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-4 flex-1">
                        {/* Avatar */}
                        <div className="w-16 h-16 rounded-full flex items-center justify-center text-white text-2xl font-bold shadow-lg bg-gradient-to-br from-blue-500 to-purple-600">
                          {app.username?.charAt(0).toUpperCase() || 'U'}
                        </div>

                        {/* User Info */}
                        <div className="flex-1">
                          <h3 className="text-xl font-bold text-gray-800 mb-1">{app.username}</h3>
                          <p className="text-gray-600 flex items-center gap-2 mb-1">
                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                            </svg>
                            {app.email}
                          </p>
                          <p className="text-sm text-gray-500 flex items-center gap-2">
                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                            </svg>
                            {formatDate(app.applied_at)}
                          </p>
                        </div>
                      </div>

                      {/* Score & CV Button */}
                      <div className="flex items-center gap-4">
                        <div className="text-center">
                          <p className="text-sm text-gray-600 font-semibold mb-1">Eşleşme</p>
                          <div className="text-3xl font-bold px-6 py-2 rounded-xl shadow-md bg-gradient-to-r from-blue-500 to-blue-600 text-white">
                            {app.match_score}%
                          </div>
                        </div>

                        <button
                          onClick={() => navigateToPDF(app.userid)}
                          className="flex items-center gap-2 text-white bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 focus:ring-4 focus:outline-none focus:ring-green-300 font-semibold rounded-xl text-sm px-6 py-3 shadow-lg hover:shadow-xl transition-all duration-200 transform hover:scale-105"
                        >
                          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                          </svg>
                          CV Görüntüle
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

        </div>
      </div>
    </div>
  );
}
