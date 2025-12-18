import React from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuthStore } from '../Services/auth'

const Home = () => {
  const navigate = useNavigate()
  const { isAuthenticated } = useAuthStore()
  const [isScrolled, setIsScrolled] = React.useState(false)

  // Handle scroll effect for navbar
  React.useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20)
    }
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  return (
    <div className="min-h-screen bg-brutal-yellow relative overflow-hidden font-sans">
      {/* Navigation */}
      <nav className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 border-b-4 border-black ${
        isScrolled ? 'bg-white shadow-neo' : 'bg-white'
      }`}>
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <Link to="/" className="flex items-center space-x-3 group cursor-pointer">
              <div className="w-12 h-12 bg-black flex items-center justify-center shadow-neo-sm transition-transform duration-300 hover:-translate-y-1 hover:translate-x-1 hover:shadow-none border-2 border-black">
                <span className="text-white font-bold text-2xl">R</span>
              </div>
              <span className="text-3xl font-black text-black uppercase tracking-tighter">
                ResuAI
              </span>
            </Link>
            <div className="flex items-center space-x-4">
              {isAuthenticated ? (
                <Link
                  to="/dashboard"
                  className="px-6 py-3 bg-black text-white border-2 border-black hover:bg-white hover:text-black hover:shadow-neo transition-all duration-300 font-bold uppercase tracking-wider"
                >
                  Dashboard
                </Link>
              ) : (
                <>
                  <Link
                    to="/login"
                    className="px-6 py-3 text-black font-bold hover:underline decoration-4 underline-offset-4 uppercase tracking-wider"
                  >
                    Login
                  </Link>
                  <Link
                    to="/login?signup=true"
                    className="px-6 py-3 bg-brutal-pink text-black border-2 border-black shadow-neo hover:shadow-none hover:translate-x-[2px] hover:translate-y-[2px] transition-all duration-300 font-bold uppercase tracking-wider"
                  >
                    Get Started
                  </Link>
                </>
              )}
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="container mx-auto px-6 pt-32 pb-20 relative">
        <div className="max-w-7xl mx-auto">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            {/* Left Content */}
            <div className="text-left space-y-8 animate-fade-in-up">
              <div className="inline-flex items-center space-x-2 bg-white border-4 border-black px-6 py-3 shadow-neo transform -rotate-2 hover:rotate-0 transition-transform duration-200">
                <span className="w-4 h-4 bg-brutal-green border-2 border-black"></span>
                <span className="font-black font-mono text-base uppercase tracking-wider">AI-Powered Resume Builder</span>
              </div>
              
              <h1 className="text-6xl md:text-8xl font-black text-black leading-none tracking-tighter">
                BUILD YOUR
                <span className="block text-white text-stroke-black">
                  PERFECT RESUME
                </span>
              </h1>
              
              <p className="text-xl text-black font-bold border-l-8 border-black pl-6 py-4 bg-white border-y-4 border-r-4 shadow-neo-sm">
                Create professional, ATS-optimized resumes in minutes with AI-powered suggestions. 
                Stand out from the crowd and land your dream job faster.
              </p>
              
              <div className="flex flex-col sm:flex-row items-start gap-6 pt-8">
                <Link
                  to={isAuthenticated ? "/dashboard" : "/login?signup=true"}
                  className="group px-10 py-5 bg-black text-white border-4 border-black shadow-neo-lg hover:shadow-none hover:translate-x-[6px] hover:translate-y-[6px] transition-all duration-200 font-black text-xl flex items-center space-x-3 uppercase tracking-widest"
                >
                  <span>{isAuthenticated ? "Go to Dashboard" : "Create Resume"}</span>
                  <svg className="w-6 h-6 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                  </svg>
                </Link>
                <button
                  onClick={() => document.getElementById('features').scrollIntoView({ behavior: 'smooth' })}
                  className="group px-10 py-5 bg-white text-black border-4 border-black shadow-neo-lg hover:shadow-none hover:translate-x-[6px] hover:translate-y-[6px] transition-all duration-200 font-black text-xl flex items-center space-x-3 uppercase tracking-widest"
                >
                  <span>Learn More</span>
                  <svg className="w-6 h-6 group-hover:translate-y-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M19 14l-7 7m0 0l-7-7m7 7V3" />
                  </svg>
                </button>
              </div>

              {/* Stats */}
              <div className="flex items-center space-x-8 pt-8 border-t-4 border-black">
                <div>
                  <div className="text-5xl font-black text-black">10k+</div>
                  <div className="text-sm font-black font-mono uppercase bg-white px-2 border-2 border-black inline-block transform -rotate-2 shadow-neo-sm">Resumes Created</div>
                </div>
                <div>
                  <div className="text-5xl font-black text-black">95%</div>
                  <div className="text-sm font-black font-mono uppercase bg-white px-2 border-2 border-black inline-block transform rotate-2 shadow-neo-sm">Success Rate</div>
                </div>
                <div>
                  <div className="text-5xl font-black text-black">4.9/5</div>
                  <div className="text-sm font-black font-mono uppercase bg-white px-2 border-2 border-black inline-block transform -rotate-1 shadow-neo-sm">User Rating</div>
                </div>
              </div>
            </div>

            {/* Right Content - Visual Element */}
            <div className="relative animate-fade-in-up animation-delay-300 hidden md:block">
              <div className="relative bg-white border-4 border-black shadow-neo-lg p-8 transform rotate-2 hover:rotate-0 transition-transform duration-300">
                {/* Mock Resume Preview */}
                <div className="space-y-6 border-4 border-dashed border-gray-300 p-6">
                  <div className="flex items-center space-x-4">
                    <div className="w-20 h-20 bg-black border-4 border-black"></div>
                    <div className="flex-1 space-y-3">
                      <div className="h-6 bg-black w-3/4"></div>
                      <div className="h-4 bg-gray-400 w-1/2"></div>
                    </div>
                  </div>
                  <div className="space-y-3 pt-4 border-t-4 border-black">
                    <div className="h-4 bg-gray-300 w-full"></div>
                    <div className="h-4 bg-gray-300 w-full"></div>
                    <div className="h-4 bg-gray-300 w-5/6"></div>
                  </div>
                  <div className="pt-4 space-y-4">
                    <div className="h-6 bg-brutal-blue w-1/3 border-4 border-black"></div>
                    <div className="space-y-3">
                      <div className="h-4 bg-gray-300 w-full"></div>
                      <div className="h-4 bg-gray-300 w-4/5"></div>
                    </div>
                  </div>
                </div>
                
                {/* Floating badges */}
                <div className="absolute -top-6 -right-6 bg-brutal-pink text-black border-4 border-black px-6 py-3 font-black shadow-neo transform rotate-12">
                  ATS OPTIMIZED ✓
                </div>
                <div className="absolute -bottom-6 -left-6 bg-brutal-green text-black border-4 border-black px-6 py-3 font-black shadow-neo transform -rotate-12">
                  AI POWERED 🚀
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="bg-white border-t-4 border-black py-20">
        <div className="container mx-auto px-6">
          <div className="text-center mb-20 space-y-4">
            <div className="inline-block">
              <span className="bg-black text-white px-6 py-2 font-mono font-bold uppercase tracking-wider border-4 border-black shadow-neo-sm transform -rotate-1">
                Features
              </span>
            </div>
            <h2 className="text-5xl md:text-7xl font-black text-black uppercase leading-none">
              Everything You Need<br/>
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-brutal-blue to-brutal-purple" style={{ WebkitTextStroke: '2px black' }}>
                To Land The Job
              </span>
            </h2>
          </div>

          <div className="grid md:grid-cols-3 gap-8 max-w-7xl mx-auto">
            {[
              { title: 'AI-Powered Content', icon: '🤖', color: 'bg-brutal-blue', desc: 'Get intelligent suggestions and enhancements for your resume content.' },
              { title: 'ATS Optimization', icon: '🎯', color: 'bg-brutal-pink', desc: 'Ensure your resume passes Applicant Tracking Systems with our intelligent scoring.' },
              { title: 'Job Recommendations', icon: '💼', color: 'bg-brutal-green', desc: 'Get personalized job recommendations based on your skills and experience.' },
              { title: 'AI Chat Assistant', icon: '💬', color: 'bg-brutal-yellow', desc: 'Chat with our AI assistant to get instant help and suggestions.' },
              { title: 'Multiple Templates', icon: '📄', color: 'bg-brutal-purple', desc: 'Choose from professionally designed templates that make your resume stand out.' },
              { title: 'Export Options', icon: '📥', color: 'bg-brutal-red', desc: 'Download your resume in multiple formats including PDF and DOCX.' },
            ].map((feature, idx) => (
              <div key={idx} className="group bg-white p-8 border-4 border-black shadow-neo hover:shadow-none hover:translate-x-[4px] hover:translate-y-[4px] transition-all duration-200">
                <div className={`w-16 h-16 ${feature.color} border-4 border-black flex items-center justify-center mb-6 shadow-neo-sm`}>
                  <span className="text-3xl">{feature.icon}</span>
                </div>
                <h3 className="text-2xl font-black text-black mb-3 uppercase">{feature.title}</h3>
                <p className="text-black font-bold leading-relaxed border-l-4 border-black pl-4">
                  {feature.desc}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-brutal-blue border-t-4 border-black py-20">
        <div className="container mx-auto px-6">
          <div className="max-w-4xl mx-auto bg-white border-4 border-black shadow-neo-lg p-12 text-center relative overflow-hidden">
            <div className="relative z-10 space-y-8">
              <h2 className="text-4xl md:text-6xl font-black text-black uppercase leading-none">
                Ready to Build Your<br/>Perfect Resume?
              </h2>
              <p className="text-xl font-black text-black max-w-2xl mx-auto border-b-4 border-black pb-4 inline-block">
                Join thousands of job seekers who have successfully landed their dream jobs with ResuAI
              </p>
              
              <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-8">
                <Link
                  to={isAuthenticated ? "/dashboard" : "/login?signup=true"}
                  className="px-12 py-6 bg-black text-white border-4 border-black shadow-neo-lg hover:bg-brutal-yellow hover:text-black hover:shadow-none hover:translate-x-[6px] hover:translate-y-[6px] transition-all duration-200 font-black text-2xl uppercase tracking-widest"
                >
                  {isAuthenticated ? "Go to Dashboard" : "Get Started Now"}
                </Link>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-black text-white border-t-4 border-black pt-20 pb-10">
        <div className="container mx-auto px-6">
          <div className="grid md:grid-cols-4 gap-12 mb-12">
            <div className="space-y-4">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-white border-2 border-white flex items-center justify-center">
                  <span className="text-black font-black text-xl">R</span>
                </div>
                <span className="text-2xl font-black uppercase">ResuAI</span>
              </div>
              <p className="text-gray-400 font-mono text-sm">
                Build your perfect resume with AI-powered technology.
              </p>
            </div>
            
            {['Product', 'Company', 'Legal'].map((col) => (
              <div key={col}>
                <h3 className="text-lg font-bold mb-4 uppercase border-b-2 border-white/20 pb-2 inline-block">{col}</h3>
                <ul className="space-y-2 text-gray-400 font-mono text-sm">
                  <li><a href="#" className="hover:text-brutal-yellow hover:underline decoration-2 underline-offset-4">Link 1</a></li>
                  <li><a href="#" className="hover:text-brutal-yellow hover:underline decoration-2 underline-offset-4">Link 2</a></li>
                  <li><a href="#" className="hover:text-brutal-yellow hover:underline decoration-2 underline-offset-4">Link 3</a></li>
                </ul>
              </div>
            ))}
          </div>

          <div className="border-t-2 border-white/20 pt-8 flex flex-col md:flex-row items-center justify-between font-mono text-sm text-gray-400">
            <p>&copy; 2025 ResuAI. All rights reserved.</p>
            <div className="flex space-x-6 mt-4 md:mt-0">
              {/* Social Icons */}
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default Home
