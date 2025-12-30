import React, { useEffect, useState } from 'react';

export default function UserProfile() {
  const [loading, setLoading] = useState(true);
  const [profile, setProfile] = useState(null);
  const [userData, setUserData] = useState(null);

  useEffect(() => {
    const user = window.localStorage.getItem('userData');
    if (!user) {
      window.location.href = '/login';
      return;
    }
    
    const parsedUser = JSON.parse(user);
    setUserData(parsedUser);
    fetchProfile(parsedUser.userid);
  }, []);

  const fetchProfile = async (userid) => {
    try {
      const response = await fetch(`http://localhost:8000/api/user/profile/${userid}`);
      const data = await response.json();
      setProfile(data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching profile:', error);
      setLoading(false);
    }
  };

  const clearLocalStorage = () => {
    window.localStorage.clear();
  };

  if (loading) {
    return (
      <div className="w-screen h-screen flex justify-center items-center bg-gradient-to-br from-gray-50 to-gray-100">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600 text-xl">Profil Yükleniyor...</p>
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
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
          </svg>
          <span className="font-bold">PROFİL</span>
        </div>
        
        <div className="flex flex-col gap-4 w-full px-4 mt-8">
          <button
            onClick={() => window.location.href = '/dashboard/user'}
            className="w-full bg-white/10 hover:bg-white/20 rounded-xl px-4 py-3 text-sm font-semibold transition-all duration-200 text-left flex items-center gap-2"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
            </svg>
            Ana Sayfa
          </button>
          
          <button
            onClick={() => window.location.href = '/analytics'}
            className="w-full bg-white/10 hover:bg-white/20 rounded-xl px-4 py-3 text-sm font-semibold transition-all duration-200 text-left flex items-center gap-2"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
            Analytics
          </button>

          <button
            className="w-full bg-white/30 rounded-xl px-4 py-3 text-sm font-semibold text-left flex items-center gap-2"
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
          <span className="text-xl font-semibold text-gray-700">👤 Profilim</span>
          
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
          
          {/* Profile Header */}
          <div className="w-full max-w-7xl mx-auto mb-8">
            <div className="bg-white rounded-2xl shadow-lg p-8">
              <div className="flex items-center gap-6">
                <div className="w-24 h-24 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-white text-4xl font-bold shadow-xl">
                  {profile?.user?.username?.charAt(0).toUpperCase()}
                </div>
                <div className="flex-1">
                  <h1 className="text-3xl font-bold text-gray-800 mb-2">{profile?.user?.username}</h1>
                  <p className="text-gray-600 text-lg mb-1">{profile?.user?.email}</p>
                  <div className="flex items-center gap-2">
                    <span className="px-3 py-1 bg-blue-100 text-blue-700 rounded-lg text-sm font-semibold">
                      {profile?.user?.role}
                    </span>
                    {profile?.user?.has_cv ? (
                      <span className="px-3 py-1 bg-green-100 text-green-700 rounded-lg text-sm font-semibold flex items-center gap-1">
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        CV Yüklü
                      </span>
                    ) : (
                      <span className="px-3 py-1 bg-red-100 text-red-700 rounded-lg text-sm font-semibold">
                        CV Yok
                      </span>
                    )}
                  </div>
                  
                  {/* CV Butonları */}
                  {profile?.user?.has_cv && (
                    <div className="mt-4 flex items-center gap-3">
                      
                      <button
                        onClick={() => {
                          const userid = JSON.parse(window.localStorage.getItem('userData')).userid;
                          const link = document.createElement('a');
                          link.href = `http://localhost:8000/api/user/cv/${userid}`;
                          link.download = `cv_${profile?.user?.username}.pdf`;
                          document.body.appendChild(link);
                          link.click();
                          document.body.removeChild(link);
                        }}
                        className="flex items-center gap-2 text-white bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800 focus:ring-4 focus:outline-none focus:ring-green-300 font-semibold rounded-xl text-sm px-6 py-3 shadow-lg hover:shadow-xl transition-all duration-200 transform hover:scale-105"
                      >
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                        </svg>
                         CV İndir
                      </button>
                    </div>
                  )}
                  
                </div>
              </div>
            </div>
          </div>

          {/* Stats Cards */}
          <div className="w-full max-w-7xl mx-auto mb-8">
            <h2 className="text-2xl font-bold text-gray-800 mb-4 flex items-center gap-2">
              <svg className="w-7 h-7 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
              İstatistiklerim
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="bg-white rounded-2xl shadow-lg p-6 hover:shadow-xl transition-all duration-200">
                <div className="flex items-center justify-between mb-4">
                  <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-blue-400 to-blue-600 flex items-center justify-center">
                    <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                  </div>
                </div>
                <h3 className="text-gray-600 text-sm font-semibold uppercase tracking-wide mb-2">Toplam Beceri</h3>
                <p className="text-4xl font-bold text-gray-800">{profile?.skill_count || 0}</p>
              </div>

              <div className="bg-white rounded-2xl shadow-lg p-6 hover:shadow-xl transition-all duration-200">
                <div className="flex items-center justify-between mb-4">
                  <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-green-400 to-green-600 flex items-center justify-center">
                    <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                    </svg>
                  </div>
                </div>
                <h3 className="text-gray-600 text-sm font-semibold uppercase tracking-wide mb-2">Talep Gören</h3>
                <p className="text-4xl font-bold text-gray-800">{profile?.skills_in_demand || 0}</p>
              </div>

              <div className="bg-white rounded-2xl shadow-lg p-6 hover:shadow-xl transition-all duration-200">
                <div className="flex items-center justify-between mb-4">
                  <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-purple-400 to-purple-600 flex items-center justify-center">
                    <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                    </svg>
                  </div>
                </div>
                <h3 className="text-gray-600 text-sm font-semibold uppercase tracking-wide mb-2">Pazar Kapsamı</h3>
                <p className="text-4xl font-bold text-gray-800">{profile?.market_coverage || 0}%</p>
              </div>
            </div>
          </div>

          {/* My Skills */}
          <div className="w-full max-w-7xl mx-auto mb-8">
            <h2 className="text-2xl font-bold text-gray-800 mb-4 flex items-center gap-2">
              <svg className="w-7 h-7 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
              </svg>
              Becerilerim
            </h2>
            
            <div className="bg-white rounded-2xl shadow-lg p-6">
              {profile?.skills_with_demand?.length > 0 ? (
                <div className="flex flex-wrap gap-3">
                  {profile.skills_with_demand.map((item, index) => (
                    <div 
                      key={index} 
                      className={`px-4 py-2 rounded-xl font-semibold shadow-md hover:shadow-lg transition-all duration-200 transform hover:scale-105 ${
                        item.in_demand 
                          ? 'bg-gradient-to-r from-green-500 to-emerald-600 text-white' 
                          : 'bg-gradient-to-r from-gray-400 to-gray-500 text-white'
                      }`}
                      title={item.in_demand ? `${item.demand_count} iş ilanında aranan` : 'Şu an talep görmüyor'}
                    >
                      {item.skill}
                      {item.in_demand && (
                        <span className="ml-2 text-xs opacity-80">✓</span>
                      )}
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-gray-500 text-center py-8">Henüz beceri eklenmemiş. CV yükleyin!</p>
              )}
            </div>
            
            {/* Legend */}
            <div className="mt-4 flex items-center gap-6 text-sm">
              <div className="flex items-center gap-2">
                <div className="w-4 h-4 rounded bg-gradient-to-r from-green-500 to-emerald-600"></div>
                <span className="text-gray-600">Talep Gören ({profile?.skills_in_demand || 0})</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-4 h-4 rounded bg-gradient-to-r from-gray-400 to-gray-500"></div>
                <span className="text-gray-600">Diğer ({(profile?.skill_count || 0) - (profile?.skills_in_demand || 0)})</span>
              </div>
            </div>
          </div>

          {/* Recommended Skills */}
          <div className="w-full max-w-7xl mx-auto mb-8">
            <h2 className="text-2xl font-bold text-gray-800 mb-4 flex items-center gap-2">
              <svg className="w-7 h-7 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
              Öğrenmen Gereken Top 5 Beceri
            </h2>
            
            <div className="bg-white rounded-2xl shadow-lg p-6">
              {profile?.recommended_skills?.length > 0 ? (
                <div className="space-y-4">
                  {profile.recommended_skills.map((item, index) => (
                    <div key={index} className="flex items-center justify-between p-4 bg-gradient-to-r from-orange-50 to-red-50 rounded-xl hover:shadow-md transition-all duration-200">
                      <div className="flex items-center gap-4">
                        <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-orange-500 to-red-500 text-white flex items-center justify-center font-bold text-lg shadow-md">
                          {index + 1}
                        </div>
                        <div>
                          <h3 className="font-bold text-gray-800 text-lg capitalize">{item.skill}</h3>
                          <p className="text-sm text-gray-600">
                            <span className="font-semibold text-orange-600">{item.demand}</span> iş ilanında aranan
                          </p>
                        </div>
                      </div>
                      <button className="px-6 py-2 bg-gradient-to-r from-orange-500 to-red-500 text-white rounded-xl font-semibold shadow-md hover:shadow-lg transition-all duration-200 transform hover:scale-105">
                        Kurs Bul
                      </button>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-gray-500 text-center py-8">Harika! Tüm önemli becerilere sahipsin! 🎉</p>
              )}
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}