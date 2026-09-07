from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

CAREERS = {
    "Full Stack Developer": {
        "skills": ["HTML", "CSS", "JavaScript", "React", "Node.js", "SQL"],
        "keywords": ["web", "website", "frontend", "backend", "full stack", "javascript"]
    },
    "AI / ML Engineer": {
        "skills": ["Python", "Machine Learning", "Statistics", "NumPy", "Pandas", "AI"],
        "keywords": ["ai", "artificial intelligence", "machine learning", "python", "data"]
    },
    "Cybersecurity Analyst": {
        "skills": ["Networking", "Linux", "Python", "Cybersecurity", "Ethical Hacking", "SIEM"],
        "keywords": ["security", "cyber", "cybersecurity", "network", "hacking", "linux"]
    },
    "Data Analyst": {
        "skills": ["Excel", "SQL", "Python", "Statistics", "Power BI", "Data Visualization"],
        "keywords": ["data", "analytics", "analysis", "statistics", "excel", "power bi"]
    }
}

def clean_list(value):
    return [x.strip() for x in value.split(",") if x.strip()]

def recommend_career(skills, interests, goal):
    text = " ".join(skills + interests + [goal]).lower()
    scores = {}

    for career, info in CAREERS.items():
        score = 0
        for keyword in info["keywords"]:
            if keyword in text:
                score += 2
        for skill in skills:
            if skill.lower() in [s.lower() for s in info["skills"]]:
                score += 1
        scores[career] = score

    best = max(scores, key=scores.get)

    # If there is no meaningful match, choose based on the stated goal.
    if scores[best] == 0:
        if "data" in text:
            best = "Data Analyst"
        elif "security" in text or "cyber" in text:
            best = "Cybersecurity Analyst"
        elif "ai" in text or "machine" in text:
            best = "AI / ML Engineer"
        else:
            best = "Full Stack Developer"

    return best

@app.route("/")
def home():
    return render_template("index.html")

@app.post("/api/analyze")
def analyze():
    data = request.get_json(silent=True) or {}

    name = data.get("name", "Student").strip() or "Student"
    course = data.get("course", "BCA").strip() or "BCA"
    skills = clean_list(data.get("skills", ""))
    interests = clean_list(data.get("interests", ""))
    goal = data.get("goal", "").strip()

    career = recommend_career(skills, interests, goal)
    required = CAREERS[career]["skills"]

    skill_lower = {s.lower() for s in skills}
    matched = [s for s in required if s.lower() in skill_lower]
    missing = [s for s in required if s.lower() not in skill_lower]

    score = round((len(matched) / len(required)) * 100) if required else 0

    roadmap = [
        f"Strengthen your basics in {missing[0]}" if missing else "Review your strongest technical skills",
        f"Learn {missing[1]}" if len(missing) > 1 else "Build a small practical project",
        f"Practice {missing[2]}" if len(missing) > 2 else "Build a portfolio project",
        "Create a GitHub portfolio and document your projects",
        "Apply for internships and practice interview questions"
    ]

    return jsonify({
        "name": name,
        "course": course,
        "career": career,
        "score": score,
        "matched": matched,
        "missing": missing,
        "roadmap": roadmap,
        "message": f"Based on your profile, {career} is a strong career direction to explore."
    })

@app.post("/api/chat")
def chat():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip().lower()

    if not message:
        return jsonify({"reply": "Ask me about careers, skills, roadmaps, or projects."})

    if "java" in message:
        reply = "If you know Java, you can explore backend development. Learn SQL, Spring Boot, REST APIs and build a small backend project."
    elif "python" in message:
        reply = "Python can lead toward AI/ML, data analysis or backend development. Start with Python fundamentals and then choose one path."
    elif "frontend" in message or "website" in message:
        reply = "For frontend development, learn HTML, CSS and JavaScript first, then React. Build 2–3 small projects."
    elif "ai" in message or "machine learning" in message:
        reply = "For AI/ML, start with Python, NumPy, Pandas and basic statistics, then move to machine learning and small projects."
    elif "internship" in message:
        reply = "Build a few good projects, keep your GitHub updated, prepare a short resume and practice explaining your projects clearly."
    elif "roadmap" in message:
        reply = "Choose one target career, identify its required skills, learn them in order, build projects, then prepare for internships."
    else:
        reply = "I can help with career choices, skill gaps, learning roadmaps, internships and project ideas. Try asking: 'What should I learn after Java?'"

    return jsonify({"reply": reply})

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
