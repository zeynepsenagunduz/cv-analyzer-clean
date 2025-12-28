import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import '../App.css';
export default function Register() {
  const params = useParams();
  const navigate = useNavigate();

  useEffect(() => {
    if (window.localStorage.getItem('userData')) {
      navigate('/dashboard');
    }
  }, []);

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');
  const [isHeadHunter, setIsHeadHunter] = useState(0);

  useEffect(() => {
    const checkInviteCodeIsValid = async () => {
      const response = await fetch(
        `http://localhost:8000/check-invite-code/${params.invite_code}`,
        {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        },
      );

      if (response.ok) {
        setIsHeadHunter(1);
      } else {
        alert('Davet kodu geçersiz!');
        navigate('/login');
      }
    };

    if (params.invite_code) {
      checkInviteCodeIsValid();
    }

    // ed7d583e-426f-4141-9859-aa70df2076a8
  }, []);

  useEffect(() => {
    console.log('isHeadHunter', isHeadHunter);
  }, [isHeadHunter]);

  useEffect(() => {
    console.log('params', params);
  }, [params]);

  const registerFetch = async () => {
    const response = await fetch('http://localhost:8000/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username: document.getElementById('username').value,
        password: document.getElementById('password').value,
        mail: document.getElementById('email').value,
        role: isHeadHunter.toString(),
        has_cv: false,
        has_jobpost: false,
      }),
    });

    if (response.ok) {
      const data = await response.json();
      navigate('/login');
    } else {
      alert('Kullanıcı adı veya şifre yanlış!');
    }
  };

  return (
    <div className="w-screen h-screen flex justify-center items-center bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      <div className="w-11/12 max-w-6xl h-5/6 flex justify-center items-center shadow-2xl rounded-3xl overflow-hidden">
        <div className="w-1/2 h-full loginImage hidden md:block relative">
          <div className="absolute inset-0 bg-gradient-to-r from-blue-600/80 to-purple-600/80"></div>
          <div className="absolute inset-0 flex flex-col justify-center items-center text-white p-10">
            <h2 className="text-4xl font-bold mb-4">Yeni Hesap Oluşturun</h2>
            <p className="text-xl text-center">Kariyer yolculuğunuza bugün başlayın</p>
          </div>
        </div>
        <div className="w-full md:w-1/2 h-full bg-white/95 backdrop-blur-sm flex flex-col justify-center items-center p-10 gap-6 overflow-y-auto">
          <div className="text-center mb-4">
            <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-2">
              Kayıt Ol
            </h1>
            <p className="text-gray-600 mt-2">Yeni hesap oluşturmak için bilgilerinizi girin</p>
          </div>

          <div className="w-full max-w-md space-y-5">
            <div className="relative">
              <input
                onChange={(e) => {
                  setUsername(e.target.value);
                }}
                type="text"
                id="username"
                className="w-full bg-gray-50 border-2 border-gray-200 text-gray-900 text-sm rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 block p-4 pl-12 transition-all duration-200 hover:border-blue-300"
                placeholder="Kullanıcı adı girin"
                required
              />
              <svg className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
            </div>
            <div className="relative">
              <input
                onChange={(e) => {
                  setPassword(e.target.value);
                }}
                type="password"
                id="password"
                className="w-full bg-gray-50 border-2 border-gray-200 text-gray-900 text-sm rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 block p-4 pl-12 transition-all duration-200 hover:border-blue-300"
                placeholder="Şifre girin"
                required
              />
              <svg className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
            </div>
            <div className="relative">
              <input
                onChange={(e) => {
                  setEmail(e.target.value);
                }}
                type="email"
                id="email"
                className="w-full bg-gray-50 border-2 border-gray-200 text-gray-900 text-sm rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 block p-4 pl-12 transition-all duration-200 hover:border-blue-300"
                placeholder="E-posta girin"
                required
              />
              <svg className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
            </div>

            {isHeadHunter === 1 && (
              <div className="bg-blue-100 border-2 border-blue-300 rounded-xl p-4 flex items-center gap-3">
                <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span className="text-blue-800 font-semibold">Yetenek avcısı olarak kayıt oluyorsunuz</span>
              </div>
            )}
          </div>

          <button
            onClick={() => {
              registerFetch();
            }}
            type="submit"
            className="w-full max-w-md text-white bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 focus:ring-4 focus:outline-none focus:ring-green-300 font-semibold rounded-xl text-base px-8 py-4 text-center shadow-lg hover:shadow-xl transition-all duration-200 transform hover:scale-105"
          >
            Kayıt Ol
          </button>
        </div>
      </div>
    </div>
  );
}
