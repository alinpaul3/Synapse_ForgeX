/** @type {import('tailwindcss').Config} */
export default {
  content: ["./src/**/*.{ts,tsx,html}"],
  theme: {
    extend: {
      colors: {
        primary: {
          50: "#f0f4ff",
          100: "#e0eaff",
          500: "#4f6ef7",
          600: "#3b5bdb",
          700: "#2c46c7",
        },
        ocean: {
          openness: "#8b5cf6",
          conscientiousness: "#3b82f6",
          extraversion: "#f59e0b",
          agreeableness: "#10b981",
          neuroticism: "#ef4444",
        },
      },
    },
  },
  plugins: [],
};
