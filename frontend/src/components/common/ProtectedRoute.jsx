/**
 * Wraps pages that require authentication. Redirects to /login if no
 * user session exists; shows a loader while session is being restored.
 */
import { Navigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import Loader from "./Loader";

export default function ProtectedRoute({ children }) {
  const { user, loading } = useAuth();

  if (loading) return <Loader fullScreen />;
  if (!user) return <Navigate to="/login" replace />;

  return children;
}
