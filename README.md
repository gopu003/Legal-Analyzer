# Legal Document Analyzer

A simple AI-powered tool that analyzes legal documents to identify risks, missing clauses, and provides plain-language summaries.

## 📸 Current Screenshots

| Login Page | File Upload | Analysis Result |
|------------|-------------|-----------------|
| ![Login](app/screenshots/login%20page.png) | ![Upload](app/screenshots/file%20upload.png) | ![Analysis](app/screenshots/analysis%20result.png) |

## What This Tool Does

- **Analyzes Legal Documents**: Upload PDF or DOCX files for instant analysis
- **Identifies Risks**: Highlights potentially problematic clauses
- **Provides Summaries**: Converts legal jargon into plain English
- **Offers Improvements**: Suggests ways to strengthen your documents

## Quick Setup Guide

### Step 1: Install Python

1. Download and install [Python 3.7 or higher](https://www.python.org/downloads/)
2. During installation, check "Add Python to PATH"

### Step 2: Get a Free Groq API Key

1. Visit [Groq Console](https://console.groq.com/keys)
2. Create a free account
3. Generate a new API key (starts with `gsk_`)
4. Copy your key for the next step

### Step 3: Set Up the Application

1. Open the `.env` file in the `app` folder
2. Replace the existing API key with your own Groq API key
3. Save the file

### Step 4: Install Dependencies

1. Open Command Prompt or PowerShell
2. Navigate to the app folder:
   ```
   cd "path\to\Legal_Analyzer\app"
   ```
3. Install required packages:
   ```
   pip install -r requirements.txt
   ```

### Step 5: Run the Application

1. In the same Command Prompt or PowerShell window:
   ```
   python main.py
   ```
2. Open your browser and go to: http://127.0.0.1:5000
3. Register a new account or log in with any username/password

## How to Use

1. **Upload a Document**: Click "Choose File" and select a PDF or DOCX file
2. **Analyze**: Click the "Analyze Document" button
3. **Review Results**: The analysis will show:
   - Document overview
   - Risk assessment
   - Missing elements
   - Plain language summary
   - Improvement recommendations
4. **Navigate Sections**: Use the dropdown menu to jump to specific sections
5. **Download Report**: Click "Download Analysis Report" to save the results

## Sample Documents

Try these included sample documents:
- `uploads/sample_contract.pdf`
- `uploads/test_nda.docx`

## Troubleshooting

### Common Issues

- **"Module not found" error**: Run `pip install -r requirements.txt` again
- **"Invalid API key"**: Check that your Groq API key is correctly entered in the `.env` file
- **Empty analysis results**: Make sure your document is not password-protected

### Quick Fixes

1. Restart the application
2. Verify Python is installed: Type `python --version` in Command Prompt
3. Check your internet connection (required for API calls)

## Important Notes

- This tool is for educational purposes only and not a substitute for legal advice
- The free Groq API has usage limits
- Only PDF and DOCX files are supported
- Maximum file size: 10MB

---

**Disclaimer**: This application processes documents through the Groq API. While we don't store your documents, they are transmitted to Groq for analysis. Please don't upload confidential information.