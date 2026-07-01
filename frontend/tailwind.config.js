/** Tailwind config with a dark/light theme via class strategy */
module.exports = {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        primary: {
          50: "#eef4ff", 100: "#d9e6ff", 500: "#3b6fed",
          600: "#2f5bd1", 700: "#274aac",
        },
        danger: { 500: "#ef4444", 600: "#dc2626" },
        success: { 500: "#22c55e", 600: "#16a34a" },
        surface: {
          light: "#ffffff", dark: "#111827",
        },
      },
    },
  },
  plugins: [],
};
