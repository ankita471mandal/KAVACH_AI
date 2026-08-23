/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        base: {
          bg: '#0B1220',
          panel: '#121A2B',
          panel2: '#182338',
          border: '#25314A',
          text: '#E7ECF5',
          muted: '#8C9BB5',
        },
        critical: { DEFAULT: '#E5484D', bg: '#3A1518', text: '#FF9A9D' },
        high: { DEFAULT: '#F2994A', bg: '#3A2712', text: '#FFC182' },
        moderate: { DEFAULT: '#F2C94C', bg: '#3A3212', text: '#FFE18C' },
        safe: { DEFAULT: '#27AE60', bg: '#123A24', text: '#8CFFC0' },
        info: { DEFAULT: '#2F80ED', bg: '#12233A', text: '#8CC0FF' },
        inactive: { DEFAULT: '#5A6B87', bg: '#1A2233', text: '#9AA7BD' },
      },
      fontFamily: {
        display: ['"Space Grotesk"', 'system-ui', 'sans-serif'],
        body: ['"Inter"', 'system-ui', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'monospace'],
      },
      boxShadow: {
        panel: '0 1px 0 0 rgba(255,255,255,0.03) inset, 0 8px 24px -12px rgba(0,0,0,0.6)',
      },
      animation: {
        'pulse-live': 'pulse-live 1.6s ease-in-out infinite',
        'slide-in': 'slide-in 0.25s ease-out',
      },
      keyframes: {
        'pulse-live': {
          '0%, 100%': { opacity: 1 },
          '50%': { opacity: 0.35 },
        },
        'slide-in': {
          from: { opacity: 0, transform: 'translateY(-6px)' },
          to: { opacity: 1, transform: 'translateY(0)' },
        },
      },
    },
  },
  plugins: [],
}
