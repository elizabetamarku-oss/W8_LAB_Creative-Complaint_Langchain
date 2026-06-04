# 🙃 Downside-Up Complaint Bureau
### NormalObjects — Creative Complaint Handler (LangChain Lab)
 
A LangChain agent that handles complaints about inconsistencies in the Normal Objects universe using flexible, creative tool-calling. Built with the modern **LCEL (LangChain Expression Language)** API (LangChain 0.3+).
 
---
 
## Files
 
| File | Description |
|------|-------------|
| `normalobjects_langchain.ipynb` | Main notebook — all 5 steps in one file |
| `lab_summary.md` | One-paragraph reflection (see submission guidelines) |
| `README.md` | This file |
 
---
 
## Requirements
 
- Python 3.9+
- An OpenAI API key (`gpt-4o-mini` access)
---
 
## Setup & Run
 
### Google Colab (recommended)
1. Upload `normalobjects_langchain.ipynb` via **File → Upload notebook**
2. Run the install cell: `!pip install -q langchain langchain-openai`
3. Paste your OpenAI key into the API key cell
4. Run all cells top to bottom (**Runtime → Run all**)
### Local Jupyter
```bash
pip install langchain langchain-openai notebook
jupyter notebook normalobjects_langchain.ipynb
```
 
Then open the notebook and paste your API key in Step 1.
 
---
 
## How It Works
 
The agent uses `llm.bind_tools()` (LangChain 0.3+ LCEL style) instead of the deprecated `AgentExecutor`. It loops until the LLM stops calling tools and returns a final response.
 
**Four creative tools:**
 
| Tool | Purpose |
|------|---------|
| `consult_demogorgon` | Creature perspective on Upside Down inconsistencies |
| `check_hawkins_records` | Historical patterns and documented evidence |
| `cast_interdimensional_spell` | Imaginative magical fixes |
| `gather_party_wisdom` | Grounded insights from the D&D party |
 
The agent decides which tools to call and in what order — no fixed sequence.
 
---
 
## Note on LangChain Versions
 
The lab handout uses `AgentExecutor` and `create_openai_tools_agent`, which were **removed in LangChain 0.3**. This repo uses the current API:
 
```python
# Old (broken on 0.3+)
from langchain.agents import AgentExecutor, create_openai_tools_agent
 
# New (works on 0.3+)
llm_with_tools = llm.bind_tools(tools)   # replaces create_openai_tools_agent
# + a manual loop replaces AgentExecutor
```
 
---
 
## Lab Context
 
This is **Lab 1** of the NormalObjects project.  
Lab 2 implements the same complaint handler using **LangGraph** with strict, ordered workflows — allowing a direct comparison of freeform vs structured agent approaches.
