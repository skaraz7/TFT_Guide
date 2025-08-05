// Firebase configuration for TFT Guide
import { initializeApp } from 'firebase/app';
import { getFirestore } from 'firebase/firestore';
import { getAuth } from 'firebase/auth';
import { getStorage } from 'firebase/storage';
import { getAnalytics } from 'firebase/analytics';

const firebaseConfig = {
  apiKey: "AIzaSyCwbWW_4Gy_1dEEcVbFjMkLHakWIyF10JQ",
  authDomain: "tft-metapro.firebaseapp.com",
  projectId: "tft-metapro",
  storageBucket: "tft-metapro.firebasestorage.app",
  messagingSenderId: "1048415348944",
  appId: "1:1048415348944:web:e79b1b9a9350a77cf8d6d5",
  measurementId: "G-DDFHZHQBET"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Firebase services
export const db = getFirestore(app);
export const auth = getAuth(app);
export const storage = getStorage(app);
export const analytics = getAnalytics(app);

export default app;