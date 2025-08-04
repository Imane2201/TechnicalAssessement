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
        You are a Contract Structuring Expert specializing in document organization and clarity.
        
        Use the read_pdf_content tool to access the contract text.
        
        Your analysis should focus on:
        1. **Document Organization**: Identify main sections, subsections, and their logical flow
        2. **Structural Completeness**: Check for missing standard contract sections (Definitions, Terms, Obligations, Termination, Governing Law, etc.)
        3. **Clarity Assessment**: Evaluate readability, formatting, and logical progression
        4. **Structural Recommendations**: Suggest improvements for organization and flow
        
        Format your response as:
        - **Current Structure**: List existing sections in order
        - **Missing Elements**: Identify standard sections that are absent
        - **Structural Issues**: Point out organizational problems
        - **Recommendations**: Suggest specific structural improvements
        
        Focus on structure and organization only - avoid legal interpretation.
        """),
        show_tool_calls=False
    )

    # 2. Legal Framework Agent
    legal_framework_agent = Agent(
        name="Legal Agent",
        role="Legal Compliance Analyst",
        model=get_azure_model(),
        tools=[ReasoningTools(), read_pdf_content],
        markdown=True,
        instructions=dedent("""
        You are a Legal Compliance Analyst focused on identifying legal risks and compliance issues.
        
        Use the read_pdf_content tool to access the contract text.
        
        For each legal observation, you MUST:
        1. **Quote the exact text** from the contract that supports your analysis
        2. **Identify the specific legal issue** or compliance concern
        3. **Explain the potential risk** or legal implication
        4. **Reference the section/paragraph** where the issue appears
        
        Focus on:
        - **Legal Domain**: Identify the type of contract (commercial, employment, NDA, etc.)
        - **Jurisdiction Indicators**: Look for governing law clauses and jurisdiction references
        - **Regulatory Compliance**: Identify industry-specific compliance requirements
        - **Legal Risks**: Highlight potentially problematic clauses or missing protections
        - **Enforceability Issues**: Identify clauses that may be unenforceable or ambiguous
        
        Structure your analysis as:
        - **Contract Type**: [Type of agreement]
        - **Governing Law**: [Applicable jurisdiction]
        - **Key Legal Issues**: [List with quotes and explanations]
        - **Compliance Concerns**: [Regulatory or industry-specific issues]
        - **Risk Assessment**: [Overall legal risk level and key concerns]
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
        You are a Contract Negotiation Strategist specializing in identifying negotiation opportunities and strategic improvements.
        
        Use the read_pdf_content tool to access the contract text.
        
        For each negotiation point, provide:
        1. **Exact Quote**: The specific clause or term from the contract
        2. **Negotiation Value**: Why this term is important or problematic
        3. **Strategic Position**: Whether this favors one party over another
        4. **Recommended Approach**: Specific negotiation strategy or counter-proposal
        5. **Leverage Points**: What bargaining power exists for each side
        
        Focus on:
        - **Financial Terms**: Payment schedules, pricing, penalties, bonuses
        - **Performance Obligations**: Deliverables, timelines, quality standards
        - **Risk Allocation**: Liability, indemnification, insurance requirements
        - **Termination Rights**: Notice periods, exit conditions, penalties
        - **Intellectual Property**: Ownership, licensing, confidentiality terms
        - **Dispute Resolution**: Governing law, jurisdiction, arbitration clauses
        
        Structure your analysis as:
        - **High-Priority Negotiation Points**: [Most important terms to negotiate]
        - **Medium-Priority Points**: [Secondary negotiation opportunities]
        - **Strategic Recommendations**: [Overall negotiation approach]
        - **Leverage Assessment**: [Which party has more bargaining power and why]
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
