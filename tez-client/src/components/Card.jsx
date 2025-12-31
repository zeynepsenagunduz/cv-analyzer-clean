import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

export default function Card({ job }) {
  console.log('🔍 JOB OBJECT:', job);
  console.log('🔍 JOB ID:', job.id);
  console.log('🔍 ALL KEYS:', Object.keys(job));
  
  const [isOpen, setIsOpen] = useState(false);
  const [applying, setApplying] = useState(false);
  const [applied, setApplied] = useState(false);
  const [showModal, setShowModal] = useState(false);

  // Başvuru kontrolü
  useEffect(() => {
    checkIfApplied();
  }, []);

  const checkIfApplied = async () => {
    try {
      const userData = JSON.parse(window.localStorage.getItem('userData'));
      const response = await fetch(`http://localhost:8000/api/applications/user/${userData.userid}`);
      const data = await response.json();
      
      // Bu iş ilanına başvuru yapılmış mı kontrol et
      const hasApplied = data.applications.some(app => app.jobpostid === job.id);
      setApplied(hasApplied);
    } catch (error) {
      console.error('Error checking application:', error);
    }
  };

  const handleApply = async (e) => {
    e.stopPropagation();
    
    if (applied) {
      alert('Bu iş ilanına zaten başvurdunuz!');
      return;
    }
    
    setShowModal(true);
  };

  const confirmApply = async () => {
    setApplying(true);
    
    try {
      const userData = JSON.parse(window.localStorage.getItem('userData'));
      
      const response = await fetch(`http://localhost:8000/api/apply?userid=${userData.userid}&jobpostid=${job.id}&cover_letter=`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        }
      });
      
      const data = await response.json();
      
      if (response.ok) {
        setApplied(true);
        setShowModal(false);
        alert(`✅ Başvurunuz başarıyla kaydedildi!\n\n🎯 Eşleşme Skoru: ${data.match_score}%`);
      } else {
        alert(`❌ Hata: ${data.detail}`);
      }
    } catch (error) {
      console.error('Error applying:', error);
      alert('❌ Başvuru sırasında bir hata oluştu!');
    } finally {
      setApplying(false);
    }
  };

  return (
    <>
      <div
        onClick={() => {
          setIsOpen(!isOpen);
        }}
        className="w-full bg-white border-2 border-gray-200 flex flex-col justify-center items-center text-xl p-6 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-200 transform hover:scale-[1.01] cursor-pointer"
      >
        <div className="w-full flex justify-between items-center mb-4">
          <div className="flex items-center gap-3 text-gray-800 font-semibold">
            <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
            </svg>
            İş İlanı Detayları
          </div>
          
          <div className="flex items-center gap-3">
            <button
              onClick={(e) => {
                e.stopPropagation();
                window.open(`http://localhost:8000/static/jobposts/${job.userid}.txt`, '_blank');
              }}
              className="flex items-center gap-2 text-white bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-semibold rounded-xl text-sm px-6 py-3 shadow-lg hover:shadow-xl transition-all duration-200 transform hover:scale-105"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              İlanı Görüntüle
            </button>

            <button
              onClick={handleApply}
              disabled={applying || applied}
              type="button"
              className={`flex items-center gap-2 text-white font-semibold rounded-xl text-sm px-6 py-3 shadow-lg hover:shadow-xl transition-all duration-200 transform hover:scale-105 ${
                applied 
                ? 'bg-gray-500 cursor-not-allowed opacity-75' 
                  : applying
                  ? 'bg-blue-400 cursor-wait'
                  : 'bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 focus:ring-4 focus:outline-none focus:ring-green-300'
              }`}
            >
              {applying ? (
                <>
                  <svg className="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Başvuruluyor...
                </>
              ) : applied ? (
                <>
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  Başvuruldu
                </>
              ) : (
                <>
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  Başvur
                </>
              )}
            </button>
          </div>
        </div>
        
        {isOpen && (
          <div className="w-full mt-4 space-y-4">
            <div className="bg-gray-50 p-5 rounded-xl border border-gray-200">
              <p className="text-gray-700 leading-relaxed">{job.text.slice(0, 800)}...</p>
            </div>
            <div className="w-full flex flex-wrap justify-center gap-3 mt-4">
              {job.keywords.map((keyword, index) => {
                return (
                  <div key={index} className="bg-gradient-to-r from-green-500 to-emerald-600 text-white px-4 py-2 rounded-xl text-sm font-semibold shadow-md hover:shadow-lg transition-all duration-200 transform hover:scale-105">
                    {keyword}
                  </div>
                );
              })}
            </div>
            <div className="flex items-center justify-center gap-3 mt-6 bg-gradient-to-r from-blue-500 to-blue-600 text-white px-6 py-4 rounded-xl shadow-lg">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
              </svg>
              <span className="text-xl font-bold">İş Skoru: {job.point}</span>
            </div>
          </div>
        )}
        {!isOpen && (
          <div className="w-full mt-4 flex items-center justify-center text-gray-500 text-sm">
            <span>Detayları görmek için tıklayın</span>
            <svg className="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
            </svg>
          </div>
        )}
      </div>

      {/* Başvuru Onay Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" onClick={() => setShowModal(false)}>
          <div className="bg-white rounded-2xl p-8 max-w-md w-full mx-4 shadow-2xl" onClick={(e) => e.stopPropagation()}>
            <div className="text-center mb-6">
              <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <h3 className="text-2xl font-bold text-gray-800 mb-2">Başvuruyu Onayla</h3>
              <p className="text-gray-600">Bu iş ilanına başvurmak istediğinize emin misiniz?</p>
            </div>
            
            <div className="space-y-3">
              <button
                onClick={confirmApply}
                className="w-full bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 text-white font-semibold py-3 px-6 rounded-xl shadow-lg hover:shadow-xl transition-all duration-200"
              >
                Evet, Başvur
              </button>
              <button
                onClick={() => setShowModal(false)}
                className="w-full bg-gray-200 hover:bg-gray-300 text-gray-700 font-semibold py-3 px-6 rounded-xl transition-all duration-200"
              >
                İptal
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}