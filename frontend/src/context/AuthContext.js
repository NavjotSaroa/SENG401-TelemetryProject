import { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const checkAuth = async () => {
      const token = sessionStorage.getItem('jwtToken');
      if (token) {
        try {
          const res = await fetch('/api/auth/me', {
            method: 'GET',
            headers: { Authorization: `Bearer ${token}` },
          });

          if (res.ok) {
            const data = await res.json();
            setUser(data);
            setIsAuthenticated(true);
          } else {
            sessionStorage.removeItem('jwtToken');
            sessionStorage.removeItem('user');
            setIsAuthenticated(false);
          }
        } catch (err) {
          sessionStorage.removeItem('jwtToken');
          sessionStorage.removeItem('user');
          setIsAuthenticated(false);
        }
      }
    };
    checkAuth();
  }, []);

  const login = async (username, password) => {
    try {
      const res = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      });

      if (!res.ok) {
        throw new Error('Authentication failed');
      }

      const data = await res.json();
      sessionStorage.setItem('jwtToken', data.token);
      sessionStorage.setItem('user', JSON.stringify(data.user));
      setUser(data.user);
      setIsAuthenticated(true);
      return true;
    } catch (error) {
      setIsAuthenticated(false);
      throw error;
    }
  };

  const logout = () => {
    sessionStorage.removeItem('jwtToken');
    sessionStorage.removeItem('user');
    setUser(null);
    setIsAuthenticated(false);
  };

  return (
    <AuthContext.Provider value={{ user, isAuthenticated, setUser, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuthContext = () => useContext(AuthContext);
