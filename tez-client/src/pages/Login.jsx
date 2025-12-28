import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import '../App.css';
export default function Login() {
  const navigate = useNavigate();

  useEffect(() => {
    const userData = window.localStorage.getItem('userData');
    if (userData) {
      try {
        const parsedData = JSON.parse(userData);
        if (parsedData.role === '0' || parsedData.role === 0) {
          navigate('/dashboard/user');
        } else {
          navigate('/dashboard/headhunter');
        }
      } catch (error) {
        console.error('Error parsing userData:', error);
      }
    }
  }, [navigate]);

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const loginFetch = async () => {
    const response = await fetch('http://localhost:8000/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username: document.getElementById('username').value,
        password: document.getElementById('password').value,
      }),
    });

    if (response.ok) {
      const data = await response.json();
      if (data.userid) {
        window.localStorage.setItem('userData', JSON.stringify(data));
        if (data.role === '0') {
          navigate('/dashboard/user');
        } else {
          navigate('/dashboard/headhunter');
        }
      } else {
        alert('Kullanıcı adı veya şifre yanlış!');
      }
    }
  };

  return (
    <div className="w-screen h-screen flex justify-center items-center bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      <div className="w-11/12 max-w-6xl h-5/6 flex justify-center items-center shadow-2xl rounded-3xl overflow-hidden">
        <div className="w-1/2 h-full loginImage hidden md:block relative">
          <div className="absolute inset-0 bg-gradient-to-r from-blue-600/80 to-purple-600/80"></div>
          <div className="absolute inset-0 flex flex-col justify-center items-center text-white p-10">
            <h2 className="text-4xl font-bold mb-4">CV Analyzer'a Hoş Geldiniz</h2>
            <p className="text-xl text-center">Kariyerinize uygun iş fırsatlarını keşfedin</p>
          </div>
        </div>
        <div className="w-full md:w-1/2 h-full bg-white/95 backdrop-blur-sm flex flex-col justify-center items-center p-10 gap-8">
          <div className="text-center mb-4">
            <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-2">
              Hesabınıza Giriş Yapın
            </h1>
            <p className="text-gray-600 mt-2">Devam etmek için bilgilerinizi girin</p>
          </div>

          <div className="w-full max-w-md space-y-6">
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
              <svg
                className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                />
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
              <svg
                className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"
                />
              </svg>
            </div>
          </div>

          <div className="w-full max-w-md flex flex-col sm:flex-row gap-4">
            <button
              onClick={() => {
                loginFetch();
              }}
              type="submit"
              className="flex-1 text-white bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 focus:ring-4 focus:outline-none focus:ring-green-300 font-semibold rounded-xl text-base px-8 py-4 text-center shadow-lg hover:shadow-xl transition-all duration-200 transform hover:scale-105"
            >
              Giriş Yap
            </button>
            <button
              onClick={() => {
                window.location.href = '/register';
              }}
              className="flex-1 text-white bg-gradient-to-r from-orange-500 to-red-500 hover:from-orange-600 hover:to-red-600 focus:ring-4 focus:outline-none focus:ring-orange-300 font-semibold rounded-xl text-base px-8 py-4 text-center shadow-lg hover:shadow-xl transition-all duration-200 transform hover:scale-105"
            >
              Kayıt Ol
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
