/**
 * Global auth state — wraps the app, exposes user/token/login/logout,
 * and restores session from localStorage on reload.
 */
import { createContext, useContext, useState, useEffect } from "react";
import axiosClient from "../api/axiosClient";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (!token) {
      setLoading(false);
      return;
    }

    axiosClient
      .get("/auth/me")
      .then((res) => setUser(res.data))
      .catch(() => localStorage.removeItem("access_token"))
      .finally(() => setLoading(false));
  }, []);

  const login = async (username, password) => {
    const res = await axiosClient.post("/auth/login", { username, password });
    localStorage.setItem("access_token", res.data.access_token);
    const meRes = await axiosClient.get("/auth/me");
    setUser(meRes.data);
    return meRes.data;
  };

  const register = async (payload) => {
    await axiosClient.post("/auth/register", payload);
  };

  const logout = () => {
    localStorage.removeItem("access_token");
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);
