# TCS Uruguay AI Initiatives - Employee Data Form

A Streamlit application for collecting employee information and technical profile data for TCS Uruguay AI initiatives.

## Features

- 🔐 **Google OAuth Authentication**: Secure login with Google accounts
- 📊 **Google Sheets Integration**: Automatic data storage in Google Sheets
- 👤 **User Profile Management**: Display user information in sidebar
- 📝 **Employee Data Collection**: Collect name, employee number, and profile type
- 🎨 **Modern UI**: Clean and professional interface
- 🔒 **Session Management**: Secure session handling with automatic logout

## Quick Start

### Prerequisites

- Python 3.7+
- Google Cloud Project
- Google Sheets API enabled
- Google OAuth 2.0 credentials

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd AIDG
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure Google OAuth (see [OAuth Setup Guide](oauth_setup.md))

4. Run the application:
```bash
streamlit run employee_data_form.py
```

## Configuration

### Environment Variables

Create a `.env` file in the project directory:

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

### Streamlit Cloud Deployment

For deployment on Streamlit Cloud, configure the following secrets:

```toml
# Google OAuth Configuration
google_client_id = "your_client_id_here"
google_client_secret = "your_client_secret_here"
redirect_uri = "https://your-app-name.streamlit.app"

# Google Sheets Configuration
google_sheet_id = "your_google_sheet_id_here"
google_sheets_credentials = "{\"type\":\"service_account\",...}"
```

## Authentication Flow

1. **Login Screen**: Users see a welcome screen with Google sign-in option
2. **OAuth Redirect**: Users are redirected to Google for authentication
3. **User Verification**: Google verifies the user and returns user information
4. **Session Creation**: Application creates a secure session for the user
5. **Data Access**: Users can now access the employee data form

## Data Collection

The application collects the following information:

- **Name**: Employee's full name (pre-filled from Google account)
- **Employee Number**: TCS employee identification number
- **Profile Type**: Technical expertise level (Non-Technical, Somewhat technical, Technical)
- **Timestamp**: Automatic timestamp of submission
- **User Email**: Email address from Google account

## File Structure

```
AIDG/
├── employee_data_form.py    # Main application
├── google_oauth.py         # OAuth authentication module
├── requirements.txt        # Python dependencies
├── oauth_setup.md         # OAuth configuration guide
├── README.md              # This file
├── .env                   # Environment variables (create this)
└── service_account_key.json # Google service account key (create this)
```

## Security Features

- **OAuth 2.0**: Secure authentication with Google
- **Session Management**: Automatic session timeout and logout
- **Data Validation**: Input validation and error handling
- **Secure Storage**: Credentials stored in environment variables or Streamlit secrets
- **HTTPS Support**: Full HTTPS support for production deployments

## Development

### Local Development

1. Set `dev=True` in your `.env` file
2. Run with `streamlit run employee_data_form.py`
3. Access at `http://localhost:8501`

### Testing

The application includes a simplified authentication mode for development when Google OAuth is not configured. This allows for testing without setting up full OAuth credentials.

## Troubleshooting

### Common Issues

1. **Authentication Errors**
   - Verify Google OAuth credentials are correctly configured
   - Check redirect URIs match your deployment URL
   - Ensure required Google APIs are enabled

2. **Google Sheets Access**
   - Verify service account has access to the Google Sheet
   - Check that the Google Sheets API is enabled
   - Ensure the sheet ID is correct

3. **Environment Variables**
   - Make sure all required environment variables are set
   - Check that the `.env` file is in the correct location
   - Verify Streamlit secrets are configured for cloud deployment

For detailed troubleshooting, see the [OAuth Setup Guide](oauth_setup.md).

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is proprietary to TCS Uruguay.

## Support

For technical support or questions about this application, please contact the development team.
