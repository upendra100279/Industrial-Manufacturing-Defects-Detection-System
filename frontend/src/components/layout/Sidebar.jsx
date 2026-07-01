/**
 * Fixed sidebar navigation. Active route is highlighted via NavLink's
 * built-in isActive styling.
 */
import { NavLink } from "react-router-dom";
import {
  LayoutDashboard, ScanSearch, BarChart3, History, Settings, ScanLine,
} from "lucide-react";

const NAV_ITEMS = [
  { to: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { to: "/detection", label: "Detection", icon: ScanSearch },
  { to: "/analytics", label: "Analytics", icon: BarChart3 },
  { to: "/history", label: "History", icon: History },
  { to: "/settings", label: "Settings", icon: Settings },
];

export default function Sidebar() {
  return (
    <aside className="w-64 h-screen fixed left-0 top-0 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 flex flex-col">
      <div className="flex items-center gap-2 px-6 py-5 border-b border-gray-200 dark:border-gray-700">
        <div className="bg-primary-500 p-2 rounded-lg">
          <ScanLine className="text-white" size={20} />
        </div>
        <span className="font-bold text-lg">DefectAI</span>
      </div>

      <nav className="flex-1 px-3 py-4 space-y-1">
        {NAV_ITEMS.map(({ to, label, icon: Icon }) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition ${
                isActive
                  ? "bg-primary-500 text-white"
                  : "text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
              }`
            }
          >
            <Icon size={18} />
            {label}
          </NavLink>
        ))}
      </nav>

      <div className="px-6 py-4 text-xs text-gray-400 border-t border-gray-200 dark:border-gray-700">
        v1.0.0 — Industrial Defect Detection
      </div>
    </aside>
  );
}
