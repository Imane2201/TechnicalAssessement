# Legal Contracts AI Expert System

A multi-agent AI system built with AGNO framework for comprehensive legal contract analysis using Azure OpenAI and direct PDF reading.

## Overview

This system consists of 3 specialized AI agents working together to analyze legal contracts with direct PDF processing:

1. **Contract Structure Agent** - Analyzes document structure and key components
2. **Legal Framework Agent** - Assesses legal compliance and regulatory requirements  
3. **Negotiating Agent** - Provides strategic negotiation advice and opportunities
4. **Manager Agent** - Coordinates and consolidates inputs from the 3 agents

## Features

- **Multi-Agent Architecture**: 3 specialized agents with distinct roles and expertise
- **Direct PDF Processing**: PyPDF2 integration for efficient document reading
- **Web UI**: Streamlit interface for easy PDF upload and analysis
- **Comprehensive Analysis**: Structure, legal framework, and negotiation strategy
- **Traceable Results**: All agent inputs and recommendations are tracked
- **Azure OpenAI Integration**: Powered by Azure OpenAI services
- **Professional Legal Analysis**: Industry-standard legal terminology and frameworks

## Installation

1. **Clone the repository**:
```bash
git clone <repository-url>
cd TalentPerformerTechAss
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

### 4. Manager Agent (Team Coordinator)
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
│  │              Manager Agent (Coordinator)                    │ │
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
- Drag and drop or click to upload PDF files
- Automatic text extraction with page numbering
- Content preview before analysis

### 🤖 Analysis
- **Full Team Analysis**: Complete coordinated analysis
- **Real-time Progress**: Spinner indicators during processing

### 📊 Results Display
- Clean, formatted analysis results
- Comprehensive legal insights

## Dependencies

- **agno**: Multi-agent framework
- **azure-openai**: Azure OpenAI integration
- **pypdf2**: PDF processing
- **streamlit**: Web interface
- **python-dotenv**: Environment variable management

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For questions or issues, please open an issue in the repository or contact the development team.
