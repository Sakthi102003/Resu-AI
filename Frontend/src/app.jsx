import { useEffect } from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuthStore } from './Services/auth'

// Pages
import Home from './pages/Home'
import Login from './pages/login'
import Dashboard from './pages/Dashboard'
import TemplateSelection from './pages/TemplateSelection'
import ChatEditor from './pages/Chateditor'
import ManualEditor from './pages/ManualEditor'
import LatexEditor from './pages/LatexEditor'
import Profile from './pages/Profile'

// Protected Route Component
const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, checkAuth } = useAuthStore()

  useEffect(() => {
    checkAuth()
  }, [checkAuth])

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  return children
}

function App() {
  return (
    <div className="App">
      <Routes>
        {/* Public Routes */}
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        
        {/* Protected Routes */}
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/template-selection"
          element={
            <ProtectedRoute>
              <TemplateSelection />
            </ProtectedRoute>
          }
        />
        <Route
          path="/editor/:resumeId"
          element={
            <ProtectedRoute>
              <ChatEditor />
            </ProtectedRoute>
          }
        />
        <Route
          path="/editor"
          element={
            <ProtectedRoute>
              <ChatEditor />
            </ProtectedRoute>
          }
        />
        <Route
          path="/editor/manual/:resumeId"
          element={
            <ProtectedRoute>
              <ManualEditor />
            </ProtectedRoute>
          }
        />
        <Route
          path="/editor/latex/:resumeId"
          element={
            <ProtectedRoute>
              <LatexEditor />
            </ProtectedRoute>
          }
        />
        <Route
          path="/profile"
          element={
            <ProtectedRoute>
              <Profile />
            </ProtectedRoute>
          }
        />
        
        {/* Catch-all Route */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </div>
  )
}

export default App
