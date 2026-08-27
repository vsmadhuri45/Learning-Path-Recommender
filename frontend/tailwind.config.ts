import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./lib/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        canvas: "#F7F6F3",
        surface: "#FFFFFF",
        ink: "#191F33",
        muted: "#66708A",
        line: "#E8E6E0",
        brand: "#4F46E5",
        "brand-soft": "#ECEBFB",
        gold: "#E8890C",
        "gold-soft": "#FBEFDC",
      },
      fontFamily: {
        display: ['"Space Grotesk"', "system-ui", "sans-serif"],
        sans: ['"Inter"', "system-ui", "sans-serif"],
      },
      keyframes: {
        pop: {
          "0%": { opacity: "0", transform: "scale(0.6)" },
          "60%": { transform: "scale(1.08)" },
          "100%": { opacity: "1", transform: "scale(1)" },
        },
        fadeUp: {
          "0%": { opacity: "0", transform: "translateY(8px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        grow: {
          "0%": { transform: "scaleY(0)" },
          "100%": { transform: "scaleY(1)" },
        },
        haloPulse: {
          "0%, 100%": { boxShadow: "0 0 0 0 rgba(232,137,12,0.35)" },
          "50%": { boxShadow: "0 0 0 8px rgba(232,137,12,0)" },
        },
      },
      animation: {
        pop: "pop 0.4s cubic-bezier(0.34,1.56,0.64,1)",
        "fade-up": "fadeUp 0.35s ease-out",
        grow: "grow 0.45s ease-out",
        halo: "haloPulse 2.4s ease-in-out infinite",
      },
    },
  },
  plugins: [],
};

export default config;
