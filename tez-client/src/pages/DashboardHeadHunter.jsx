import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
export default function DashboardHeadHunter() {
  const [bestApplicants, setBestApplicants] = useState([]);
  const [bestApplicantKeywords, setBestApplicantKeywords] = useState([]);
  const [credit, setCredit] = useState(0);

  const navigate = useNavigate();

  const decreaseCredit = async () => {
    const response = await fetch(
      `http://localhost:8000/decrease-credit?userid=${JSON.parse(
        window.localStorage.getItem('userData'),
      ).userid.toString()}`,
      {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      },
    );

    if (response.ok) {
      const data = await response.json();
      setCredit(data.credit);
      return true;
    } else {
      return false;
    }
  };

  const navigateToPDF = (userid) => {
    window.open(`http://localhost:8000/static/cvs/${userid}.pdf`, '_blank');
  };

  useEffect(() => {
    const fetchData = async () => {
      const response = await fetch(
        `http://localhost:8000/get-credit?userid=${JSON.parse(
          window.localStorage.getItem('userData'),
        ).userid.toString()}`,
        {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        },
      );

      if (response.ok) {
        const data = await response.json();
        setCredit(data.credit);
      }
    };

    fetchData();
  }, []);

  useEffect(() => {
    console.log('credit', credit);
  }, [credit]);

  useEffect(() => {
    const fetchData = async () => {
      const response = await fetch(
        `http://localhost:8000/best-applicant?userid=${JSON.parse(
          window.localStorage.getItem('userData'),
        ).userid.toString()}`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
        },
      );

      if (response.ok) {
        const data = await response.json();
        setBestApplicants(data.top_five);
        setBestApplicantKeywords(data.best_cv_keywords);
      }
    };

    if (!window.localStorage.getItem('userData')) {
      window.location.href = '/login';
    } else {
      fetchData();
    }
    console.log('userData', JSON.parse(window.localStorage.getItem('userData')));
  }, []);

  const deletePost = async (jobpostid) => {
    const response = await fetch(
      `http://localhost:8000/delete-jobpost/${JSON.parse(
        window.localStorage.getItem('userData'),
      ).userid.toString()}`,
    );
    alert('Is postu başarıyla silindi!');


    // update userData
    window.localStorage.setItem(
      'userData',
      JSON.stringify({
        userid: JSON.parse(window.localStorage.getItem('userData')).userid,
        username: JSON.parse(window.localStorage.getItem('userData')).username,
        mail: JSON.parse(window.localStorage.getItem('userData')).mail,
        role: JSON.parse(window.localStorage.getItem('userData')).role,
        has_cv: JSON.parse(window.localStorage.getItem('userData')).has_cv,
        has_jobpost: false,
      }),
    );
    window.location.reload(); 

  };

  const [file, setFile] = useState(null);

  const clearLocalStorage = () => {
    window.localStorage.clear();
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(
      `http://localhost:8000/upload/jobpost?userid=${JSON.parse(
        window.localStorage.getItem('userData'),
      ).userid.toString()}`,
      {
        method: 'POST',
        body: formData,
      },
    );

    if (response.ok) {
      const data = await response.json();
      alert('Is postu başarıyla yüklendi!');

      window.localStorage.setItem(
        'userData',
        JSON.stringify({
          userid: JSON.parse(window.localStorage.getItem('userData')).userid,
          username: JSON.parse(window.localStorage.getItem('userData')).username,
          mail: JSON.parse(window.localStorage.getItem('userData')).mail,
          role: JSON.parse(window.localStorage.getItem('userData')).role,
          has_cv: JSON.parse(window.localStorage.getItem('userData')).has_cv,
          has_jobpost: true,
        }),
      );

      window.location.reload();
    } else {
      alert('hata');
    }

    console.log('File:', file);
  };

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

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
          <div className="flex items-center gap-4">
            <div className="bg-gradient-to-r from-yellow-400 to-orange-500 rounded-xl px-6 py-3 shadow-lg">
              <span className="text-white font-bold text-lg">Kalan Krediniz: {credit}</span>
            </div>
          </div>
          
          <div className="flex justify-center items-center gap-6">
          {JSON.parse(window.localStorage.getItem('userData')).has_jobpost && (
            <button
              onClick={() => {
                deletePost();
              }}
              type="submit"
              className="flex items-center gap-2 text-white bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 focus:ring-4 focus:outline-none focus:ring-red-300 font-semibold rounded-xl text-sm px-6 py-3 shadow-lg hover:shadow-xl transition-all duration-200 transform hover:scale-105"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
              Postu Sil
            </button>)}
        
            <button
              onClick={() => {
                clearLocalStorage();
                window.location.href = '/login';
              }}
              type="submit"
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
        <div className="main w-full flex-1 bg-gradient-to-br from-gray-50 to-gray-100 overflow-y-auto">
          {JSON.parse(window.localStorage.getItem('userData')).has_jobpost ? (
            <div className="w-full flex flex-col justify-start items-center p-8 gap-6">
              <div className="w-full max-w-6xl">
                <h1 className="text-4xl font-bold text-gray-800 mb-2 flex items-center gap-3">
                  <svg className="w-10 h-10 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                  </svg>
                  Eşleşen Kullanıcılar
                </h1>
                <p className="text-gray-600 mb-6">İş ilanınıza en uygun adaylar</p>
              </div>
              <div className="w-full max-w-6xl space-y-4">
                {bestApplicants.map((item, index) => {
                  if (index === 0) {
                    return (
                      <div key={index} className="w-full bg-gradient-to-r from-yellow-50 to-orange-50 border-2 border-yellow-400 flex flex-col justify-start items-center text-xl p-6 rounded-2xl shadow-xl hover:shadow-2xl transition-all duration-200 transform hover:scale-[1.02]">
                        <div className="w-full flex justify-between items-center">
                          <div
                            onClick={async () => {
                              if ((await decreaseCredit()) == true) {
                                navigateToPDF(item.userid);
                                alert('Kredi yeterli');
                              } else {
                                alert('Kredi yetersiz');
                              }
                            }}
                            className="cursor-pointer font-semibold text-gray-800 hover:text-blue-600 transition-colors flex items-center gap-2"
                          >
                            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                            </svg>
                            Kullanıcı {item.username}
                          </div>
                          <div className="bg-blue-600 text-white px-4 py-2 rounded-xl font-bold shadow-lg">SCORE: {item.point}</div>
                          <div className="bg-gradient-to-r from-red-600 to-red-700 text-white px-6 py-2 rounded-xl text-xl font-bold shadow-lg flex items-center gap-2">
                            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
                            </svg>
                            En İyi Aday
                          </div>
                        </div>
                      </div>
                    );
                  }
                  return null;
                })}
                {bestApplicants.map((item, index) => {
                  if (index !== 0) {
                    return (
                      <div key={index} className="w-full bg-white border-2 border-gray-200 flex flex-col justify-start items-center text-xl p-6 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-200 transform hover:scale-[1.01]">
                        <div className="w-full flex justify-between items-center">
                          <div
                            onClick={async () => {
                              if ((await decreaseCredit()) == true) {
                                navigateToPDF(item.userid);
                                alert('Kredi yeterli');
                              } else {
                                alert('Kredi yetersiz');
                              }
                            }}
                            className="cursor-pointer font-semibold text-gray-800 hover:text-blue-600 transition-colors flex items-center gap-2"
                          >
                            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                            </svg>
                            Kullanıcı {item.username}
                          </div>
                          <div className="bg-blue-600 text-white px-4 py-2 rounded-xl font-bold shadow-lg">SCORE: {item.point}</div>
                        </div>
                      </div>
                    );
                  }
                  return null;
                })}
              </div>
            </div>
          ) : (
            <div className="w-full flex flex-col justify-center items-center min-h-full gap-8 p-8">
              <div className="bg-white rounded-3xl shadow-2xl p-12 max-w-2xl w-full text-center">
                <div className="mb-6">
                  <svg className="w-24 h-24 mx-auto text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                </div>
                <h1 className="text-4xl font-bold text-gray-800 mb-4">Lütfen İş Postunu Giriniz</h1>
                <p className="text-gray-600 mb-8">Eşleşen adayları görmek için iş ilanınızı yükleyin</p>
                <form onSubmit={handleSubmit} className="flex flex-col items-center gap-6">
                  <label className="w-full max-w-md cursor-pointer">
                    <div className="border-2 border-dashed border-gray-300 rounded-2xl p-8 hover:border-blue-500 transition-all duration-200 bg-gray-50 hover:bg-blue-50">
                      <div className="text-center">
                        <svg className="w-12 h-12 mx-auto text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                        </svg>
                        <p className="text-gray-600 font-semibold">Dosya Seçin</p>
                        <p className="text-sm text-gray-500 mt-2">TXT formatında iş ilanı yükleyin</p>
                      </div>
                    </div>
                    <input type="file" onChange={handleFileChange} className="hidden" accept=".txt" />
                  </label>
                  {file && (
                    <div className="text-green-600 font-semibold flex items-center gap-2">
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      {file.name}
                    </div>
                  )}
                  <button
                    onClick={handleSubmit}
                    type="submit"
                    className="text-white bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-semibold rounded-xl text-base px-10 py-4 shadow-lg hover:shadow-xl transition-all duration-200 transform hover:scale-105"
                  >
                    Yükle ve Gönder
                  </button>
                </form>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
