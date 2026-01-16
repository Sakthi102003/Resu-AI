import React from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuthStore } from '../Services/auth'
import { motion } from 'framer-motion'
import Marquee from '../components/Marquee'

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

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1
      }
    }
  }

  const itemVariants = {
    hidden: { opacity: 0, y: 50 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { type: "spring", stiffness: 100 }
    }
  }

  return (
    <div className="min-h-screen relative overflow-x-hidden font-sans selection:bg-cyber-primary selection:text-black">
      {/* Background Blobs */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none -z-10 bg-cyber-background">
        <div className="absolute top-[-10%] left-[-10%] w-[500px] h-[500px] bg-cyber-secondary rounded-full mix-blend-screen filter blur-[100px] opacity-20 animate-blob"></div>
        <div className="absolute top-[20%] right-[-10%] w-[500px] h-[500px] bg-cyber-primary rounded-full mix-blend-screen filter blur-[100px] opacity-20 animate-blob animation-delay-2000"></div>
        <div className="absolute bottom-[-10%] left-[20%] w-[500px] h-[500px] bg-cyber-accent rounded-full mix-blend-screen filter blur-[100px] opacity-20 animate-blob animation-delay-4000"></div>
        <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-20 brightness-100 contrast-150"></div>
      </div>

      {/* Navigation */}
      <motion.nav
        initial={{ y: -100 }}
        animate={{ y: 0 }}
        transition={{ type: "spring", stiffness: 100, damping: 20 }}
        className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 border-b border-white/5 ${isScrolled ? 'bg-cyber-background/80 backdrop-blur-md shadow-lg shadow-cyber-primary/5' : 'bg-transparent backdrop-blur-sm'
          }`}
      >
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <Link to="/" className="flex items-center space-x-3 group cursor-pointer">
              <motion.div
                whileHover={{ rotate: 180, scale: 1.1 }}
                transition={{ duration: 0.5 }}
                className="w-10 h-10 bg-gradient-to-tr from-cyber-primary to-cyber-secondary flex items-center justify-center rounded-lg shadow-glow-sm"
              >
                <span className="text-black font-black text-xl">R</span>
              </motion.div>
              <span className="text-2xl font-bold text-white tracking-tighter group-hover:text-cyber-primary transition-colors">
                ResuAI
              </span>
            </Link>
            <div className="flex items-center space-x-4">
              {isAuthenticated ? (
                <Link to="/dashboard">
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    className="glass-button px-6 py-2 rounded-full text-white font-medium text-sm flex items-center gap-2 hover:border-cyber-primary/50 hover:shadow-glow-sm"
                  >
                    Dashboard
                  </motion.button>
                </Link>
              ) : (
                <>
                  <Link
                    to="/login"
                    className="hidden sm:block px-6 py-2 text-gray-300 hover:text-white font-medium transition-colors"
                  >
                    Login
                  </Link>
                  <Link to="/login?signup=true">
                    <motion.button
                      whileHover={{ scale: 1.05, boxShadow: "0 0 20px rgba(0, 242, 255, 0.4)" }}
                      whileTap={{ scale: 0.95 }}
                      className="px-6 py-2 bg-gradient-to-r from-cyber-primary to-cyber-secondary text-black font-bold rounded-full shadow-glow-sm hover:brightness-110 transition-all"
                    >
                      Get Started
                    </motion.button>
                  </Link>
                </>
              )}
            </div>
          </div>
        </div>
      </motion.nav>

      {/* Hero Section */}
      <section className="container mx-auto px-6 pt-32 pb-12 relative min-h-[90vh] flex items-center">
        <div className="max-w-7xl mx-auto w-full">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            {/* Left Content */}
            <motion.div
              variants={containerVariants}
              initial="hidden"
              animate="visible"
              className="text-left space-y-8 relative z-10"
            >
              <motion.div variants={itemVariants} className="inline-flex items-center space-x-2 glass-card px-4 py-2 rounded-full border border-white/10">
                <span className="w-2 h-2 rounded-full bg-cyber-green animate-pulse shadow-[0_0_10px_#4ade80]"></span>
                <span className="text-cyber-green font-mono text-xs uppercase tracking-widest">Next Gen Resume Builder</span>
              </motion.div>

              <motion.h1 variants={itemVariants} className="text-6xl md:text-7xl font-bold text-white leading-tight tracking-tight">
                Craft Your <br />
                <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyber-primary via-cyber-secondary to-cyber-accent animate-gradient bg-[length:200%_auto]">
                  Digital Future
                </span>
              </motion.h1>

              <motion.p variants={itemVariants} className="text-lg text-gray-400 max-w-lg leading-relaxed border-l-2 border-cyber-primary/50 pl-6">
                Forge professional, ATS-optimized resumes with our AI-powered engine.
                Stand out in the digital noise.
              </motion.p>

              <motion.div variants={itemVariants} className="flex flex-col sm:flex-row items-center gap-6 pt-4">
                <Link to={isAuthenticated ? "/dashboard" : "/login?signup=true"}>
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    className="group px-8 py-4 bg-white text-black rounded-lg font-bold text-lg flex items-center gap-3 hover:bg-cyber-primary transition-colors shadow-[0_0_20px_rgba(255,255,255,0.3)]"
                  >
                    <span>{isAuthenticated ? "Go to Dashboard" : "Start Building"}</span>
                    <motion.span
                      animate={{ x: [0, 5, 0] }}
                      transition={{ repeat: Infinity, duration: 1.5 }}
                    >
                      →
                    </motion.span>
                  </motion.button>
                </Link>
                <div className="flex items-center gap-4 text-sm font-mono text-gray-500">
                  <span className="flex items-center gap-2">
                    <span className="w-1.5 h-1.5 bg-cyber-primary rounded-full"></span> AI Powered
                  </span>
                  <span className="flex items-center gap-2">
                    <span className="w-1.5 h-1.5 bg-cyber-secondary rounded-full"></span> ATS Friendly
                  </span>
                </div>
              </motion.div>

              {/* Stats */}
              <motion.div variants={itemVariants} className="flex gap-12 pt-8 border-t border-white/10">
                <div>
                  <div className="text-3xl font-bold text-white mb-1">10k+</div>
                  <div className="text-xs text-cyber-primary uppercase tracking-wider font-mono">Resumes Built</div>
                </div>
                <div>
                  <div className="text-3xl font-bold text-white mb-1">95%</div>
                  <div className="text-xs text-cyber-secondary uppercase tracking-wider font-mono">Success Rate</div>
                </div>
              </motion.div>
            </motion.div>

            {/* Right Content - Visual Element */}
            <motion.div
              initial={{ opacity: 0, x: 100, scale: 0.8 }}
              animate={{ opacity: 1, x: 0, scale: 1 }}
              transition={{ type: "spring", duration: 1.5 }}
              className="relative hidden md:block perspective-1000"
            >
              <motion.div
                animate={{
                  y: [-15, 15, -15],
                  rotateX: [5, -5, 5],
                  rotateY: [-5, 5, -5]
                }}
                transition={{ repeat: Infinity, duration: 8, ease: "easeInOut" }}
                className="relative glass-card p-1 rounded-2xl border border-white/10 shadow-2xl shadow-cyber-primary/10"
              >
                {/* Mock Resume UI */}
                <div className="bg-[#0a0a0a] rounded-xl p-8 aspect-[3/4] overflow-hidden relative">
                  <div className="absolute inset-0 bg-gradient-to-b from-cyber-primary/5 to-transparent pointer-events-none"></div>

                  {/* Header */}
                  <div className="flex gap-6 mb-8">
                    <div className="w-20 h-20 rounded-xl bg-gradient-to-br from-gray-800 to-black border border-white/10"></div>
                    <div className="space-y-3 flex-1">
                      <div className="h-6 w-3/4 bg-white/10 rounded animate-pulse"></div>
                      <div className="h-4 w-1/2 bg-white/5 rounded"></div>
                    </div>
                  </div>

                  {/* Lines */}
                  <div className="space-y-4">
                    {[1, 2, 3, 4].map((i) => (
                      <div key={i} className="space-y-2">
                        <div className="h-3 w-full bg-white/5 rounded"></div>
                        <div className="h-3 w-5/6 bg-white/5 rounded"></div>
                      </div>
                    ))}
                  </div>

                  {/* Floating Elements */}
                  <motion.div
                    animate={{ y: [0, -10, 0] }}
                    transition={{ repeat: Infinity, duration: 4, delay: 1 }}
                    className="absolute top-20 right-[-20px] glass-card px-4 py-2 rounded-lg border border-cyber-accent/30 text-cyber-accent text-xs font-bold shadow-lg shadow-cyber-accent/20"
                  >
                    Optimization: 98%
                  </motion.div>

                  <motion.div
                    animate={{ y: [0, -10, 0] }}
                    transition={{ repeat: Infinity, duration: 4, delay: 0 }}
                    className="absolute bottom-20 left-[-20px] glass-card px-4 py-2 rounded-lg border border-cyber-primary/30 text-cyber-primary text-xs font-bold shadow-lg shadow-cyber-primary/20"
                  >
                    Skills Matched
                  </motion.div>
                </div>
              </motion.div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Marquee Section */}
      <div className="border-y border-white/10 bg-black/30 backdrop-blur-sm z-20 relative transform -rotate-1 skew-x-12 scale-110 origin-left my-20">
        <Marquee
          items={["Future Ready", "AI Enhanced", "Cyber Secure", "Career Boost", "Next Level"]}
          speed={30}
          className="bg-transparent text-white/50"
        />
      </div>

      {/* Features Section */}
      <section id="features" className="py-24 relative z-0">
        <div className="container mx-auto px-6">
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-20 space-y-4"
          >
            <h2 className="text-4xl md:text-6xl font-bold text-white mb-6">
              Upgrade Your <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyber-primary to-cyber-secondary">CareerOS</span>
            </h2>
            <p className="text-gray-400 max-w-2xl mx-auto">
              Advanced tools for the modern professional. Built with precision, powered by intelligence.
            </p>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-6 max-w-7xl mx-auto">
            {[
              { title: 'Neural Engine', icon: '🧠', color: 'text-cyber-primary', desc: 'Deep learning models analyze and enhance your professional story.' },
              { title: 'ATS Bypass', icon: '🛡️', color: 'text-cyber-accent', desc: 'Algorithm-friendly formats designed to pass automated screenings.' },
              { title: 'Smart Match', icon: '⚡', color: 'text-cyber-secondary', desc: 'Real-time job matching based on your unique skill signature.' },
              { title: 'AI Assistant', icon: '🤖', color: 'text-cyber-primary', desc: '24/7 intelligent chat support for career guidance.' },
              { title: 'Holographic Templates', icon: '💠', color: 'text-cyber-secondary', desc: 'Stand out with next-gen visual layouts.' },
              { title: 'Multi-Format Export', icon: '💾', color: 'text-cyber-accent', desc: 'Universal compatibility with PDF, DOCX, and JSON exports.' },
            ].map((feature, idx) => (
              <motion.div
                key={idx}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: idx * 0.1 }}
                whileHover={{ y: -5, backgroundColor: "rgba(255,255,255,0.05)" }}
                className="group glass-card p-8 rounded-2xl border border-white/5 transition-all duration-300 hover:border-cyber-primary/30 hover:shadow-glow-sm cursor-pointer"
              >
                <div className="mb-6 w-12 h-12 rounded-lg bg-white/5 flex items-center justify-center text-2xl group-hover:scale-110 transition-transform duration-300">
                  {feature.icon}
                </div>
                <h3 className={`text-xl font-bold text-white mb-3 group-hover:${feature.color} transition-colors`}>{feature.title}</h3>
                <p className="text-gray-400 text-sm leading-relaxed">
                  {feature.desc}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24 relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-b from-transparent to-cyber-primary/5"></div>
        <div className="container mx-auto px-6 relative z-10">
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            whileInView={{ scale: 1, opacity: 1 }}
            viewport={{ once: true }}
            className="max-w-4xl mx-auto glass-card rounded-3xl p-12 text-center border border-white/10 shadow-glow-lg overflow-hidden"
          >
            <div className="relative z-10 space-y-8">
              <h2 className="text-4xl md:text-5xl font-bold text-white">
                Initialize Your Sequence
              </h2>
              <p className="text-xl text-gray-400 max-w-2xl mx-auto">
                Join the network of professionals who have upgraded their career trajectory.
              </p>

              <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-8">
                <Link to={isAuthenticated ? "/dashboard" : "/login?signup=true"}>
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    className="px-12 py-4 bg-white text-black rounded-full font-bold text-lg hover:bg-cyber-primary transition-colors shadow-glow"
                  >
                    {isAuthenticated ? "Enter Dashboard" : "Get Started Free"}
                  </motion.button>
                </Link>
              </div>
            </div>

            {/* Decorative background grid */}
            <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.03)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.03)_1px,transparent_1px)] bg-[size:40px_40px] [mask-image:radial-gradient(ellipse_at_center,black,transparent_70%)] pointer-events-none"></div>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-white/10 bg-black/50 backdrop-blur-md pt-20 pb-10">
        <div className="container mx-auto px-6">
          <div className="grid md:grid-cols-4 gap-12 mb-12">
            <div className="space-y-4">
              <div className="flex items-center space-x-3">
                <div className="w-8 h-8 rounded bg-gradient-to-br from-cyber-primary to-cyber-secondary flex items-center justify-center">
                  <span className="text-black font-bold text-sm">R</span>
                </div>
                <span className="text-xl font-bold text-white">ResuAI</span>
              </div>
              <p className="text-gray-500 text-sm">
                Next-generation career tools for the digital age.
              </p>
            </div>

            {['Product', 'Company', 'Legal'].map((col) => (
              <div key={col}>
                <h3 className="text-white font-bold mb-4">{col}</h3>
                <ul className="space-y-2 text-gray-500 text-sm">
                  <li><a href="#" className="hover:text-cyber-primary transition-colors">Link 1</a></li>
                  <li><a href="#" className="hover:text-cyber-primary transition-colors">Link 2</a></li>
                  <li><a href="#" className="hover:text-cyber-primary transition-colors">Link 3</a></li>
                </ul>
              </div>
            ))}
          </div>

          <div className="border-t border-white/5 pt-8 flex flex-col md:flex-row items-center justify-between text-sm text-gray-600">
            <p>&copy; 2025 ResuAI. System Status: Online.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default Home
