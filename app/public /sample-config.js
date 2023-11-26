// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyDzIarG4tYrkA2xOOBx5hd66kdRLQ929Js",
  authDomain: "awdevmyid.firebaseapp.com",
  databaseURL: "https://awdevmyid-default-rtdb.firebaseio.com",
  projectId: "awdevmyid",
  storageBucket: "awdevmyid.appspot.com",
  messagingSenderId: "1025289085908",
  appId: "1:1025289085908:web:08228b4c81b0c215b9ac41",
  measurementId: "G-D4FMFSEHC2"
};

// Initialize Firebase
firebase.initializeApp(config);
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);



// Google OAuth Client ID, needed to support One-tap sign-up.
// Set to null if One-tap sign-up is not supported.
var CLIENT_ID =
    '106457840177755049060';
