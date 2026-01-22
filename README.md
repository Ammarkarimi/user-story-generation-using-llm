# Lab Experiment: Requirement Engineering Assistant

## 📋 Overview

This project implements an **end-to-end AI-powered Requirement Engineering Assistant** that automates the requirements engineering (RE) process using Large Language Models (LLMs). The system guides users through stakeholder analysis, elicitation techniques, user story generation, validation, and prioritization.

## 🎯 Purpose

The Lab Experiment aims to:
- **Automate stakeholder identification** from problem statements
- **Recommend elicitation techniques** tailored to each stakeholder
- **Generate comprehensive user stories** with success and failure scenarios
- **Validate user stories** against quality frameworks (INVEST, Semantic, Syntactic, Pragmatic, Stakeholder-specific criteria)
- **Prioritize user stories** based on business value and dependencies
- **Track experiments** using LLMs (Groq API) and evaluate RE tool effectiveness

## 📁 Project Structure

```
Lab_Experiment/
├── app.py                          # Streamlit web application
├── main.py                         # Core RE assistant functions
├── db.py                          # Database utilities (PostgreSQL)
├── requirements.txt               # Python dependencies
├── README.md                      # This file
│
├── Prompts/                       # LLM prompt templates
│   ├── StakeholderCriteriaPrompt.py      # Stakeholder representation evaluation
│   ├── InvestCriteriaPrompt.py           # INVEST framework validation
│   ├── SemanticCriteriaPrompt.py         # Semantic quality assessment
│   ├── SyntacticCriteriaPrompt.py        # Syntactic quality assessment
│   ├── PragmaticCriteriaPrompt.py        # Pragmatic quality assessment
│   └── __init__.py
│
├── EvaluationPipeline/            # Experiment evaluation notebooks
│   ├── pipeline.ipynb             # Main evaluation pipeline
│   ├── pipeline_ollama.ipynb      # Ollama-based evaluation
│   ├── insights.ipynb             # Analysis and insights
│   ├── intermediate_results.csv   # Pipeline execution results
│   ├── progress.txt               # Progress tracking
│   └── __init__.py
│
├── documents/                     # Reference documents and datasets
│   ├── LIC_Problem_Statement.pdf
│   ├── MentCare_Problem_Statement.pdf
│   ├── Baseline_for_LIC.txt            # Manual RE baseline for LIC
│   ├── Baseline_for_LIC_Stakeholder.txt
│   ├── Baseline_for_MentCare.txt       # Manual RE baseline for MentCare
│   ├── Baseline_for_MentCare_Stakeholder.txt
│   ├── Generate_Stakeholder_for_US.csv
│   ├── Generate_User_Stories_Database_for_US.csv
│   ├── combined_user_stakeholder_userstories.csv
│   ├── Manual_and_Tool_together.csv    # Comparison data
│   ├── Students_Feedbacks_AI_for_RE.xlsx     # Student feedback on AI approach
│   └── Students_Feedbacks_LLM_for_RE.xlsx    # Student feedback on LLM approach
│
├── OutputDocuments/               # Generated outputs
│   ├── Students_Feedbacks_AI_for_RE_with_Emotions_Output.csv
│   └── Students_Feedbacks_LLM_for_RE_with_Emotions_Output.csv
│
└── __pycache__/
```

## 🚀 Key Features

### 1. **Stakeholder Analysis** (`main.py::findStakeholder()`)
- Identifies stakeholders from problem statements
- Categorizes users as primary (direct) or secondary (indirect)
- Lists stakeholder roles, expectations, and concerns
- Identifies potential conflicts and resolutions

### 2. **Elicitation Techniques Generator** (`main.py::generateElicitationTechniques()`)
- Recommends appropriate elicitation techniques (interviews, surveys, workshops, etc.)
- Provides justifications for each recommendation
- Tailored to specific stakeholder groups

### 3. **User Story Generation** (`main.py::generateUserStories()`)
- Creates detailed user stories following the "Front & Back of Card" approach
- Includes success scenarios and failure scenarios
- Covers system failures, user input errors, hardware issues, and security concerns
- Generates 15+ stories per user type

### 4. **Validation** (`main.py::validateUserStories()`)
- **INVEST Framework** (`InvestCriteriaPrompt.py`): Validates user stories against Independent, Negotiable, Valuable, Estimable, Small, and Testable criteria


### 5. **Prioritization** (`main.py::Prioritize()`)
- Ranks user stories by business value
- Considers dependencies and effort
- Identifies epic relationships

### 6. **Web Interface** (`app.py`)
- Streamlit-based UI for the RE assistant
- Student ID and model selection (Groq API integration)
- Step-by-step workflow through RE process
- Real-time LLM response processing
- Event logging to PostgreSQL database

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- PostgreSQL database (optional, for logging)
- Groq API key (for LLM access)

### Installation Steps

```bash
# 1. Clone/navigate to the project
cd Lab_Experiment

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up environment variables
# Create a .env file with:
GROQ_API_KEY=your_groq_api_key_here

# 4. Configure Streamlit secrets (for web app)
# Create .streamlit/secrets.toml with database credentials:
user = "postgres_user"
password = "postgres_password"
host = "localhost"
port = 5432
dbname = "requirement_engineering"
```

## 📦 Dependencies

| Package | Purpose |
|---------|---------|
| `langchain` | LLM orchestration framework |
| `langchain-groq` | Groq LLM provider integration |
| `python-dotenv` | Environment variable management |
| `streamlit` | Web application framework |
| `sqlalchemy` | Database ORM |
| `psycopg2-binary` | PostgreSQL adapter |

## 🏃 Running the Application

### Option 1: Streamlit Web App
```bash
streamlit run app.py
```
Access the application at `http://localhost:8501`

### Option 2: Command-line Processing
```bash
python main.py
```

### Option 3: Evaluation Pipeline
```bash
# Run Jupyter notebooks in EvaluationPipeline/
jupyter notebook EvaluationPipeline/pipeline.ipynb
```

## 📊 Workflow

1. **Problem Input** → Enter problem statement
2. **Stakeholder Identification** → Find all relevant stakeholders
3. **Elicitation Planning** → Select techniques for each stakeholder
4. **User Story Generation** → Create detailed user stories
5. **Validation** → Evaluate against multiple criteria
6. **Prioritization** → Rank stories by business value
7. **Epic Conflict Detection** → Identify related stories and dependencies

## 🧪 Evaluation & Experiments

### Baseline Comparison
The project includes manual RE baselines for two case studies:
- **LIC**: LIC Market‐Driven System
- **MentCare**: Mental healthcare management system

### Evaluation Metrics
- User story quality scores (INVEST, Semantic, Syntactic, Pragmatic)
- Stakeholder representation coverage
- Comparison with manual RE approach
- Student feedback on AI vs LLM approaches

### Experiment Tracking
- Student feedback data with emotion analysis
- Intermediate results stored in CSV format
- Progress tracking for pipeline execution

## 📝 Example Usage

```python
from main import findStakeholder, generateElicitationTechniques, generateUserStories

# Define your problem
problem = "Develop a subway ticket distribution system..."

# Get API key
api_key = "your_groq_api_key"
model = "mixtral-8x7b-32768"

# Step 1: Find stakeholders
stakeholders = findStakeholder(problem, api_key, model)

# Step 2: Generate elicitation techniques
techniques = generateElicitationTechniques(stakeholders, api_key, model)

# Step 3: Create user stories
stories = generateUserStories(stakeholders, api_key, model)
```

## 🗄️ Database Schema

The application logs user interactions to PostgreSQL:

```sql
CREATE TABLE logs (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255),
    student_id VARCHAR(255),
    model_name VARCHAR(255),
    action VARCHAR(255),
    details TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 📋 Output Formats

### User Stories
- Format: "As a [user], I want to [action], so that [benefit]"
- Includes acceptance criteria
- Success scenarios
- Failure scenarios with error messages

## 🔬 Research Context

This lab experiment was designed to evaluate:
- **Effectiveness of LLM-based RE assistance** compared to manual approaches
- **User satisfaction** with AI-generated requirements
- **Quality metrics** of manually-created user stories after getting assistance by AI vs manually-created user stories before getting assistance from AI.


## 📚 References

- INVEST Framework for User Story Quality
- Requirement Engineering Best Practices
- LLM Prompting Strategies for Software Engineering
- Stakeholder-Driven Requirements Elicitation

## 📧 Contact & Support

Mail Ids: 
1. 202411080@dau.ac.in
2. saurabh_t@dau.ac.in

---

**Last Updated**: January 2026
**Status**: Active Research & Development

