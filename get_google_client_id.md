# How to Get Google Client ID - Step by Step Guide

## 🎯 **Quick Overview**
You need a Google Client ID to enable Google OAuth authentication in your Streamlit app. Here's exactly how to get one:

## 📋 **Step-by-Step Instructions**

### **Step 1: Go to Google Cloud Console**
1. Open your browser and go to: [https://console.cloud.google.com/](https://console.cloud.google.com/)
2. Sign in with your Google account
3. If you don't have a project, create one or select an existing one

### **Step 2: Create a New Project (if needed)**
1. Click on the project dropdown at the top
2. Click **"New Project"**
3. Enter a project name (e.g., "TCS Uruguay AI Initiatives")
4. Click **"Create"**

### **Step 3: Enable Required APIs**
1. In the left sidebar, click **"APIs & Services"** → **"Library"**
2. Search for and enable these APIs one by one:
   - **Google Sheets API** - Click "Enable"
   - **Google+ API** (if available) - Click "Enable"
   - **Google OAuth2 API** - Click "Enable"

### **Step 4: Create OAuth 2.0 Credentials**
1. Go to **"APIs & Services"** → **"Credentials"**
2. Click **"Create Credentials"** → **"OAuth 2.0 Client IDs"**
3. If prompted, configure the OAuth consent screen first:
   - Choose **"External"** user type
   - Fill in the app name: **"TCS Uruguay AI Initiatives"**
   - Add your email as developer contact
   - Save and continue

### **Step 5: Configure OAuth Client**
1. Choose **"Web application"** as the application type
2. Fill in the details:
   - **Name**: `TCS Uruguay AI Initiatives`
   - **Authorized JavaScript origins**:
     ```
     http://localhost:8501
     https://your-app-name.streamlit.app
     ```
   - **Authorized redirect URIs**:
     ```
     http://localhost:8501
     https://your-app-name.streamlit.app
     ```
3. Click **"Create"**

### **Step 6: Copy Your Credentials**
After creation, you'll see a popup with your credentials:
- **Client ID** (copy this - looks like: `123456789-abcdefghijklmnop.apps.googleusercontent.com`)
- **Client Secret** (copy this too)

## 🔧 **Configure in Your App**

### **For Local Development:**
Create a `.env` file in your `AIDG` folder:

```env
# Google OAuth Configuration
GOOGLE_CLIENT_ID=your_client_id_here
GOOGLE_CLIENT_SECRET=your_client_secret_here
REDIRECT_URI=http://localhost:8501

# Development mode
dev=True
```

### **For Streamlit Cloud:**
In your Streamlit Cloud dashboard, add these secrets:

```toml
# Google OAuth Configuration
google_client_id = "your_client_id_here"
google_client_secret = "your_client_secret_here"
redirect_uri = "https://your-app-name.streamlit.app"
```

## 🚨 **Important Notes**

### **Security:**
- Never commit your Client Secret to version control
- Keep your credentials secure
- Use environment variables or Streamlit secrets

### **URLs:**
- For local development: use `http://localhost:8501`
- For Streamlit Cloud: use your actual app URL like `https://your-app-name.streamlit.app`

### **Testing:**
- The app will work without OAuth for development
- You'll see a simplified login form
- Once you add the Client ID, you'll get the full Google OAuth experience

## 🔍 **Troubleshooting**

### **Common Issues:**

1. **"Invalid redirect URI" error**
   - Make sure your redirect URI exactly matches what's in Google Cloud Console
   - Check for typos in the URL

2. **"Client ID not found" error**
   - Verify you copied the entire Client ID
   - Make sure the Google OAuth2 API is enabled

3. **"Access denied" error**
   - Check that your app is in the correct Google Cloud project
   - Verify the OAuth consent screen is configured

### **Still Having Issues?**
1. Check the [main OAuth setup guide](oauth_setup.md)
2. Verify all APIs are enabled
3. Make sure your redirect URIs are correct
4. Test with the simplified authentication first

## ✅ **Test Your Setup**

1. Add your Client ID to the `.env` file
2. Run your app: `streamlit run employee_data_form.py`
3. You should see the Google sign-in button
4. Click it and test the authentication flow

## 📞 **Need Help?**

If you're still having trouble:
1. Check the Google Cloud Console error messages
2. Verify all steps were completed
3. Try the simplified authentication mode first
4. Check the [main README](README.md) for more details 