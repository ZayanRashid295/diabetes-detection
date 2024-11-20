// DOM Elements
const dropZone = document.getElementById('drop-zone');
const fileInfo = document.getElementById('file-info');
const analyzeButton = document.querySelector('.analyze-button');
let currentFile = null;

// Prevent default drag behaviors
['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, preventDefaults, false);
    document.body.addEventListener(eventName, preventDefaults, false);
});

// Highlight drop zone when file is dragged over
['dragenter', 'dragover'].forEach(eventName => {
    dropZone.addEventListener(eventName, highlight, false);
});

['dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, unhighlight, false);
});

// Handle dropped files
dropZone.addEventListener('drop', handleDrop, false);

// Handle click to select file
dropZone.addEventListener('click', () => {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.csv,.xlsx,.xls';
    input.style.display = 'none';
    
    input.onchange = (e) => {
        const file = e.target.files[0];
        handleFile(file);
    };
    
    document.body.appendChild(input);
    input.click();
    document.body.removeChild(input);
});

// Handle analyze button click
analyzeButton.addEventListener('click', analyzeData);

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

function highlight(e) {
    dropZone.classList.add('hover');
    dropZone.style.borderColor = '#2563eb';
    dropZone.style.backgroundColor = '#f8fafc';
}

function unhighlight(e) {
    dropZone.classList.remove('hover');
    dropZone.style.borderColor = '#e5e7eb';
    dropZone.style.backgroundColor = 'white';
}

function handleDrop(e) {
    const dt = e.dataTransfer;
    const file = dt.files[0];
    handleFile(file);
}

function handleFile(file) {
    validateFile(file) ? uploadFile(file) : showError('Please upload a valid Excel or CSV file');
}

function validateFile(file) {
    const validTypes = [
        'application/vnd.ms-excel',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'text/csv'
    ];
    
    const fileName = file.name.toLowerCase();
    const fileExtension = fileName.substring(fileName.lastIndexOf('.'));
    
    return validTypes.includes(file.type) || 
           ['.csv', '.xlsx', '.xls'].includes(fileExtension);
}

async function uploadFile(file) {
    currentFile = file;
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Upload failed');
        }
        
        showSuccess();
        analyzeButton.style.display = 'block';
        
    } catch (error) {
        showError(error.message);
    }
}

async function analyzeData() {
    if (!currentFile) {
        showError('Please upload a file first');
        return;
    }
    
    analyzeButton.disabled = true;
    analyzeButton.textContent = 'Analyzing...';
    
    try {
        const response = await fetch('/analyze', {
            method: 'POST'
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Analysis failed');
        }
        
        // Handle successful analysis
        window.location.href = `/results/${data.analysisId}`;
        
    } catch (error) {
        showError(error.message);
        analyzeButton.disabled = false;
        analyzeButton.textContent = 'Analyze Data';
    }
}

function showSuccess() {
    fileInfo.style.display = 'block';
    fileInfo.textContent = 'File uploaded successfully';
    fileInfo.style.backgroundColor = '#f3f4f6';
}

function showError(message) {
    fileInfo.style.display = 'block';
    fileInfo.textContent = message;
    fileInfo.style.backgroundColor = '#fee2e2';
}

// Add loading indicator functions
function showLoading() {
    analyzeButton.disabled = true;
    analyzeButton.innerHTML = `
        <span class="loading-spinner"></span>
        Processing...
    `;
}

function hideLoading() {
    analyzeButton.disabled = false;
    analyzeButton.innerHTML = 'Analyze Data';
}