/** @type {import('tailwindcss').Config} */
export default {
  content: ["./gemini_app/**/*.{html,js}", "./templates/**/*.html", "./gemini_app/templates/base.html", "./gemini_app/templates/quiz.html"],
  theme: {
    extend: {
      colors: {
        'deep-space': '#120F1A',
        'dark-matter': '#251E38',
        'code-white': '#EAEAF2',
        'ghost-gray': '#9A92B3',
        'void-purple': '#7F5AF0',
        'deep-void': '#6844E1',
        'neon-mint': '#05F2AF',
        'hot-pink': '#F72585',
        'cyber-blue': '#2CB6F6',
      },
    },
  },
  plugins: [],
  safelist: [
    // Asegura que estas clases siempre estén incluidas en el build
    'bg-deep-space',
    'bg-dark-matter',
    'text-code-white',
    'text-ghost-gray',
    'text-void-purple',
    'border-void-purple',
    'bg-void-purple',
    'bg-neon-mint/10',
    'border-neon-mint',
    'text-neon-mint',
    'bg-hot-pink/10',
    'border-hot-pink',
    'text-hot-pink',
  ]
}