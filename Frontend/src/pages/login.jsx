import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Mail, Lock, User, Phone, Sparkles } from 'lucide-react'
import toast from 'react-hot-toast'
import { useAuthStore } from '../Services/auth'
import { signInWithPopup, signInWithRedirect, getRedirectResult } from 'firebase/auth'
import { auth, googleProvider } from '../config/firebase'

export default function Login() {
  const navigate = useNavigate()
  const { login, register, isLoading } = useAuthStore()
  
  const [isSignUp, setIsSignUp] = useState(false)
  const [isGoogleSignInProgress, setIsGoogleSignInProgress] = useState(false)
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    full_name: '',
    phone: '',
  })

  // Check for redirect result on component mount
  React.useEffect(() => {
    const checkRedirectResult = async () => {
      try {
        const result = await getRedirectResult(auth)
        if (result?.user) {
          const user = result.user
          await handleFirebaseUser(user)
        }
      } catch (error) {
        console.error('Redirect result error:', error)
        if (error.code !== 'auth/popup-closed-by-user') {
          toast.error('Authentication failed')
        }
      }
    }
    checkRedirectResult()
  }, [])

  const handleFirebaseUser = async (user) => {
    try {
      toast.dismiss() // Clear loading toast
      toast.loading('Authenticating with backend...')
      
      // Create user data from Google profile
      const userData = {
        email: user.email,
        full_name: user.displayName,
        phone: user.phoneNumber || '',
        password: user.uid, // Use Firebase UID as password for backend
      }

      // Always try login first, if fails then register (for Google Sign-In)
      let authResult = await login(user.email, user.uid)
      
      if (!authResult.success) {
        // User doesn't exist, register them
        console.log('User not found, registering new user...')
        authResult = await register(userData)
      }

      toast.dismiss()
      
      if (authResult.success) {
        toast.success(`Welcome ${user.displayName}!`)
        navigate('/dashboard')
      } else {
        toast.error(authResult.error || 'Authentication failed')
      }
    } catch (error) {
      console.error('Backend auth error:', error)
      toast.dismiss()
      toast.error('Failed to authenticate with backend')
    }
  }

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  const handleGoogleSignIn = async () => {
    // Prevent multiple concurrent sign-in attempts
    if (isGoogleSignInProgress) {
      console.log('Google sign-in already in progress')
      return
    }

    try {
      setIsGoogleSignInProgress(true)
      toast.loading('Opening Google Sign In...')
      
      const result = await signInWithPopup(auth, googleProvider)
      const user = result.user
      await handleFirebaseUser(user)
    } catch (error) {
      console.error('Google sign-in error:', error)
      
      // Handle specific error cases
      if (error.code === 'auth/popup-closed-by-user' || error.code === 'auth/cancelled-popup-request') {
        toast.dismiss()
        return // User intentionally closed popup, no error message needed
      } else if (error.code === 'auth/popup-blocked') {
        toast.error('Popup was blocked. Please allow popups for this site.')
      } else {
        toast.error('Failed to sign in with Google')
      }
    } finally {
      setIsGoogleSignInProgress(false)
      toast.dismiss()
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (isSignUp) {
      // Registration
      const result = await register(formData)
      if (result.success) {
        toast.success('Account created successfully!')
        navigate('/dashboard')
      } else {
        toast.error(result.error || 'Registration failed')
      }
    } else {
      // Login
      const result = await login(formData.email, formData.password)
      if (result.success) {
        toast.success('Welcome back!')
        navigate('/dashboard')
      } else {
        toast.error(result.error || 'Login failed')
      }
    }
  }

  return (
    <div className="min-h-screen bg-brutal-yellow flex items-center justify-center p-4 font-sans">
      <div className="w-full max-w-6xl grid md:grid-cols-2 gap-8 items-center">
        {/* Left Side - Branding */}
        <motion.div
          initial={{ opacity: 0, x: -50 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.6 }}
          className="text-black space-y-6 hidden md:block"
        >
          <div className="flex items-center gap-3">
            <div className="w-16 h-16 bg-black flex items-center justify-center shadow-neo border-2 border-black">
              <span className="text-white font-black text-3xl">R</span>
            </div>
            <h1 className="text-6xl font-black uppercase tracking-tighter">ResuAI</h1>
          </div>
          <h2 className="text-4xl font-black uppercase leading-none bg-white inline-block px-4 py-2 border-2 border-black shadow-neo">
            Build Your Perfect<br/>Resume with AI
          </h2>
          <p className="text-xl text-black font-bold border-l-4 border-black pl-4">
            Chat with our AI assistant to create professional, ATS-optimized resumes in minutes.
          </p>
          <div className="space-y-4 pt-8">
            <div className="flex items-start gap-3">
              <div className="w-8 h-8 bg-brutal-green border-2 border-black flex items-center justify-center flex-shrink-0 shadow-neo-sm">
                <span className="font-bold">✓</span>
              </div>
              <div>
                <h3 className="font-black uppercase">AI-Powered Chat Interface</h3>
                <p className="text-black font-mono text-sm">Build your resume through natural conversation</p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <div className="w-8 h-8 bg-brutal-pink border-2 border-black flex items-center justify-center flex-shrink-0 shadow-neo-sm">
                <span className="font-bold">✓</span>
              </div>
              <div>
                <h3 className="font-black uppercase">ATS Optimization</h3>
                <p className="text-black font-mono text-sm">Get scored and optimized for applicant tracking systems</p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <div className="w-8 h-8 bg-brutal-blue border-2 border-black flex items-center justify-center flex-shrink-0 shadow-neo-sm">
                <span className="font-bold">✓</span>
              </div>
              <div>
                <h3 className="font-black uppercase">Job Recommendations</h3>
                <p className="text-black font-mono text-sm">AI suggests perfect job matches based on your resume</p>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Right Side - Login Form */}
        <motion.div
          initial={{ opacity: 0, x: 50 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.6 }}
          className="bg-white border-4 border-black shadow-neo-lg p-8 md:p-10"
        >
          <div className="text-center mb-8">
            <h2 className="text-3xl font-black text-black uppercase">
              {isSignUp ? 'Create Account' : 'Welcome Back'}
            </h2>
            <p className="text-black font-mono mt-2 text-sm">
              {isSignUp
                ? 'Sign up to start building your resume'
                : 'Sign in to continue to your dashboard'}
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            {isSignUp && (
              <>
                <div>
                  <label className="block text-sm font-bold text-black mb-2 uppercase">
                    Full Name
                  </label>
                  <div className="relative">
                    <User className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-black" />
                    <input
                      type="text"
                      name="full_name"
                      value={formData.full_name}
                      onChange={handleChange}
                      className="input pl-10"
                      placeholder="JOHN DOE"
                      required={isSignUp}
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-bold text-black mb-2 uppercase">
                    Phone (Optional)
                  </label>
                  <div className="relative">
                    <Phone className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-black" />
                    <input
                      type="tel"
                      name="phone"
                      value={formData.phone}
                      onChange={handleChange}
                      className="input pl-10"
                      placeholder="+1 (555) 123-4567"
                    />
                  </div>
                </div>
              </>
            )}

            <div>
              <label className="block text-sm font-bold text-black mb-2 uppercase">
                Email
              </label>
              <div className="relative">
                <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-black" />
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  className="input pl-10"
                  placeholder="YOU@EXAMPLE.COM"
                  required
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-bold text-black mb-2 uppercase">
                Password
              </label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-black" />
                <input
                  type="password"
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  className="input pl-10"
                  placeholder="••••••••"
                  required
                  minLength={6}
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="w-full btn bg-black text-white hover:bg-gray-800 py-3 text-lg font-black uppercase tracking-wider disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? (
                <div className="flex items-center justify-center gap-2">
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  {isSignUp ? 'Creating Account...' : 'Signing In...'}
                </div>
              ) : (
                <>{isSignUp ? 'Create Account' : 'Sign In'}</>
              )}
            </button>
          </form>

          <div className="relative my-6">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t-2 border-black"></div>
            </div>
            <div className="relative flex justify-center text-sm">
              <span className="px-4 bg-white text-black font-bold uppercase border-2 border-black shadow-neo-sm">Or continue with</span>
            </div>
          </div>

          <button
            onClick={handleGoogleSignIn}
            type="button"
            disabled={isGoogleSignInProgress || isLoading}
            className="w-full flex items-center justify-center gap-3 px-4 py-3 border-2 border-black shadow-neo hover:shadow-none hover:translate-x-[2px] hover:translate-y-[2px] bg-white transition-all font-bold text-black uppercase disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <svg className="w-5 h-5" viewBox="0 0 24 24">
              <path
                fill="#000000"
                d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
              />
              <path
                fill="#000000"
                d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
              />
              <path
                fill="#000000"
                d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
              />
              <path
                fill="#000000"
                d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
              />
            </svg>
            Sign {isSignUp ? 'up' : 'in'} with Google
          </button>

          <div className="mt-6 text-center">
            <button
              onClick={() => setIsSignUp(!isSignUp)}
              className="text-black hover:text-brutal-pink font-bold uppercase underline decoration-2 underline-offset-4"
            >
              {isSignUp
                ? 'Already have an account? Sign In'
                : "Don't have an account? Sign Up"}
            </button>
          </div>
        </motion.div>
      </div>
    </div>
  )
}
