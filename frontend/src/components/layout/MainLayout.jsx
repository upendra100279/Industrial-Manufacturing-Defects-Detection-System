/**
 * Shell layout for all authenticated pages: fixed Sidebar + Topbar,
 * with <Outlet /> rendering the active page. Topbar title is derived
 * from the current route.
 */
import { Outlet, useLocation } from "react-router-dom";
import Sidebar from "./Sidebar";
import Topbar from "./Topbar";

const TITLES = {
  "/dashboard": "Dashboard",
  "/detection": "Defect Detection",
  "/analytics": "Analytics",
  "/history": "Inspection History",
  "/settings": "Settings",
};

export default function MainLayout() {
  const location = useLocation();
  const title = TITLES[location.pathname] || "Dashboard";

  return (
    <div className="min-h-screen">
      <Sidebar />
      <div className="ml-64 flex flex-col min-h-screen">
        <Topbar title={title} />
        <main className="flex-1 p-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
