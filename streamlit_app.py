import streamlit as st
import PyPDF2
import tempfile
import os
import re
from ai_legal_agent import create_agents_with_pdf

# Page configuration
st.set_page_config(
    page_title="Legal Contracts AI Expert",
    page_icon="⚖️",
    layout="wide"
)

def read_pdf_content(uploaded_file):
    """Extract text content from an uploaded PDF file"""
    try:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name
        
        # Read the PDF
        with open(tmp_file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text_content = ""
            
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text_content += f"\n--- Page {page_num + 1} ---\n"
                text_content += page.extract_text()
        
        # Clean up temporary file
        os.unlink(tmp_file_path)
        
        return {
            "success": True,
            "content": text_content,
            "pages": len(pdf_reader.pages),
            "filename": uploaded_file.name
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "filename": uploaded_file.name
        }

def clean_ansi_codes(text):
    """Remove ANSI escape codes from text"""
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

def analyze_contract_with_team(pdf_content):
    """Run the legal contracts team analysis"""
    try:
        print("Creating AI agents...")
        print(f"PDF content length: {len(pdf_content)} characters")
        print(f"PDF content preview: {pdf_content[:200]}...")
        
        # Create agents with PDF content
        contract_structure_agent, legal_framework_agent, negotiating_agent, legal_contracts_team = create_agents_with_pdf(pdf_content)
        
        print("Starting contract analysis...")
        # Run the team analysis and get response directly
        with st.spinner("Analyzing contract..."):
            response = legal_contracts_team.run(
                f"""Please analyze the uploaded contract comprehensively. 

IMPORTANT: You MUST use the read_pdf_content tool to access the contract text before providing any analysis.

After reading the contract, provide a comprehensive analysis including:

1. **Executive Summary**: Contract type, key parties, overall assessment
2. **Structural Analysis**: Document organization, missing sections, recommendations
3. **Legal Risk Assessment**: Key legal issues with specific quotes from the contract
4. **Negotiation Strategy**: High-priority negotiation points with specific clauses
5. **Action Items**: Specific recommendations and next steps

Ensure all analysis is based on actual contract content with specific quotes and references."""
            )
        
        print("Analysis completed!")
        print(f"Response type: {type(response)}")
        if hasattr(response, 'content'):
            print(f"Response content length: {len(response.content)}")
            print(f"Response preview: {response.content[:200]}...")
        
        # Clean the response and display it
        if response and hasattr(response, 'content'):
            clean_response = clean_ansi_codes(response.content)
            st.markdown(clean_response)
            return clean_response
        else:
            error_msg = "No response received from the team."
            st.error(error_msg)
            return error_msg
            
    except Exception as e:
        error_msg = f"Error during analysis: {str(e)}"
        print(f"Error: {error_msg}")
        st.error(error_msg)
        return error_msg

def main():
    # Header
    st.title("Legal Contracts AI Expert")
    
    # Sidebar
    with st.sidebar:
        st.header("Upload")
        uploaded_file = st.file_uploader(
            "Upload PDF contract",
            type=['pdf']
        )
    
    # Main content
    if uploaded_file is not None:
        # Read PDF content
        with st.spinner("Reading PDF..."):
            pdf_result = read_pdf_content(uploaded_file)
        
        if pdf_result["success"]:
            st.success(f"PDF loaded: {pdf_result['pages']} pages")
            
            # Analysis button
            if st.button("Analyze Contract", type="primary"):
                st.header("Analysis Results")
                result = analyze_contract_with_team(pdf_result["content"])
        else:
            st.error(f"Error reading PDF: {pdf_result['error']}")
    else:
        st.info("Upload a PDF contract to begin analysis.")

if __name__ == "__main__":
    main() 