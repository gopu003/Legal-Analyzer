import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze_text(text):
    # First, determine the document type based on content
    document_type = determine_document_type(text)
    
    # Create a document-specific prompt
    prompt = create_document_specific_prompt(text, document_type)
    
    # Get the analysis from the AI
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama3-70b-8192"
    )
    
    # Format the response for better readability
    formatted_response = format_response(response.choices[0].message.content, document_type)
    
    return formatted_response


def determine_document_type(text):
    """Determine the type of legal document based on its content."""
    text_lower = text.lower()
    
    # Check for common document types
    if "non-disclosure" in text_lower or "confidentiality" in text_lower or "nda" in text_lower:
        return "Non-Disclosure Agreement"
    elif "employment" in text_lower and ("agreement" in text_lower or "contract" in text_lower):
        return "Employment Agreement"
    elif "service" in text_lower and "agreement" in text_lower:
        return "Service Agreement"
    elif "lease" in text_lower or "rental" in text_lower:
        return "Lease Agreement"
    elif "purchase" in text_lower and "agreement" in text_lower:
        return "Purchase Agreement"
    elif "terms" in text_lower and "conditions" in text_lower:
        return "Terms and Conditions"
    elif "privacy" in text_lower and "policy" in text_lower:
        return "Privacy Policy"
    else:
        return "Legal Document"


def create_document_specific_prompt(text, document_type):
    """Create a prompt tailored to the specific document type."""
    
    # Base prompt structure
    base_prompt = f"""You are an expert legal assistant specializing in {document_type} analysis. 

Analyze the following {document_type.lower()}:

{text}

"""
    
    # Add document-specific questions
    if document_type == "Non-Disclosure Agreement":
        specific_questions = """
Please provide a detailed analysis including:

1. DOCUMENT OVERVIEW:
   - Parties involved and their roles (disclosing/receiving)
   - Duration of confidentiality obligations
   - Scope of confidential information

2. RISK ASSESSMENT:
   - Identify any risky or unclear terms
   - Evaluate the definition of confidential information
   - Assess exceptions to confidentiality
   - Analyze remedies for breach

3. MISSING ELEMENTS:
   - Identify any standard clauses missing from this NDA
   - Suggest additional protections that should be included

4. PLAIN LANGUAGE SUMMARY:
   - Provide a clear, non-legal explanation of key obligations

5. IMPROVEMENT RECOMMENDATIONS:
   - Specific suggestions to strengthen the agreement
   - Language clarifications needed
"""
    elif document_type == "Employment Agreement":
        specific_questions = """
Please provide a detailed analysis including:

1. DOCUMENT OVERVIEW:
   - Employment terms (position, compensation, benefits)
   - Duration and termination conditions
   - Key responsibilities

2. RISK ASSESSMENT:
   - Identify any risky or unclear terms
   - Evaluate non-compete and non-solicitation provisions
   - Assess intellectual property rights
   - Analyze termination clauses

3. MISSING ELEMENTS:
   - Identify any standard clauses missing from this agreement
   - Suggest additional protections that should be included

4. PLAIN LANGUAGE SUMMARY:
   - Provide a clear, non-legal explanation of key obligations

5. IMPROVEMENT RECOMMENDATIONS:
   - Specific suggestions to strengthen the agreement
   - Language clarifications needed
"""
    else:
        # Generic analysis for other document types
        specific_questions = """
Please provide a detailed analysis including:

1. DOCUMENT OVERVIEW:
   - Parties involved and their roles
   - Key terms and obligations
   - Duration and termination conditions

2. RISK ASSESSMENT:
   - Identify any risky or unclear terms
   - Evaluate liability and indemnification provisions
   - Assess dispute resolution mechanisms

3. MISSING ELEMENTS:
   - Identify any standard clauses missing from this document
   - Suggest additional protections that should be included

4. PLAIN LANGUAGE SUMMARY:
   - Provide a clear, non-legal explanation of key obligations

5. IMPROVEMENT RECOMMENDATIONS:
   - Specific suggestions to strengthen the agreement
   - Language clarifications needed
"""
    
    return base_prompt + specific_questions


def format_response(response_text, document_type):
    """Format the AI response for better readability."""
    
    # Add a header with the document type
    formatted_text = f"# {document_type} Analysis\n\n"
    
    # Add the response text
    formatted_text += response_text
    
    # Add a footer with disclaimer
    formatted_text += "\n\n---\n*Disclaimer: This analysis is provided for informational purposes only and does not constitute legal advice. Please consult with a qualified attorney for specific legal guidance.*"
    
    return formatted_text
