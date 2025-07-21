# Reasoning Operations Research Agent

## 📋 General Description

This repository contains experiments and analysis related to research in **Operations Research III**, specifically focused on automatic resolution of optimization problems using natural language processing (NLP) techniques and constraint programming.

## 🎯 Project Objective

The project seeks to evaluate and compare different approaches for automatic optimization problem resolution:

1. **NLP4LP (Natural Language Processing for Linear Programming)**: Analysis of linear programming problems using natural language processing
2. **Text2Zinc**: Conversion of problem descriptions in text to constraint models in Zinc format
3. **RORA (Results and Optimization Research Analysis)**: Comparative analysis of optimization results

## 📁 Repository Structure

```
experiments/
├── data/                          # Input data
│   ├── nlp4lp/                   # NLP4LP problem dataset
│   │   ├── entry_0.json          # Individual problems (238 files)
│   │   └── ...
│   └── text2zinc/                # Text2Zinc dataset
│       └── train/                # Training data
├── outputs/                       # Experiment results
│   ├── nlp4lp_logs/              # NLP4LP execution logs
│   ├── nlp4lp_results/           # Detailed NLP4LP results
│   ├── text2zinc_results/        # Text2Zinc results
│   ├── RORA_results.csv          # RORA comparative analysis
│   └── text_2_zinc_results_non4lp.csv
├── src/                          # Source code
│   ├── agent/                    # Processing agents
│   │   ├── gates/               # Logic gates
│   │   ├── nodes/               # Processing nodes
│   │   └── tools/               # Auxiliary tools
│   ├── prompts/                 # LLM prompts
│   └── main.py                  # Main entry point
├── playground_v1.ipynb          # Experimentation notebook
├── requirements.txt              # Project dependencies
└── venv/                        # Virtual environment
```

## 🔬 Main Experiments

### 1. NLP4LP (Natural Language Processing for Linear Programming)

**Objective**: Analyze linear programming problems described in natural language and generate automatic solutions.

**Dataset**: 238 optimization problems with:
- Natural language description
- Expected solution
- Problem information (parameters, variables, constraints)
- Automatically generated code

**Results**: 
- Execution logs for each problem
- Detailed results with accuracy metrics
- Performance analysis by problem type

### 2. Text2Zinc

**Objective**: Convert problem descriptions in text to constraint models in Zinc format.

**Dataset**: Training problems organized in subdirectories with:
- `input.json`: Problem description
- `output.json`: Expected solution
- `model.mzn`: Generated Zinc model
- `data.dzn`: Instance data

**Covered domains**:
- Transportation and Logistics
- Scheduling
- Puzzles and Games
- Mathematical Modeling
- Finance and Investment
- Healthcare and Human Systems
- Industrial Engineering and Design

### 3. RORA (Results and Optimization Research Analysis)

**Objective**: Comparative analysis of optimization results between different approaches.

**Analyzed metrics**:
- Optimal Gen vs Optimal Ground Truth
- Accuracy by problem type
- Objective difference
- Comments on solution quality

**Evaluated problem types**:
- Min (Minimization)
- Max (Maximization)
- Pattern (Pattern problems)
- Satisfaction (Satisfaction problems)
- Scheduling (Scheduling)
- Logistic (Logistics)

## 📊 Highlighted Results

### Accuracy by Domain (Text2Zinc)
- **Mathematical Modeling**: 56.36% accuracy
- **Transportation and Logistics**: High performance in routing problems
- **Scheduling**: Good performance in scheduling problems
- **Puzzles and Games**: Excellent performance in satisfaction problems

### RORA Analysis
- **Correctly solved problems**: ~60% of cases
- **Best performances**: Satisfaction and scheduling problems
- **Areas for improvement**: Complex maximization problems

## 🛠️ Installation and Configuration

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone the repository**:
```bash
git clone <repository-url>
cd experiments
```

2. **Create virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

### Main Dependencies
- `openai>=1.0.0`: OpenAI API for natural language processing
- `numpy>=1.24.0`: Numerical computation
- `ortools>=9.7.0`: Google's optimization tools
- `pulp>=2.7.0`: Linear programming
- `cvxpy>=1.4.0`: Convex optimization
- `datasets>=2.15.0`: Dataset handling
- `huggingface_hub>=0.20.0`: Hugging Face models
- `pymzn`: MiniZinc integration

## 🚀 Usage

### Run NLP4LP Experiments
```bash
cd src
python main.py --experiment nlp4lp --dataset data/nlp4lp
```

### Analyze Results
```bash
python playground_v1.ipynb
```

### Run RORA Analysis
```bash
python analyze_rora.py --input outputs/RORA_results.csv
```

## 📈 Metrics and Evaluation

### Accuracy Metrics
- **Accuracy**: Percentage of correctly solved problems
- **Optimal Match**: Comparison between generated solution and ground truth
- **Objective Difference**: Difference in objective value

### Evaluated Problem Types
1. **Minimization**: Optimization problems with minimize objective
2. **Maximization**: Optimization problems with maximize objective
3. **Satisfaction**: Constraint satisfaction problems
4. **Pattern**: Pattern recognition problems

## 🔍 Data Analysis

### NLP4LP Data Structure
Each entry in `data/nlp4lp/entry_X.json` contains:
```json
{
  "description": "Problem description in natural language",
  "solution": "Expected solution in JSON format",
  "problem_info": "Structured problem information",
  "parameters": "Numerical parameters",
  "optimus_code": "Automatically generated code"
}
```

### Text2Zinc Data Structure
Each problem in `data/text2zinc/train/` contains:
- `input.json`: Problem description
- `output.json`: Expected solution
- `model.mzn`: Zinc model
- `data.dzn`: Instance data

## 📝 Research Notes

### Main Findings
1. **Satisfaction problems**: Higher accuracy due to binary nature
2. **Programming problems**: Good performance in linear constraints
3. **Complex problems**: Difficulty with non-linear constraints
4. **Objective optimization**: Better performance in minimization than maximization

### Identified Limitations
- Dependency on problem description quality
- Difficulty with complex constraints
- Performance variability by domain
- Need for manual validation in critical cases

## 🤝 Contributions

To contribute to the project:

1. Fork the repository
2. Create a branch for your feature (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## 📄 License

This project is part of academic research in Operations Research III.

## 👥 Authors

- **Principal Researcher**: [Name]
- **Institution**: [University]
- **Course**: Operations Research III

## 📞 Contact

For questions or collaborations, contact:
- Email: [email]
- Department: [Department]

---

*This repository is part of a research project in automatic optimization using natural language processing techniques.* # rora
