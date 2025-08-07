# DFIR Log Sorter

A Digital Forensics and Incident Response (DFIR) tool for logging and sorting events by timestamp to create accurate timelines for incident analysis.

## Features

- **Log Entry Management**: Add log entries with timestamps, severity levels, and detailed descriptions
- **Flexible Timestamp Parsing**: Supports multiple timestamp formats commonly used in DFIR
- **Timeline Sorting**: Sort all log entries chronologically to create accurate timelines
- **Severity Levels**: Categorize events by severity (Critical, High, Medium, Low, Info)
- **Export Capabilities**: Export sorted timelines to CSV or JSON format
- **Import Functionality**: Import existing log data from CSV files
- **Edit Entries**: Double-click entries to edit them
- **User-Friendly GUI**: Intuitive interface designed for forensic investigators

## Supported Timestamp Formats

The application automatically parses various timestamp formats:
- `YYYY-MM-DD HH:MM:SS` (e.g., 2024-01-15 14:30:25)
- `YYYY/MM/DD HH:MM:SS` (e.g., 2024/01/15 14:30:25)
- `DD/MM/YYYY HH:MM:SS` (e.g., 15/01/2024 14:30:25)
- `MM/DD/YYYY HH:MM:SS` (e.g., 01/15/2024 14:30:25)
- `YYYY-MM-DD HH:MM:SS.ffffff` (with microseconds)
- `YYYY-MM-DDTHH:MM:SS` (ISO format)
- `YYYY-MM-DDTHH:MM:SS.ffffffZ` (ISO with timezone)
- `DD-MM-YYYY HH:MM:SS`

## Installation

1. Ensure you have Python 3.7+ installed
2. Clone or download this application
3. No additional dependencies required (uses Python standard library)

### Linux Users
If tkinter is not installed:
```bash
sudo apt-get install python3-tk  # Ubuntu/Debian
sudo yum install tkinter         # CentOS/RHEL
```

## Usage

### Running the Application
```bash
python dfir_log_sorter.py
```

### Basic Workflow
1. **Add Log Entries**: Enter timestamp, select severity, and add description
2. **Use "Now" Button**: Quickly insert current timestamp
3. **Sort Timeline**: Click "Sort Logs by Timestamp" to organize chronologically
4. **Export Results**: Save sorted timeline as CSV or JSON
5. **Edit Entries**: Double-click any entry to modify it

### Import/Export
- **Import CSV**: Load existing log data from CSV files
- **Export CSV**: Save timeline for use in other tools
- **Export JSON**: Save with metadata for backup/sharing

## Use Cases

### Incident Response
- Log system events, user actions, and network activities
- Create chronological timeline of security incidents
- Document evidence collection timestamps
- Track investigation progress

### Digital Forensics
- Timeline analysis of file system events
- Correlate events across multiple sources
- Document chain of custody timestamps
- Create investigation reports

### Security Analysis
- Log security events and alerts
- Timeline malware behavior
- Document vulnerability exploitation
- Track remediation activities

## Example Workflow

1. **Initial Setup**: Start the application and begin adding relevant log entries
2. **Data Entry**: 
   ```
   Timestamp: 2024-01-15 09:15:30
   Severity: High
   Description: Suspicious file download detected from external IP 192.168.1.100
   ```
3. **Continue Adding**: Add all relevant events with accurate timestamps
4. **Sort Timeline**: Click "Sort Logs by Timestamp" to create chronological order
5. **Export**: Save the sorted timeline as CSV for further analysis or reporting

## File Formats

### CSV Export Format
```csv
Timestamp,Severity,Description,Parsed Time
2024-01-15 09:15:30,High,Suspicious file download,2024-01-15 09:15:30
```

### JSON Export Format
```json
{
  "export_time": "2024-01-15T10:30:45.123456",
  "total_entries": 5,
  "is_sorted": true,
  "entries": [
    {
      "timestamp": "2024-01-15 09:15:30",
      "description": "Suspicious file download",
      "severity": "High",
      "parsed_time": "2024-01-15T09:15:30"
    }
  ]
}
```

## Tips for DFIR Use

1. **Consistent Timezone**: Ensure all timestamps use the same timezone
2. **Detailed Descriptions**: Include relevant details like IPs, files, users
3. **Regular Sorting**: Sort frequently to maintain timeline accuracy
4. **Backup Data**: Export regularly to prevent data loss
5. **Source Documentation**: Note the source of each log entry in the description

## Troubleshooting

### Timestamp Issues
- If timestamps aren't parsing correctly, try reformatting to YYYY-MM-DD HH:MM:SS
- Check for extra spaces or special characters
- Ensure consistent date formats throughout your entries

### Performance
- Large datasets (1000+ entries) may take a moment to sort
- Consider breaking very large investigations into multiple files
- Export and reimport if experiencing slow performance

## Security Considerations

- Log entries are stored in memory only (not automatically saved to disk)
- Export files contain all entered data - secure appropriately
- Consider encryption for sensitive investigation data
- Review exported files before sharing

## License

This tool is provided for educational and professional DFIR use. Please ensure compliance with your organization's policies and applicable laws when conducting digital forensics activities.
