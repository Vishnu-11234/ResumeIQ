\# ResumeIQ – AI-Powered Student Career Intelligence Platform



ResumeIQ is an AI-powered career intelligence platform designed to help students understand their career readiness, analyze resumes, identify skill gaps, and discover relevant job opportunities.



The platform combines machine learning, natural language processing, and modern web technologies to provide personalized career insights.



\## 🎯 Problem Statement



Students often struggle to understand how well their resumes align with job requirements, which skills they lack, and how to prepare for their target roles.



ResumeIQ aims to address these challenges through automated resume analysis, job matching, skill gap identification, and career preparation tools.



\## 🚀 Key Features



\- Resume information extraction using a fine-tuned language model.

\- Job description information extraction.

\- Resume–job matching based on skills, experience, and semantic similarity.

\- Job recommendation and ranking.

\- ATS compatibility analysis.

\- Skill gap analysis.

\- Resume improvement assistance.

\- Interview preparation.



\*Feature implementation is ongoing. Not every listed feature is currently operational.\*



\## 🛠️ Technology Stack



| Component | Technologies |

|---|---|

| Frontend | React, JavaScript, Vite |

| Backend | Python, FastAPI |

| Machine Learning | PyTorch, Scikit-learn |

| NLP and LLM | Transformers, PEFT, QLoRA |

| Model | Qwen2.5-3B-Instruct |

| Data Processing | Python |



\## 🏗️ Project Architecture



```text

ResumeIQ/

│

├── backend/

│   ├── app/

│   │   ├── api/

│   │   ├── core/

│   │   ├── models/

│   │   ├── repositories/

│   │   ├── schemas/

│   │   ├── services/

│   │   └── main.py

│   └── tests/

│

├── contracts/

│

├── docs/

│

├── frontend/

│   └── src/

│       ├── api/

│       ├── components/

│       ├── pages/

│       └── styles/

│

├── ml\_engine/

│   ├── data/

│   ├── notebooks/

│   ├── src/

│   │   ├── extraction/

│   │   ├── jd\_extraction/

│   │   ├── llm/

│   │   ├── matching/

│   │   ├── preprocessing/

│   │   ├── ats/

│   │   ├── analysis/

│   │   └── interview/

│   │

│   └── trained\_model/

│

└── storage/

```



\## 🧠 Machine Learning Modules



\### 1. Resume Information Extraction



A fine-tuned Qwen2.5-3B-Instruct model using QLoRA extracts structured information from resumes and generates JSON output.



\### 2. Job Description Extraction



Designed to extract structured job requirements, including skills and experience requirements.



\### 3. Resume–Job Matching



Implemented matching components include:



\- Skill normalization.

\- Exact skill matching.

\- Semantic skill matching.

\- Experience matching.

\- Weighted scoring.



\### 4. Job Recommendation and Ranking



Ranks job opportunities according to their calculated resume–job alignment scores and returns the highest-ranked recommendations.



\### 5. Additional Career Intelligence Modules



ATS analysis, skill gap analysis, resume improvement, and interview preparation are part of the planned platform architecture and remain under development.



\## 🤖 Resume Extraction Model



\- Base model: Qwen/Qwen2.5-3B-Instruct

\- Fine-tuning: Supervised Fine-Tuning (SFT)

\- Parameter-efficient fine-tuning: LoRA / QLoRA

\- Quantization: 4-bit NF4

\- Adapter configuration: LoRA



The trained adapter weights are distributed separately and are not included in this Git repository.



\## 📚 Documentation



Additional technical documentation is available in the `docs/` directory:



\- Architecture

\- API endpoints

\- Development workflow

\- Model integration



\## 🔧 Development Status



ResumeIQ is actively under development.



The initial focus is on building and integrating the machine learning components before completing the full backend and frontend workflows.



\## 🔮 Future Improvements



\- Complete end-to-end resume processing.

\- Integrate job description extraction.

\- Improve matching and ranking evaluation.

\- Complete ATS and skill gap analysis.

\- Integrate the ML engine with FastAPI.

\- Complete frontend and backend integration.

\- Add comprehensive testing and deployment.



\## ⚠️ Disclaimer



ResumeIQ provides estimated career insights and job alignment scores. These scores do not represent a guarantee of employment or an employer's actual ATS decision.





