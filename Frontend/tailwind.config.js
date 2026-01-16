/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        cyber: {
          background: '#030014', // Deep space blue/black
          primary: '#00f2ff',    // Neon Cyan
          secondary: '#b026ff',  // Neon Purple
          accent: '#ff0055',     // Neon Pink
          muted: '#94a3b8',
          glass: 'rgba(255, 255, 255, 0.03)',
          glassBorder: 'rgba(255, 255, 255, 0.1)',
        }
      },
      boxShadow: {
        'glow-sm': '0 0 10px rgba(0, 242, 255, 0.3)',
        'glow': '0 0 20px rgba(176, 38, 255, 0.4)',
        'glow-lg': '0 0 30px rgba(255, 0, 85, 0.5)',
        'glass': '0 8px 32px 0 rgba(0, 0, 0, 0.37)',
      },
      fontFamily: {
        sans: ['"Space Grotesk"', 'Inter', 'system-ui', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'monospace'],
      },
      backgroundImage: {
        'cyber-gradient': 'linear-gradient(to right bottom, #030014, #0f0728, #030014)',
        'glass-gradient': 'linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.03) 100%)',
      },
      animation: {
        'pulse-slow': 'pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'float': 'float 6s ease-in-out infinite',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-20px)' },
        }
      }
    },
  },
  plugins: [],
}
