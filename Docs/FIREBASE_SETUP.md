# Firebase Setup Guide

## Configuration

The application uses Firebase for Google Authentication. The Firebase configuration is stored in environment variables for security.

### Environment Variables

#### Frontend (.env)
```bash
VITE_FIREBASE_API_KEY=your-api-key
VITE_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=your-project-id
VITE_FIREBASE_STORAGE_BUCKET=your-project.firebasestorage.app
VITE_FIREBASE_MESSAGING_SENDER_ID=your-sender-id
VITE_FIREBASE_APP_ID=your-app-id
VITE_FIREBASE_MEASUREMENT_ID=your-measurement-id
```

#### Backend (.env)
```bash
FIREBASE_API_KEY=your-api-key
FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_STORAGE_BUCKET=your-project.firebasestorage.app
FIREBASE_MESSAGING_SENDER_ID=your-sender-id
FIREBASE_APP_ID=your-app-id
FIREBASE_MEASUREMENT_ID=your-measurement-id
```

## Setup Instructions

1. **Copy example files:**
   ```bash
   # Frontend
   cd Frontend
   cp .env.example .env
   
   # Backend
   cd ../Backend
   cp .env.example .env
   ```

2. **Update .env files with your Firebase credentials** (already configured if using the provided .env files)

3. **Ensure Firebase project has Google Authentication enabled:**
   - Go to Firebase Console: https://console.firebase.google.com/
   - Select your project
   - Navigate to Authentication > Sign-in method
   - Enable Google provider

4. **Add authorized domains in Firebase:**
   - In Firebase Console > Authentication > Settings > Authorized domains
   - Add: `localhost`, your production domain

## Features

- ✅ Google Sign-in/Sign-up
- ✅ Automatic user profile creation
- ✅ Seamless backend integration
- ✅ Secure token-based authentication

## Files

- `Frontend/src/config/firebase.js` - Firebase initialization and configuration
- `Frontend/src/pages/login.jsx` - Login page with Google Auth button
- `Frontend/.env` - Frontend environment variables (not committed to git)
- `Backend/.env` - Backend environment variables (not committed to git)

## Security Notes

⚠️ **IMPORTANT**: 
- Never commit .env files to version control
- Keep your Firebase API keys secure
- The .env files are already in .gitignore
- Use .env.example as templates for new developers
