import React, { useEffect, useState } from 'react';

export default function HeadHunterProfile() {
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
      const response = await fetch(`http://localhost:8000/api/headhunter/profile/${userid}`);
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
          <div className="w-full max-w-4xl mx-auto mb-8">
            <div className="bg-white rounded-2xl shadow-lg p-8">
              <div className="flex items-center gap-6">
                <div className="w-24 h-24 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-white text-4xl font-bold shadow-xl">
                  {profile?.username?.charAt(0).toUpperCase()}
                </div>
                <div className="flex-1">
                  <h1 className="text-3xl font-bold text-gray-800 mb-2">{profile?.username}</h1>
                  <p className="text-gray-600 text-lg mb-1 flex items-center gap-2">
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                    </svg>
                    {profile?.email}
                  </p>
                  <div className="flex items-center gap-2 mt-2">
                    <span className="px-3 py-1 bg-purple-100 text-purple-700 rounded-lg text-sm font-semibold">
                      HeadHunter
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Job Post Status Card */}
          <div className="w-full max-w-4xl mx-auto mb-8">
            <h2 className="text-2xl font-bold text-gray-800 mb-4 flex items-center gap-2">
              <svg className="w-7 h-7 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
              İş İlanı Durumu
            </h2>
            
            <div className="bg-white rounded-2xl shadow-lg p-8">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <div className={`w-16 h-16 rounded-full flex items-center justify-center shadow-lg ${
                    profile?.has_jobpost 
                      ? 'bg-gradient-to-br from-green-400 to-emerald-500' 
                      : 'bg-gradient-to-br from-gray-400 to-gray-500'
                  }`}>
                    <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      {profile?.has_jobpost ? (
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                      ) : (
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                      )}
                    </svg>
                  </div>
                  <div>
                    <h3 className="text-xl font-bold text-gray-800">
                      {profile?.has_jobpost ? 'İş İlanı Aktif' : 'İş İlanı Yok'}
                    </h3>
                    <p className="text-gray-600">
                      {profile?.has_jobpost 
                        ? 'İş ilanınız yayında ve adaylarla eşleştiriliyor' 
                        : 'Henüz iş ilanı yüklemediniz'}
                    </p>
                  </div>
                </div>
                
                <div className={`px-6 py-3 rounded-xl font-bold shadow-md ${
                  profile?.has_jobpost
                    ? 'bg-green-100 text-green-700'
                    : 'bg-gray-100 text-gray-700'
                }`}>
                  {profile?.has_jobpost ? 'YAYINDA' : 'PASİF'}
                </div>
              </div>

              {!profile?.has_jobpost && (
                <div className="mt-6 pt-6 border-t border-gray-200">
                  <p className="text-gray-600 mb-4">
                    İş ilanı yüklemek için ana sayfaya gidin ve "İş İlanı Yükle" bölümünü kullanın.
                  </p>
                  <button
                    onClick={() => window.location.href = '/dashboard/headhunter'}
                    className="flex items-center gap-2 text-white bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-semibold rounded-xl text-sm px-6 py-3 shadow-lg hover:shadow-xl transition-all duration-200 transform hover:scale-105"
                  >
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                    </svg>
                    İş İlanı Yükle
                  </button>
                </div>
              )}
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}
