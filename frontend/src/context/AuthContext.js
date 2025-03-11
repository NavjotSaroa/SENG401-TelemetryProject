import { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [token, setToken] = useState(sessionStorage.getItem('jwtToken') || null);

  useEffect(() => {
    const checkAuth = () => {
      const storedToken = sessionStorage.getItem('jwtToken');
      if (storedToken) {
        setToken(storedToken);
      }
    };
    checkAuth();
  }, []);

  const login = (newToken) => {
    sessionStorage.setItem('jwtToken', newToken);
    setToken(newToken);
  };

  const logout = () => {
    sessionStorage.removeItem('jwtToken');
    setToken(null);
  };

  return (
    <AuthContext.Provider value={{ token, setToken, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuthContext = () => useContext(AuthContext);
