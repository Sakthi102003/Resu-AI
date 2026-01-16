import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { ArrowLeft, Save, User, Mail, Link as LinkIcon, Github, Globe } from 'lucide-react'
import toast from 'react-hot-toast'
import { useAuthStore } from '../Services/auth'

export default function Profile() {
  const navigate = useNavigate()
  const { user, updateProfile } = useAuthStore()

  const [formData, setFormData] = useState({
    full_name: user?.full_name || '',
    email: user?.email || '',
    phone: user?.phone || '',
    linkedin: user?.linkedin || '',
    github: user?.github || '',
    portfolio: user?.portfolio || '',
  })

  const [isLoading, setIsLoading] = useState(false)

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setIsLoading(true)

    const result = await updateProfile(formData)

    if (result.success) {
      toast.success('Profile updated successfully!')
    } else {
      toast.error(result.error || 'Failed to update profile')
    }

    setIsLoading(false)
  }

  return (
    <div className="min-h-screen bg-transparent font-sans">
      {/* Header */}
      <header className="fixed top-0 left-0 right-0 z-40 bg-cyber-background/80 backdrop-blur-md border-b border-white/10">
        <div className="max-w-4xl mx-auto px-4 py-4 flex items-center justify-between gap-4">
          <div className="flex items-center gap-4">
            <button
              onClick={() => navigate('/dashboard')}
              className="p-2 hover:bg-white/10 rounded-lg transition text-gray-400 hover:text-white"
            >
              <ArrowLeft className="w-5 h-5" />
            </button>
            <div>
              <h1 className="text-xl font-bold text-white">Profile Settings</h1>
              <p className="text-sm text-gray-400 font-mono">Manage your identity parameters</p>
            </div>
          </div>
          <button
            onClick={() => navigate('/')}
            className="text-lg font-bold text-transparent bg-clip-text bg-gradient-to-r from-cyber-primary to-cyber-secondary hover:brightness-110 transition-all hidden sm:block"
          >
            ResuAI
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-4 py-24">
        <div className="glass-card rounded-2xl p-8 border border-white/10">
          <div className="flex items-center gap-6 mb-8 pb-8 border-b border-white/10">
            <div className="w-20 h-20 rounded-full bg-gradient-to-br from-cyber-primary to-cyber-secondary flex items-center justify-center shadow-glow">
              <span className="text-3xl font-black text-black">{formData.full_name?.charAt(0) || 'U'}</span>
            </div>
            <div>
              <h2 className="text-2xl font-bold text-white">{formData.full_name || 'User'}</h2>
              <p className="text-cyber-primary font-mono text-sm">Level {Math.floor(Math.random() * 10) + 1} Developer</p>
            </div>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="grid md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-bold text-gray-400 mb-2 uppercase tracking-wider flex items-center gap-2">
                  <User className="w-4 h-4 text-cyber-primary" /> Full Name
                </label>
                <input
                  type="text"
                  name="full_name"
                  value={formData.full_name}
                  onChange={handleChange}
                  className="w-full bg-black/40 border border-white/10 rounded-lg py-3 px-4 text-white focus:outline-none focus:border-cyber-primary focus:ring-1 focus:ring-cyber-primary transition-all placeholder-gray-600 font-mono"
                  placeholder="John Doe"
                />
              </div>

              <div>
                <label className="block text-sm font-bold text-gray-400 mb-2 uppercase tracking-wider flex items-center gap-2">
                  <Mail className="w-4 h-4 text-cyber-primary" /> Email
                </label>
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  className="w-full bg-black/40 border border-white/10 rounded-lg py-3 px-4 text-gray-500 cursor-not-allowed font-mono"
                  placeholder="you@example.com"
                  disabled
                />
                <p className="text-xs text-gray-600 mt-1 pl-1">
                  Identity locked. Cannot be modified.
                </p>
              </div>
            </div>

            <div>
              <label className="block text-sm font-bold text-gray-400 mb-2 uppercase tracking-wider">
                Phone
              </label>
              <input
                type="tel"
                name="phone"
                value={formData.phone}
                onChange={handleChange}
                className="w-full bg-black/40 border border-white/10 rounded-lg py-3 px-4 text-white focus:outline-none focus:border-cyber-primary focus:ring-1 focus:ring-cyber-primary transition-all placeholder-gray-600 font-mono"
                placeholder="+1 (555) 123-4567"
              />
            </div>

            <div className="space-y-4 pt-4 border-t border-white/10">
              <h3 className="text-white font-bold text-lg mb-4">Digital Presence</h3>

              <div>
                <label className="block text-sm font-bold text-gray-400 mb-2 uppercase tracking-wider flex items-center gap-2">
                  <LinkIcon className="w-4 h-4 text-cyber-secondary" /> LinkedIn URL
                </label>
                <input
                  type="url"
                  name="linkedin"
                  value={formData.linkedin}
                  onChange={handleChange}
                  className="w-full bg-black/40 border border-white/10 rounded-lg py-3 px-4 text-white focus:outline-none focus:border-cyber-secondary focus:ring-1 focus:ring-cyber-secondary transition-all placeholder-gray-600 font-mono"
                  placeholder="https://linkedin.com/in/yourname"
                />
              </div>

              <div>
                <label className="block text-sm font-bold text-gray-400 mb-2 uppercase tracking-wider flex items-center gap-2">
                  <Github className="w-4 h-4 text-cyber-secondary" /> GitHub URL
                </label>
                <input
                  type="url"
                  name="github"
                  value={formData.github}
                  onChange={handleChange}
                  className="w-full bg-black/40 border border-white/10 rounded-lg py-3 px-4 text-white focus:outline-none focus:border-cyber-secondary focus:ring-1 focus:ring-cyber-secondary transition-all placeholder-gray-600 font-mono"
                  placeholder="https://github.com/yourname"
                />
              </div>

              <div>
                <label className="block text-sm font-bold text-gray-400 mb-2 uppercase tracking-wider flex items-center gap-2">
                  <Globe className="w-4 h-4 text-cyber-secondary" /> Portfolio URL
                </label>
                <input
                  type="url"
                  name="portfolio"
                  value={formData.portfolio}
                  onChange={handleChange}
                  className="w-full bg-black/40 border border-white/10 rounded-lg py-3 px-4 text-white focus:outline-none focus:border-cyber-secondary focus:ring-1 focus:ring-cyber-secondary transition-all placeholder-gray-600 font-mono"
                  placeholder="https://yourportfolio.com"
                />
              </div>
            </div>

            <div className="flex gap-4 pt-8">
              <button
                type="submit"
                disabled={isLoading}
                className="flex-1 bg-cyber-primary text-black font-bold uppercase tracking-wider py-3 rounded-lg hover:shadow-glow hover:bg-cyan-300 transition-all flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <Save className="w-4 h-4" />
                {isLoading ? 'Saving...' : 'Save Changes'}
              </button>
              <button
                type="button"
                onClick={() => navigate('/dashboard')}
                className="px-8 py-3 rounded-lg border border-white/20 text-white font-bold uppercase tracking-wider hover:bg-white/10 transition-all"
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      </main>
    </div>
  )
}
