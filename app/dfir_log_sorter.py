#!/usr/bin/env python3
"""
DFIR Log Sorter Application
A Digital Forensics and Incident Response tool for logging and sorting events by timestamp.

Author: FSMutairi
Created: 2025
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import csv
import json
from typing import List, Dict, Any
import re
import threading
import os
from pathlib import Path


class LogEntry:
    """Represents a single log entry with timestamp and description."""
    
    def __init__(self, timestamp: str, description: str, severity: str = "Info"):
        self.timestamp = timestamp
        self.description = description
        self.severity = severity
        self.parsed_time = self._parse_timestamp(timestamp)
    
    def _parse_timestamp(self, timestamp: str) -> datetime:
        """Parse various timestamp formats into datetime object."""
        # Common timestamp formats for DFIR
        formats = [
            "%Y-%m-%d-%H-%M-%S",      # 2024-01-15-14-30-25 (custom format)
            "%Y-%m-%d %H:%M:%S",      # 2024-01-15 14:30:25
            "%Y/%m/%d %H:%M:%S",      # 2024/01/15 14:30:25
            "%d/%m/%Y %H:%M:%S",      # 15/01/2024 14:30:25
            "%m/%d/%Y %H:%M:%S",      # 01/15/2024 14:30:25
            "%Y-%m-%d %H:%M:%S.%f",   # 2024-01-15 14:30:25.123456
            "%Y-%m-%dT%H:%M:%S",      # 2024-01-15T14:30:25
            "%Y-%m-%dT%H:%M:%S.%fZ",  # 2024-01-15T14:30:25.123456Z
            "%d-%m-%Y %H:%M:%S",      # 15-01-2024 14:30:25
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(timestamp.strip(), fmt)
            except ValueError:
                continue
        
        # If no format matches, try to extract date/time components
        try:
            # Remove common timezone indicators
            clean_timestamp = re.sub(r'[+-]\d{2}:?\d{2}$|Z$', '', timestamp.strip())
            return datetime.fromisoformat(clean_timestamp.replace('T', ' '))
        except:
            # Return current time as fallback
            print(f"Warning: Could not parse timestamp '{timestamp}', using current time")
            return datetime.now()
    
    def __lt__(self, other):
        """Enable sorting by timestamp."""
        return self.parsed_time < other.parsed_time
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert log entry to dictionary for export."""
        return {
            "timestamp": self.timestamp,
            "description": self.description,
            "severity": self.severity,
            "parsed_time": self.parsed_time.isoformat()
        }


class DFIRLogSorter:
    """Main application class for DFIR Log Sorter."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("DFIR Log Sorter - Digital Forensics Timeline Tool")
        self.root.geometry("1200x800")
        self.root.configure(bg="#0f1419")
        self.root.resizable(True, True)
        
        # Set application icon and styling
        try:
            self.root.iconbitmap(default="")  # Remove default icon
        except:
            pass
        
        # Data storage
        self.log_entries: List[LogEntry] = []
        self.is_sorted = False
        self.investigation_name = "Default Investigation"
        self.session_start_time = datetime.now()
        
        # File management
        self.logs_dir = Path(__file__).parent / 'logs'
        self.logs_dir.mkdir(exist_ok=True)
        
        # Color scheme
        self.colors = {
            'bg_primary': '#0f1419',      # Dark blue-black
            'bg_secondary': '#1e2328',    # Slightly lighter
            'bg_accent': '#2d3748',       # Card background
            'text_primary': '#ffffff',    # White text
            'text_secondary': '#a0aec0',  # Light gray
            'accent_blue': '#4299e1',     # Blue accent
            'accent_green': '#48bb78',    # Green accent
            'accent_red': '#f56565',      # Red accent
            'accent_orange': '#ed8936',   # Orange accent
            'accent_purple': '#9f7aea',   # Purple accent
            'border': '#4a5568',          # Border color
            'hover': '#2d3748',           # Hover color
            'success': '#38a169',         # Success green
            'warning': '#d69e2e',         # Warning yellow
            'error': '#e53e3e'            # Error red
        }
        
        # Setup GUI
        self.setup_styles()
        self.create_widgets()
        self.center_window()
        
        # Show investigation setup dialog
        self.setup_investigation()
    
    def setup_styles(self):
        """Configure custom styles for the application."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Main title style
        style.configure('Title.TLabel', 
                       font=('Segoe UI', 20, 'bold'),
                       background=self.colors['bg_primary'],
                       foreground=self.colors['text_primary'])
        
        # Section headings
        style.configure('Heading.TLabel',
                       font=('Segoe UI', 11, 'bold'),
                       background=self.colors['bg_accent'],
                       foreground=self.colors['accent_blue'])
        
        # Subtitle style
        style.configure('Subtitle.TLabel',
                       font=('Segoe UI', 9),
                       background=self.colors['bg_accent'],
                       foreground=self.colors['text_secondary'])
        
        # Custom button styles
        style.configure('Primary.TButton',
                       font=('Segoe UI', 10, 'bold'),
                       padding=(20, 10),
                       background=self.colors['accent_blue'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor=self.colors['accent_blue'])
        
        style.configure('Success.TButton',
                       font=('Segoe UI', 10, 'bold'),
                       padding=(15, 8),
                       background=self.colors['success'],
                       foreground='white',
                       borderwidth=0)
        
        style.configure('Warning.TButton',
                       font=('Segoe UI', 10, 'bold'),
                       padding=(15, 8),
                       background=self.colors['warning'],
                       foreground='white',
                       borderwidth=0)
        
        style.configure('Danger.TButton',
                       font=('Segoe UI', 10, 'bold'),
                       padding=(15, 8),
                       background=self.colors['error'],
                       foreground='white',
                       borderwidth=0)
        
        style.configure('Secondary.TButton',
                       font=('Segoe UI', 10),
                       padding=(15, 8),
                       background=self.colors['bg_accent'],
                       foreground=self.colors['text_primary'],
                       borderwidth=1,
                       bordercolor=self.colors['border'])
        
        # Entry and text styles
        style.configure('Custom.TEntry',
                       font=('Consolas', 10),
                       fieldbackground=self.colors['bg_secondary'],
                       foreground=self.colors['text_primary'],
                       borderwidth=2,
                       insertcolor=self.colors['text_primary'],
                       bordercolor=self.colors['border'],
                       lightcolor=self.colors['border'],
                       darkcolor=self.colors['border'])
        
        # Combobox style
        style.configure('Custom.TCombobox',
                       font=('Segoe UI', 10),
                       fieldbackground=self.colors['bg_secondary'],
                       foreground=self.colors['text_primary'],
                       borderwidth=2,
                       bordercolor=self.colors['border'],
                       arrowcolor=self.colors['text_primary'],
                       background=self.colors['bg_secondary'])
        
        # Frame styles
        style.configure('Card.TLabelframe',
                       background=self.colors['bg_accent'],
                       borderwidth=2,
                       bordercolor=self.colors['border'],
                       relief='solid')
        
        style.configure('Card.TLabelframe.Label',
                       font=('Segoe UI', 12, 'bold'),
                       background=self.colors['bg_accent'],
                       foreground=self.colors['accent_blue'])
        
        # Treeview styling
        style.configure('Custom.Treeview',
                       background=self.colors['bg_secondary'],
                       foreground=self.colors['text_primary'],
                       fieldbackground=self.colors['bg_secondary'],
                       borderwidth=0,
                       font=('Segoe UI', 9))
        
        style.configure('Custom.Treeview.Heading',
                       font=('Segoe UI', 10, 'bold'),
                       background=self.colors['bg_accent'],
                       foreground=self.colors['text_primary'],
                       borderwidth=1,
                       bordercolor=self.colors['border'])
        
        # Map treeview colors
        style.map('Custom.Treeview',
                 background=[('selected', self.colors['accent_blue'])],
                 foreground=[('selected', 'white')])
        
        # Map button hover effects
        style.map('Primary.TButton',
                 background=[('active', '#3182ce'), ('pressed', '#2c5282')])
        style.map('Success.TButton',
                 background=[('active', '#2f855a'), ('pressed', '#276749')])
        style.map('Warning.TButton',
                 background=[('active', '#b7791f'), ('pressed', '#975a16')])
        style.map('Danger.TButton',
                 background=[('active', '#c53030'), ('pressed', '#9c2626')])
        style.map('Secondary.TButton',
                 background=[('active', self.colors['hover']), ('pressed', '#1a202c')])
    
    def center_window(self):
        """Center the window on the screen."""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (self.root.winfo_width() // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.root.winfo_height() // 2)
        self.root.geometry(f"+{x}+{y}")
    
    def create_widgets(self):
        """Create and layout all GUI widgets."""
        # Main container with gradient-like effect
        main_frame = tk.Frame(self.root, bg=self.colors['bg_primary'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # Header section with logo area
        header_frame = tk.Frame(main_frame, bg=self.colors['bg_primary'], height=80)
        header_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
        header_frame.pack_propagate(False)
        
        # Title with icon placeholder
        title_container = tk.Frame(header_frame, bg=self.colors['bg_primary'])
        title_container.pack(expand=True)
        
        # Main title
        title_label = ttk.Label(title_container, 
                               text="🔍 DFIR Log Sorter",
                               style='Title.TLabel')
        title_label.pack(side=tk.TOP)
        
        # Subtitle
        subtitle_label = tk.Label(title_container,
                                 text="Digital Forensics & Incident Response Timeline Analysis",
                                 font=('Segoe UI', 11),
                                 bg=self.colors['bg_primary'],
                                 fg=self.colors['text_secondary'])
        subtitle_label.pack(side=tk.TOP, pady=(5, 0))
        
        # Content area with better spacing
        content_frame = tk.Frame(main_frame, bg=self.colors['bg_primary'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(10, 20))
        
        # Investigation header
        self.create_investigation_header(content_frame)
        
        # Input section
        self.create_input_section(content_frame)
        
        # Control buttons
        self.create_control_section(content_frame)
        
        # Results section
        self.create_results_section(content_frame)
        
        # AI Analysis section
        self.create_ai_analysis_section(content_frame)
        
        # AI Results section (initially hidden)
        self.create_ai_results_section(content_frame)
        
        # Status bar
        self.create_status_bar(main_frame)
    
    def create_input_section(self, parent):
        """Create the log entry input section."""
        input_frame = ttk.LabelFrame(parent, text="📝 Add New Log Entry", 
                                   padding="25", style='Card.TLabelframe')
        input_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Create grid layout with better spacing
        input_frame.grid_columnconfigure(1, weight=1)
        
        # Timestamp input row
        timestamp_row = tk.Frame(input_frame, bg=self.colors['bg_accent'])
        timestamp_row.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(0, 15))
        timestamp_row.grid_columnconfigure(1, weight=1)
        
        ttk.Label(timestamp_row, text="⏰ Timestamp:", 
                 style='Heading.TLabel').grid(row=0, column=0, sticky=tk.W, padx=(0, 15))
        
        self.timestamp_var = tk.StringVar()
        self.timestamp_entry = ttk.Entry(timestamp_row, textvariable=self.timestamp_var, 
                                       width=35, style='Custom.TEntry')
        self.timestamp_entry.grid(row=0, column=1, sticky="ew", padx=(0, 15))
        
        # Current time button with icon
        current_time_btn = ttk.Button(timestamp_row, text="🕐 Now", 
                                     command=self.insert_current_time,
                                     style='Secondary.TButton')
        current_time_btn.grid(row=0, column=2)
        
        # Timestamp format help
        format_label = tk.Label(input_frame, 
                               text="💡 Supported formats: YYYY-MM-DD HH:MM:SS, DD/MM/YYYY HH:MM:SS, ISO formats, etc.",
                               font=('Segoe UI', 8),
                               bg=self.colors['bg_accent'],
                               fg=self.colors['text_secondary'])
        format_label.grid(row=1, column=0, columnspan=3, sticky=tk.W, pady=(0, 20))
        
        # Severity and description row
        details_row = tk.Frame(input_frame, bg=self.colors['bg_accent'])
        details_row.grid(row=2, column=0, columnspan=3, sticky="ew", pady=(0, 20))
        details_row.grid_columnconfigure(1, weight=1)
        
        # Severity input
        severity_frame = tk.Frame(details_row, bg=self.colors['bg_accent'])
        severity_frame.grid(row=0, column=0, sticky="nw", padx=(0, 20))
        
        ttk.Label(severity_frame, text="⚠️ Severity:", 
                 style='Heading.TLabel').pack(anchor=tk.W, pady=(0, 8))
        
        self.severity_var = tk.StringVar(value="Info")
        severity_combo = ttk.Combobox(severity_frame, textvariable=self.severity_var,
                                     values=["🔴 Critical", "🟠 High", "🟡 Medium", "🔵 Low", "ℹ️ Info"],
                                     state="readonly", width=12,
                                     style='Custom.TCombobox')
        severity_combo.pack(anchor=tk.W)
        
        # Description input
        desc_frame = tk.Frame(details_row, bg=self.colors['bg_accent'])
        desc_frame.grid(row=0, column=1, sticky="ew")
        desc_frame.grid_columnconfigure(0, weight=1)
        
        ttk.Label(desc_frame, text="📄 Description:", 
                 style='Heading.TLabel').grid(row=0, column=0, sticky=tk.W, pady=(0, 8))
        
        # Text widget with custom styling
        text_container = tk.Frame(desc_frame, bg=self.colors['border'], bd=2)
        text_container.grid(row=1, column=0, sticky="ew")
        text_container.grid_columnconfigure(0, weight=1)
        
        self.description_text = tk.Text(text_container, height=4, width=50, 
                                       font=('Consolas', 10),
                                       bg=self.colors['bg_secondary'], 
                                       fg=self.colors['text_primary'],
                                       insertbackground=self.colors['text_primary'],
                                       selectbackground=self.colors['accent_blue'],
                                       bd=0, padx=10, pady=8,
                                       wrap=tk.WORD)
        self.description_text.grid(row=0, column=0, sticky="ew")
        
        # Add scrollbar to text
        text_scroll = tk.Scrollbar(text_container, orient=tk.VERTICAL, 
                                  command=self.description_text.yview,
                                  bg=self.colors['bg_secondary'])
        text_scroll.grid(row=0, column=1, sticky="ns")
        self.description_text.configure(yscrollcommand=text_scroll.set)
        
        # Add entry button with prominent styling
        button_frame = tk.Frame(input_frame, bg=self.colors['bg_accent'])
        button_frame.grid(row=3, column=0, columnspan=3, pady=(10, 0))
        
        add_btn = ttk.Button(button_frame, text="➕ Add Log Entry", 
                            command=self.add_log_entry,
                            style='Primary.TButton')
        add_btn.pack()
    
    def create_control_section(self, parent):
        """Create the control buttons section."""
        # Main control container with card styling
        control_container = tk.Frame(parent, bg=self.colors['bg_accent'], 
                                   relief='solid', bd=2)
        control_container.pack(fill=tk.X, pady=(0, 20))
        
        # Control header
        header_frame = tk.Frame(control_container, bg=self.colors['bg_accent'])
        header_frame.pack(fill=tk.X, padx=20, pady=(15, 10))
        
        control_title = tk.Label(header_frame, 
                               text="🎛️ Timeline Controls",
                               font=('Segoe UI', 12, 'bold'),
                               bg=self.colors['bg_accent'],
                               fg=self.colors['accent_blue'])
        control_title.pack(side=tk.LEFT)
        
        # Button grid for better organization
        button_grid = tk.Frame(control_container, bg=self.colors['bg_accent'])
        button_grid.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # Primary actions (left side)
        primary_frame = tk.Frame(button_grid, bg=self.colors['bg_accent'])
        primary_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Sort button (prominent)
        self.sort_btn = ttk.Button(primary_frame, text="🔄 Sort Logs by Timestamp", 
                                  command=self.sort_logs,
                                  style='Primary.TButton')
        self.sort_btn.pack(side=tk.LEFT, padx=(0, 15))
        
        # Clear button (warning style)
        clear_btn = ttk.Button(primary_frame, text="🗑️ Clear All", 
                              command=self.clear_logs,
                              style='Danger.TButton')
        clear_btn.pack(side=tk.LEFT, padx=(0, 15))
        
                # Delete selected button
        self.delete_btn = ttk.Button(primary_frame, text="🗑️ Delete Selected", 
                                     command=self.delete_selected_entry,
                                     style='Danger.TButton')
        self.delete_btn.pack(side=tk.LEFT, padx=(0, 15))
        
        # LLM Analysis button
        llm_btn = ttk.Button(primary_frame, text="🤖 AI Analysis", 
                            command=self.analyze_with_llm,
                            style='Primary.TButton')
        llm_btn.pack(side=tk.LEFT, padx=(0, 15))
        
        # Secondary actions (right side)
        secondary_frame = tk.Frame(button_grid, bg=self.colors['bg_accent'])
        secondary_frame.pack(side=tk.RIGHT)
        
        # Export section
        export_label = tk.Label(secondary_frame,
                               text="Export:",
                               font=('Segoe UI', 9, 'bold'),
                               bg=self.colors['bg_accent'],
                               fg=self.colors['text_secondary'])
        export_label.pack(side=tk.LEFT, padx=(0, 10))
        
        export_btn = ttk.Button(secondary_frame, text="📤 Export", 
                               command=self.show_export_dialog,
                               style='Success.TButton')
        export_btn.pack(side=tk.LEFT, padx=(0, 15))
        
        # Import button
        import_btn = ttk.Button(secondary_frame, text="📥 Import CSV", 
                               command=self.import_csv,
                               style='Secondary.TButton')
        import_btn.pack(side=tk.LEFT)
    
    def create_results_section(self, parent):
        """Create the results display section."""
        results_frame = ttk.LabelFrame(parent, text="📊 Log Entries Timeline", 
                                     padding="20", style='Card.TLabelframe')
        results_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Results header with stats
        header_frame = tk.Frame(results_frame, bg=self.colors['bg_accent'])
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Entry count display
        self.entry_count_var = tk.StringVar(value="No entries")
        count_label = tk.Label(header_frame,
                              textvariable=self.entry_count_var,
                              font=('Segoe UI', 10),
                              bg=self.colors['bg_accent'],
                              fg=self.colors['text_secondary'])
        count_label.pack(side=tk.LEFT)
        
        # Sort status indicator
        self.sort_status_var = tk.StringVar(value="")
        sort_status = tk.Label(header_frame,
                              textvariable=self.sort_status_var,
                              font=('Segoe UI', 10, 'bold'),
                              bg=self.colors['bg_accent'],
                              fg=self.colors['accent_green'])
        sort_status.pack(side=tk.RIGHT)
        
        # Create treeview container with border
        tree_container = tk.Frame(results_frame, bg=self.colors['border'], bd=2)
        tree_container.pack(fill=tk.BOTH, expand=True)
        
        # Treeview with custom styling
        columns = ("timestamp", "severity", "description")
        self.tree = ttk.Treeview(tree_container, columns=columns, show="headings", 
                               height=12, style='Custom.Treeview')
        
        # Configure columns with better widths and styling
        self.tree.heading("timestamp", text="🕐 Timestamp", anchor=tk.W)
        self.tree.heading("severity", text="⚠️ Severity", anchor=tk.CENTER)
        self.tree.heading("description", text="📄 Description", anchor=tk.W)
        
        # Create sort buttons for timestamp column
        self.create_sort_buttons(results_frame)
        
        self.tree.column("timestamp", width=220, anchor=tk.W, minwidth=180)
        self.tree.column("severity", width=120, anchor=tk.CENTER, minwidth=100)
        self.tree.column("description", width=500, anchor=tk.W, minwidth=300)
        
        # Scrollbars with custom styling
        v_scrollbar = tk.Scrollbar(tree_container, orient=tk.VERTICAL, 
                                  command=self.tree.yview,
                                  bg=self.colors['bg_secondary'],
                                  troughcolor=self.colors['bg_accent'],
                                  borderwidth=0)
        h_scrollbar = tk.Scrollbar(tree_container, orient=tk.HORIZONTAL, 
                                  command=self.tree.xview,
                                  bg=self.colors['bg_secondary'],
                                  troughcolor=self.colors['bg_accent'],
                                  borderwidth=0)
        
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid layout for treeview and scrollbars
        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        tree_container.grid_rowconfigure(0, weight=1)
        tree_container.grid_columnconfigure(0, weight=1)
        
        # Add help text for empty state
        self.empty_state_frame = tk.Frame(results_frame, bg=self.colors['bg_accent'])
        self.empty_state_label = tk.Label(self.empty_state_frame,
                                         text="📝 No log entries yet. Add your first entry above to get started!",
                                         font=('Segoe UI', 11),
                                         bg=self.colors['bg_accent'],
                                         fg=self.colors['text_secondary'])
        
        # Bind events
        self.tree.bind("<Double-1>", self.edit_selected_entry)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        
        # Show empty state initially
        self.update_entry_display()
        
        # Start session timer
        self.update_session_timer()
        
        # Control section already has delete button
    
    def create_sort_buttons(self, parent):
        """Create sort buttons for the timestamp column."""
        # Create a frame for sort buttons
        sort_frame = tk.Frame(parent, bg=self.colors['bg_accent'])
        sort_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Sort buttons container
        sort_buttons_frame = tk.Frame(sort_frame, bg=self.colors['bg_accent'])
        sort_buttons_frame.pack(side=tk.RIGHT, padx=10)
        
        # Sort label
        sort_label = tk.Label(sort_buttons_frame, text="Sort by Timestamp:", 
                             font=('Segoe UI', 9),
                             bg=self.colors['bg_accent'],
                             fg=self.colors['text_secondary'])
        sort_label.pack(side=tk.LEFT, padx=(0, 8))
        
        # Ascending sort button (Old to New)
        self.sort_asc_btn = tk.Button(sort_buttons_frame, 
                                     text="↑ Old to New",
                                     font=('Segoe UI', 9),
                                     bg=self.colors['bg_secondary'],
                                     fg=self.colors['text_secondary'],
                                     activebackground=self.colors['accent_blue'],
                                     activeforeground='white',
                                     relief='flat',
                                     bd=0,
                                     padx=12,
                                     pady=4,
                                     cursor='hand2',
                                     command=self.sort_ascending)
        self.sort_asc_btn.pack(side=tk.LEFT, padx=2)
        
        # Descending sort button (New to Old)
        self.sort_desc_btn = tk.Button(sort_buttons_frame, 
                                      text="↓ New to Old",
                                      font=('Segoe UI', 9),
                                      bg=self.colors['bg_secondary'],
                                      fg=self.colors['text_secondary'],
                                      activebackground=self.colors['accent_blue'],
                                      activeforeground='white',
                                      relief='flat',
                                      bd=0,
                                      padx=12,
                                      pady=4,
                                      cursor='hand2',
                                      command=self.sort_descending)
        self.sort_desc_btn.pack(side=tk.LEFT, padx=2)
        
        # Track current sort state
        self.current_sort_direction = None
    
    def create_ai_analysis_section(self, parent):
        """Create the main AI analysis section under the logs table."""
        self.ai_analysis_frame = ttk.LabelFrame(parent, text="🤖 AI Security Analysis", 
                                               padding="20", style='Card.TLabelframe')
        self.ai_analysis_frame.pack(fill=tk.X, pady=(15, 0))
        
        # Analysis status
        status_frame = tk.Frame(self.ai_analysis_frame, bg=self.colors['bg_accent'])
        status_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Status icon and text
        status_icon_frame = tk.Frame(status_frame, bg=self.colors['bg_accent'])
        status_icon_frame.pack(side=tk.LEFT, padx=(0, 15))
        
        self.ai_status_icon = tk.Label(status_icon_frame, text="🤖", 
                                      font=('Segoe UI', 16),
                                      bg=self.colors['bg_accent'],
                                      fg=self.colors['accent_blue'])
        self.ai_status_icon.pack()
        
        # Status text
        status_text_frame = tk.Frame(status_frame, bg=self.colors['bg_accent'])
        status_text_frame.pack(fill=tk.X, expand=True)
        
        self.ai_status_title = tk.Label(status_text_frame, text="Ready for Analysis", 
                                       font=('Segoe UI', 12, 'bold'),
                                       bg=self.colors['bg_accent'],
                                       fg=self.colors['text_primary'])
        self.ai_status_title.pack(anchor=tk.W)
        
        self.ai_status_message = tk.Label(status_text_frame, 
                                         text="Click 'Start AI Analysis' to send your logs to AI for comprehensive security analysis.",
                                         font=('Segoe UI', 9),
                                         bg=self.colors['bg_accent'],
                                         fg=self.colors['text_secondary'],
                                         wraplength=500,
                                         justify=tk.LEFT)
        self.ai_status_message.pack(anchor=tk.W, pady=(2, 0))
        
        # Progress bar (initially hidden)
        self.ai_progress_frame = tk.Frame(self.ai_analysis_frame, bg=self.colors['bg_accent'])
        # Don't pack initially - will be shown during analysis
        
        self.ai_progress_var = tk.DoubleVar(value=0)
        self.ai_progress_bar = ttk.Progressbar(self.ai_progress_frame, 
                                              variable=self.ai_progress_var,
                                              maximum=100,
                                              length=400,
                                              mode='determinate')
        self.ai_progress_bar.pack(pady=(10, 5))
        
        self.ai_progress_text = tk.Label(self.ai_progress_frame, text="", 
                                        font=('Segoe UI', 9),
                                        bg=self.colors['bg_accent'],
                                        fg=self.colors['text_secondary'])
        self.ai_progress_text.pack()
        
        # Analysis info
        info_frame = tk.Frame(self.ai_analysis_frame, bg=self.colors['bg_secondary'], 
                             relief='solid', bd=1)
        info_frame.pack(fill=tk.X, pady=(15, 15))
        
        info_title = tk.Label(info_frame, text="ℹ️ What will be analyzed:",
                             font=('Segoe UI', 10, 'bold'),
                             bg=self.colors['bg_secondary'],
                             fg=self.colors['text_primary'])
        info_title.pack(anchor=tk.W, padx=15, pady=(10, 5))
        
        analysis_points = [
            "• Attack timeline and sequence of events",
            "• Potential indicators of compromise (IOCs)",
            "• Compromised systems and user accounts", 
            "• Containment and remediation recommendations",
            "• Immediate actions for SOC/IR teams",
            "• Executive summary for management"
        ]
        
        for point in analysis_points:
            point_label = tk.Label(info_frame, text=point,
                                  font=('Segoe UI', 9),
                                  bg=self.colors['bg_secondary'],
                                  fg=self.colors['text_secondary'])
            point_label.pack(anchor=tk.W, padx=25, pady=1)
        
        # Bottom padding
        tk.Label(info_frame, text="", bg=self.colors['bg_secondary']).pack(pady=5)
        
        # Start Analysis button
        self.start_main_ai_btn = tk.Button(self.ai_analysis_frame,
                                          text="🚀 Start AI Analysis",
                                          font=('Segoe UI', 11, 'bold'),
                                          bg=self.colors['accent_blue'],
                                          fg='white',
                                          relief='flat',
                                          bd=0,
                                          padx=30,
                                          pady=12,
                                          cursor='hand2',
                                          command=self.start_main_ai_analysis)
        self.start_main_ai_btn.pack(pady=(0, 10))
    
    def create_ai_results_section(self, parent):
        """Create the AI results section (initially hidden)."""
        self.ai_results_frame = ttk.LabelFrame(parent, text="🤖 AI Security Analysis Results", 
                                              padding="20", style='Card.TLabelframe')
        # Don't pack initially - will be shown when results are available
        
        # Results header
        results_header = tk.Frame(self.ai_results_frame, bg=self.colors['bg_accent'])
        results_header.pack(fill=tk.X, pady=(0, 15))
        
        # Title and actions
        self.ai_results_title = tk.Label(results_header, text="Analysis Complete",
                                         font=('Segoe UI', 12, 'bold'),
                                         bg=self.colors['bg_accent'],
                                         fg=self.colors['text_primary'])
        self.ai_results_title.pack(side=tk.LEFT)
        
        # Action buttons
        actions_frame = tk.Frame(results_header, bg=self.colors['bg_accent'])
        actions_frame.pack(side=tk.RIGHT)
        
        self.export_ai_results_btn = tk.Button(actions_frame,
                                              text="💾 Export Analysis",
                                              font=('Segoe UI', 9),
                                              bg=self.colors['accent_green'],
                                              fg='white',
                                              relief='flat',
                                              bd=0,
                                              padx=12,
                                              pady=6,
                                              cursor='hand2',
                                              command=self.export_main_ai_results)
        self.export_ai_results_btn.pack(side=tk.LEFT, padx=(0, 8))
        
        self.clear_ai_results_btn = tk.Button(actions_frame,
                                             text="🗑️ Clear Results",
                                             font=('Segoe UI', 9),
                                             bg=self.colors['bg_secondary'],
                                             fg=self.colors['text_primary'],
                                             relief='flat',
                                             bd=0,
                                             padx=12,
                                             pady=6,
                                             cursor='hand2',
                                             command=self.clear_main_ai_results)
        self.clear_ai_results_btn.pack(side=tk.LEFT)
        
        # Results content
        self.ai_results_text = tk.Text(self.ai_results_frame,
                                      height=12,
                                      font=('Consolas', 9),
                                      bg=self.colors['bg_secondary'],
                                      fg=self.colors['text_primary'],
                                      wrap=tk.WORD,
                                      state=tk.DISABLED,
                                      relief='solid',
                                      bd=1)
        self.ai_results_text.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar for results
        results_scrollbar = ttk.Scrollbar(self.ai_results_frame, orient=tk.VERTICAL, 
                                         command=self.ai_results_text.yview)
        self.ai_results_text.configure(yscrollcommand=results_scrollbar.set)
        results_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_status_bar(self, parent):
        """Create the status bar."""
        status_container = tk.Frame(parent, bg=self.colors['bg_secondary'], 
                                  relief='solid', bd=1)
        status_container.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # Status content
        status_content = tk.Frame(status_container, bg=self.colors['bg_secondary'])
        status_content.pack(fill=tk.X, padx=15, pady=8)
        
        # Status icon and text
        status_icon = tk.Label(status_content, text="ℹ️", 
                              bg=self.colors['bg_secondary'],
                              fg=self.colors['accent_blue'],
                              font=('Segoe UI', 10))
        status_icon.pack(side=tk.LEFT, padx=(0, 8))
        
        self.status_var = tk.StringVar(value="Ready - Enter log entries and click Sort to organize timeline")
        status_label = tk.Label(status_content, textvariable=self.status_var,
                               bg=self.colors['bg_secondary'],
                               fg=self.colors['text_primary'],
                               font=('Segoe UI', 9),
                               anchor=tk.W)
        status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Version info
        version_label = tk.Label(status_content, text="v1.0",
                               bg=self.colors['bg_secondary'],
                               fg=self.colors['text_secondary'],
                               font=('Segoe UI', 8))
        version_label.pack(side=tk.RIGHT)
    
    def update_entry_display(self):
        """Update the entry count and empty state display."""
        count = len(self.log_entries)
        if count == 0:
            self.entry_count_var.set("No entries")
            # Show empty state
            if hasattr(self, 'empty_state_frame'):
                self.empty_state_frame.pack(fill=tk.X, pady=20)
                self.empty_state_label.pack()
        else:
            self.entry_count_var.set(f"{count} {'entry' if count == 1 else 'entries'}")
            # Hide empty state
            if hasattr(self, 'empty_state_frame'):
                self.empty_state_frame.pack_forget()
        
        # Update sort status
        if self.is_sorted and count > 1:
            self.sort_status_var.set("✅ Sorted")
        elif count > 1:
            self.sort_status_var.set("⚠️ Unsorted")
        else:
            self.sort_status_var.set("")
    
    def on_tree_select(self, event):
        """Handle treeview selection events."""
        selection = self.tree.selection()
        if selection:
            # Could add preview functionality here
            pass
    
    def insert_current_time(self):
        """Insert current timestamp into the timestamp field."""
        # Use the custom format that matches web app
        current_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        self.timestamp_var.set(current_time)
    
    def add_log_entry(self):
        """Add a new log entry to the list."""
        timestamp = self.timestamp_var.get().strip()
        description = self.description_text.get("1.0", tk.END).strip()
        severity_text = self.severity_var.get()
        # Extract actual severity from emoji text
        severity_map = {
            "🔴 Critical": "Critical",
            "🟠 High": "High", 
            "🟡 Medium": "Medium",
            "🔵 Low": "Low",
            "ℹ️ Info": "Info"
        }
        severity = severity_map.get(severity_text, "Info")
        
        if not timestamp:
            messagebox.showerror("Error", "Please enter a timestamp")
            return
        
        if not description:
            messagebox.showerror("Error", "Please enter a description")
            return
        
        try:
            # Create log entry
            log_entry = LogEntry(timestamp, description, severity)
            self.log_entries.append(log_entry)
            
            # Add to treeview with emoji
            self.tree.insert("", tk.END, values=(timestamp, severity_text, description))
            
            # Clear input fields
            self.timestamp_var.set("")
            self.description_text.delete("1.0", tk.END)
            self.severity_var.set("ℹ️ Info")
            
            # Update displays
            self.update_entry_display()
            self.status_var.set(f"✅ Added log entry and auto-saved to investigation folder")
            self.is_sorted = False
            self.current_sort_direction = None
            
            # Auto-save to CSV file
            self.auto_save_logs_to_csv()
            
            # Reset sort button states
            self.update_sort_button_states(None)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add log entry: {str(e)}")
    
    def sort_logs(self):
        """Sort all log entries by timestamp."""
        if not self.log_entries:
            messagebox.showwarning("Warning", "No log entries to sort")
            return
        
        try:
            # Sort entries
            self.log_entries.sort()
            
            # Clear and repopulate treeview with emoji severity
            self.tree.delete(*self.tree.get_children())
            severity_emoji_map = {
                "Critical": "🔴 Critical",
                "High": "🟠 High",
                "Medium": "🟡 Medium", 
                "Low": "🔵 Low",
                "Info": "ℹ️ Info"
            }
            
            for entry in self.log_entries:
                severity_display = severity_emoji_map.get(entry.severity, entry.severity)
                self.tree.insert("", tk.END, values=(entry.timestamp, severity_display, entry.description))
            
            self.is_sorted = True
            self.update_entry_display()
            self.status_var.set(f"🔄 Sorted {len(self.log_entries)} log entries by timestamp")
            
            # Auto-save sorted entries to CSV
            self.auto_save_logs_to_csv()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to sort logs: {str(e)}")
    
    def sort_ascending(self):
        """Sort log entries in ascending order (Old to New)."""
        if not self.log_entries:
            messagebox.showwarning("Warning", "No log entries to sort")
            return
        
        try:
            # Sort entries in ascending order
            self.log_entries.sort()
            
            # Update button states
            self.update_sort_button_states('asc')
            
            # Clear and repopulate treeview
            self.refresh_treeview()
            
            self.is_sorted = True
            self.current_sort_direction = 'asc'
            self.update_entry_display()
            self.status_var.set(f"🔄 Sorted {len(self.log_entries)} entries (Old to New)")
            
            # Auto-save sorted entries to CSV
            self.auto_save_logs_to_csv()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to sort logs: {str(e)}")
    
    def sort_descending(self):
        """Sort log entries in descending order (New to Old)."""
        if not self.log_entries:
            messagebox.showwarning("Warning", "No log entries to sort")
            return
        
        try:
            # Sort entries in descending order
            self.log_entries.sort(reverse=True)
            
            # Update button states
            self.update_sort_button_states('desc')
            
            # Clear and repopulate treeview
            self.refresh_treeview()
            
            self.is_sorted = True
            self.current_sort_direction = 'desc'
            self.update_entry_display()
            self.status_var.set(f"🔄 Sorted {len(self.log_entries)} entries (New to Old)")
            
            # Auto-save sorted entries to CSV
            self.auto_save_logs_to_csv()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to sort logs: {str(e)}")
    
    def update_sort_button_states(self, active_direction):
        """Update the visual state of sort buttons."""
        # Reset both buttons to default state
        self.sort_asc_btn.config(
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_secondary']
        )
        self.sort_desc_btn.config(
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_secondary']
        )
        
        # Highlight the active button
        if active_direction == 'asc':
            self.sort_asc_btn.config(
                bg=self.colors['accent_blue'],
                fg='white'
            )
        elif active_direction == 'desc':
            self.sort_desc_btn.config(
                bg=self.colors['accent_blue'],
                fg='white'
            )
        # If active_direction is None, both buttons remain in default state
    
    def refresh_treeview(self):
        """Refresh the treeview with current log entries."""
        self.tree.delete(*self.tree.get_children())
        severity_emoji_map = {
            "Critical": "🔴 Critical",
            "High": "🟠 High",
            "Medium": "🟡 Medium", 
            "Low": "🔵 Low",
            "Info": "ℹ️ Info"
        }
        
        for entry in self.log_entries:
            severity_display = severity_emoji_map.get(entry.severity, entry.severity)
            self.tree.insert("", tk.END, values=(entry.timestamp, severity_display, entry.description))
    
    def clear_logs(self):
        """Clear all log entries."""
        if self.log_entries and messagebox.askyesno("Confirm Clear", "Are you sure you want to clear all log entries?\n\nThis action cannot be undone."):
            self.log_entries.clear()
            self.tree.delete(*self.tree.get_children())
            self.update_entry_display()
            self.status_var.set("🗑️ All log entries cleared")
            self.is_sorted = False
            self.current_sort_direction = None
            
            # Auto-save (will delete CSV file since no entries)
            self.auto_save_logs_to_csv()
            
            # Reset sort button states
            self.update_sort_button_states(None)
    
    def export_csv(self):
        """Export log entries to CSV file."""
        if not self.log_entries:
            messagebox.showwarning("Warning", "No log entries to export")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Export logs to CSV"
        )
        
        if filename:
            try:
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(["Timestamp", "Severity", "Description", "Parsed Time"])
                    
                    entries_to_export = self.log_entries if self.is_sorted else sorted(self.log_entries)
                    for entry in entries_to_export:
                        writer.writerow([entry.timestamp, entry.severity, entry.description, 
                                       entry.parsed_time.strftime("%Y-%m-%d %H:%M:%S")])
                
                self.status_var.set(f"📊 Exported {len(self.log_entries)} entries to CSV")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export CSV: {str(e)}")
    
    def export_json(self):
        """Export log entries to JSON file."""
        if not self.log_entries:
            messagebox.showwarning("Warning", "No log entries to export")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Export logs to JSON"
        )
        
        if filename:
            try:
                entries_to_export = self.log_entries if self.is_sorted else sorted(self.log_entries)
                data = {
                    "export_time": datetime.now().isoformat(),
                    "total_entries": len(entries_to_export),
                    "is_sorted": self.is_sorted,
                    "entries": [entry.to_dict() for entry in entries_to_export]
                }
                
                with open(filename, 'w', encoding='utf-8') as jsonfile:
                    json.dump(data, jsonfile, indent=2, ensure_ascii=False)
                
                self.status_var.set(f"📄 Exported {len(self.log_entries)} entries to JSON")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export JSON: {str(e)}")
    
    def export_txt(self):
        """Export log entries to TXT file."""
        if not self.log_entries:
            messagebox.showwarning("Warning", "No log entries to export")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Export logs to TXT"
        )
        
        if filename:
            try:
                entries_to_export = self.log_entries if self.is_sorted else sorted(self.log_entries)
                
                with open(filename, 'w', encoding='utf-8') as txtfile:
                    txtfile.write(f"DFIR Log Sorter - Timeline Export\n")
                    txtfile.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    txtfile.write(f"Total Entries: {len(entries_to_export)}\n")
                    txtfile.write(f"Sorted: {'Yes' if self.is_sorted else 'No'}\n")
                    txtfile.write("=" * 80 + "\n\n")
                    
                    for i, entry in enumerate(entries_to_export, 1):
                        txtfile.write(f"{i:3d}. [{entry.timestamp}] [{entry.severity}] {entry.description}\n")
                
                self.status_var.set(f"📄 Exported {len(self.log_entries)} entries to TXT")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export TXT: {str(e)}")
    
    def import_csv(self):
        """Import log entries from CSV file."""
        filename = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Import logs from CSV"
        )
        
        if filename:
            try:
                imported_count = 0
                with open(filename, 'r', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        timestamp = row.get('Timestamp', '').strip()
                        description = row.get('Description', '').strip()
                        severity = row.get('Severity', 'Info').strip()
                        
                        if timestamp and description:
                            log_entry = LogEntry(timestamp, description, severity)
                            self.log_entries.append(log_entry)
                            # Add with emoji severity
                            severity_emoji_map = {
                                "Critical": "🔴 Critical",
                                "High": "🟠 High",
                                "Medium": "🟡 Medium", 
                                "Low": "🔵 Low",
                                "Info": "ℹ️ Info"
                            }
                            severity_display = severity_emoji_map.get(severity, severity)
                            self.tree.insert("", tk.END, values=(timestamp, severity_display, description))
                            imported_count += 1
                
                self.update_entry_display()
                self.status_var.set(f"📥 Imported {imported_count} entries and auto-saved to investigation folder")
                self.is_sorted = False
                
                # Auto-save to CSV file
                self.auto_save_logs_to_csv()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import CSV: {str(e)}")
    
    def edit_selected_entry(self, event):
        """Edit the selected log entry."""
        selection = self.tree.selection()
        if not selection:
            return
        
        item = self.tree.item(selection[0])
        values = item['values']
        
        if values:
            # Find the corresponding log entry
            for i, entry in enumerate(self.log_entries):
                if (entry.timestamp == values[0] and 
                    entry.severity == values[1] and 
                    entry.description == values[2]):
                    
                    # Open edit dialog
                    self.open_edit_dialog(i, entry)
                    break
    
    def open_edit_dialog(self, index: int, entry: LogEntry):
        """Open dialog to edit a log entry."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Log Entry")
        dialog.geometry("500x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Create edit form
        ttk.Label(dialog, text="Timestamp:").pack(pady=5)
        timestamp_var = tk.StringVar(value=entry.timestamp)
        ttk.Entry(dialog, textvariable=timestamp_var, width=40).pack(pady=5)
        
        ttk.Label(dialog, text="Severity:").pack(pady=5)
        severity_var = tk.StringVar(value=entry.severity)
        ttk.Combobox(dialog, textvariable=severity_var,
                    values=["Critical", "High", "Medium", "Low", "Info"],
                    state="readonly").pack(pady=5)
        
        ttk.Label(dialog, text="Description:").pack(pady=5)
        desc_text = tk.Text(dialog, height=6, width=50)
        desc_text.pack(pady=5, padx=20, fill=tk.BOTH, expand=True)
        desc_text.insert("1.0", entry.description)
        
        def save_changes():
            try:
                new_timestamp = timestamp_var.get().strip()
                new_severity = severity_var.get()
                new_description = desc_text.get("1.0", tk.END).strip()
                
                if new_timestamp and new_description:
                    # Update log entry
                    updated_entry = LogEntry(new_timestamp, new_description, new_severity)
                    self.log_entries[index] = updated_entry
                    
                    # Update treeview
                    item_id = self.tree.get_children()[index]
                    self.tree.item(item_id, values=(new_timestamp, new_severity, new_description))
                    
                    self.is_sorted = False
                    
                    # Auto-save to CSV file
                    self.auto_save_logs_to_csv()
                    
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", "Please fill all fields")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update entry: {str(e)}")
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="Save", command=save_changes).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def setup_investigation(self):
        """Show investigation setup dialog on startup."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Investigation Setup")
        dialog.geometry("500x300")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.configure(bg=self.colors['bg_primary'])
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Main container
        main_frame = tk.Frame(dialog, bg=self.colors['bg_primary'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(main_frame, 
                              text="🔍 Investigation Setup",
                              font=('Segoe UI', 16, 'bold'),
                              bg=self.colors['bg_primary'],
                              fg=self.colors['text_primary'])
        title_label.pack(pady=(0, 20))
        
        # Subtitle
        subtitle_label = tk.Label(main_frame,
                                 text="Enter your investigation details to get started",
                                 font=('Segoe UI', 10),
                                 bg=self.colors['bg_primary'],
                                 fg=self.colors['text_secondary'])
        subtitle_label.pack(pady=(0, 30))
        
        # Investigation name input
        name_frame = tk.Frame(main_frame, bg=self.colors['bg_primary'])
        name_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(name_frame, text="Investigation Name:",
                font=('Segoe UI', 10, 'bold'),
                bg=self.colors['bg_primary'],
                fg=self.colors['text_primary']).pack(anchor=tk.W)
        
        self.investigation_var = tk.StringVar(value="New Investigation")
        name_entry = tk.Entry(name_frame, 
                             textvariable=self.investigation_var,
                             font=('Segoe UI', 11),
                             bg=self.colors['bg_secondary'],
                             fg=self.colors['text_primary'],
                             insertbackground=self.colors['text_primary'],
                             relief='flat',
                             bd=2)
        name_entry.pack(fill=tk.X, pady=(5, 0))
        
        # Help text
        help_label = tk.Label(main_frame,
                             text="💡 This name will be used for file naming and session tracking",
                             font=('Segoe UI', 8),
                             bg=self.colors['bg_primary'],
                             fg=self.colors['text_secondary'])
        help_label.pack(pady=(10, 30))
        
        # Buttons
        button_frame = tk.Frame(main_frame, bg=self.colors['bg_primary'])
        button_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        def start_investigation():
            name = self.investigation_var.get().strip()
            if name:
                self.investigation_name = name
                self.session_start_time = datetime.now()
                dialog.destroy()
                self.update_investigation_display()
            else:
                messagebox.showerror("Error", "Please enter an investigation name")
        
        start_btn = tk.Button(button_frame,
                             text="🚀 Start Investigation",
                             font=('Segoe UI', 11, 'bold'),
                             bg=self.colors['accent_blue'],
                             fg='white',
                             relief='flat',
                             bd=0,
                             padx=20,
                             pady=10,
                             cursor='hand2',
                             command=start_investigation)
        start_btn.pack(side=tk.RIGHT)
        
        # Focus on entry
        name_entry.focus_set()
        name_entry.select_range(0, tk.END)
    
    def update_investigation_display(self):
        """Update the investigation display in the header."""
        if hasattr(self, 'investigation_label'):
            session_duration = datetime.now() - self.session_start_time
            hours = session_duration.seconds // 3600
            minutes = (session_duration.seconds % 3600) // 60
            duration_text = f"{hours}h {minutes}m"
            
            # Get investigation folder path
            try:
                folder_path = self.get_investigation_folder()
                folder_name = folder_path.name
            except:
                folder_name = "Unknown"
            
            self.investigation_label.config(
                text=f"📁 {self.investigation_name} | 💾 logs/{folder_name}/ | ⏱️ Session: {duration_text}"
            )
    
    def create_investigation_header(self, parent):
        """Create investigation header display."""
        header_frame = tk.Frame(parent, bg=self.colors['bg_accent'], relief='solid', bd=1)
        header_frame.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        # Investigation info
        info_frame = tk.Frame(header_frame, bg=self.colors['bg_accent'])
        info_frame.pack(fill=tk.X, padx=15, pady=10)
        
        self.investigation_label = tk.Label(info_frame,
                                           text=f"📁 {self.investigation_name} | ⏱️ Session: 0h 0m",
                                           font=('Segoe UI', 10, 'bold'),
                                           bg=self.colors['bg_accent'],
                                           fg=self.colors['text_primary'])
        self.investigation_label.pack(side=tk.LEFT)
        
        # Action buttons
        actions_frame = tk.Frame(info_frame, bg=self.colors['bg_accent'])
        actions_frame.pack(side=tk.RIGHT)
        
        # Export button
        export_btn = tk.Button(actions_frame,
                              text="💾 Export Log File",
                              font=('Segoe UI', 9),
                              bg=self.colors['accent_green'],
                              fg='white',
                              relief='flat',
                              bd=0,
                              padx=12,
                              pady=4,
                              cursor='hand2',
                              command=self.show_export_dialog)
        export_btn.pack(side=tk.LEFT, padx=(0, 8))
        
        # New investigation button
        new_investigation_btn = tk.Button(actions_frame,
                                         text="🔄 New Investigation",
                                         font=('Segoe UI', 9),
                                         bg=self.colors['accent_blue'],
                                         fg='white',
                                         relief='flat',
                                         bd=0,
                                         padx=12,
                                         pady=4,
                                         cursor='hand2',
                                         command=self.new_investigation)
        new_investigation_btn.pack(side=tk.LEFT)
    
    def export_to_file(self):
        """Export logs to a structured text file."""
        if not self.log_entries:
            messagebox.showwarning("Warning", "No log entries to export")
            return
        
        # Create logs directory if it doesn't exist
        import os
        logs_dir = "logs"
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{logs_dir}/{self.investigation_name}_{timestamp}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                # Header
                f.write("=" * 80 + "\n")
                f.write(f"DFIR LOG SORTER - INVESTIGATION REPORT\n")
                f.write("=" * 80 + "\n")
                f.write(f"Investigation: {self.investigation_name}\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total Entries: {len(self.log_entries)}\n")
                f.write(f"Sort Status: {'Sorted' if self.is_sorted else 'Unsorted'}\n")
                f.write("=" * 80 + "\n\n")
                
                # Sort entries if not already sorted
                entries_to_export = self.log_entries if self.is_sorted else sorted(self.log_entries)
                
                # Export entries
                for i, entry in enumerate(entries_to_export, 1):
                    f.write(f"Entry #{i}\n")
                    f.write(f"Timestamp: {entry.timestamp}\n")
                    f.write(f"Severity: {entry.severity}\n")
                    f.write(f"Description: {entry.description}\n")
                    f.write(f"Parsed Time: {entry.parsed_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write("-" * 60 + "\n\n")
                
                # Footer
                f.write("=" * 80 + "\n")
                f.write("End of Report\n")
                f.write("=" * 80 + "\n")
            
            self.status_var.set(f"💾 Exported {len(self.log_entries)} entries to {filename}")
            messagebox.showinfo("Export Successful", f"Log file saved to:\n{filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export file: {str(e)}")
    
    def show_export_dialog(self):
        """Show a dialog with multiple export options."""
        if not self.log_entries:
            messagebox.showwarning("Warning", "No log entries to export")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Export Options")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.configure(bg=self.colors['bg_primary'])
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Main container
        main_frame = tk.Frame(dialog, bg=self.colors['bg_primary'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(main_frame, 
                              text="📤 Export Options",
                              font=('Segoe UI', 14, 'bold'),
                              bg=self.colors['bg_primary'],
                              fg=self.colors['text_primary'])
        title_label.pack(pady=(0, 10))
        
        # Info label
        info_label = tk.Label(main_frame, 
                             text="📁 Logs automatically saved to investigation_logs.csv",
                             font=('Segoe UI', 9),
                             bg=self.colors['bg_primary'],
                             fg=self.colors['text_secondary'])
        info_label.pack(pady=(0, 15))
        
        # Export buttons
        buttons_frame = tk.Frame(main_frame, bg=self.colors['bg_primary'])
        buttons_frame.pack(fill=tk.BOTH, expand=True)
        
        # TXT Export
        txt_btn = tk.Button(buttons_frame,
                           text="📄 Export as TXT (Structured Report)",
                           font=('Segoe UI', 10),
                           bg=self.colors['accent_blue'],
                           fg='white',
                           relief='flat',
                           bd=0,
                           padx=20,
                           pady=10,
                           cursor='hand2',
                           command=lambda: [self.export_to_file(), dialog.destroy()])
        txt_btn.pack(fill=tk.X, pady=5)
        
        # CSV Export
        csv_btn = tk.Button(buttons_frame,
                           text="📊 Export as CSV (Spreadsheet)",
                           font=('Segoe UI', 10),
                           bg=self.colors['accent_green'],
                           fg='white',
                           relief='flat',
                           bd=0,
                           padx=20,
                           pady=10,
                           cursor='hand2',
                           command=lambda: [self.export_csv(), dialog.destroy()])
        csv_btn.pack(fill=tk.X, pady=5)
        
        # Cancel button
        cancel_btn = tk.Button(buttons_frame,
                              text="❌ Cancel",
                              font=('Segoe UI', 10),
                              bg=self.colors['bg_secondary'],
                              fg=self.colors['text_primary'],
                              relief='flat',
                              bd=0,
                              padx=20,
                              pady=10,
                              cursor='hand2',
                              command=dialog.destroy)
        cancel_btn.pack(fill=tk.X, pady=5)
    
    def new_investigation(self):
        """Start a new investigation."""
        if messagebox.askyesno("New Investigation", 
                              "Are you sure you want to start a new investigation?\n\n"
                              "This will clear all current log entries."):
            self.log_entries.clear()
            self.tree.delete(*self.tree.get_children())
            self.is_sorted = False
            self.current_sort_direction = None
            self.update_sort_button_states(None)
            self.update_entry_display()
            self.setup_investigation()
    
    def delete_selected_entry(self):
        """Delete the selected log entry."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an entry to delete")
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this entry?"):
            item = self.tree.item(selection[0])
            values = item['values']
            
            # Find and remove the corresponding log entry
            for i, entry in enumerate(self.log_entries):
                if (entry.timestamp == values[0] and 
                    entry.description == values[2]):
                    del self.log_entries[i]
                    break
            
            # Remove from treeview
            self.tree.delete(selection[0])
            self.update_entry_display()
            self.status_var.set("🗑️ Entry deleted successfully")
            
            # Auto-save to CSV file
            self.auto_save_logs_to_csv()
    
    def analyze_with_llm(self):
        """Analyze log entries using LLM (Ollama)."""
        if not self.log_entries:
            messagebox.showwarning("Warning", "No log entries to analyze")
            return
        
        # Show confirmation dialog
        if not messagebox.askyesno("AI Analysis", 
                                  f"Send {len(self.log_entries)} log entries to AI for analysis?\n\n"
                                  "This will use Ollama to analyze the logs for potential security incidents."):
            return
        
        # Create a separate window for the analysis
        self.show_llm_analysis()
    
    def show_llm_analysis(self):
        """Show LLM analysis in a separate window."""
        analysis_window = tk.Toplevel(self.root)
        analysis_window.title("AI Analysis - DFIR Log Investigation")
        analysis_window.geometry("900x700")
        analysis_window.transient(self.root)
        analysis_window.configure(bg=self.colors['bg_primary'])
        
        # Center window
        analysis_window.update_idletasks()
        x = (analysis_window.winfo_screenwidth() // 2) - (analysis_window.winfo_width() // 2)
        y = (analysis_window.winfo_screenheight() // 2) - (analysis_window.winfo_height() // 2)
        analysis_window.geometry(f"+{x}+{y}")
        
        # Main frame
        main_frame = tk.Frame(analysis_window, bg=self.colors['bg_primary'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(main_frame,
                              text="🤖 AI Security Analysis",
                              font=('Segoe UI', 16, 'bold'),
                              bg=self.colors['bg_primary'],
                              fg=self.colors['text_primary'])
        title_label.pack(pady=(0, 20))
        
        # Status label
        status_label = tk.Label(main_frame,
                               text="🔄 Analyzing logs with AI... Please wait.",
                               font=('Segoe UI', 11),
                               bg=self.colors['bg_primary'],
                               fg=self.colors['accent_blue'])
        status_label.pack(pady=(0, 20))
        
        # Text area for results
        text_frame = tk.Frame(main_frame, bg=self.colors['border'], bd=2)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        result_text = tk.Text(text_frame,
                             font=('Consolas', 10),
                             bg=self.colors['bg_secondary'],
                             fg=self.colors['text_primary'],
                             insertbackground=self.colors['text_primary'],
                             selectbackground=self.colors['accent_blue'],
                             bd=0, padx=15, pady=15,
                             wrap=tk.WORD)
        
        # Add scrollbar
        scrollbar = tk.Scrollbar(text_frame, orient=tk.VERTICAL, command=result_text.yview)
        result_text.configure(yscrollcommand=scrollbar.set)
        
        result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Buttons frame
        button_frame = tk.Frame(main_frame, bg=self.colors['bg_primary'])
        button_frame.pack(fill=tk.X)
        
        # Close button
        close_btn = tk.Button(button_frame,
                             text="❌ Close",
                             font=('Segoe UI', 10),
                             bg=self.colors['bg_secondary'],
                             fg=self.colors['text_primary'],
                             relief='flat',
                             bd=0,
                             padx=20,
                             pady=8,
                             cursor='hand2',
                             command=analysis_window.destroy)
        close_btn.pack(side=tk.RIGHT)
        
        # Export analysis button
        export_btn = tk.Button(button_frame,
                              text="💾 Export Analysis",
                              font=('Segoe UI', 10),
                              bg=self.colors['accent_green'],
                              fg='white',
                              relief='flat',
                              bd=0,
                              padx=20,
                              pady=8,
                              cursor='hand2',
                              command=lambda: self.export_analysis(result_text.get("1.0", tk.END)))
        export_btn.pack(side=tk.RIGHT, padx=(0, 10))
        
        # Start analysis in a separate thread to avoid blocking UI
        def run_analysis():
            try:
                result = self.perform_llm_analysis()
                # Update UI in main thread
                analysis_window.after(0, lambda: self.update_analysis_result(status_label, result_text, result))
            except Exception as e:
                error_msg = f"Error during analysis: {str(e)}"
                analysis_window.after(0, lambda: self.update_analysis_error(status_label, result_text, error_msg))
        
        # Start analysis thread
        analysis_thread = threading.Thread(target=run_analysis, daemon=True)
        analysis_thread.start()
    
    def perform_llm_analysis(self):
        """Perform the actual LLM analysis."""
        try:
            import ollama
        except ImportError:
            raise Exception("Ollama is not installed. Please install it with: pip install ollama")
        
        # Sort entries for chronological analysis
        sorted_entries = sorted(self.log_entries)
        
        # Format logs for the prompt
        log_text = "\n".join([
            f"[{entry.timestamp}] [{entry.severity}] {entry.description}"
            for entry in sorted_entries
        ])
        
        # Create the full prompt
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
        
        # Make the API call
        response = ollama.chat(model="qwen2.5:7b", messages=[{"role": "user", "content": user_input}])
        
        return response['message']['content']
    
    def update_analysis_result(self, status_label, result_text, result):
        """Update the analysis window with results."""
        status_label.config(text="✅ Analysis completed!", fg=self.colors['accent_green'])
        result_text.delete("1.0", tk.END)
        result_text.insert("1.0", result)
        
        # Auto-save to investigation folder
        try:
            filepath = self.save_ai_analysis_to_file(result)
            if filepath:
                self.status_var.set("🤖 AI analysis completed and auto-saved to investigation folder")
            else:
                self.status_var.set("🤖 AI analysis completed successfully")
        except Exception as e:
            print(f"Auto-save failed in modal: {e}")
            self.status_var.set("🤖 AI analysis completed successfully")
    
    def update_analysis_error(self, status_label, result_text, error_msg):
        """Update the analysis window with error."""
        status_label.config(text="❌ Analysis failed", fg=self.colors['accent_red'])
        result_text.delete("1.0", tk.END)
        result_text.insert("1.0", f"Error: {error_msg}\n\nPlease ensure Ollama is installed and running.")
        self.status_var.set("❌ AI analysis failed")
    
    def export_analysis(self, analysis_text):
        """Export the analysis to a text file."""
        if not analysis_text.strip():
            messagebox.showwarning("Warning", "No analysis to export")
            return
        
        # Auto-save to investigation folder
        try:
            filepath = self.save_ai_analysis_to_file(analysis_text)
            if filepath:
                messagebox.showinfo("Export Successful", 
                                  f"Analysis auto-saved to investigation folder:\n{filepath.name}")
                self.status_var.set(f"🤖 AI analysis auto-saved to investigation folder")
                return
        except Exception as e:
            print(f"Auto-save failed: {e}")
        
        # Fallback to manual save dialog
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Export AI Analysis"
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write("=" * 80 + "\n")
                    f.write("DFIR LOG SORTER - AI SECURITY ANALYSIS\n")
                    f.write("=" * 80 + "\n")
                    f.write(f"Investigation: {self.investigation_name}\n")
                    f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"Total Entries Analyzed: {len(self.log_entries)}\n")
                    f.write("=" * 80 + "\n\n")
                    f.write(analysis_text)
                    f.write("\n\n" + "=" * 80 + "\n")
                    f.write("End of Analysis\n")
                    f.write("=" * 80 + "\n")
                
                messagebox.showinfo("Export Successful", f"Analysis saved to:\n{filename}")
                self.status_var.set(f"💾 AI analysis exported to {filename}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export analysis: {str(e)}")

    
    def update_session_timer(self):
        """Update the session timer every minute."""
        self.update_investigation_display()
        # Schedule next update in 60 seconds (60000 milliseconds)
        self.root.after(60000, self.update_session_timer)
    
    def get_investigation_folder(self):
        """Get or create investigation folder."""
        safe_name = re.sub(r'[<>:"/\\|?*]', '_', self.investigation_name)
        investigation_dir = self.logs_dir / safe_name
        investigation_dir.mkdir(exist_ok=True)
        return investigation_dir
    
    def get_investigation_csv_path(self):
        """Get the path to the single CSV file for this investigation."""
        investigation_dir = self.get_investigation_folder()
        return investigation_dir / "investigation_logs.csv"
    
    def auto_save_logs_to_csv(self):
        """Automatically save logs to the investigation CSV file."""
        if not self.log_entries:
            # If no entries, delete the CSV file if it exists
            csv_path = self.get_investigation_csv_path()
            if csv_path.exists():
                try:
                    csv_path.unlink()
                except Exception as e:
                    print(f"Warning: Failed to delete empty CSV file: {e}")
            return
        
        try:
            csv_path = self.get_investigation_csv_path()
            
            # Sort entries by timestamp
            sorted_entries = sorted(self.log_entries, key=lambda x: x.parsed_time)
            
            # Write CSV file (overwrite with all current entries)
            with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Timestamp', 'Severity', 'Description'])
                
                for entry in sorted_entries:
                    writer.writerow([entry.timestamp, entry.severity, entry.description])
            
            print(f"Auto-saved {len(sorted_entries)} entries to {csv_path}")
            
        except Exception as e:
            print(f"Warning: Failed to auto-save logs: {e}")
    
    def save_ai_analysis_to_file(self, analysis_text):
        """Save AI analysis to a text file in the investigation folder."""
        if not analysis_text:
            return None
        
        try:
            investigation_dir = self.get_investigation_folder()
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"ai_analysis_{timestamp}.txt"
            filepath = investigation_dir / filename
            
            # Generate file content
            content = []
            content.append("=" * 80)
            content.append(f"AI Security Analysis: {self.investigation_name}")
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
            
            print(f"AI analysis saved to: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"Warning: Failed to save AI analysis: {e}")
            return None
    
    def start_main_ai_analysis(self):
        """Start AI analysis from the main section."""
        if not self.log_entries:
            messagebox.showwarning("Warning", "No log entries to analyze")
            return
        
        # Update UI to analyzing state
        self.ai_status_title.config(text="Analyzing Logs...")
        self.ai_status_message.config(text="AI is processing your logs. This may take a few minutes.")
        
        # Show progress bar
        self.ai_progress_frame.pack(fill=tk.X, pady=(15, 0))
        
        # Disable start button
        self.start_main_ai_btn.config(state=tk.DISABLED, text="🔄 Analyzing...")
        
        # Start analysis in background thread
        def run_analysis():
            try:
                # Simulate progress updates
                self.root.after(100, lambda: self.update_main_ai_progress(20, "Preparing log data..."))
                self.root.after(500, lambda: self.update_main_ai_progress(40, "Sending to AI model..."))
                
                # Perform actual analysis
                result = self.perform_llm_analysis()
                
                self.root.after(100, lambda: self.update_main_ai_progress(80, "Processing AI response..."))
                self.root.after(500, lambda: self.update_main_ai_progress(100, "Analysis completed!"))
                
                # Show results after a brief delay
                self.root.after(1000, lambda: self.show_main_ai_results(result))
                
            except Exception as e:
                error_msg = str(e)
                self.root.after(0, lambda: self.show_main_ai_error(error_msg))
        
        # Start analysis thread
        analysis_thread = threading.Thread(target=run_analysis, daemon=True)
        analysis_thread.start()
    
    def update_main_ai_progress(self, percentage, text):
        """Update the main AI analysis progress."""
        self.ai_progress_var.set(percentage)
        self.ai_progress_text.config(text=text)
        self.root.update_idletasks()
    
    def show_main_ai_results(self, analysis_text):
        """Show AI analysis results in the main section."""
        # Hide analysis section
        self.ai_analysis_frame.pack_forget()
        
        # Show results section
        self.ai_results_frame.pack(fill=tk.BOTH, expand=True, pady=(15, 0))
        
        # Update results content
        self.ai_results_text.config(state=tk.NORMAL)
        self.ai_results_text.delete("1.0", tk.END)
        self.ai_results_text.insert("1.0", analysis_text)
        self.ai_results_text.config(state=tk.DISABLED)
        
        # Auto-save to investigation folder
        try:
            print(f"Attempting to auto-save AI analysis...")
            filepath = self.save_ai_analysis_to_file(analysis_text)
            if filepath:
                print(f"Auto-save successful: {filepath}")
                self.status_var.set(f"🤖 AI analysis completed and auto-saved to investigation folder")
            else:
                print("Auto-save returned None")
                self.status_var.set("🤖 AI analysis completed (auto-save failed)")
        except Exception as e:
            print(f"Auto-save failed: {e}")
            self.status_var.set("🤖 AI analysis completed (auto-save failed)")
    
    def show_main_ai_error(self, error_msg):
        """Show AI analysis error in the main section."""
        # Reset UI state
        self.ai_status_title.config(text="Analysis Failed", fg=self.colors['accent_red'])
        self.ai_status_message.config(text=f"Error: {error_msg}\n\nPlease ensure Ollama is installed and running.")
        
        # Hide progress bar
        self.ai_progress_frame.pack_forget()
        
        # Re-enable start button
        self.start_main_ai_btn.config(state=tk.NORMAL, text="🚀 Start AI Analysis")
        
        self.status_var.set("❌ AI analysis failed")
    
    def export_main_ai_results(self):
        """Export the main AI results."""
        analysis_text = self.ai_results_text.get("1.0", tk.END).strip()
        if analysis_text:
            self.export_analysis(analysis_text)
    
    def clear_main_ai_results(self):
        """Clear the main AI results and show analysis section again."""
        # Hide results section
        self.ai_results_frame.pack_forget()
        
        # Show analysis section again
        self.ai_analysis_frame.pack(fill=tk.X, pady=(15, 0))
        
        # Reset analysis section state
        self.ai_status_title.config(text="Ready for Analysis", fg=self.colors['text_primary'])
        self.ai_status_message.config(text="Click 'Start AI Analysis' to send your logs to AI for comprehensive security analysis.")
        
        # Hide progress bar
        self.ai_progress_frame.pack_forget()
        
        # Reset progress
        self.ai_progress_var.set(0)
        self.ai_progress_text.config(text="")
        
        # Re-enable start button
        self.start_main_ai_btn.config(state=tk.NORMAL, text="🚀 Start AI Analysis")
        
        self.status_var.set("Ready for new AI analysis")


def main():
    """Main function to run the DFIR Log Sorter application."""
    root = tk.Tk()
    app = DFIRLogSorter(root)
    root.mainloop()


if __name__ == "__main__":
    main()
