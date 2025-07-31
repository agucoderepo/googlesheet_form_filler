# Google OAuth Setup Guide

This guide will help you set up Google OAuth authentication for the TCS Uruguay AI Initiatives application.

## Prerequisites

1. A Google Cloud Project
2. Google Cloud Console access
3. Basic understanding of OAuth 2.0

## Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Note down your Project ID

## Step 2: Enable Required APIs

1. In the Google Cloud Console, go to "APIs & Services" > "Library"
2. Search for and enable the following APIs:
   - Google Sheets API
   - Google+ API (if available)
   - Google OAuth2 API

## Step 3: Create OAuth 2.0 Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth 2.0 Client IDs"
3. Choose "Web application" as the application type
4. Configure the following:
   - **Name**: TCS Uruguay AI Initiatives
   - **Authorized JavaScript origins**:
     - `http://localhost:8501` (for local development)
     - `https://your-app-name.streamlit.app` (for Streamlit Cloud deployment)
   - **Authorized redirect URIs**:
     - `http://localhost:8501` (for local development)
     - `https://your-app-name.streamlit.app` (for Streamlit Cloud deployment)
5. Click "Create"
6. Note down the Client ID and Client Secret

## Step 4: Configure Environment Variables

### For Local Development

Create a `.env` file in your project directory:

```env
# Google OAuth Configuration
GOOGLE_CLIENT_ID=your_client_id_here
GOOGLE_CLIENT_SECRET=your_client_secret_here
REDIRECT_URI=http://localhost:8501

# Google Sheets Configuration
GOOGLE_SHEET_ID=your_google_sheet_id_here
GOOGLE_SHEETS_CREDENTIALS={"type":"service_account",...}

# Development mode
dev=True
```

### For Streamlit Cloud Deployment

In your Streamlit Cloud dashboard, add the following secrets:

```toml
# Google OAuth Configuration
google_client_id = "your_client_id_here"
google_client_secret = "your_client_secret_here"
redirect_uri = "https://your-app-name.streamlit.app"

# Google Sheets Configuration
google_sheet_id = "your_google_sheet_id_here"
google_sheets_credentials = "{\"type\":\"service_account\",...}"
```

## Step 5: Create Service Account for Google Sheets

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "Service Account"
3. Fill in the details:
   - **Name**: TCS Employee Data Service
   - **Description**: Service account for accessing Google Sheets
4. Click "Create and Continue"
5. Skip the optional steps and click "Done"
6. Click on the created service account
7. Go to "Keys" tab
8. Click "Add Key" > "Create new key"
9. Choose "JSON" format
10. Download the JSON file and save it as `service_account_key.json` in your project directory

## Step 6: Create and Configure Google Sheet

1. Create a new Google Sheet
2. Copy the Sheet ID from the URL (the long string between `/d/` and `/edit`)
3. Share the sheet with the service account email (found in the JSON file)
4. Give it "Editor" permissions

## Step 7: Test the Application

1. Run the application locally:
   ```bash
   streamlit run employee_data_form.py
   ```

2. Navigate to `http://localhost:8501`
3. You should see the Google authentication screen
4. Click "Sign in with Google" - this will open Google's login page in a new tab
5. Complete the Google sign-in process
6. You'll be redirected back to your application

## Important Notes About OAuth Flow

### X-Frame-Options Issue

Google's OAuth pages have `X-Frame-Options: deny` which prevents them from being embedded in iframes. Our implementation handles this by:

1. **Opening Google OAuth in a new tab** (`target="_blank"`)
2. **Providing manual URL option** if the button doesn't work
3. **Clear instructions** for users about the OAuth flow

### Redirect URI Configuration

Make sure your redirect URIs in Google Cloud Console exactly match your application URLs:

- **Local development**: `http://localhost:8501`
- **Streamlit Cloud**: `https://your-app-name.streamlit.app`

### OAuth Flow Process

1. User clicks "Sign in with Google"
2. Google OAuth page opens in new tab
3. User signs in with Google account
4. Google redirects back to your app with authorization code
5. App exchanges code for access token
6. App gets user information from Google
7. User is authenticated and can access the application

## Troubleshooting

### Common Issues

1. **"Google OAuth not configured" warning**
   - Make sure you've set the `GOOGLE_CLIENT_ID` environment variable
   - Check that the client ID is correct

2. **"Invalid redirect URI" error**
   - Verify that your redirect URI matches exactly what's configured in Google Cloud Console
   - For local development, use `http://localhost:8501`
   - For production, use your actual Streamlit app URL

3. **"X-Frame-Options" error**
   - This is expected behavior - Google prevents embedding their OAuth page
   - Use the new tab approach or copy the OAuth URL manually
   - The app will handle the redirect properly

4. **"Access denied" when accessing Google Sheets**
   - Make sure the service account email has access to the Google Sheet
   - Verify that the Google Sheets API is enabled
   - Check that the service account JSON file is correctly configured

5. **"Client ID not found" error**
   - Ensure the Google OAuth2 API is enabled in your Google Cloud Project
   - Verify that the client ID is correctly copied from Google Cloud Console

### Security Best Practices

1. **Never commit credentials to version control**
   - Use environment variables or Streamlit secrets
   - Add `.env` and `service_account_key.json` to `.gitignore`

2. **Use HTTPS in production**
   - Always use HTTPS URLs for production deployments
   - Update redirect URIs accordingly

3. **Regularly rotate credentials**
   - Periodically update your OAuth client secrets
   - Monitor for any suspicious activity

4. **Limit API scopes**
   - Only request the minimum scopes needed
   - Current scopes: `openid email profile`

## Advanced Configuration

### Custom OAuth Scopes

If you need additional permissions, modify the scopes in `google_oauth.py`:

```python
'scope': 'openid email profile https://www.googleapis.com/auth/spreadsheets'
```

### Custom Redirect Handling

For more complex redirect handling, you can modify the `authenticate_with_google()` function in `google_oauth.py`.

### Session Management

The application uses Streamlit's session state for session management. For production applications, consider implementing more robust session management with database storage. 