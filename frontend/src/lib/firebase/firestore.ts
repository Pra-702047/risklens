import { db } from "./config";
import { doc, getDoc, setDoc } from "firebase/firestore";

export interface UserProfile {
  uid: string;
  email: string | null;
  displayName: string | null;
  phoneNumber: string | null;
  role: string;
  departmentId: string | null;
  zoneId: string | null;
  wardId: string | null;
  isActive: boolean;
  isVerified: boolean;
  createdAt: Date;
  updatedAt: Date;
  lastLoginAt: Date | null;
}

export const createUserProfile = async (uid: string, profileData: Partial<UserProfile>) => {
  const docRef = doc(db, "users", uid);
  await setDoc(docRef, {
    ...profileData,
    uid,
    role: "CITIZEN", // Default role
    isActive: true,
    isVerified: false,
    createdAt: new Date(),
    updatedAt: new Date(),
    lastLoginAt: new Date()
  }, { merge: true });
};

export const getUserProfile = async (uid: string): Promise<UserProfile | null> => {
  const docRef = doc(db, "users", uid);
  const docSnap = await getDoc(docRef);
  if (docSnap.exists()) {
    return docSnap.data() as UserProfile;
  }
  return null;
};
