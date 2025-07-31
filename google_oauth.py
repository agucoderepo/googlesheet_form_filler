import streamlit as st
import requests
import json
import hashlib
import time
from urllib.parse import urlencode
import os
from dotenv import load_dotenv

load_dotenv()

class GoogleOAuth:
    def __init__(self):
        # Try to get credentials from different sources
        self.client_id = None
        self.client_secret = None
        self.redirect_uri = None
        
        # Try Streamlit secrets first
        try:
            if hasattr(st, 'secrets') and st.secrets:
                self.client_id = st.secrets.get('google_client_id')
                self.client_secret = st.secrets.get('google_client_secret')
                self.redirect_uri = st.secrets.get('redirect_uri')
        except Exception:
            pass
        
        # Fallback to environment variables
        if not self.client_id:
            self.client_id = os.getenv('GOOGLE_CLIENT_ID')
        if not self.client_secret:
            self.client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
        if not self.redirect_uri:
            self.redirect_uri = os.getenv('REDIRECT_URI', 'http://localhost:8501')
        
    def get_authorization_url(self):
        """Generate Google OAuth authorization URL."""
        if not self.client_id:
            return None
            
        params = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'response_type': 'code',
            'scope': 'openid email profile',
            'access_type': 'offline',
            'prompt': 'consent'
        }
        return f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"
    
    def exchange_code_for_tokens(self, authorization_code):
        """Exchange authorization code for access and ID tokens."""
        if not self.client_id or not self.client_secret:
            return None
            
        token_url = "https://oauth2.googleapis.com/token"
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': authorization_code,
            'grant_type': 'authorization_code',
            'redirect_uri': self.redirect_uri
        }
        
        response = requests.post(token_url, data=data)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Token exchange failed: {response.text}")
            return None
    
    def get_user_info(self, access_token):
        """Get user information from Google API."""
        userinfo_url = "https://www.googleapis.com/oauth2/v2/userinfo"
        headers = {'Authorization': f'Bearer {access_token}'}
        
        response = requests.get(userinfo_url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to get user info: {response.text}")
            return None
    
    def verify_id_token(self, id_token):
        """Verify Google ID token."""
        verify_url = "https://oauth2.googleapis.com/tokeninfo"
        params = {'id_token': id_token}
        
        response = requests.get(verify_url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"ID token verification failed: {response.text}")
            return None

def create_session_token(user_info):
    """Create a session token for the authenticated user."""
    timestamp = str(int(time.time()))
    token_data = f"{user_info['email']}:{user_info['name']}:{timestamp}"
    return hashlib.sha256(token_data.encode()).hexdigest()

def authenticate_with_google():
    """Main authentication function."""
    oauth = GoogleOAuth()
    
    # Check if user is already authenticated
    if st.session_state.get('authenticated') and st.session_state.get('user_info'):
        return st.session_state.user_info
    
    # Check for authorization code in URL parameters
    auth_code = st.query_params.get('code')
    
    if auth_code and oauth.client_id:
        # Exchange code for tokens
        tokens = oauth.exchange_code_for_tokens(auth_code)
        if tokens:
            # Get user info
            user_info = oauth.get_user_info(tokens['access_token'])
            if user_info:
                # Create session token
                session_token = create_session_token(user_info)
                
                # Store in session state
                st.session_state.authenticated = True
                st.session_state.user_info = user_info
                st.session_state.session_token = session_token
                
                # Clear URL parameters
                st.query_params.clear()
                
                st.success("✅ Successfully authenticated with Google!")
                st.rerun()
    
    # Display login interface
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <h2>Welcome to TCS Uruguay AI Initiatives</h2>
        <p>Please sign in with your Google account to continue.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # For development/testing, provide a simplified login
    if not oauth.client_id:
        st.warning("""
        **Google OAuth not configured. Using simplified authentication for development.**
        
        To enable full Google OAuth:
        1. Create a Google Cloud Project
        2. Enable Google OAuth2 API
        3. Create OAuth 2.0 credentials
        4. Set GOOGLE_CLIENT_ID in your .env file
        """)
        
        # Create login form for simplified authentication
        with st.form("google_oauth_form"):
            st.markdown("### 🔐 Google Authentication")
            
            email = st.text_input("Google Email", placeholder="your.email@tcs.com")
            name = st.text_input("Full Name", placeholder="Your Full Name")
            google_verified = st.checkbox("✅ I confirm this is my Google account")
            
            submitted = st.form_submit_button("🔐 Sign in with Google", type="primary")
            
            if submitted and email and name and google_verified:
                if '@' in email and '.' in email:
                    user_info = {
                        'email': email,
                        'name': name,
                        'userid': hashlib.md5(email.encode()).hexdigest(),
                        'picture': None
                    }
                    
                    session_token = create_session_token(user_info)
                    st.session_state.authenticated = True
                    st.session_state.user_info = user_info
                    st.session_state.session_token = session_token
                    
                    st.success("✅ Authentication successful!")
                    st.rerun()
                else:
                    st.error("Please enter a valid email address.")
            elif submitted:
                st.error("Please fill in all fields and confirm your Google account.")
    else:
        # Real Google OAuth - no form needed
        st.markdown("### 🔐 Google Authentication")
        
        auth_url = oauth.get_authorization_url()
        if auth_url:
            st.markdown(f"""
            <div style="text-align: center;">
                <a href="{auth_url}" target="_self">
                    <button style="
                        background-color: #4285f4;
                        color: white;
                        padding: 12px 24px;
                        border: none;
                        border-radius: 4px;
                        font-size: 16px;
                        cursor: pointer;
                        display: inline-flex;
                        align-items: center;
                        gap: 8px;
                    ">
                        <span>🔐</span>
                        Sign in with Google
                    </button>
                </a>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("Failed to generate OAuth URL. Please check your configuration.")
    
    st.markdown("""
    <div style="text-align: center; margin-top: 20px;">
        <small>This application requires Google authentication to access employee data.</small>
    </div>
    """, unsafe_allow_html=True)
    
    return None

def sign_out():
    """Sign out the current user."""
    st.session_state.authenticated = False
    st.session_state.user_info = None
    st.session_state.session_token = None
    st.rerun() 