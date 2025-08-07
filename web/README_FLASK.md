# DFIR Log Sorter - Flask Web Application

A modern, web-based Digital Forensics and Incident Response (DFIR) tool for timeline analysis and log management with enhanced time entry and automatic file generation.

## 🌟 Features

### Core Functionality
- **Log Entry Management**: Add, edit, delete, and sort log entries with timestamps
- **Enhanced Time Entry**: Multiple time input methods including datetime-local picker and manual entry
- **Severity Classification**: Five levels (Critical, High, Medium, Low, Info) with visual indicators
- **Investigation Sessions**: Named investigation sessions with automatic file organization
- **Real-time Sorting**: Chronological sorting of log entries by timestamp
- **Export Options**: Multiple export formats (TXT, CSV, JSON)

### Advanced Features
- **Automatic File Generation**: Creates structured log files in the `logs/` folder
- **Session Management**: Persistent investigation sessions with Flask sessions
- **Responsive Design**: Modern, dark-themed UI that works on all devices
- **Flash Messages**: User feedback for all operations
- **Error Handling**: Comprehensive error handling and validation

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Navigate to the web directory:**
   ```bash
   cd ManafProject/web
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Access the application:**
   Open your browser and go to: `http://localhost:5000`

### Alternative: Use the batch file
```bash
run_flask.bat
```

## 📁 Project Structure

```
ManafProject/web/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── run_flask.bat         # Windows batch file to run the app
├── test_flask.py         # Test script for verification
├── logs/                 # Generated log files (auto-created)
├── static/               # Static assets
│   ├── styles.css        # Application styling
│   └── script.js         # Frontend JavaScript
└── templates/            # HTML templates
    ├── base.html         # Base template
    ├── setup.html        # Investigation setup page
    ├── index.html        # Main application page
    └── error.html        # Error page template
```

## 🔧 Configuration

### Session Settings
- **Secret Key**: Configured in `app.py` (change for production)
- **Session Lifetime**: 8 hours (configurable)
- **Session Storage**: Server-side with Flask sessions

### File Storage
- **Logs Directory**: `logs/` (auto-created)
- **File Naming**: `{investigation_name}_{timestamp}.txt`
- **File Format**: Structured text with headers and summaries

## 📊 Usage Guide

### 1. Starting an Investigation

1. **Access the application** at `http://localhost:5000`
2. **Enter investigation name** (e.g., "Company_SecInc_2024", "Case_001_MalwareAnalysis")
3. **Click "Start Investigation"** to begin

### 2. Adding Log Entries

1. **Enter timestamp** using one of these methods:
   - **Datetime picker**: Click the calendar icon for easy selection
   - **Manual entry**: Type in format `YYYY-MM-DD-H-M-S`
   - **"Now" button**: Automatically insert current time

2. **Enter log description** in the long input field

3. **Select severity level** from the dropdown:
   - 🔴 Critical
   - 🟠 High  
   - 🟡 Medium
   - 🔵 Low
   - ℹ️ Info

4. **Click "Add Entry"** to save

### 3. Managing Entries

- **Sort**: Click "Sort Entries" to arrange chronologically
- **Edit**: Click the edit icon on any entry
- **Delete**: Click the delete icon on any entry
- **Clear All**: Remove all entries from current session

### 4. Exporting Data

- **Export to File**: Creates a structured TXT file in `logs/` folder
- **Export CSV**: Download as CSV format
- **Export JSON**: Download as JSON format

## 📄 File Output Format

### Generated Log File Structure
```
================================================================================
DFIR Investigation Log: {investigation_name}
================================================================================
Generated: 2024-01-15 14:30:00
Total Entries: 25
================================================================================

SUMMARY BY SEVERITY:
----------------------------------------
🔴 Critical: 2 entries
🟠 High: 5 entries
🟡 Medium: 8 entries
🔵 Low: 6 entries
ℹ️ Info: 4 entries

================================================================================
TIMELINE (Chronological Order)
================================================================================

[2024-01-15 09:00:00] ℹ️ INFO: Investigation started
[2024-01-15 09:15:30] 🔴 CRITICAL: Malware detected on endpoint
[2024-01-15 09:20:15] 🟠 HIGH: Network traffic anomaly detected
...
```

## 🔌 API Endpoints

### Core Routes
- `GET /` - Main application (redirects to setup if no session)
- `GET /setup` - Investigation setup page
- `POST /start_investigation` - Start new investigation
- `POST /reset` - Reset current investigation

### API Endpoints
- `GET /api/entries` - Get all log entries
- `POST /api/entries` - Add new log entry
- `PUT /api/entries/<id>` - Update log entry
- `DELETE /api/entries/<id>` - Delete log entry
- `POST /api/sort` - Sort entries by timestamp
- `POST /api/clear` - Clear all entries
- `GET /current_time` - Get current time in various formats

### Export Endpoints
- `POST /api/export/file` - Export to TXT file
- `GET /api/export/csv` - Export to CSV
- `GET /api/export/json` - Export to JSON

## 🎨 UI Features

### Design Elements
- **Dark Theme**: Professional dark interface
- **Card Layout**: Organized sections with cards
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Visual Indicators**: Emoji icons for severity levels
- **Hover Effects**: Interactive elements with smooth transitions
- **Status Messages**: Real-time feedback for all actions

### Enhanced Time Entry
- **Datetime-local input**: Native browser date/time picker
- **Manual entry**: Support for custom timestamp formats
- **Auto-formatting**: Automatic parsing of various time formats
- **Current time button**: One-click current time insertion

## 🛠️ Technical Details

### Backend Technologies
- **Flask**: Python web framework
- **Jinja2**: Template engine
- **Session Management**: Flask sessions for state persistence
- **File I/O**: Automatic log file generation
- **JSON API**: RESTful API endpoints

### Frontend Technologies
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with CSS Grid and Flexbox
- **JavaScript**: Dynamic interactions and API calls
- **Fetch API**: Asynchronous data handling

### Data Validation
- **Input Validation**: Server-side validation for all inputs
- **Timestamp Parsing**: Multiple format support
- **Error Handling**: Comprehensive error messages
- **Session Security**: Secure session management

## 🔒 Security Considerations

### Development vs Production
- **Secret Key**: Change the secret key in production
- **Debug Mode**: Disable debug mode in production
- **HTTPS**: Use HTTPS in production environments
- **Input Sanitization**: All inputs are validated and sanitized

## 🧪 Testing

### Test the Application
```bash
python test_flask.py
```

This will test:
- Server availability
- Setup page accessibility
- API endpoints functionality
- Session management
- Entry creation and retrieval

## 🐛 Troubleshooting

### Common Issues

1. **Port 5000 already in use**
   ```bash
   # Change port in app.py
   app.run(debug=True, host='0.0.0.0', port=5001)
   ```

2. **Dependencies not installed**
   ```bash
   pip install -r requirements.txt
   ```

3. **Permission errors with logs folder**
   - Ensure write permissions in the web directory
   - The application will create the logs folder automatically

4. **Session not persisting**
   - Check that cookies are enabled in your browser
   - Clear browser cache if needed

## 📈 Performance

### Optimizations
- **Session Storage**: Efficient server-side session management
- **Minimal Dependencies**: Lightweight Flask application
- **Static Assets**: Optimized CSS and JavaScript
- **Caching**: Browser caching for static assets

### Scalability
- **Stateless API**: RESTful design for scalability
- **File-based Storage**: Simple, reliable storage mechanism
- **Session Management**: Configurable session lifetime

## 🤝 Contributing

### Development Setup
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `python app.py`
4. Make changes and test with `python test_flask.py`

### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add comments for complex logic
- Maintain consistent formatting

## 📝 License

This project is developed for educational and professional use in Digital Forensics and Incident Response.

## 🆘 Support

For issues or questions:
1. Check the troubleshooting section
2. Run the test script: `python test_flask.py`
3. Review the application logs in the console output

---

**🎯 Ready for Professional DFIR Work!**

The Flask version provides a robust, web-based solution for timeline analysis with enhanced usability and automatic file generation capabilities.
