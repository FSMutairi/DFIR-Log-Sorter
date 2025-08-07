# 🔍 DFIR Log Sorter

A comprehensive Digital Forensics and Incident Response (DFIR) log management tool with AI-powered analysis capabilities. Available in both **Desktop** (Tkinter) and **Web** (Flask) versions.

## 🚀 Features

### 📊 **Log Management**
- **Timeline Control**: Add, edit, delete, and sort log entries
- **Multiple Severity Levels**: Critical, High, Medium, Low, Info
- **Timestamp Support**: Manual entry and date/time picker
- **CSV Import/Export**: Bulk data operations
- **Auto-Save**: Automatic CSV backup to investigation folders

### 🤖 **AI-Powered Analysis**
- **Ollama Integration**: Local LLM analysis using qwen2.5:7b model
- **Security Analysis**: Automated threat detection and prioritization
- **Investigation Context**: AI understands investigation scope and timeline
- **Auto-Save Results**: Analysis saved as timestamped TXT files

### 📁 **Investigation Management**
- **Named Investigations**: Create dedicated folders for each case
- **Organized Storage**: Automatic file organization in `logs/Investigation_Name/`
- **File Structure**:
  ```
  logs/
  └── Investigation_Name/
      ├── investigation_logs.csv          ← Current log data
      ├── ai_analysis_20241207_143022.txt ← AI analysis results
      └── ai_analysis_20241207_150531.txt ← Multiple analyses
  ```

## 🖥️ Desktop Application

### Requirements
- Python 3.7+
- Tkinter (usually included with Python)
- Ollama (for AI analysis)

### Installation
```bash
cd app/
pip install -r requirements.txt
```

### Usage
```bash
# Run the desktop application
python dfir_log_sorter.py

# Or use the batch file (Windows)
run_dfir_app.bat
```

### Features
- **Native GUI**: Tkinter-based interface
- **Threading**: Non-blocking AI analysis
- **Progress Tracking**: Visual progress bars
- **Export Options**: CSV, TXT formats
- **Sort Controls**: Ascending/Descending timeline sorting

## 🌐 Web Application

### Requirements
- Python 3.7+
- Flask
- Ollama (for AI analysis)

### Installation
```bash
cd web/
pip install -r requirements.txt
```

### Usage
```bash
# Run the Flask web server
python app.py

# Or use the batch file (Windows)
run_flask.bat
```

### Features
- **Modern Web UI**: Responsive design with drag & drop
- **Real-time Updates**: Live status and progress indicators
- **Session Management**: Persistent investigation state
- **Export/Import**: CSV file operations
- **AI Analysis**: Web-based LLM integration

## 🤖 AI Analysis

### Setup
1. **Install Ollama**: [https://ollama.ai/](https://ollama.ai/)
2. **Pull Model**: `ollama pull qwen2.5:7b`
3. **Start Ollama**: `ollama serve`

### Analysis Features
- **Security Prioritization**: Identifies critical threats
- **Timeline Analysis**: Correlates events chronologically
- **Threat Assessment**: Evaluates severity and impact
- **Recommendations**: Provides actionable insights

## 📁 Project Structure

```
ManafProject/
├── app/                          # Desktop Application
│   ├── dfir_log_sorter.py       # Main desktop app
│   ├── requirements.txt          # Python dependencies
│   ├── run_dfir_app.bat         # Windows launcher
│   └── README.md                # Desktop documentation
├── web/                         # Web Application
│   ├── app.py                   # Flask server
│   ├── requirements.txt          # Web dependencies
│   ├── run_flask.bat            # Windows launcher
│   ├── static/                  # CSS, JS, assets
│   ├── templates/               # HTML templates
│   └── README_FLASK.md          # Web documentation
├── Model.py                     # AI prompt configuration
├── .gitignore                   # Git ignore rules
└── README.md                    # This file
```

## 🔧 Configuration

### AI Model Settings
Edit `Model.py` to customize the AI analysis prompt:
```python
# Customize the analysis prompt
user_input = f"""
These are the logs:
{logs_text}

Please prioritize...
"""
```

### Investigation Settings
- **Auto-save**: Enabled by default
- **File Formats**: CSV for logs, TXT for analysis
- **Timestamp Format**: `YYYY-MM-DD-HH-MM-SS`

## 🚀 Quick Start

### Desktop Version
1. Navigate to `app/` directory
2. Install dependencies: `pip install -r requirements.txt`
3. Run: `python dfir_log_sorter.py`
4. Enter investigation name when prompted
5. Start adding log entries and analyzing!

### Web Version
1. Navigate to `web/` directory
2. Install dependencies: `pip install -r requirements.txt`
3. Run: `python app.py`
4. Open browser to `http://localhost:5000`
5. Enter investigation name and start working!

## 📋 Dependencies

### Desktop App
- `tkinter` - GUI framework
- `ollama` - AI model integration
- `pathlib` - File path handling
- `datetime` - Timestamp operations
- `csv` - Data import/export

### Web App
- `flask` - Web framework
- `ollama` - AI model integration
- `pathlib` - File path handling
- `datetime` - Timestamp operations
- `csv` - Data import/export

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues, questions, or feature requests:
- Email me : farissaudm@gmail.com
- Create an issue on GitHub
- Check the documentation in each app's README
- Ensure Ollama is properly installed and running

## 👨‍💻 Author

**FSMutairi** - *Creator & Developer*

---

**Made with ❤️ for the DFIR community**
