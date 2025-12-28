import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
export default function AdminDashboard() {
  const [bestApplicants, setBestApplicants] = useState([]);

  const [name, setName] = useState('');
  const [keywords, setKeywords] = useState('');
  const [link, setLink] = useState('');
  const [inviteCode, setInviteCode] = useState(null);
  const [courses, setCourses] = useState([]);

  const createInviteCode = async () => {
    const response = await fetch('http://localhost:8000/admin/create-invite-code', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (response.status === 200) {
      const data = await response.json();
      setInviteCode(data.invite_code);
    } else {
      alert('Kod oluşturulamadı');
    }
  };

  const deleteCourse = async (courseid) => {
    // /admin/delete-course/:courseid  get req
    const response = await fetch(`http://localhost:8000/admin/delete-course/${courseid}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (response.status === 200) {
      alert('Kurs Silindi');
    } else {
      alert('Kurs Silinemedi');
    }
  };

  const saveCourse = async () => {
    const response = await fetch('http://localhost:8000/admin/add-courses', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        name: name,
        keywords: keywords,
        link: link,
      }),
    });

    if (response.status === 200) {
      alert('Kurs Kaydedildi');
    } else {
      alert('Kurs Kaydedilemedi');
    }
  };

  useEffect(() => {
    const getCourses = async () => {
      const response = await fetch('http://localhost:8000/admin/get-courses', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      const data = await response.json();
      if (data) {
        setCourses(data.courses);
      }
    };
    getCourses();
  }, []);

  useEffect(() => {
    console.log('courses', courses);
  }, [courses]);

  return (
    <div className="w-screen h-screen flex justify-start items-center bg-gradient-to-br from-gray-50 to-gray-100">
      <div className="sidebar w-64 h-full flex flex-col justify-start items-center text-white pt-9 text-2xl bg-gradient-to-b from-blue-700 to-blue-900 shadow-2xl">
        <div className="flex items-center gap-2 mb-8">
          <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <span className="font-bold">CV ANALYZER</span>
        </div>
      </div>
      <div className="w-full h-full flex flex-col">
        <div className="navbar w-full h-20 flex justify-between items-center pr-8 pl-8 bg-white shadow-md border-b border-gray-200">
          <span className="text-xl font-semibold text-gray-700">Admin Paneli</span>
          <div className="w-12 h-12 rounded-full bg-gradient-to-br from-blue-400 to-purple-500 flex items-center justify-center shadow-lg">
            <img className="w-10 h-10 rounded-full object-cover" src="../../public/user.png" alt="User" />
          </div>
        </div>
        <div className="main w-full flex-1 bg-gradient-to-br from-gray-50 to-gray-100 overflow-y-auto p-8">
          <div className="max-w-6xl mx-auto space-y-8">
            <div className="bg-white rounded-3xl shadow-xl p-8">
              <h2 className="text-3xl font-bold text-gray-800 mb-6 flex items-center gap-3">
                <svg className="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                </svg>
                Davet Kodu Oluştur
              </h2>
              <button 
                onClick={createInviteCode} 
                className="w-full bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 text-white font-semibold rounded-xl text-lg px-8 py-4 shadow-lg hover:shadow-xl transition-all duration-200 transform hover:scale-105"
              >
                Davet Kodu Oluştur
              </button>
              {inviteCode && (
                <div className="mt-6 p-6 bg-gradient-to-r from-green-50 to-emerald-50 border-2 border-green-300 rounded-2xl">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      <span className="text-xl font-bold text-gray-800">Davet Kodu:</span>
                    </div>
                    <div className="bg-white px-6 py-3 rounded-xl border-2 border-green-400 shadow-lg">
                      <code className="text-lg font-mono font-bold text-green-700">{inviteCode}</code>
                    </div>
                  </div>
                </div>
              )}
            </div>

            <div className="bg-white rounded-3xl shadow-xl p-8">
              <h1 className="text-3xl font-bold text-gray-800 mb-6 flex items-center gap-3">
                <svg className="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                </svg>
                Kurs Kayıt
              </h1>
              <div className="space-y-5">
                <div className="relative">
                  <input
                    onChange={(e) => {
                      setName(e.target.value);
                    }}
                    type="text"
                    id="name"
                    className="w-full bg-gray-50 border-2 border-gray-200 text-gray-900 text-sm rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 block p-4 pl-12 transition-all duration-200 hover:border-blue-300"
                    placeholder="Kurs Adı"
                    required
                  />
                  <svg className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                  </svg>
                </div>
                <div className="relative">
                  <input
                    onChange={(e) => {
                      setKeywords(e.target.value);
                    }}
                    type="text"
                    id="keywords"
                    className="w-full bg-gray-50 border-2 border-gray-200 text-gray-900 text-sm rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 block p-4 pl-12 transition-all duration-200 hover:border-blue-300"
                    placeholder="Anahtar Kelimeler (virgülle ayırın)"
                    required
                  />
                  <svg className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                  </svg>
                </div>
                <div className="relative">
                  <input
                    onChange={(e) => {
                      setLink(e.target.value);
                    }}
                    type="url"
                    id="link"
                    className="w-full bg-gray-50 border-2 border-gray-200 text-gray-900 text-sm rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 block p-4 pl-12 transition-all duration-200 hover:border-blue-300"
                    placeholder="Kurs Linki"
                    required
                  />
                  <svg className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
                  </svg>
                </div>
                <button
                  onClick={() => {
                    saveCourse();
                  }}
                  type="submit"
                  className="w-full text-white bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-semibold rounded-xl text-base px-8 py-4 shadow-lg hover:shadow-xl transition-all duration-200 transform hover:scale-105"
                >
                  Kaydet
                </button>
              </div>
            </div>

            <div className="bg-white rounded-3xl shadow-xl p-8">
              <h1 className="text-3xl font-bold text-gray-800 mb-6 flex items-center gap-3">
                <svg className="w-8 h-8 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                </svg>
                Mevcut Kurslar
              </h1>
              <div className="space-y-4">
                {courses.map((course, index) => {
                  return (
                    <div key={index} className="bg-gradient-to-r from-gray-50 to-blue-50 border-2 border-gray-200 rounded-2xl p-6 hover:shadow-lg transition-all duration-200">
                      <div className="flex flex-col gap-4">
                        <div className="flex items-center justify-between">
                          <div className="flex-1">
                            <h3 className="text-xl font-bold text-gray-800 mb-2">Kurs Adı: {course[1]}</h3>
                            <p className="text-gray-600 mb-3">
                              <span className="font-semibold">Anahtar Kelimeler:</span> {course[2]}
                            </p>
                            <Link 
                              to={`${course[3]}`} 
                              target="_blank"
                              className="inline-flex items-center gap-2 text-blue-600 hover:text-blue-800 font-semibold transition-colors"
                            >
                              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                              </svg>
                              Kursa Git
                            </Link>
                          </div>
                          <button
                            onClick={() => {
                              deleteCourse(course[0]);
                            }}
                            type="submit"
                            className="flex items-center gap-2 text-white bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 focus:ring-4 focus:outline-none focus:ring-red-300 font-semibold rounded-xl text-sm px-6 py-3 shadow-lg hover:shadow-xl transition-all duration-200 transform hover:scale-105"
                          >
                            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                            </svg>
                            Sil
                          </button>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
