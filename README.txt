# CareerPilot AI — Beginner Hackathon Prototype

## What this project contains
- Frontend: HTML + CSS + JavaScript
- Backend: Python + Flask
- Career recommendation logic
- Skill-gap analysis
- Personalized roadmap
- Career chatbot demo

## Run on Windows

1. Install Python 3.11+ from python.org.
2. Open this folder in VS Code.
3. Open VS Code Terminal.
4. Create a virtual environment:
   py -m venv .venv
5. Activate it:
   .venv\Scripts\activate
6. Install Flask:
   pip install -r requirements.txt
7. Start the server:
   py app.py
8. Open the address shown in the terminal, normally:
   http://127.0.0.1:5000

Keep the terminal open while using the website.

## Project structure

CareerPilot_AI/
├── app.py
├── requirements.txt
├── templates/
│   └── index.html
└── static/
    ├── style.css
    └── app.js

## Important
The included "AI" is a rule-based demo so the project works without an API key or paid service.
For the hackathon, you can later connect the chatbot/recommendation layer to a real AI API after learning the basics.
