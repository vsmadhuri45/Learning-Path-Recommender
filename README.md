# Learning-Path-Recommender
# Adaptive Learning Path Recommender

An intelligent, full-stack adaptive learning platform designed to generate personalized, prerequisite-ordered study roadmaps through real-time diagnostic assessments and Bayesian Knowledge Tracing (BKT).

---

## Key Features

- **Conversational Profile Extraction**: Interactively captures user goals, experience levels, and existing skills.
- **Adaptive Diagnostic Assessment Engine**: A structured 14-question sequence featuring **10 Multiple-Choice Questions (MCQs)**, **3 Two-Liner Short Answers**, and **1 Paragraph Evaluation**.
- **Instant Local Text Evaluation**: Pure Python keyword-overlap and length-check grading engine providing instantaneous feedback without external API latency.
- **Bayesian Knowledge Tracing (BKT)**: Dynamically tracks concept mastery and uncertainty in real-time as users progress through assessments.
- **Prerequisite-Ordered Roadmaps**: Automatically calculates knowledge gaps and generates a prioritized study path respecting concept dependencies.
- **Direct Resource Redirection**: Clean UI cards enabling instant redirection to curated learning materials.
- **AI Assistant Integration**: Powered by Groq to answer contextual questions and explain why specific topics appear on a student's learning path.

---

## Tech Stack

### **Frontend**
- **Framework**: Next.js / React (App Router)
- **Styling**: Tailwind CSS
- **Icons**: Lucide React

### **Backend**
- **API Framework**: FastAPI (Python)
- **Engine Logic**: Custom Bayesian Knowledge Tracing & Graph Topological Sorting
- **LLM / Assistant Client**: OpenAI SDK configured with Groq API endpoints

---

## Project Structure

```text
Learning-Path-Recommender/
├── backend/
│   ├── app/
│   │   ├── assessment.py    # Adaptive quiz state & local text grading logic
│   │   ├── assistant.py     # AI path explanation & Q&A handler
│   │   ├── bkt.py           # Bayesian Knowledge Tracing math module
│   │   ├── graph.py         # Concept dependency graph & topological sort
│   │   ├── gaps.py          # Knowledge gap analysis engine
│   │   ├── llm.py           # Groq client configuration
│   │   ├── main.py          # FastAPI application & WebSocket endpoints
│   │   ├── questions.py     # Comprehensive question bank (MCQ, short, para)
│   │   ├── resources.py     # Curated learning resource mappings
│   │   └── roadmap.py       # Prioritized study path generator
│   ├── fixtures/            # Sample beginner & advanced profiles
│   ├── tests/               # Pytest test suite
│   └── requirements.txt     # Python dependencies
└── frontend/
    ├── app/                 # Next.js pages and layouts
    ├── components/          # UI components (JourneyRail, QuizInterface, etc.)
    └── lib/                 # TypeScript types and API utilities
