import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import Card from '../components/Card';
import CardForCourses from '../components/CardForCourses';
export default function DashboardUser() {
  useEffect(() => {
    if (!window.localStorage.getItem('userData')) {
      window.location.href = '/login';
    }
  }, []);
  const [jobs, setJobs] = useState([]);
  const [courses, setCourses] = useState([]);

  const [file, setFile] = useState(null);

  useEffect(() => {
    console.log('file', file);
  }, [file]);

  
  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };
  const handleSubmit = async (event) => {
    event.preventDefault();

    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(
      `http://localhost:8000/upload/cv?userid=${JSON.parse(
        window.localStorage.getItem('userData'),
      ).userid.toString()}`,
      {
        method: 'POST',
        body: formData,
      },
    );

    if (response.ok) {
      const data = await response.json();
      alert('CV başarıyla yüklendi!');

      window.localStorage.setItem(
        'userData',
        JSON.stringify({
          userid: JSON.parse(window.localStorage.getItem('userData')).userid,
          username: JSON.parse(window.localStorage.getItem('userData')).username,
          mail: JSON.parse(window.localStorage.getItem('userData')).mail,
          role: JSON.parse(window.localStorage.getItem('userData')).role,
          has_cv: true,
          has_jobpost: JSON.parse(window.localStorage.getItem('userData')).has_jobpost,
        }),
      );

      window.location.reload();
    } else {
      alert('hata');
    }

    console.log('File:', file);
  };

  const deleteCv = async (cvsid) => {
    const response = await fetch(
      `http://localhost:8000/delete-cv/${JSON.parse(
        window.localStorage.getItem('userData'),
      ).userid.toString()}`,
    );
    alert('CV postu başarıyla silindi!');
  

    // update userData
    window.localStorage.setItem(
      'userData',
      JSON.stringify({
        userid: JSON.parse(window.localStorage.getItem('userData')).userid,
        username: JSON.parse(window.localStorage.getItem('userData')).username,
        mail: JSON.parse(window.localStorage.getItem('userData')).mail,
        role: JSON.parse(window.localStorage.getItem('userData')).role,
        has_cv: false,
        has_jobpost: JSON.parse(window.localStorage.getItem('userData')).has_jobpost
      }),
    );
    window.location.reload(); 

  };



  useEffect(() => {
    const fetchJobs = async () => {
      if (JSON.parse(window.localStorage.getItem('userData')).has_cv) {
        const response = await fetch('http://localhost:8000/best-job', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            userid: JSON.parse(window.localStorage.getItem('userData')).userid.toString(),
          }),
        });
        if (response.ok) {
          const data = await response.json();
          setJobs(data.top_five);
          setCourses(data.courses);
        }
      }
    };

    fetchJobs();
  }, []);

  const clearLocalStorage = () => {
    window.localStorage.clear();
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
          <span className="text-xl font-semibold text-gray-700"></span>
          
          <div className="flex justify-center items-center gap-6">
          {JSON.parse(window.localStorage.getItem('userData')).has_cv && (
  <button
    onClick={() => {
      deleteCv();
    }}
    type="submit"
    className="flex items-center gap-2 text-white bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 focus:ring-4 focus:outline-none focus:ring-red-300 font-semibold rounded-xl text-sm px-6 py-3 shadow-lg hover:shadow-xl transition-all duration-200 transform hover:scale-105"
  >
    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
        d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
      />
    </svg>
    CV Sil
  </button>
)}

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
        <div className="main w-full flex-1 flex flex-col justify-start items-start bg-gradient-to-br from-gray-50 to-gray-100 overflow-y-auto">
          {JSON.parse(window.localStorage.getItem('userData')).has_cv ? (
            <div className="w-full flex flex-col justify-start items-center p-8 gap-8">
              <div className="w-full max-w-6xl">
                <h1 className="text-4xl font-bold text-gray-800 mb-2 flex items-center gap-3">
                  <svg className="w-10 h-10 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                  </svg>
                  Size Uygun İş Postları
                </h1>
                <p className="text-gray-600 mb-6">Profilinize en uygun iş ilanları</p>
              </div>
              <div className="w-full max-w-6xl space-y-4">
                {jobs.map((job, index) => {
                  return <Card key={index} job={job} />;
                })}
              </div>
              <div className="w-full max-w-6xl mt-8">
                <h1 className="text-4xl font-bold text-gray-800 mb-2 flex items-center gap-3">
                  <svg className="w-10 h-10 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                  </svg>
                  Size Özel Kurs Önerilerimiz
                </h1>
                <p className="text-gray-600 mb-6">Gelişiminiz için önerilen kurslar</p>
              </div>
              <div className="w-full max-w-6xl space-y-4">
                {courses?.length > 0 ? (
                  courses.map((course, index) => {
                    return <CardForCourses key={index} title={course[1]} link={course[3]} />;
                  })
                ) : (
                  <div className="w-full bg-white rounded-2xl p-8 text-center text-gray-500 shadow-lg">
                    Henüz kurs önerisi bulunmamaktadır
                  </div>
                )}
              </div>
            </div>
          ) : (
            <div className="w-full flex flex-col justify-center items-center min-h-full gap-8 p-8">
              <div className="bg-white rounded-3xl shadow-2xl p-12 max-w-2xl w-full text-center">
                <div className="mb-6">
                  <svg className="w-24 h-24 mx-auto text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                  </svg>
                </div>
                <h1 className="text-4xl font-bold text-gray-800 mb-4">Lütfen Özgeçmiş Yükleyin</h1>
                <p className="text-gray-600 mb-8">Size uygun iş ilanlarını görmek için özgeçmişinizi yükleyin</p>
                <form onSubmit={handleSubmit} className="flex flex-col items-center gap-6">
                  <label className="w-full max-w-md cursor-pointer">
                    <div className="border-2 border-dashed border-gray-300 rounded-2xl p-8 hover:border-blue-500 transition-all duration-200 bg-gray-50 hover:bg-blue-50">
                      <div className="text-center">
                        <svg className="w-12 h-12 mx-auto text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                        </svg>
                        <p className="text-gray-600 font-semibold">Dosya Seçin</p>
                        <p className="text-sm text-gray-500 mt-2">PDF formatında özgeçmiş yükleyin</p>
                      </div>
                    </div>
                    <input type="file" onChange={handleFileChange} className="hidden" accept=".pdf" />
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
