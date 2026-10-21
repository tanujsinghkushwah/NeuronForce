/**
 * Firebase Client Configuration & Google SSO Provider
 * Enables Google Single Sign-On via Firebase Authentication popup.
 */

import { initializeApp, getApps, getApp, FirebaseApp } from 'firebase/app';
import { getAuth, GoogleAuthProvider, signInWithPopup, Auth, UserCredential } from 'firebase/auth';

export const firebaseConfig = {
  apiKey: process.env.NEXT_PUBLIC_FIREBASE_API_KEY || '',
  authDomain: process.env.NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN || '',
  projectId: process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID || '',
  storageBucket: process.env.NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET || '',
  messagingSenderId: process.env.NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID || '',
  appId: process.env.NEXT_PUBLIC_FIREBASE_APP_ID || '',
};

export function isFirebaseConfigured(): boolean {
  return !!(
    firebaseConfig.apiKey &&
    firebaseConfig.apiKey.length > 5 &&
    firebaseConfig.projectId
  );
}

let firebaseApp: FirebaseApp | null = null;
let firebaseAuth: Auth | null = null;

export function getFirebaseInstance(): { app: FirebaseApp | null; auth: Auth | null } {
  if (typeof window === 'undefined') {
    return { app: null, auth: null };
  }

  if (!isFirebaseConfigured()) {
    return { app: null, auth: null };
  }

  if (!firebaseApp) {
    firebaseApp = getApps().length > 0 ? getApp() : initializeApp(firebaseConfig);
    firebaseAuth = getAuth(firebaseApp);
  }

  return { app: firebaseApp, auth: firebaseAuth };
}

/**
 * Execute real Google SSO popup using Firebase Authentication
 */
export async function signInWithGoogleFirebase(): Promise<{
  idToken: string;
  email: string | null;
  displayName: string | null;
  photoURL: string | null;
  uid: string;
}> {
  const { auth } = getFirebaseInstance();

  if (!auth) {
    throw new Error('Firebase Authentication is not configured with active credentials.');
  }

  const provider = new GoogleAuthProvider();
  provider.addScope('email');
  provider.addScope('profile');
  provider.setCustomParameters({ prompt: 'select_account' });

  const result: UserCredential = await signInWithPopup(auth, provider);
  const user = result.user;
  const idToken = await user.getIdToken();

  return {
    idToken,
    email: user.email,
    displayName: user.displayName,
    photoURL: user.photoURL,
    uid: user.uid,
  };
}
