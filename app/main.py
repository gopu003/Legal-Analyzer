from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
import os
from file_handler import extract_text  # Changed from app.file_handler
from ai_utils import analyze_text      # Changed from app.ai_utils

UPLOAD_FOLDER = "uploads"

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'your-secret-key-change-this-in-production'

# In-memory user storage (replace with database in production)
users = {}

# Create uploads folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Update the index route with better error handling and debugging
@app.route("/", methods=["GET", "POST"])
def index():
    # Check if user is logged in
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))
    
    result = None
    error = None
    processing_status = None
    
    if request.method == "POST":
        file = request.files["file"]
        if file:
            filename = secure_filename(file.filename)
            file_extension = filename.split('.')[-1].lower()
            
            # Validate file type
            if file_extension not in ['pdf', 'docx']:
                error = "Only PDF and DOCX files are supported."
                return render_template("index.html", result=result, error=error, processing_status="failed")
            
            # Validate file size (10MB limit)
            file.seek(0, 2)  # Seek to end
            file_size = file.tell()
            file.seek(0)  # Reset to beginning
            
            if file_size > 10 * 1024 * 1024:  # 10MB
                error = "File size exceeds 10MB limit."
                return render_template("index.html", result=result, error=error, processing_status="failed")
            
            try:
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                file.save(filepath)
                
                processing_status = "extracting"
                print(f"Processing file: {filename}, size: {file_size} bytes")
                
                # Extract text with better error handling
                text = extract_text(filepath, file_extension)
                if not text or len(text.strip()) < 10:
                    raise ValueError("Could not extract meaningful text from the document. The file might be empty, password-protected, or corrupted.")
                
                processing_status = "analyzing"
                print(f"Text extracted successfully, length: {len(text)} characters")
                
                # Analyze text with timeout handling
                result = analyze_text(text)
                if not result:
                    raise ValueError("Analysis returned empty results.")
                
                processing_status = "completed"
                print("Analysis completed successfully")
                
                # Update session counters
                session['analyses_count'] = session.get('analyses_count', 0) + 1
                
                # Extract document type from the result (first line after # prefix)
                doc_type_line = result.split('\n')[0] if '\n' in result else result
                doc_type = doc_type_line.replace('#', '').strip()
                session['last_document_type'] = doc_type
                
                # Count potential risks (improved heuristic based on RISK ASSESSMENT section)
                risk_section = None
                if "RISK ASSESSMENT:" in result:
                    risk_section_start = result.find("RISK ASSESSMENT:")
                    next_section = result.find("MISSING ELEMENTS:", risk_section_start)
                    if next_section > 0:
                        risk_section = result[risk_section_start:next_section]
                    else:
                        risk_section = result[risk_section_start:]
                
                if risk_section:
                    # Count bullet points in risk section as risks
                    risk_bullets = risk_section.count('-')
                    session['risks_found'] = session.get('risks_found', 0) + max(1, risk_bullets)  # At least 1 risk
                else:
                    # Fallback to keyword counting if section not found
                    risk_keywords = ['risk', 'liability', 'penalty', 'terminate', 'breach', 'violation', 'damages']
                    risks_found = sum(1 for keyword in risk_keywords if keyword in result.lower())
                    session['risks_found'] = session.get('risks_found', 0) + risks_found
                
            except Exception as e:
                print(f"Processing error: {str(e)}")
                error = f"Error processing file: {str(e)}"
                processing_status = "failed"
                
                # Clean up failed file
                try:
                    if os.path.exists(filepath):
                        os.remove(filepath)
                except:
                    pass
    
    return render_template("index.html", result=result, error=error, processing_status=processing_status)

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        # Check if user exists and password matches
        if username in users and users[username]['password'] == password:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('index'))
        else:
            error = "Invalid Credentials. Please try again."
    return render_template("login.html", error=error)

@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        
        # Validation
        if password != confirm_password:
            error = "Passwords do not match."
        elif username in users:
            error = "Username already exists."
        elif len(username) < 3:
            error = "Username must be at least 3 characters long."
        elif len(password) < 6:
            error = "Password must be at least 6 characters long."
        else:
            # Register new user
            users[username] = {
                'password': password,
                'email': email
            }
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('index'))
    
    return render_template("register.html", error=error)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))

# Add this new route for advanced content search
@app.route("/search_content", methods=["POST"])
def search_content():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))
    
    search_term = request.json.get('search_term', '').lower()
    content = request.json.get('content', '')
    
    if not search_term or not content:
        return {"error": "Search term and content are required"}, 400
    
    # Find all occurrences
    lines = content.split('\n')
    results = []
    
    for i, line in enumerate(lines):
        if search_term in line.lower():
            # Get context around the match
            start = max(0, i - 2)
            end = min(len(lines), i + 3)
            context = lines[start:end]
            
            results.append({
                "line_number": i + 1,
                "content": '\n'.join(context),
                "highlighted_line": line
            })
    
    return {"results": results, "total_matches": len(results)}

if __name__ == "__main__":
    app.run(debug=True)
