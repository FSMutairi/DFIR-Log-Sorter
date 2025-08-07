#!/usr/bin/env python3
"""
DFIR Log Sorter - Flask Web Application
A Digital Forensics and Incident Response tool with enhanced time entry and automatic log file generation.

Author: Faris
Created: 2025
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
import os
import json
from datetime import datetime, timedelta
import re
from pathlib import Path
import uuid

app = Flask(__name__)
app.secret_key = 'dfir_log_sorter_secret_key_2024'  # Change this in production
app.permanent_session_lifetime = timedelta(hours=8)  # Session expires after 8 hours

# Ensure required directories exist
LOGS_DIR = Path(__file__).parent / 'logs'
LOGS_DIR.mkdir(exist_ok=True)

class LogEntry:
    """Represents a single log entry with timestamp and description."""
    
    def __init__(self, timestamp, description, severity="Info", entry_id=None):
        self.id = entry_id or str(uuid.uuid4())
        self.timestamp = timestamp
        self.description = description
        self.severity = severity
        self.parsed_time = self._parse_timestamp(timestamp)
        self.created_at = datetime.now()
    
    def _parse_timestamp(self, timestamp_str):
        """Parse various timestamp formats into datetime object."""
        formats = [
            "%Y-%m-%d-%H-%M-%S",      # YYYY-MM-DD-H-M-S
            "%Y-%m-%d %H:%M:%S",      # YYYY-MM-DD HH:MM:SS
            "%Y-%m-%dT%H:%M",         # HTML datetime-local format
            "%Y-%m-%dT%H:%M:%S",      # ISO format
            "%Y/%m/%d %H:%M:%S",      # YYYY/MM/DD HH:MM:SS
            "%d/%m/%Y %H:%M:%S",      # DD/MM/YYYY HH:MM:SS
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(timestamp_str.strip(), fmt)
            except ValueError:
                continue
        
        # Try ISO format parsing
        try:
            return datetime.fromisoformat(timestamp_str.replace('T', ' '))
        except:
            print(f"Warning: Could not parse timestamp '{timestamp_str}', using current time")
            return datetime.now()
    
    def to_dict(self):
        """Convert log entry to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'timestamp': self.timestamp,
            'description': self.description,
            'severity': self.severity,
            'parsed_time': self.parsed_time.isoformat(),
            'created_at': self.created_at.isoformat()
        }
    
    def to_log_line(self):
        """Convert entry to formatted log line for file output."""
        severity_icon = {
            'Critical': '🔴',
            'High': '🟠',
            'Medium': '🟡',
            'Low': '🔵',
            'Info': 'ℹ️'
        }.get(self.severity, 'ℹ️')
        
        return f"[{self.parsed_time.strftime('%Y-%m-%d %H:%M:%S')}] {severity_icon} {self.severity.upper()}: {self.description}"

def get_session_logs():
    """Get log entries from session."""
    if 'log_entries' not in session:
        session['log_entries'] = []
    
    log_entries = []
    for entry_data in session['log_entries']:
        # Extract only the parameters that LogEntry.__init__ accepts
        entry = LogEntry(
            timestamp=entry_data['timestamp'],
            description=entry_data['description'],
            severity=entry_data['severity'],
            entry_id=entry_data['id']
        )
        log_entries.append(entry)
    
    return log_entries

def save_session_logs(log_entries):
    """Save log entries to session."""
    session['log_entries'] = [entry.to_dict() for entry in log_entries]
    session.permanent = True

def get_investigation_folder(investigation_name):
    """Get or create investigation folder."""
    safe_name = re.sub(r'[<>:"/\\|?*]', '_', investigation_name)
    investigation_dir = LOGS_DIR / safe_name
    investigation_dir.mkdir(exist_ok=True)
    return investigation_dir

def save_logs_to_file(investigation_name, log_entries):
    """Save logs to a single CSV file in the investigation folder (overwrites previous)."""
    if not log_entries:
        return None
    
    investigation_dir = get_investigation_folder(investigation_name)
    filename = "investigation_logs.csv"
    filepath = investigation_dir / filename
    
    # Sort entries by timestamp
    sorted_entries = sorted(log_entries, key=lambda x: x.parsed_time)
    
    # Write CSV file (overwrite with all current entries)
    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        f.write("Timestamp,Severity,Description\n")
        for entry in sorted_entries:
            # Escape commas in description
            description = entry.description.replace('"', '""')
            f.write(f'"{entry.timestamp}","{entry.severity}","{description}"\n')
    
    return filepath

def save_ai_analysis_to_file(investigation_name, analysis_text):
    """Save AI analysis to a text file in the investigation folder."""
    if not analysis_text:
        return None
    
    investigation_dir = get_investigation_folder(investigation_name)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"ai_analysis_{timestamp}.txt"
    filepath = investigation_dir / filename
    
    # Generate file content
    content = []
    content.append("=" * 80)
    content.append(f"AI Security Analysis: {investigation_name}")
    content.append("=" * 80)
    content.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    content.append("=" * 80)
    content.append("")
    content.append(analysis_text)
    content.append("")
    content.append("=" * 80)
    content.append("End of AI Analysis")
    content.append("=" * 80)
    
    # Write to file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(content))
    
    return filepath

@app.route('/')
def index():
    """Main page - check if investigation is set."""
    if 'investigation_name' not in session:
        return redirect(url_for('setup_investigation'))
    
    log_entries = get_session_logs()
    return render_template('index.html', 
                         investigation_name=session['investigation_name'],
                         log_count=len(log_entries))

@app.route('/setup')
def setup_investigation():
    """Setup page for entering investigation name."""
    return render_template('setup.html')

@app.route('/start_investigation', methods=['POST'])
def start_investigation():
    """Start a new investigation with the given name."""
    investigation_name = request.form.get('investigation_name', '').strip()
    
    if not investigation_name:
        flash('Investigation name is required', 'error')
        return redirect(url_for('setup_investigation'))
    
    if len(investigation_name) < 3:
        flash('Investigation name must be at least 3 characters long', 'error')
        return redirect(url_for('setup_investigation'))
    
    # Clear any existing session data
    session.clear()
    session['investigation_name'] = investigation_name
    session['created_at'] = datetime.now().isoformat()
    session.permanent = True
    
    flash(f'Investigation "{investigation_name}" started successfully', 'success')
    return redirect(url_for('index'))

@app.route('/api/entries', methods=['GET'])
def get_entries():
    """Get all log entries."""
    log_entries = get_session_logs()
    return jsonify({
        'entries': [entry.to_dict() for entry in log_entries],
        'investigation_name': session.get('investigation_name', 'Unknown'),
        'total_count': len(log_entries)
    })

@app.route('/api/entries', methods=['POST'])
def add_entry():
    """Add a new log entry."""
    data = request.get_json()
    
    timestamp = data.get('timestamp', '').strip()
    description = data.get('description', '').strip()
    severity = data.get('severity', 'Info')
    
    # Validation
    if not timestamp:
        return jsonify({'error': 'Timestamp is required'}), 400
    
    if not description:
        return jsonify({'error': 'Description is required'}), 400
    
    if len(description) < 5:
        return jsonify({'error': 'Description must be at least 5 characters long'}), 400
    
    try:
        # Create new log entry
        log_entry = LogEntry(timestamp, description, severity)
        
        # Get existing entries and add new one
        log_entries = get_session_logs()
        log_entries.append(log_entry)
        
        # Save back to session
        save_session_logs(log_entries)
        
        # Automatically save to investigation folder
        investigation_name = session.get('investigation_name', 'Unknown')
        try:
            save_logs_to_file(investigation_name, log_entries)
        except Exception as e:
            print(f"Warning: Failed to auto-save logs: {e}")
        
        return jsonify({
            'success': True,
            'entry': log_entry.to_dict(),
            'total_count': len(log_entries)
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to add entry: {str(e)}'}), 500

@app.route('/api/entries/<entry_id>', methods=['PUT'])
def update_entry(entry_id):
    """Update an existing log entry."""
    data = request.get_json()
    
    timestamp = data.get('timestamp', '').strip()
    description = data.get('description', '').strip()
    severity = data.get('severity', 'Info')
    
    # Validation
    if not timestamp or not description:
        return jsonify({'error': 'Timestamp and description are required'}), 400
    
    try:
        log_entries = get_session_logs()
        
        # Find and update the entry
        for entry in log_entries:
            if entry.id == entry_id:
                entry.timestamp = timestamp
                entry.description = description
                entry.severity = severity
                entry.parsed_time = entry._parse_timestamp(timestamp)
                break
        else:
            return jsonify({'error': 'Entry not found'}), 404
        
        # Save back to session
        save_session_logs(log_entries)
        
        # Automatically update CSV file in investigation folder
        investigation_name = session.get('investigation_name', 'Unknown')
        try:
            save_logs_to_file(investigation_name, log_entries)
        except Exception as e:
            print(f"Warning: Failed to auto-save logs after update: {e}")
        
        return jsonify({'success': True})
        
    except Exception as e:
        return jsonify({'error': f'Failed to update entry: {str(e)}'}), 500

@app.route('/api/entries/<entry_id>', methods=['DELETE'])
def delete_entry(entry_id):
    """Delete a log entry."""
    try:
        log_entries = get_session_logs()
        
        # Find and remove the entry
        original_count = len(log_entries)
        log_entries = [entry for entry in log_entries if entry.id != entry_id]
        
        if len(log_entries) == original_count:
            return jsonify({'error': 'Entry not found'}), 404
        
        # Save back to session
        save_session_logs(log_entries)
        
        # Automatically update CSV file in investigation folder
        investigation_name = session.get('investigation_name', 'Unknown')
        try:
            save_logs_to_file(investigation_name, log_entries)
        except Exception as e:
            print(f"Warning: Failed to auto-save logs after deletion: {e}")
        
        return jsonify({'success': True, 'total_count': len(log_entries)})
        
    except Exception as e:
        return jsonify({'error': f'Failed to delete entry: {str(e)}'}), 500

@app.route('/api/sort', methods=['POST'])
def sort_entries():
    """Sort all log entries by timestamp."""
    try:
        log_entries = get_session_logs()
        
        if not log_entries:
            return jsonify({'error': 'No entries to sort'}), 400
        
        # Sort entries by parsed timestamp
        log_entries.sort(key=lambda x: x.parsed_time)
        
        # Save back to session
        save_session_logs(log_entries)
        
        return jsonify({
            'success': True,
            'entries': [entry.to_dict() for entry in log_entries],
            'message': f'Sorted {len(log_entries)} entries by timestamp'
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to sort entries: {str(e)}'}), 500

@app.route('/api/clear', methods=['POST'])
def clear_entries():
    """Clear all log entries."""
    session['log_entries'] = []
    
    # Delete or update the CSV file when clearing all entries
    investigation_name = session.get('investigation_name', 'Unknown')
    try:
        investigation_dir = get_investigation_folder(investigation_name)
        csv_filepath = investigation_dir / "investigation_logs.csv"
        if csv_filepath.exists():
            csv_filepath.unlink()  # Delete the CSV file since no entries remain
    except Exception as e:
        print(f"Warning: Failed to delete CSV file after clearing: {e}")
    
    return jsonify({'success': True, 'message': 'All entries cleared'})

@app.route('/api/export/file', methods=['POST'])
def export_to_file():
    """Export logs to a text file in the logs directory."""
    try:
        log_entries = get_session_logs()
        
        if not log_entries:
            return jsonify({'error': 'No entries to export'}), 400
        
        investigation_name = session.get('investigation_name', 'Unknown_Investigation')
        filepath = save_logs_to_file(investigation_name, log_entries)
        
        if filepath:
            return jsonify({
                'success': True,
                'message': f'Investigation log saved to {filepath.name}',
                'filename': filepath.name,
                'entry_count': len(log_entries)
            })
        else:
            return jsonify({'error': 'Failed to save log file'}), 500
            
    except Exception as e:
        return jsonify({'error': f'Failed to export: {str(e)}'}), 500

@app.route('/api/export/csv', methods=['GET'])
def export_csv():
    """Export logs to CSV format."""
    try:
        log_entries = get_session_logs()
        
        if not log_entries:
            return jsonify({'error': 'No entries to export'}), 400
        
        # Sort entries
        sorted_entries = sorted(log_entries, key=lambda x: x.parsed_time)
        
        # Generate CSV content
        csv_lines = ['Timestamp,Severity,Description,Parsed Time']
        for entry in sorted_entries:
            # Escape quotes in description for CSV
            escaped_description = entry.description.replace('"', '""')
            csv_lines.append(f'"{entry.timestamp}","{entry.severity}","{escaped_description}","{entry.parsed_time.strftime("%Y-%m-%d %H:%M:%S")}"')
        
        return jsonify({
            'success': True,
            'csv_content': '\n'.join(csv_lines),
            'filename': f"{session.get('investigation_name', 'investigation')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to export CSV: {str(e)}'}), 500

@app.route('/api/export/txt', methods=['GET'])
def export_txt():
    """Export logs to TXT format."""
    try:
        log_entries = get_session_logs()
        
        if not log_entries:
            return jsonify({'error': 'No entries to export'}), 400
        
        # Sort entries
        sorted_entries = sorted(log_entries, key=lambda x: x.parsed_time)
        
        # Generate TXT content
        txt_lines = [
            f"DFIR Log Sorter - Timeline Export",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Investigation: {session.get('investigation_name', 'Unknown')}",
            f"Total Entries: {len(sorted_entries)}",
            f"Created: {session.get('created_at', 'Unknown')}",
            "=" * 80,
            ""
        ]
        
        for i, entry in enumerate(sorted_entries, 1):
            txt_lines.append(f"{i:3d}. [{entry.timestamp}] [{entry.severity}] {entry.description}")
        
        return jsonify({
            'success': True,
            'txt_content': '\n'.join(txt_lines),
            'filename': f"{session.get('investigation_name', 'investigation')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to export TXT: {str(e)}'}), 500

@app.route('/api/import/csv', methods=['POST'])
def import_csv():
    """Import log entries from CSV data."""
    try:
        data = request.get_json()
        
        if not data or 'entries' not in data:
            return jsonify({'error': 'No entries data provided'}), 400
        
        entries_data = data['entries']
        
        if not entries_data:
            return jsonify({'error': 'No entries to import'}), 400
        
        # Get current log entries from session
        current_entries = get_session_logs()
        imported_count = 0
        
        # Process each entry
        for entry_data in entries_data:
            try:
                timestamp = entry_data.get('timestamp', '').strip()
                description = entry_data.get('description', '').strip()
                severity = entry_data.get('severity', 'Info').strip()
                
                # Validate required fields
                if not timestamp or not description:
                    continue
                
                # Normalize severity
                severity_map = {
                    'critical': 'Critical',
                    'high': 'High',
                    'medium': 'Medium',
                    'low': 'Low',
                    'info': 'Info',
                    'information': 'Info'
                }
                severity = severity_map.get(severity.lower(), severity)
                
                # Create LogEntry object
                log_entry = LogEntry(timestamp, description, severity)
                current_entries.append(log_entry)
                imported_count += 1
                
            except Exception as e:
                print(f"Warning: Skipping invalid entry: {e}")
                continue
        
        # Save updated entries back to session
        session['log_entries'] = [entry.to_dict() for entry in current_entries]
        
        return jsonify({
            'success': True,
            'imported_count': imported_count,
            'total_entries': len(current_entries),
            'message': f'Successfully imported {imported_count} entries'
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to import CSV: {str(e)}'}), 500

@app.route('/api/ai-analysis', methods=['POST'])
def ai_analysis():
    """Analyze logs using Ollama AI."""
    try:
        data = request.get_json()
        
        if not data or 'logs' not in data:
            return jsonify({'error': 'No logs data provided'}), 400
        
        logs_data = data['logs']
        
        if not logs_data:
            return jsonify({'error': 'No logs to analyze'}), 400
        
        # Format logs for the prompt
        log_text = "\n".join([
            f"[{log.get('timestamp', '')}] [{log.get('severity', 'Info')}] {log.get('description', '')}"
            for log in logs_data
        ])
        
        # Create the full prompt (same as in Model.py)
        user_input = f"""Incident Investigation Request

I am currently investigating a cyberattack on my company. Below is a series of suspicious log entries I've extracted from our environment. I need your help to analyze this potential breach comprehensively.

Please perform a thorough investigation of the logs and provide insight into the following:

What You Should Analyze and Report:
1. Attack Timeline & Description

    1-1. Construct a detailed timeline of the incident based on the log timestamps

    1-2. Clearly describe the attacker's goals and tactics (Initial Access, Execution, Lateral Movement, etc.)

2. Compromised Elements

    2-1. List all compromised user accounts

    2-2. Identify affected hosts, services, and sensitive data assets

3. IOCs (Indicators of Compromise)
Extract any relevant:

    3-1. Malicious IPs

    3-2. File hashes / names

    3-3. Domains (e.g. C2 servers)

    3-4. Suspicious processes or commands

    3-5. Ports used (e.g., 8080, 9001, SSH)

4. Containment & Remediation Recommendations

    4-1. Give prioritized steps to contain the incident (e.g., isolate hosts, disable accounts)

    4-2. Suggest remediation actions (malware removal, password rotation, patching, etc.)

    4-3. Include command-line examples for Linux/Windows systems if applicable

    5. Immediate Actions for SOC/IR Team

    5-1. As an investigator, what actions should I take right now?

    5-2. Include advice on:

    5-2-1. Evidence preservation

    5-2-2. Log collection

    5-2-3. Internal and external communication

    5-2-4. Next phase of forensic investigation

6. (Optional) Executive Summary

    6-1. If possible, provide a short summary suitable for non-technical management

    6-2. Focus on impact, business risk, and high-level next steps

These are the logs:

{log_text}

Please prioritize accuracy, clarity, and real-world best practices. If something is unclear from the logs, feel free to note assumptions or ask for more data."""
        
        try:
            import ollama
        except ImportError:
            return jsonify({'error': 'Ollama is not installed. Please install it with: pip install ollama'}), 500
        
        # Make the API call to Ollama
        try:
            response = ollama.chat(model="qwen2.5:7b", messages=[{"role": "user", "content": user_input}])
            analysis_result = response['message']['content']
            
            # Automatically save AI analysis to investigation folder
            investigation_name = session.get('investigation_name', 'Unknown')
            try:
                save_ai_analysis_to_file(investigation_name, analysis_result)
            except Exception as save_error:
                print(f"Warning: Failed to auto-save AI analysis: {save_error}")
            
            return jsonify({
                'success': True,
                'analysis': analysis_result,
                'logs_analyzed': len(logs_data),
                'message': f'Successfully analyzed {len(logs_data)} log entries'
            })
            
        except Exception as ollama_error:
            return jsonify({'error': f'Ollama analysis failed: {str(ollama_error)}. Please ensure Ollama is running and the qwen2.5:7b model is available.'}), 500
        
    except Exception as e:
        return jsonify({'error': f'Failed to analyze logs: {str(e)}'}), 500

@app.route('/reset', methods=['POST'])
def reset_investigation():
    """Reset the current investigation."""
    session.clear()
    flash('Investigation reset. You can start a new investigation.', 'info')
    return redirect(url_for('setup_investigation'))

@app.route('/current_time')
def current_time():
    """Get current time in various formats for the frontend."""
    now = datetime.now()
    return jsonify({
        'datetime_local': now.strftime('%Y-%m-%dT%H:%M:%S'),  # For HTML datetime-local input with seconds
        'formatted': now.strftime('%Y-%m-%d-%H-%M-%S'),    # Our custom format
        'iso': now.isoformat(),
        'display': now.strftime('%Y-%m-%d %H:%M:%S')
    })

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', 
                         title='Page Not Found',
                         message='The page you are looking for does not exist.'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html',
                         title='Internal Server Error', 
                         message='An internal server error occurred.'), 500

if __name__ == '__main__':
    print("🔍 Starting DFIR Log Sorter Flask Application...")
    print(f"📁 Logs directory: {LOGS_DIR.absolute()}")
    print("🌐 Application will be available at: http://localhost:5000")
    print("🔄 Auto-reload enabled for development")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
