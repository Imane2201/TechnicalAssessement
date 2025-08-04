# Legal Contracts AI Expert System

A multi-agent AI system built with AGNO framework for comprehensive legal contract analysis using Azure OpenAI and direct PDF reading.

## Overview

This system consists of 3 specialized AI agents working together to analyze legal contracts with direct PDF processing:

1. **Contract Structure Agent** - Analyzes document structure and key components
2. **Legal Framework Agent** - Assesses legal compliance and regulatory requirements  
3. **Negotiating Agent** - Provides strategic negotiation advice and opportunities
4. **Team Coordinator** - Combines and synthesizes inputs from all agents

## Features

- **Multi-Agent Architecture**: 3 specialized agents with distinct roles and expertise
- **Direct PDF Processing**: PyPDF2 integration for efficient document reading
- **Minimalist Web UI**: Clean Streamlit interface for easy PDF upload and analysis
- **Comprehensive Analysis**: Structure, legal framework, and negotiation strategy
- **Azure OpenAI Integration**: Powered by Azure OpenAI services
- **Professional Legal Analysis**: Industry-standard legal terminology and frameworks

## Installation

1. **Clone the repository**:
```bash
git clone https://github.com/Imane2201/TechnicalAssessement.git
cd TechnicalAssessement
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**:
Create a `.env` file with your Azure OpenAI credentials:
```env
AZURE_OPENAI_API_KEY=your_azure_openai_api_key_here
AZURE_OPENAI_ENDPOINT=your_azure_openai_endpoint_here
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment_name_here
```

## Usage

### Web Interface (Recommended)

1. **Start the Streamlit app**:
```bash
streamlit run streamlit_app.py
```

2. **Open your browser** and go to `http://localhost:8501`

3. **Upload a PDF contract** and click "Analyze Contract"

### Command Line Usage

```python
from ai_legal_agent import analyze_contract

# Analyze a contract comprehensively
analyze_contract("ServicesAgreementSample.pdf")
```

### Running the Demo

```bash
python ai_legal_agent.py
```

## Agent Descriptions

### 1. Contract Structure Agent
- **Role**: Analyzes document structure and organization
- **Expertise**: Contract components, sections, clauses, parties
- **Output**: Structural mapping, hierarchy analysis, missing sections

### 2. Legal Framework Agent  
- **Role**: Assesses legal compliance and regulatory requirements
- **Expertise**: Contract law, commercial law, regulatory compliance
- **Output**: Legal risk assessment, compliance recommendations, enforceability analysis

### 3. Negotiating Agent
- **Role**: Provides strategic negotiation advice
- **Expertise**: Commercial negotiations, deal structuring, risk allocation
- **Output**: Negotiation strategies, leverage points, term improvements

### 4. Team Coordinator
- **Role**: Coordinates and consolidates inputs from the 3 agents
- **Expertise**: Project management, legal consulting, executive communication
- **Output**: Comprehensive reports, executive summaries, action items

## System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   PDF Document  │───▶│  PyPDF2 Reader  │───▶│  Text Content   │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Legal Contracts Team                        │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐               │
│  │  Structure  │ │   Legal     │ │ Negotiation │               │
│  │   Agent     │ │ Framework   │ │    Agent    │               │
│  │             │ │   Agent     │ │             │               │
│  └─────────────┘ └─────────────┘ └─────────────┘               │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │              Team Coordinator                               │ │
│  └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Comprehensive Analysis                       │
│  • Structural Analysis                                          │
│  • Legal Compliance Assessment                                  │
│  • Negotiation Strategy                                         │
└─────────────────────────────────────────────────────────────────┘
```

## Web Interface Features

### 📄 PDF Upload
- Simple drag and drop or click to upload PDF files
- Automatic text extraction with page numbering
- Clean success/error messaging

### 🤖 Analysis
- **Single Analysis Type**: Complete coordinated analysis from all agents
- **Real-time Progress**: Spinner indicators during processing
- **Clean Output**: Formatted results without terminal artifacts

### 📊 Results Display
- Clean, formatted analysis results
- Comprehensive legal insights
- Direct display without tabs or complex UI

## Technical Implementation

### PDF Processing
- Uses PyPDF2 for text extraction
- Handles temporary file management
- Provides page-by-page content with numbering

### Response Handling
- Captures AI responses without ANSI escape codes
- Cleans terminal formatting for web display
- Provides error handling and user feedback

### Agent Coordination
- Uses AGNO framework for multi-agent orchestration
- Coordinates specialized agents with shared PDF access
- Synthesizes comprehensive analysis results

## Dependencies

- **agno**: Multi-agent framework
- **azure-openai**: Azure OpenAI integration
- **pypdf2**: PDF processing
- **streamlit**: Web interface
- **python-dotenv**: Environment variable management


---

**Imane Labbassi**  
*Building intelligent multi-agent systems with Agno*
