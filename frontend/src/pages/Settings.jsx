/**
 * Settings page — profile info, theme toggle, confidence threshold preference.
 */
import { useState } from "react";
import toast from "react-hot-toast";
import { Sun, Moon } from "lucide-react";
import { useAuth } from "../context/AuthContext";
import { useTheme } from "../context/ThemeContext";

export default function Settings() {
  const { user } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const [confidenceThreshold, setConfidenceThreshold] = useState(
    localStorage.getItem("confidence_threshold") || "0.4"
  );

  const handleThresholdSave = () => {
    localStorage.setItem("confidence_threshold", confidenceThreshold);
    toast.success("Preference saved");
  };

  return (
    <div className="max-w-2xl space-y-6">
      <div className="bg-white dark:bg-gray-800 rounded-xl p-5 shadow-sm border border-gray-100 dark:border-gray-700">
        <h3 className="font-semibold mb-4">Profile</h3>
        <div className="grid grid-cols-2 gap-4 text-sm">
          <div>
            <p className="text-gray-500 dark:text-gray-400">Username</p>
            <p className="font-medium">{user?.username}</p>
          </div>
          <div>
            <p className="text-gray-500 dark:text-gray-400">Email</p>
            <p className="font-medium">{user?.email}</p>
          </div>
          <div>
            <p className="text-gray-500 dark:text-gray-400">Full Name</p>
            <p className="font-medium">{user?.full_name || "—"}</p>
          </div>
          <div>
            <p className="text-gray-500 dark:text-gray-400">Member Since</p>
            <p className="font-medium">{new Date(user?.created_at).toLocaleDateString()}</p>
          </div>
        </div>
      </div>

      <div className="bg-white dark:bg-gray-800 rounded-xl p-5 shadow-sm border border-gray-100 dark:border-gray-700">
        <h3 className="font-semibold mb-4">Appearance</h3>
        <div className="flex items-center justify-between">
          <p className="text-sm text-gray-600 dark:text-gray-300">Theme</p>
          <button
            onClick={toggleTheme}
            className="flex items-center gap-2 px-3 py-1.5 rounded-lg border border-gray-300 dark:border-gray-600 text-sm"
          >
            {theme === "light" ? <Moon size={14} /> : <Sun size={14} />}
            {theme === "light" ? "Switch to Dark" : "Switch to Light"}
          </button>
        </div>
      </div>

      <div className="bg-white dark:bg-gray-800 rounded-xl p-5 shadow-sm border border-gray-100 dark:border-gray-700">
        <h3 className="font-semibold mb-4">Detection Preferences</h3>
        <label className="block text-sm text-gray-600 dark:text-gray-300 mb-2">
          Display Confidence Threshold: {(confidenceThreshold * 100).toFixed(0)}%
        </label>
        <input
          type="range"
          min="0.1"
          max="0.9"
          step="0.05"
          value={confidenceThreshold}
          onChange={(e) => setConfidenceThreshold(e.target.value)}
          className="w-full accent-primary-500"
        />
        <button
          onClick={handleThresholdSave}
          className="mt-3 bg-primary-500 hover:bg-primary-600 text-white text-sm font-medium px-4 py-2 rounded-lg"
        >
          Save Preference
        </button>
      </div>
    </div>
  );
}
