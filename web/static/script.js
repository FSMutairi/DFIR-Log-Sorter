// DFIR Log Sorter Flask Application
// Enhanced JavaScript functionality with Flask backend integration

class DFIRLogSorter {
    constructor() {
        this.logEntries = [];
        this.currentEditId = null;
        this.timeMode = 'picker'; // 'picker' or 'manual'
        
        this.initializeElements();
        this.bindEvents();
        this.loadEntries();
        this.initializeTimeEntry();
        this.updateSessionTime();
    }

    initializeElements() {
        // Form elements
        this.logForm = document.getElementById('logForm');
        this.datetimePicker = document.getElementById('datetimePicker');
        this.manualInput = document.getElementById('manualInput');
        this.descriptionInput = document.getElementById('description');
        this.severitySelect = document.getElementById('severity');
        this.currentTimeBtn = document.getElementById('currentTimeBtn');

        // Time mode buttons
        this.pickerModeBtn = document.getElementById('pickerMode');
        this.manualModeBtn = document.getElementById('manualMode');
        this.timeHelpText = document.getElementById('timeHelpText');

        // Control buttons
        this.sortBtn = document.getElementById('sortBtn');
        this.clearBtn = document.getElementById('clearBtn');
        this.saveFileBtn = document.getElementById('saveFileBtn');
        this.exportBtn = document.getElementById('exportBtn');

        // Sort buttons
        this.sortAscBtn = document.getElementById('sortAscBtn');
        this.sortDescBtn = document.getElementById('sortDescBtn');

        // Display elements
        this.entryCount = document.getElementById('entryCount');
        this.sortStatus = document.getElementById('sortStatus');
        this.timelineCount = document.getElementById('timelineCount');
        this.timelineStatus = document.getElementById('timelineStatus');
        this.statusMessage = document.getElementById('statusMessage');
        this.emptyState = document.getElementById('emptyState');
        this.timelineContainer = document.getElementById('timelineContainer');
        this.timelineBody = document.getElementById('timelineBody');

        // Modal elements
        this.editModal = document.getElementById('editModal');
        this.editForm = document.getElementById('editForm');
        this.editEntryId = document.getElementById('editEntryId');
        this.editTimestamp = document.getElementById('editTimestamp');
        this.editSeverity = document.getElementById('editSeverity');
        this.editDescription = document.getElementById('editDescription');
        this.closeModal = document.getElementById('closeModal');
        this.cancelEdit = document.getElementById('cancelEdit');
        
        // Export modal elements
        this.exportModal = document.getElementById('exportModal');
        this.closeExportModal = document.getElementById('closeExportModal');
        this.cancelExport = document.getElementById('cancelExport');
        this.exportCsvBtn = document.getElementById('exportCsvBtn');
        this.exportTxtBtn = document.getElementById('exportTxtBtn');
        
        // Import modal elements
        this.importBtn = document.getElementById('importBtn');
        this.importModal = document.getElementById('importModal');
        this.closeImportModal = document.getElementById('closeImportModal');
        this.cancelImport = document.getElementById('cancelImport');
        this.csvFileInput = document.getElementById('csvFileInput');
        this.fileInfo = document.getElementById('fileInfo');
        this.fileName = document.getElementById('fileName');
        this.fileSize = document.getElementById('fileSize');
        this.removeFile = document.getElementById('removeFile');
        this.importCsvBtn = document.getElementById('importCsvBtn');
        this.importProgress = document.getElementById('importProgress');
        this.progressFill = document.getElementById('progressFill');
        this.progressText = document.getElementById('progressText');
        
        // AI Analysis modal elements
        this.aiAnalysisBtn = document.getElementById('aiAnalysisBtn');
        this.aiAnalysisModal = document.getElementById('aiAnalysisModal');
        this.closeAiModal = document.getElementById('closeAiModal');
        this.cancelAiAnalysis = document.getElementById('cancelAiAnalysis');
        this.startAnalysisBtn = document.getElementById('startAnalysisBtn');
        this.exportAnalysisBtn = document.getElementById('exportAnalysisBtn');
        this.analysisStatus = document.getElementById('analysisStatus');
        this.statusTitle = document.getElementById('statusTitle');
        this.aiStatusMessage = document.getElementById('aiStatusMessage');
        this.analysisProgress = document.getElementById('analysisProgress');
        this.aiProgressFill = document.getElementById('aiProgressFill');
        this.aiProgressText = document.getElementById('aiProgressText');
        this.analysisResults = document.getElementById('analysisResults');
        this.analysisText = document.getElementById('analysisText');
        
        // AI Results section elements
        this.aiResultsSection = document.getElementById('aiResultsSection');
        this.aiResultsTitle = document.getElementById('aiResultsTitle');
        this.aiResultsMessage = document.getElementById('aiResultsMessage');
        this.aiResultsText = document.getElementById('aiResultsText');
        this.exportAiResultsBtn = document.getElementById('exportAiResultsBtn');
        this.clearAiResultsBtn = document.getElementById('clearAiResultsBtn');
        
        // Main AI Analysis section elements
        this.aiAnalysisSection = document.getElementById('aiAnalysisSection');
        this.startMainAnalysisBtn = document.getElementById('startMainAnalysisBtn');
        this.mainAnalysisStatus = document.getElementById('mainAnalysisStatus');
        this.mainStatusTitle = document.getElementById('mainStatusTitle');
        this.mainStatusMessage = document.getElementById('mainStatusMessage');
        this.mainAnalysisProgress = document.getElementById('mainAnalysisProgress');
        this.mainProgressFill = document.getElementById('mainProgressFill');
        this.mainProgressText = document.getElementById('mainProgressText');
    }

    bindEvents() {
        // Form submission
        if (this.logForm) {
        this.logForm.addEventListener('submit', (e) => this.handleAddEntry(e));
        }
        
        // Time mode toggle
        if (this.pickerModeBtn) {
            this.pickerModeBtn.addEventListener('click', () => this.switchTimeMode('picker'));
        }
        if (this.manualModeBtn) {
            this.manualModeBtn.addEventListener('click', () => this.switchTimeMode('manual'));
        }
        
        // Current time button
        if (this.currentTimeBtn) {
        this.currentTimeBtn.addEventListener('click', () => this.insertCurrentTime());
        }
        
        // Control buttons
        if (this.sortBtn) {
        this.sortBtn.addEventListener('click', () => this.sortLogs());
        }
        if (this.clearBtn) {
        this.clearBtn.addEventListener('click', () => this.clearLogs());
        }
        if (this.saveFileBtn) {
            this.saveFileBtn.addEventListener('click', () => this.saveToFile());
        }
        if (this.exportBtn) {
            this.exportBtn.addEventListener('click', () => this.showExportDialog());
        }

        // Sort buttons
        if (this.sortAscBtn) {
            this.sortAscBtn.addEventListener('click', () => this.sortByTimestamp('asc'));
        }
        if (this.sortDescBtn) {
            this.sortDescBtn.addEventListener('click', () => this.sortByTimestamp('desc'));
        }

        // Modal events
        if (this.closeModal) {
        this.closeModal.addEventListener('click', () => this.closeEditModal());
        }
        if (this.cancelEdit) {
        this.cancelEdit.addEventListener('click', () => this.closeEditModal());
        }
        if (this.editForm) {
        this.editForm.addEventListener('submit', (e) => this.handleEditEntry(e));
        }

        // Close modal on backdrop click
        if (this.editModal) {
        this.editModal.addEventListener('click', (e) => {
            if (e.target === this.editModal) {
                this.closeEditModal();
            }
        });
        }
        
        // Export modal events
        if (this.closeExportModal) {
            this.closeExportModal.addEventListener('click', () => this.closeExportModal());
        }
        if (this.cancelExport) {
            this.cancelExport.addEventListener('click', () => this.closeExportModal());
        }
        if (this.exportCsvBtn) {
            this.exportCsvBtn.addEventListener('click', () => this.exportCsv());
        }
        if (this.exportTxtBtn) {
            this.exportTxtBtn.addEventListener('click', () => this.exportTxt());
        }

        // Close export modal on backdrop click
        if (this.exportModal) {
            this.exportModal.addEventListener('click', (e) => {
                if (e.target === this.exportModal) {
                    this.closeExportModal();
                }
            });
        }
        
        // Import modal events
        if (this.importBtn) {
            this.importBtn.addEventListener('click', () => this.showImportDialog());
        }
        if (this.closeImportModal) {
            this.closeImportModal.addEventListener('click', () => this.closeImportDialog());
        }
        if (this.cancelImport) {
            this.cancelImport.addEventListener('click', () => this.closeImportDialog());
        }
        if (this.csvFileInput) {
            this.csvFileInput.addEventListener('change', (e) => this.handleFileSelect(e));
        }
        if (this.removeFile) {
            this.removeFile.addEventListener('click', () => this.clearSelectedFile());
        }
        if (this.importCsvBtn) {
            this.importCsvBtn.addEventListener('click', () => this.importCsvFile());
        }

        // Close import modal on backdrop click
        if (this.importModal) {
            this.importModal.addEventListener('click', (e) => {
                if (e.target === this.importModal) {
                    this.closeImportDialog();
                }
            });
        }
        
        // Drag and drop events
        if (this.csvFileInput && this.csvFileInput.parentElement) {
            const dropZone = this.csvFileInput.parentElement;
            
            dropZone.addEventListener('dragover', (e) => {
                e.preventDefault();
                dropZone.classList.add('drag-over');
            });
            
            dropZone.addEventListener('dragleave', (e) => {
                e.preventDefault();
                dropZone.classList.remove('drag-over');
            });
            
            dropZone.addEventListener('drop', (e) => {
                e.preventDefault();
                dropZone.classList.remove('drag-over');
                
                const files = e.dataTransfer.files;
                if (files.length > 0) {
                    this.handleFileSelect({ target: { files: files } });
                }
            });
        }
        
        // AI Analysis modal events
        if (this.aiAnalysisBtn) {
            this.aiAnalysisBtn.addEventListener('click', () => this.showAiAnalysisDialog());
        }
        if (this.closeAiModal) {
            this.closeAiModal.addEventListener('click', () => this.closeAiAnalysisDialog());
        }
        if (this.cancelAiAnalysis) {
            this.cancelAiAnalysis.addEventListener('click', () => this.closeAiAnalysisDialog());
        }
        if (this.startAnalysisBtn) {
            this.startAnalysisBtn.addEventListener('click', () => this.startAiAnalysis());
        }
                if (this.exportAnalysisBtn) {
            this.exportAnalysisBtn.addEventListener('click', () => this.exportAiAnalysis());
        }

        // AI Results section events
        if (this.exportAiResultsBtn) {
            this.exportAiResultsBtn.addEventListener('click', () => this.exportAiResults());
        }
        if (this.clearAiResultsBtn) {
            this.clearAiResultsBtn.addEventListener('click', () => this.clearAiResults());
        }
        
        // Main AI Analysis section events
        if (this.startMainAnalysisBtn) {
            this.startMainAnalysisBtn.addEventListener('click', () => this.startMainAiAnalysis());
        }

        // Close AI analysis modal on backdrop click
        if (this.aiAnalysisModal) {
            this.aiAnalysisModal.addEventListener('click', (e) => {
                if (e.target === this.aiAnalysisModal) {
                    this.closeAiAnalysisDialog();
            }
        });
        }

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.closeEditModal();
            }
        });
    }

    initializeTimeEntry() {
        // Set initial time mode
        this.switchTimeMode('picker');
        
        // Set current time as default
        this.insertCurrentTime();
    }

    switchTimeMode(mode) {
        this.timeMode = mode;
        
        if (mode === 'picker') {
            this.pickerModeBtn.classList.add('active');
            this.manualModeBtn.classList.remove('active');
            this.datetimePicker.style.display = 'block';
            this.manualInput.style.display = 'none';
            this.timeHelpText.textContent = 'Use the date/time picker for easy selection (includes seconds)';
        } else {
            this.manualModeBtn.classList.add('active');
            this.pickerModeBtn.classList.remove('active');
            this.datetimePicker.style.display = 'none';
            this.manualInput.style.display = 'block';
            this.timeHelpText.textContent = 'Enter time in YYYY-MM-DD-H-M-S format';
        }
    }

    async insertCurrentTime() {
        try {
            const response = await fetch('/current_time');
            const data = await response.json();
            
            if (this.timeMode === 'picker') {
                this.datetimePicker.value = data.datetime_local;
            } else {
                this.manualInput.value = data.formatted;
            }
        } catch (error) {
            console.error('Error getting current time:', error);
            // Fallback to client-side time
        const now = new Date();
            if (this.timeMode === 'picker') {
                const localTime = new Date(now.getTime() - now.getTimezoneOffset() * 60000);
                this.datetimePicker.value = localTime.toISOString().slice(0, 19);
            } else {
        const timestamp = now.getFullYear() + '-' + 
            String(now.getMonth() + 1).padStart(2, '0') + '-' + 
            String(now.getDate()).padStart(2, '0') + '-' + 
            String(now.getHours()).padStart(2, '0') + '-' + 
            String(now.getMinutes()).padStart(2, '0') + '-' + 
            String(now.getSeconds()).padStart(2, '0');
                this.manualInput.value = timestamp;
            }
        }
    }

    getTimestampValue() {
        if (this.timeMode === 'picker') {
            // Convert from datetime-local format (YYYY-MM-DDTHH:MM:SS) to our standard format (YYYY-MM-DD-HH-MM-SS)
            const pickerValue = this.datetimePicker.value;
            if (pickerValue) {
                return pickerValue.replace('T', '-').replace(/:/g, '-');
            }
            return '';
        } else {
            return this.manualInput.value;
        }
    }

    setTimestampValue(value) {
        if (this.timeMode === 'picker') {
            // Convert from our standard format (YYYY-MM-DD-HH-MM-SS) to datetime-local format (YYYY-MM-DDTHH:MM:SS)
            try {
                if (value && value.includes('-')) {
                    // If it's our custom format, convert it
                    const parts = value.split('-');
                    if (parts.length === 6) {
                        const isoFormat = `${parts[0]}-${parts[1]}-${parts[2]}T${parts[3]}:${parts[4]}:${parts[5]}`;
                        this.datetimePicker.value = isoFormat;
                    } else {
                        // Try parsing as a regular date
                const date = new Date(value);
                const localTime = new Date(date.getTime() - date.getTimezoneOffset() * 60000);
                        this.datetimePicker.value = localTime.toISOString().slice(0, 19);
                    }
                } else {
                    this.datetimePicker.value = value;
                }
        } catch (error) {
                this.datetimePicker.value = value;
            }
        } else {
            this.manualInput.value = value;
        }
    }

    async loadEntries() {
        try {
            const response = await fetch('/api/entries');
            const data = await response.json();
            
            this.logEntries = data.entries || [];
            this.updateDisplay();
            
        } catch (error) {
            console.error('Error loading entries:', error);
            this.showMessage('Failed to load entries', 'error');
        }
    }

    async handleAddEntry(e) {
        e.preventDefault();
        
        const timestamp = this.getTimestampValue().trim();
        const severity = this.severitySelect.value;
        const description = this.descriptionInput.value.trim();

        // Client-side validation
        if (!timestamp) {
            this.showMessage('Timestamp is required', 'error');
            return;
        }
        
        if (!description) {
            this.showMessage('Description is required', 'error');
            return;
        }

        if (description.length < 5) {
            this.showMessage('Description must be at least 5 characters long', 'error');
            return;
        }

        try {
            const response = await fetch('/api/entries', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                timestamp: timestamp,
                severity: severity,
                    description: description
                })
            });

            const data = await response.json();

            if (response.ok) {
            // Clear form
            this.logForm.reset();
            this.severitySelect.value = 'Info';
                this.insertCurrentTime(); // Reset to current time
                
                // Reload entries
                await this.loadEntries();
                
                this.showMessage('✅ Log entry added and saved to investigation_logs.csv', 'success');
                
                // Focus back to description for quick entry
                this.descriptionInput.focus();
                
            } else {
                this.showMessage(data.error || 'Failed to add entry', 'error');
            }

        } catch (error) {
            console.error('Error adding entry:', error);
            this.showMessage('Failed to add entry: ' + error.message, 'error');
        }
    }

    async sortLogs() {
        try {
            const response = await fetch('/api/sort', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            const data = await response.json();

            if (response.ok) {
                this.logEntries = data.entries;
                this.updateDisplay();
                this.showMessage(data.message, 'success');
            } else {
                this.showMessage(data.error || 'Failed to sort entries', 'error');
            }

        } catch (error) {
            console.error('Error sorting entries:', error);
            this.showMessage('Failed to sort entries', 'error');
        }
    }

    async sortByTimestamp(direction) {
        try {
            // Update button states
            this.updateSortButtonStates(direction);
            
            // Sort entries locally
            const sortedEntries = [...this.logEntries].sort((a, b) => {
                const timeA = new Date(a.parsed_time);
                const timeB = new Date(b.parsed_time);
                
                if (direction === 'asc') {
                    return timeA - timeB; // Old to New
                } else {
                    return timeB - timeA; // New to Old
                }
            });
            
            this.logEntries = sortedEntries;
            this.updateDisplay();
            
            const directionText = direction === 'asc' ? 'Old to New' : 'New to Old';
            this.showMessage(`✅ Timeline sorted ${directionText}`, 'success');
            
        } catch (error) {
            console.error('Error sorting by timestamp:', error);
            this.showMessage('Failed to sort by timestamp', 'error');
        }
    }

    updateSortButtonStates(activeDirection) {
        // Remove active class from all sort buttons
        if (this.sortAscBtn) this.sortAscBtn.classList.remove('active');
        if (this.sortDescBtn) this.sortDescBtn.classList.remove('active');
        
        // Add active class to the clicked button
        if (activeDirection === 'asc' && this.sortAscBtn) {
            this.sortAscBtn.classList.add('active');
        } else if (activeDirection === 'desc' && this.sortDescBtn) {
            this.sortDescBtn.classList.add('active');
        }
        
        // Update status message
        const directionText = activeDirection === 'asc' ? 'Old to New' : 'New to Old';
        if (this.statusMessage) {
            this.statusMessage.textContent = `Timeline sorted ${directionText} - Ready for log entries`;
        }
    }

    async clearLogs() {
        if (this.logEntries.length === 0) {
            this.showMessage('No entries to clear', 'info');
            return;
        }

        if (confirm('Are you sure you want to clear all log entries?\n\nThis action cannot be undone.')) {
            try {
                const response = await fetch('/api/clear', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                });

                const data = await response.json();

                if (response.ok) {
                    await this.loadEntries();
                    this.showMessage(data.message, 'info');
                } else {
                    this.showMessage(data.error || 'Failed to clear entries', 'error');
                }

            } catch (error) {
                console.error('Error clearing entries:', error);
                this.showMessage('Failed to clear entries', 'error');
            }
        }
    }

    async saveToFile() {
        try {
            const response = await fetch('/api/export/file', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            const data = await response.json();

            if (response.ok) {
                this.showMessage(`💾 ${data.message}`, 'success');
            } else {
                this.showMessage(data.error || 'Failed to save log file', 'error');
            }

        } catch (error) {
            console.error('Error saving file:', error);
            this.showMessage('Failed to save log file', 'error');
        }
    }

    async exportCsv() {
        try {
            const response = await fetch('/api/export/csv');
            const data = await response.json();

            if (response.ok) {
                this.downloadFile(data.csv_content, data.filename, 'text/csv');
                this.showMessage('📊 Exported timeline to CSV', 'success');
                this.closeExportModal();
            } else {
                this.showMessage(data.error || 'Failed to export CSV', 'error');
            }

        } catch (error) {
            console.error('Error exporting CSV:', error);
            this.showMessage('Failed to export CSV', 'error');
        }
    }

    async exportTxt() {
        try {
            const response = await fetch('/api/export/txt');
            const data = await response.json();

            if (response.ok) {
                this.downloadFile(data.txt_content, data.filename, 'text/plain');
                this.showMessage('📄 Exported timeline to TXT', 'success');
                this.closeExportModal();
            } else {
                this.showMessage(data.error || 'Failed to export TXT', 'error');
            }

        } catch (error) {
            console.error('Error exporting TXT:', error);
            this.showMessage('Failed to export TXT', 'error');
        }
    }



    showExportDialog() {
        if (this.exportModal) {
            this.exportModal.classList.add('show');
        }
    }

    closeExportModal() {
        if (this.exportModal) {
            this.exportModal.classList.remove('show');
        }
    }

    showImportDialog() {
        if (this.importModal) {
            this.importModal.classList.add('show');
            this.clearSelectedFile();
        }
    }

    closeImportDialog() {
        if (this.importModal) {
            this.importModal.classList.remove('show');
            this.clearSelectedFile();
        }
    }

    handleFileSelect(event) {
        const files = event.target.files;
        if (files.length === 0) return;

        const file = files[0];
        
        // Validate file type
        if (!file.name.toLowerCase().endsWith('.csv')) {
            this.showMessage('Please select a CSV file', 'error');
            return;
        }
        
        // Validate file size (max 10MB)
        const maxSize = 10 * 1024 * 1024; // 10MB
        if (file.size > maxSize) {
            this.showMessage('File size must be less than 10MB', 'error');
            return;
        }
        
        // Show file info
        this.displayFileInfo(file);
        
        // Enable import button
        if (this.importCsvBtn) {
            this.importCsvBtn.disabled = false;
        }
    }

    displayFileInfo(file) {
        if (this.fileName) {
            this.fileName.textContent = file.name;
        }
        if (this.fileSize) {
            this.fileSize.textContent = this.formatFileSize(file.size);
        }
        if (this.fileInfo) {
            this.fileInfo.style.display = 'block';
        }
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    clearSelectedFile() {
        if (this.csvFileInput) {
            this.csvFileInput.value = '';
        }
        if (this.fileInfo) {
            this.fileInfo.style.display = 'none';
        }
        if (this.importCsvBtn) {
            this.importCsvBtn.disabled = true;
        }
        if (this.importProgress) {
            this.importProgress.style.display = 'none';
        }
    }

    async importCsvFile() {
        const files = this.csvFileInput.files;
        if (files.length === 0) {
            this.showMessage('Please select a CSV file', 'error');
            return;
        }

        const file = files[0];
        
        try {
            // Show progress
            this.showImportProgress(true);
            this.updateProgress(0, 'Reading file...');
            
            // Read file content
            const content = await this.readFileAsText(file);
            this.updateProgress(30, 'Parsing CSV data...');
            
            // Parse CSV
            const entries = this.parseCSV(content);
            this.updateProgress(60, 'Validating entries...');
            
            if (entries.length === 0) {
                throw new Error('No valid entries found in CSV file');
            }
            
            // Send to server
            this.updateProgress(80, 'Importing to server...');
            const response = await fetch('/api/import/csv', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ entries: entries })
            });

            const data = await response.json();

            if (response.ok) {
                this.updateProgress(100, 'Import completed!');
                
                // Wait a moment to show completion
                setTimeout(() => {
                    this.showImportProgress(false);
                    this.closeImportDialog();
                    this.loadEntries(); // Refresh the timeline
                    this.showMessage(`📥 Successfully imported ${data.imported_count} entries`, 'success');
                }, 1000);
            } else {
                throw new Error(data.error || 'Failed to import CSV');
            }

        } catch (error) {
            console.error('Error importing CSV:', error);
            this.showImportProgress(false);
            this.showMessage(`Failed to import CSV: ${error.message}`, 'error');
        }
    }

    readFileAsText(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = e => resolve(e.target.result);
            reader.onerror = e => reject(new Error('Failed to read file'));
            reader.readAsText(file);
        });
    }

    parseCSV(content) {
        const lines = content.split('\n').map(line => line.trim()).filter(line => line);
        if (lines.length < 2) {
            throw new Error('CSV file must have at least a header row and one data row');
        }

        const header = lines[0].split(',').map(col => col.trim().replace(/"/g, ''));
        const entries = [];

        // Find column indices
        const timestampIdx = header.findIndex(col => 
            col.toLowerCase().includes('timestamp') || col.toLowerCase().includes('time')
        );
        const severityIdx = header.findIndex(col => 
            col.toLowerCase().includes('severity') || col.toLowerCase().includes('level')
        );
        const descriptionIdx = header.findIndex(col => 
            col.toLowerCase().includes('description') || col.toLowerCase().includes('message')
        );

        if (timestampIdx === -1) {
            throw new Error('CSV must contain a timestamp column');
        }
        if (descriptionIdx === -1) {
            throw new Error('CSV must contain a description column');
        }

        // Parse data rows
        for (let i = 1; i < lines.length; i++) {
            try {
                const row = this.parseCSVRow(lines[i]);
                
                if (row.length <= Math.max(timestampIdx, descriptionIdx)) {
                    continue; // Skip rows with insufficient columns
                }

                const timestamp = row[timestampIdx]?.trim();
                const description = row[descriptionIdx]?.trim();
                const severity = severityIdx !== -1 ? row[severityIdx]?.trim() : 'Info';

                if (timestamp && description) {
                    entries.push({
                        timestamp: timestamp,
                        description: description,
                        severity: severity || 'Info'
                    });
                }
            } catch (error) {
                console.warn(`Skipping invalid row ${i + 1}: ${error.message}`);
            }
        }

        return entries;
    }

    parseCSVRow(row) {
        const result = [];
        let current = '';
        let inQuotes = false;
        
        for (let i = 0; i < row.length; i++) {
            const char = row[i];
            
            if (char === '"') {
                if (inQuotes && row[i + 1] === '"') {
                    current += '"';
                    i++; // Skip next quote
                } else {
                    inQuotes = !inQuotes;
                }
            } else if (char === ',' && !inQuotes) {
                result.push(current);
                current = '';
            } else {
                current += char;
            }
        }
        
        result.push(current);
        return result;
    }

    showImportProgress(show) {
        if (this.importProgress) {
            this.importProgress.style.display = show ? 'block' : 'none';
        }
        if (this.importCsvBtn) {
            this.importCsvBtn.disabled = show;
        }
    }

    updateProgress(percentage, text) {
        if (this.progressFill) {
            this.progressFill.style.width = percentage + '%';
        }
        if (this.progressText) {
            this.progressText.textContent = text;
        }
    }

    showAiAnalysisDialog() {
        if (this.logEntries.length === 0) {
            this.showMessage('No log entries to analyze', 'error');
            return;
        }
        
        if (this.aiAnalysisModal) {
            this.aiAnalysisModal.classList.add('show');
            this.resetAnalysisDialog();
        }
    }

    closeAiAnalysisDialog() {
        if (this.aiAnalysisModal) {
            this.aiAnalysisModal.classList.remove('show');
        }
    }

    resetAnalysisDialog() {
        // Reset status
        if (this.analysisStatus) {
            this.analysisStatus.className = 'analysis-status';
        }
        if (this.statusTitle) {
            this.statusTitle.textContent = 'Ready for Analysis';
        }
        if (this.statusMessage) {
            this.statusMessage.textContent = `Click "Start Analysis" to send ${this.logEntries.length} log entries to AI for comprehensive security analysis.`;
        }
        
        // Hide progress and results
        if (this.analysisProgress) {
            this.analysisProgress.style.display = 'none';
        }
        if (this.analysisResults) {
            this.analysisResults.style.display = 'none';
        }
        
        // Reset buttons
        if (this.startAnalysisBtn) {
            this.startAnalysisBtn.style.display = 'inline-block';
            this.startAnalysisBtn.disabled = false;
        }
        if (this.exportAnalysisBtn) {
            this.exportAnalysisBtn.style.display = 'none';
        }
        
        // Clear text
        if (this.analysisText) {
            this.analysisText.value = '';
        }
    }

    async startAiAnalysis() {
        if (this.logEntries.length === 0) {
            this.showMessage('No log entries to analyze', 'error');
            return;
        }

        try {
            // Update UI to analyzing state
            this.setAnalysisStatus('analyzing', 'Analyzing Logs...', 'AI is processing your logs. This may take a few minutes.');
            
            // Show progress
            if (this.analysisProgress) {
                this.analysisProgress.style.display = 'block';
            }
            
            // Disable start button
            if (this.startAnalysisBtn) {
                this.startAnalysisBtn.disabled = true;
            }
            
            this.updateAiProgress(20, 'Preparing log data...');
            
            // Sort logs chronologically
            const sortedLogs = [...this.logEntries].sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));
            
            this.updateAiProgress(40, 'Sending to AI model...');
            
            // Send to backend
            const response = await fetch('/api/ai-analysis', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    logs: sortedLogs.map(entry => ({
                        timestamp: entry.timestamp,
                        severity: entry.severity,
                        description: entry.description
                    }))
                })
            });

            this.updateAiProgress(80, 'Processing AI response...');

            const data = await response.json();

            if (response.ok) {
                this.updateAiProgress(100, 'Analysis completed!');
                
                // Wait a moment then show results
                setTimeout(() => {
                    this.showAnalysisResults(data.analysis);
                }, 1000);
            } else {
                throw new Error(data.error || 'Failed to analyze logs');
            }

        } catch (error) {
            console.error('Error during AI analysis:', error);
            this.setAnalysisStatus('error', 'Analysis Failed', `Error: ${error.message}`);
            
            // Hide progress
            if (this.analysisProgress) {
                this.analysisProgress.style.display = 'none';
            }
            
            // Re-enable start button
            if (this.startAnalysisBtn) {
                this.startAnalysisBtn.disabled = false;
            }
            
            this.showMessage(`AI analysis failed: ${error.message}`, 'error');
        }
    }

    async startMainAiAnalysis() {
        if (this.logEntries.length === 0) {
            this.showMessage('No log entries to analyze', 'error');
            return;
        }

        try {
            // Update main section UI to analyzing state
            this.setMainAnalysisStatus('analyzing', 'Analyzing Logs...', 'AI is processing your logs. This may take a few minutes.');
            
            // Show progress in main section
            if (this.mainAnalysisProgress) {
                this.mainAnalysisProgress.style.display = 'block';
            }
            
            // Disable start button in main section
            if (this.startMainAnalysisBtn) {
                this.startMainAnalysisBtn.disabled = true;
            }
            
            this.updateMainAiProgress(20, 'Preparing log data...');
            
            // Sort logs chronologically
            const sortedLogs = [...this.logEntries].sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));
            
            this.updateMainAiProgress(40, 'Sending to AI model...');
            
            // Send to backend
            const response = await fetch('/api/ai-analysis', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    logs: sortedLogs.map(entry => ({
                        timestamp: entry.timestamp,
                        severity: entry.severity,
                        description: entry.description
                    }))
                })
            });

            this.updateMainAiProgress(80, 'Processing AI response...');

            const data = await response.json();

            if (response.ok) {
                this.updateMainAiProgress(100, 'Analysis completed!');
                
                // Wait a moment then show results
                setTimeout(() => {
                    this.showMainAnalysisResults(data.analysis);
                }, 1000);
            } else {
                throw new Error(data.error || 'Failed to analyze logs');
            }

        } catch (error) {
            console.error('Error during AI analysis:', error);
            this.setMainAnalysisStatus('error', 'Analysis Failed', `Error: ${error.message}`);
            
            // Hide progress
            if (this.mainAnalysisProgress) {
                this.mainAnalysisProgress.style.display = 'none';
            }
            
            // Re-enable start button
            if (this.startMainAnalysisBtn) {
                this.startMainAnalysisBtn.disabled = false;
            }
            
            this.showMessage(`AI analysis failed: ${error.message}`, 'error');
        }
    }

    setAnalysisStatus(state, title, message) {
        if (this.analysisStatus) {
            this.analysisStatus.className = `analysis-status ${state}`;
        }
        if (this.statusTitle) {
            this.statusTitle.textContent = title;
        }
        if (this.statusMessage) {
            this.statusMessage.textContent = message;
        }
    }

    updateAiProgress(percentage, text) {
        if (this.aiProgressFill) {
            this.aiProgressFill.style.width = percentage + '%';
        }
        if (this.aiProgressText) {
            this.aiProgressText.textContent = text;
        }
    }

    setMainAnalysisStatus(state, title, message) {
        if (this.mainAnalysisStatus) {
            this.mainAnalysisStatus.className = `ai-analysis-status ${state}`;
        }
        if (this.mainStatusTitle) {
            this.mainStatusTitle.textContent = title;
        }
        if (this.mainStatusMessage) {
            this.mainStatusMessage.textContent = message;
        }
    }

    updateMainAiProgress(percentage, text) {
        if (this.mainProgressFill) {
            this.mainProgressFill.style.width = percentage + '%';
        }
        if (this.mainProgressText) {
            this.mainProgressText.textContent = text;
        }
    }

    showMainAnalysisResults(analysisText) {
        // Update status to completed
        this.setMainAnalysisStatus('completed', 'Analysis Completed!', 'Your logs have been successfully analyzed. Review the results below.');
        
        // Hide progress
        if (this.mainAnalysisProgress) {
            this.mainAnalysisProgress.style.display = 'none';
        }
        
        // Hide the main analysis section
        if (this.aiAnalysisSection) {
            this.aiAnalysisSection.style.display = 'none';
        }
        
        // Show results in main section
        this.showAiResultsSection(analysisText);
        
        this.showMessage('🤖 AI analysis completed and auto-saved to investigation folder!', 'success');
    }

    showAnalysisResults(analysisText) {
        // Update status to completed
        this.setAnalysisStatus('completed', 'Analysis Completed!', 'Your logs have been successfully analyzed. Review the results below.');
        
        // Hide progress
        if (this.analysisProgress) {
            this.analysisProgress.style.display = 'none';
        }
        
        // Show results in modal
        if (this.analysisResults) {
            this.analysisResults.style.display = 'block';
        }
        if (this.analysisText) {
            this.analysisText.value = analysisText;
        }
        
        // Hide start button and show export button
        if (this.startAnalysisBtn) {
            this.startAnalysisBtn.style.display = 'none';
        }
        if (this.exportAnalysisBtn) {
            this.exportAnalysisBtn.style.display = 'inline-block';
        }
        
        // Show results in main section
        this.showAiResultsSection(analysisText);
        
        this.showMessage('🤖 AI analysis completed and auto-saved to investigation folder!', 'success');
    }
    
    showAiResultsSection(analysisText) {
        if (this.aiResultsSection) {
            this.aiResultsSection.style.display = 'block';
        }
        if (this.aiResultsText) {
            this.aiResultsText.value = analysisText;
        }
        if (this.aiResultsTitle) {
            this.aiResultsTitle.textContent = 'Analysis Complete';
        }
        if (this.aiResultsMessage) {
            this.aiResultsMessage.textContent = 'AI has analyzed your timeline and provided security insights.';
        }
        
        // Scroll to results section
        this.aiResultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
    
    clearAiResults() {
        if (this.aiResultsSection) {
            this.aiResultsSection.style.display = 'none';
        }
        if (this.aiResultsText) {
            this.aiResultsText.value = '';
        }
        
        // Show the main AI analysis section again
        if (this.aiAnalysisSection) {
            this.aiAnalysisSection.style.display = 'block';
        }
        
        // Reset the main analysis status
        this.setMainAnalysisStatus('ready', 'Ready for Analysis', 'Click "Start Analysis" to send your logs to AI for comprehensive security analysis.');
    }
    
    exportAiResults() {
        const analysisText = this.aiResultsText ? this.aiResultsText.value : '';
        if (analysisText.trim()) {
            const timestamp = new Date().toISOString().slice(0, 19).replace(/:/g, '-');
            const filename = `ai_analysis_${timestamp}.txt`;
            this.downloadFile(analysisText, filename, 'text/plain');
        }
    }

    exportAiAnalysis() {
        if (!this.analysisText || !this.analysisText.value.trim()) {
            this.showMessage('No analysis to export', 'error');
            return;
        }

        const analysisContent = this.analysisText.value;
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
        const filename = `ai_analysis_${timestamp}.txt`;
        
        // Create header for the export
        const header = `DFIR Log Sorter - AI Security Analysis
Generated: ${new Date().toLocaleString()}
Total Entries Analyzed: ${this.logEntries.length}
${'='.repeat(80)}

`;
        
        const fullContent = header + analysisContent + `

${'='.repeat(80)}
End of Analysis
${'='.repeat(80)}`;
        
        this.downloadFile(fullContent, filename, 'text/plain');
        this.showMessage('💾 AI analysis exported successfully', 'success');
    }

    async editEntry(entryId) {
        const entry = this.logEntries.find(e => e.id === entryId);
        if (!entry) return;

        this.currentEditId = entryId;
        
        // Populate modal form
        this.editEntryId.value = entryId;
        this.editTimestamp.value = entry.timestamp;
        this.editSeverity.value = entry.severity;
        this.editDescription.value = entry.description;

        // Show modal
        this.editModal.classList.add('show');
        this.editTimestamp.focus();
    }

    async handleEditEntry(e) {
        e.preventDefault();
        
        if (!this.currentEditId) return;

        const timestamp = this.editTimestamp.value.trim();
        const severity = this.editSeverity.value;
        const description = this.editDescription.value.trim();

        // Validation
        if (!timestamp || !description) {
            this.showMessage('Timestamp and description are required', 'error');
            return;
        }

        try {
            const response = await fetch(`/api/entries/${this.currentEditId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    timestamp: timestamp,
                    severity: severity,
                    description: description
                })
            });

            const data = await response.json();

            if (response.ok) {
                await this.loadEntries();
                this.closeEditModal();
                this.showMessage('✅ Log entry updated successfully', 'success');
            } else {
                this.showMessage(data.error || 'Failed to update entry', 'error');
            }

        } catch (error) {
            console.error('Error updating entry:', error);
            this.showMessage('Failed to update entry', 'error');
        }
    }

    async deleteEntry(entryId) {
        const entry = this.logEntries.find(e => e.id === entryId);
        if (!entry) return;

        if (confirm(`Are you sure you want to delete this log entry?\n\nTimestamp: ${entry.timestamp}\nSeverity: ${entry.severity}\n\nThis action cannot be undone.`)) {
            try {
                const response = await fetch(`/api/entries/${entryId}`, {
                    method: 'DELETE'
                });

                const data = await response.json();

                if (response.ok) {
                    await this.loadEntries();
                    this.showMessage('🗑️ Log entry deleted', 'info');
                } else {
                    this.showMessage(data.error || 'Failed to delete entry', 'error');
                }

            } catch (error) {
                console.error('Error deleting entry:', error);
                this.showMessage('Failed to delete entry', 'error');
            }
        }
    }

    closeEditModal() {
        if (this.editModal) {
            this.editModal.classList.remove('show');
        }
        this.currentEditId = null;
        if (this.editForm) {
            this.editForm.reset();
        }
    }

    updateDisplay() {
        const count = this.logEntries.length;
        
        // Update counters
        if (this.entryCount) {
        this.entryCount.textContent = count;
        }
        if (this.timelineCount) {
        this.timelineCount.textContent = count === 0 ? 'No entries' : 
            `${count} ${count === 1 ? 'entry' : 'entries'}`;
        }

        // Show/hide empty state
        if (count === 0) {
            if (this.emptyState) this.emptyState.style.display = 'block';
            if (this.timelineContainer) this.timelineContainer.style.display = 'none';
        } else {
            if (this.emptyState) this.emptyState.style.display = 'none';
            if (this.timelineContainer) this.timelineContainer.style.display = 'block';
            this.renderTimeline();
        }
    }

    renderTimeline() {
        if (!this.timelineBody) return;
        
        this.timelineBody.innerHTML = '';

        this.logEntries.forEach(entry => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td class="timestamp-cell">
                    <code>${this.escapeHtml(entry.timestamp)}</code>
                </td>
                <td class="severity-cell">
                    <span class="severity-badge ${this.getSeverityClass(entry.severity)}">
                        ${this.getSeverityIcon(entry.severity)} ${entry.severity}
                    </span>
                </td>
                <td class="description-cell">
                    ${this.escapeHtml(entry.description)}
                </td>
                <td class="actions-cell">
                    <button class="action-btn edit" onclick="app.editEntry('${entry.id}')" title="Edit entry">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="action-btn delete" onclick="app.deleteEntry('${entry.id}')" title="Delete entry">
                        <i class="fas fa-trash"></i>
                    </button>
                </td>
            `;
            this.timelineBody.appendChild(row);
        });
    }

    getSeverityIcon(severity) {
        const icons = {
            'Critical': '🔴',
            'High': '🟠',
            'Medium': '🟡',
            'Low': '🔵',
            'Info': 'ℹ️'
        };
        return icons[severity] || 'ℹ️';
    }

    getSeverityClass(severity) {
        return `severity-${severity.toLowerCase()}`;
    }

    downloadFile(content, filename, mimeType) {
        const blob = new Blob([content], { type: mimeType });
        const url = URL.createObjectURL(blob);
        
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        link.style.display = 'none';
        
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        URL.revokeObjectURL(url);
    }

    showMessage(message, type = 'info') {
        if (this.statusMessage) {
        this.statusMessage.textContent = message;
        }
        
        // Also show as flash message
        this.showFlashMessage(message, type);
        
        // Auto-clear status after 5 seconds
        setTimeout(() => {
            if (this.statusMessage) {
                this.statusMessage.textContent = 'Ready - Enter log entries and organize your investigation timeline';
            }
        }, 5000);
    }

    showFlashMessage(message, type) {
        const flashContainer = document.querySelector('.flash-messages') || this.createFlashContainer();
        
        const flashDiv = document.createElement('div');
        flashDiv.className = `flash-message flash-${type}`;
        flashDiv.innerHTML = `
            <div class="flash-content">
                <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-triangle' : 'info-circle'}"></i>
                <span>${message}</span>
                <button class="flash-close" onclick="this.parentElement.parentElement.remove()">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;
        
        flashContainer.appendChild(flashDiv);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (flashDiv.parentNode) {
                flashDiv.style.opacity = '0';
                setTimeout(() => flashDiv.remove(), 300);
            }
        }, 5000);
    }

    createFlashContainer() {
        const container = document.createElement('div');
        container.className = 'flash-messages';
        document.body.appendChild(container);
        return container;
    }

    updateSessionTime() {
        const sessionTimeElement = document.getElementById('sessionTime');
        if (sessionTimeElement) {
            const now = new Date();
            sessionTimeElement.textContent = now.toLocaleString();
        }
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Global functions for button clicks
function exportToFile() {
    if (window.app) {
        window.app.saveToFile();
    }
}

function resetInvestigation() {
    if (confirm('Are you sure you want to start a new investigation?\n\nThis will clear all current log entries and reset the session.')) {
        // Create a form and submit it to reset
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = '/reset';
        
        // Add CSRF token if needed (Flask-WTF)
        const csrfToken = document.querySelector('meta[name=csrf-token]');
        if (csrfToken) {
            const tokenInput = document.createElement('input');
            tokenInput.type = 'hidden';
            tokenInput.name = 'csrf_token';
            tokenInput.value = csrfToken.getAttribute('content');
            form.appendChild(tokenInput);
        }
        
        document.body.appendChild(form);
        form.submit();
    }
}

// Initialize the application when the DOM is loaded
let app;
document.addEventListener('DOMContentLoaded', () => {
    app = new DFIRLogSorter();
    window.app = app; // Make it globally accessible
    console.log('🔍 DFIR Log Sorter Flask application initialized successfully');
});

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + Enter to submit form
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        const activeElement = document.activeElement;
        if (activeElement && activeElement.id === 'description') {
            e.preventDefault();
            if (app && app.logForm) {
                app.logForm.dispatchEvent(new Event('submit'));
            }
        }
    }
    
    // Ctrl/Cmd + S to sort
    if ((e.ctrlKey || e.metaKey) && e.key === 's') {
        e.preventDefault();
        if (app) {
            app.sortLogs();
        }
    }
});