# Legal Contracts AI Expert - Multi-Agent System with Azure OpenAI

from agno.agent import Agent
from agno.team import Team
from agno.models.azure import AzureOpenAI
from agno.tools.reasoning import ReasoningTools
from agno.tools import tool
from dotenv import load_dotenv
from textwrap import dedent
import PyPDF2
import tempfile
import os
import io
import sys
from typing import Dict, Any

# Load environment variables
load_dotenv()

# Configure Azure OpenAI
def get_azure_model():
    return AzureOpenAI(
        id=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
    )

# Global variable to store PDF content
pdf_content_global = ""

@tool(
    name="read_pdf_content",
    description="Extract text content from the uploaded PDF file",
    show_result=True
)
def read_pdf_content(pdf_path: str = "") -> Dict[str, Any]:
    """
    Extract text content from the uploaded PDF file.
    
    Args:
        pdf_path: Path to PDF file (optional, uses global content if empty)
        
    Returns:
        Dict containing success status, content, and metadata
    """
    global pdf_content_global
    
    if pdf_content_global:
        return {
            "success": True,
            "content": pdf_content_global,
            "source": "uploaded_file",
            "pages": pdf_content_global.count("--- Page")
        }
    
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text_content = ""
            
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text_content += f"\n--- Page {page_num + 1} ---\n"
                text_content += page.extract_text()
            
            return {
                "success": True,
                "content": text_content,
                "pages": len(pdf_reader.pages),
                "file_path": pdf_path
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "file_path": pdf_path
        }

# Function to create agents with PDF content
def create_agents_with_pdf(pdf_content: str):
    """Create agents with access to the uploaded PDF content"""
    global pdf_content_global
    pdf_content_global = pdf_content
    
    # 1. Contract Structure Agent
    contract_structure_agent = Agent(
        name="Structure Agent",
        role="Contract Structuring Expert",
        model=get_azure_model(),
        tools=[ReasoningTools(), read_pdf_content],
        markdown=True,
        instructions=dedent("""
        You are a Contract Structuring Expert whose role is to evaluate the structure of a contract and suggest improvements or build a proper structure from scratch.
        
        Use the read_pdf_content tool to access the contract text.
        Analyze the contract for clarity, completeness, and legal appropriateness.
        Identify missing or unclear sections.
        If structure is missing, suggest a full structure using standard section headers (e.g., "Definitions, Terms, Obligations, Termination, Governing Law").
        Avoid legal interpretation - focus only on organization, clarity, and logical flow.
        Be concise but clear in your analysis.
        Output a markdown-style structure if creating a new structure, or bullet-pointed comments if evaluating an existing one.
        """),
        show_tool_calls=False
    )

    # 2. Legal Framework Agent
    legal_framework_agent = Agent(
        name="Legal Agent",
        role="Legal issue Analyst",
        model=get_azure_model(),
        tools=[ReasoningTools(), read_pdf_content],
        markdown=True,
        instructions=dedent("""
        You are a Legal Framework Analyst tasked with identifying legal issues, risks, and key legal principles in the uploaded contract.
        
        Use the read_pdf_content tool to access the full contract text. For every legal issue or observation, you MUST:
        - Quote the exact clause, sentence, or paragraph from the contract that your point is based on.
        - Start a new line with 'Issue:' followed by a short, clear explanation of the legal concern or principle.
        - Clearly refer to the section title, heading, or paragraph number if available.
        DO NOT make any legal assessment or comment unless it is directly supported by a quote from the contract.
        
        Your task:
        - Identify the legal domain of the contract (e.g., commercial law, employment, NDA, etc.)
        - Determine the likely jurisdiction or applicable law
        """),
        show_tool_calls=False
    )

    # 3. Negotiating Agent
    negotiating_agent = Agent(
        name="Negotiation Agent",
        role="Contract Negotiation Strategist",
        model=get_azure_model(),
        tools=[ReasoningTools(), read_pdf_content],
        markdown=True,
        instructions=dedent("""
        You are a Contract Negotiation Strategist.
        
        Use the read_pdf_content tool to access the contract text.
        Your job is to identify parts of a contract that are commonly negotiable or potentially unbalanced. You MUST:
        
        - Always quote the exact paragraph or clause you're referring to.
        - Clearly explain why it may be negotiable or needs adjustment.
        - Suggest a counter-offer or alternative phrasing.
        
        Structure your analysis like this:
        1. **Quoted clause** (exact text from contract)
        2. **Why it is negotiable or problematic**
        3. **Example strategy or counter-suggestion**
        """),
        show_tool_calls=False
    )

    # Create the coordinate team with the 3 agents
    legal_contracts_team = Team(
        name="Legal Contracts Expert Team",
        mode="coordinate",
        members=[
            contract_structure_agent,
            legal_framework_agent,
            negotiating_agent
        ],
        model=get_azure_model(),
        show_members_responses=True,
        markdown=True,
        description="A coordinated team of legal contract experts that provides comprehensive contract analysis",
        success_criteria=dedent("""
        A well-organized and traceable summary of the contract that includes:
        - Legal context highlighting potential legal issues with quoted contract text as evidence
        - Structural review with clarity and formatting suggestions
        - Negotiation strategies directly tied to specific paragraphs or clauses
        """),
        instructions=dedent("""
        You are the lead summarizer. You must combine input from:
        1. Legal Agent
        2. Structure Agent
        3. Negotiation Agent
        
        Synthesize all team member outputs into a cohesive, comprehensive response.
        Ensure the final response is well-structured and addresses all aspects of the contract.
        Coordinate the team to avoid redundancy while ensuring complete coverage of the analysis.
        Provide executive summary with key findings and actionable recommendations.
        """),
        add_datetime_to_instructions=True,
        enable_agentic_context=True,
        share_member_interactions=True
    )
    
    return contract_structure_agent, legal_framework_agent, negotiating_agent, legal_contracts_team

# PDF Reading Function for direct use
def read_pdf_content_direct(pdf_path):
    """Extract text content from a PDF file"""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text_content = ""
            
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text_content += f"\n--- Page {page_num + 1} ---\n"
                text_content += page.extract_text()
            
            return text_content
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

# Function to analyze contract with PDF content
def analyze_contract(pdf_path):
    """Analyze a contract using the multi-agent system"""
    print(f"Reading PDF: {pdf_path}")
    pdf_content = read_pdf_content_direct(pdf_path)
    
    if pdf_content.startswith("Error"):
        print(f"Error: {pdf_content}")
        return
    
    print("PDF content loaded successfully!")
    print(f"Content length: {len(pdf_content)} characters")
    
    # Create agents with PDF content
    contract_structure_agent, legal_framework_agent, negotiating_agent, legal_contracts_team = create_agents_with_pdf(pdf_content)
    
    # Test the coordinated legal contracts team
    print("\n" + "="*60)
    print("LEGAL CONTRACTS AI EXPERT - DEMO")
    print("="*60)

    # Demo: Comprehensive contract analysis
    print("\n📋 DEMO: Services Agreement Analysis")
    print("="*50)
    
    # Run the team analysis using print_response
    analysis_request = "Please provide a comprehensive analysis of the contract. Include structural analysis, legal compliance assessment, and negotiation opportunities. Provide specific recommendations and action items."
    
    # Use print_response method and capture the output
    old_stdout = sys.stdout
    new_stdout = io.StringIO()
    sys.stdout = new_stdout
    
    try:
        # Call print_response which will print to our captured stdout
        legal_contracts_team.print_response(analysis_request)
        
        # Get the captured output
        result = new_stdout.getvalue()
        
        if result.strip():
            return result
        else:
            return "No response received from the team."
            
    finally:
        # Restore stdout
        sys.stdout = old_stdout

# Main execution
if __name__ == "__main__":
    pdf_path = "ServicesAgreementSample.pdf"
    result = analyze_contract(pdf_path)
    print("\n" + "="*60)
    print("ANALYSIS RESULT:")
    print("="*60)
    print(result)
