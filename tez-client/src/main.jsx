import React from 'react';
import ReactDOM from 'react-dom/client';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import App from './App';
import './index.css';
import { Login, Register, DashboardUser, DashboardHeadHunter, AdminDashboard, AnalyticsDashboard, UserProfile, ViewCV, HeadHunterProfile, HeadHunterApplications, UserApplications } from './pages';const router = createBrowserRouter([
  {
    path: '/',
    element: <App />,
  },
  {
    path: '/login',
    element: <Login />,
  },
  {
    path: '/register/:invite_code',
    element: <Register />,
  },
  {
    path: '/register',
    element: <Register />,
  },
  {
    path: '/dashboard/user',
    element: <DashboardUser />,
  },
  {
    path: '/dashboard/headhunter',
    element: <DashboardHeadHunter />,
  },
  {
    path: '/dashboard/admin',
    element: <AdminDashboard />,
  },
  {
    path: '/analytics',
    element: <AnalyticsDashboard />,
  },
  {
    path: '/profile',
    element: <UserProfile />,
  },
  {
    path: '/view-cv',
    element: <ViewCV />,
  },
  {
    path: '/headhunter/profile',
    element: <HeadHunterProfile />,
  },
  {
    path: '/headhunter/applications',
    element: <HeadHunterApplications />,
  },
  {
    path: '/user/applications',
    element: <UserApplications />,
  },
  
]);

ReactDOM.createRoot(document.getElementById('root')).render(<RouterProvider router={router} />);
