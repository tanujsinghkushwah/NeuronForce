'use client';

import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { User, GoogleAuthPayload } from '../types/crm';
import { api } from '../lib/api';
import { signInWithGoogleFirebase, isFirebaseConfigured } from '../lib/firebase';

interface AuthContextType {
  user: User | null;
  token: string | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  isFirebaseAvailable: boolean;
  signInWithGoogleSSO: () => Promise<User>;
  loginWithGoogle: (payload: GoogleAuthPayload) => Promise<User>;
  loginWithDemoAccount: (demoUser: { email: string; full_name: string; avatar_url?: string; role?: string }) => Promise<User>;
  logout: () => Promise<void>;
  refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  // Load existing session on initial client mount
  useEffect(() => {
    async function initAuth() {
      try {
        // 1. Check for SSO token redirect parameter from Google OAuth callback
        if (typeof window !== 'undefined') {
          const urlParams = new URLSearchParams(window.location.search);
          const ssoToken = urlParams.get('sso_token');
          if (ssoToken) {
            localStorage.setItem('neuronforce_token', ssoToken);
            setToken(ssoToken);
            window.history.replaceState({}, document.title, window.location.pathname);
            try {
              const verifiedUser = await api.getMe();
              setUser(verifiedUser);
              localStorage.setItem('neuronforce_user', JSON.stringify(verifiedUser));
              setIsLoading(false);
              return;
            } catch (err) {
              console.warn('SSO token verification failed:', err);
            }
          }
        }

        const storedToken = localStorage.getItem('neuronforce_token');
        const storedUser = localStorage.getItem('neuronforce_user');

        if (storedToken && storedUser) {
          setToken(storedToken);
          setUser(JSON.parse(storedUser));

          // Verify token validity in background with server
          try {
            const verifiedUser = await api.getMe();
            setUser(verifiedUser);
            localStorage.setItem('neuronforce_user', JSON.stringify(verifiedUser));
          } catch (err) {
            console.warn('Session expired or invalid, clearing local session.');
            localStorage.removeItem('neuronforce_token');
            localStorage.removeItem('neuronforce_user');
            setToken(null);
            setUser(null);
          }
        } else {
          // If fresh session with no user, seed default session with Alex Rivera (RevOps Lead)
          try {
            const res = await api.googleAuth({
              email: 'alex.rivera@neuronforce.ai',
              full_name: 'Alex Rivera',
              avatar_url: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Alex',
              sub: 'google_alex_rivera_101',
              role: 'revops_lead'
            });
            localStorage.setItem('neuronforce_token', res.access_token);
            localStorage.setItem('neuronforce_user', JSON.stringify(res.user));
            setToken(res.access_token);
            setUser(res.user);
          } catch (initErr) {
            console.error('Initial demo auth failed:', initErr);
          }
        }
      } catch (err) {
        console.error('Failed to initialize authentication state:', err);
      } finally {
        setIsLoading(false);
      }
    }

    initAuth();
  }, []);

  const loginWithGoogle = useCallback(async (payload: GoogleAuthPayload): Promise<User> => {
    setIsLoading(true);
    try {
      const res = await api.googleAuth(payload);
      localStorage.setItem('neuronforce_token', res.access_token);
      localStorage.setItem('neuronforce_user', JSON.stringify(res.user));
      setToken(res.access_token);
      setUser(res.user);
      return res.user;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const loginWithDemoAccount = useCallback(async (demoUser: {
    email: string;
    full_name: string;
    avatar_url?: string;
    role?: string;
  }): Promise<User> => {
    return loginWithGoogle({
      email: demoUser.email,
      full_name: demoUser.full_name,
      avatar_url: demoUser.avatar_url,
      sub: `google_${demoUser.email.replace(/[@.]/g, '_')}`,
      role: demoUser.role || 'sales_rep',
    });
  }, [loginWithGoogle]);

  const logout = useCallback(async () => {
    try {
      await api.logout();
    } catch (err) {
      console.warn('Logout API call failed:', err);
    } finally {
      localStorage.removeItem('neuronforce_token');
      localStorage.removeItem('neuronforce_user');
      setToken(null);
      setUser(null);
    }
  }, []);

  const refreshUser = useCallback(async () => {
    try {
      const refreshed = await api.getMe();
      setUser(refreshed);
      localStorage.setItem('neuronforce_user', JSON.stringify(refreshed));
    } catch (err) {
      console.error('Failed to refresh user profile:', err);
    }
  }, []);

  const signInWithGoogleSSO = useCallback(async (): Promise<User> => {
    setIsLoading(true);
    try {
      if (isFirebaseConfigured()) {
        const firebaseUser = await signInWithGoogleFirebase();
        const res = await api.googleAuth({
          credential: firebaseUser.idToken,
          email: firebaseUser.email || '',
          full_name: firebaseUser.displayName || '',
          avatar_url: firebaseUser.photoURL || undefined,
          sub: firebaseUser.uid,
        });
        localStorage.setItem('neuronforce_token', res.access_token);
        localStorage.setItem('neuronforce_user', JSON.stringify(res.user));
        setToken(res.access_token);
        setUser(res.user);
        return res.user;
      } else {
        throw new Error('FIREBASE_CONFIG_REQUIRED');
      }
    } finally {
      setIsLoading(false);
    }
  }, []);

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        isLoading,
        isAuthenticated: !!user && !!token,
        isFirebaseAvailable: isFirebaseConfigured(),
        signInWithGoogleSSO,
        loginWithGoogle,
        loginWithDemoAccount,
        logout,
        refreshUser,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
