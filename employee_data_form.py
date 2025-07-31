import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import os
from dotenv import load_dotenv
import json

# Import the Google OAuth module
from google_oauth import authenticate_with_google, sign_out

# Load environment variables from .env file
load_dotenv()

# Initialize session state for authentication
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_info' not in st.session_state:
    st.session_state.user_info = None

# Main authentication flow
user_info = authenticate_with_google()

# Only show the main app if user is authenticated
if user_info:
    st.session_state.authenticated = True
    st.session_state.user_info = user_info
    
    # Display user info in sidebar
    with st.sidebar:
        st.markdown("### 👤 User Information")
        if user_info.get('picture'):
            st.image(user_info['picture'], width=50)
        st.write(f"**Name:** {user_info.get('name', 'N/A')}")
        st.write(f"**Email:** {user_info.get('email', 'N/A')}")
        
        if st.button("🚪 Sign Out"):
            sign_out()
    
    # Main app content
    st.title("TCS Uruguay AI Initiatives")
    
    # Google Sheets configuration
    SCOPES = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]

    # Form fields
    name = st.text_input("Name", value=user_info.get('name', ''))
    employee_number = st.text_input("Employee Number")
    profile_type = st.selectbox("Profile Type", ["Non-Technical", "Somewhat technical", "Technical"])

    # Google Sheets setup
    @st.cache_resource
    def get_google_sheets_client():
        """Initialize Google Sheets client with service account credentials."""
        try:
            # Priority order: Streamlit secrets > .env file > JSON file
            creds = None
            
            # Try Streamlit secrets first
            try:
                if hasattr(st, 'secrets') and st.secrets:
                    creds_dict = st.secrets.get('google_sheets_credentials')
                    if creds_dict:
                        # Handle case where credentials might be stored as string
                        if isinstance(creds_dict, str):
                            try:
                                creds_dict = json.loads(creds_dict)
                            except json.JSONDecodeError as e:
                                st.error(f"Invalid JSON format in credentials: {e}")
                                st.info("Please check your Streamlit secrets format")
                                return None
                        creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
            except Exception as e:
                # If secrets not available, continue to next method
                pass
            
            # Try environment variables if secrets failed
            if not creds and os.getenv('GOOGLE_SHEETS_CREDENTIALS'):
                try:
                    creds_str = os.getenv('GOOGLE_SHEETS_CREDENTIALS')
                    # Handle case where credentials might be stored as string
                    if isinstance(creds_str, str):
                        creds_dict = json.loads(creds_str)
                    else:
                        creds_dict = creds_str
                    creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
                except Exception as e:
                    st.error(f"Error parsing environment credentials: {e}")
                    return None
            
            # Try JSON file if other methods failed
            if not creds:
                try:
                    creds = Credentials.from_service_account_file(
                        'service_account_key.json',
                        scopes=SCOPES
                    )
                except FileNotFoundError:
                    st.warning("No Google Sheets credentials found. Please configure one of the following:")
                    st.info("1. Create a .streamlit/secrets.toml file with google_sheets_credentials")
                    st.info("2. Set GOOGLE_SHEETS_CREDENTIALS environment variable")
                    st.info("3. Place service_account_key.json in the project directory")
                    return None
                except Exception as e:
                    st.error(f"Error reading service account file: {e}")
                    return None
            
            if creds:
                client = gspread.authorize(creds)
                return client
            else:
                return None
                
        except Exception as e:
            st.error(f"Error setting up Google Sheets client: {e}")
            return None

    # Google Sheet ID - get from secrets, env file, or use placeholder
    SHEET_ID = None
    try:
        if hasattr(st, 'secrets') and st.secrets:
            SHEET_ID = st.secrets.get('google_sheet_id')
    except Exception:
        pass
    
    if not SHEET_ID:
        SHEET_ID = os.getenv('GOOGLE_SHEET_ID') or "YOUR_GOOGLE_SHEET_ID_HERE"
    
    SHEET_NAME = "Employee Data"  # Name of the worksheet

    if st.button("Submit"):
        if not name or not employee_number:
            st.error("Please fill in all fields.")
        else:
            try:
                # Get Google Sheets client
                client = get_google_sheets_client()
                if client is None:
                    st.error("Failed to initialize Google Sheets client.")
                    st.stop()
                
                # Check if SHEET_ID is configured
                if SHEET_ID == "YOUR_GOOGLE_SHEET_ID_HERE":
                    st.error("Google Sheet ID not configured. Please set GOOGLE_SHEET_ID in your environment variables or Streamlit secrets.")
                    st.stop()
                
                # Open the spreadsheet
                spreadsheet = client.open_by_key(SHEET_ID)
                
                # Try to get the worksheet, create if it doesn't exist
                try:
                    worksheet = spreadsheet.worksheet(SHEET_NAME)
                except gspread.WorksheetNotFound:
                    # Create new worksheet if it doesn't exist
                    worksheet = spreadsheet.add_worksheet(title=SHEET_NAME, rows=1000, cols=10)
                    # Add headers
                    worksheet.append_row(["Name", "Employee Number", "Profile Type", "Timestamp", "User Email"])
                
                # Prepare data for insertion
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                new_row = [name, employee_number, profile_type, timestamp, user_info.get('email', '')]
                
                # Append the new row
                worksheet.append_row(new_row)
                if os.getenv('dev') == 'True':
                    st.success("Data saved to Google Sheets successfully!")
                    
                    # Display the updated data
                    st.subheader("Current Data in Google Sheets:")
                    data = worksheet.get_all_records()
                    if data:
                        df = pd.DataFrame(data)
                        st.dataframe(df)
                    else:
                        st.info("No data found in the sheet.")
                else:
                    st.success("Thanks :)!!")
                    
            except Exception as e:
                st.error(f"Error saving data: {e}")
                if os.getenv('dev') == 'True':
                    st.info("Make sure you have:")
                    st.info("1. Created a Google Cloud Project")
                    st.info("2. Enabled Google Sheets API")
                    st.info("3. Created a service account and downloaded the JSON key file")
                    st.info("4. Shared your Google Sheet with the service account email")
                    st.info("5. Updated the SHEET_ID variable with your actual Google Sheet ID")

    # Instructions for setup - only show in development mode
    if os.getenv('dev') == 'True':
        with st.expander("Setup Instructions"):
            st.markdown("""
            ### To use Google Sheets instead of Excel, follow these steps:
            
            1. **Create a Google Cloud Project:**
               - Go to [Google Cloud Console](https://console.cloud.google.com/)
               - Create a new project or select an existing one
            
            2. **Enable Google Sheets API:**
               - In the Google Cloud Console, go to "APIs & Services" > "Library"
               - Search for "Google Sheets API" and enable it
            
            3. **Create a Service Account:**
               - Go to "APIs & Services" > "Credentials"
               - Click "Create Credentials" > "Service Account"
               - Fill in the details and create the account
               - Click on the service account email
               - Go to "Keys" tab and create a new JSON key
               - Download the JSON file
            
            4. **Configure Credentials (Choose one method):**
               
               **Method A - Local Development with JSON file:**
               - Save the JSON file as `service_account_key.json` in your project directory
               
               **Method B - Local Development with .env file:**
               - Create a `.env` file in your project directory
               - Add: `GOOGLE_SHEET_ID=your_sheet_id_here`
               - Add: `GOOGLE_SHEETS_CREDENTIALS={"type":"service_account",...}` (copy entire JSON content)
               
               **Method C - Streamlit Cloud Deployment:**
               - In Streamlit Cloud, add secrets:
                 - `google_sheet_id`: your Google Sheet ID
                 - `google_sheets_credentials`: entire JSON content as a string
            
            5. **Create a Google Sheet:**
               - Create a new Google Sheet
               - Copy the Sheet ID from the URL (the long string between /d/ and /edit)
               - Set it in your chosen configuration method
            
            6. **Share the Sheet:**
               - Share your Google Sheet with the service account email (found in the JSON file)
               - Give it "Editor" permissions
            
            7. **Install Dependencies:**
               - Run: `pip install -r requirements.txt`
            """)
