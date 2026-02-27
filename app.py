from flask import Flask, render_template, request, redirect, session

export CODECOURSE_GMAIL_USER="codeformaine@gmail.com"
export CODECOURSE_GMAIL_PASS="i love to code!"


app = Flask(__name__)
app.secret_key = "dev-key"

LANGUAGES = {
    "python": [
        {
            "id": 1,
            "title": "Python Basics 1",
            "reading": "Python is a powerful, beginner-friendly programming language used in web development, AI, data science, and more. It focuses on readability and simplicity.",
            "video": "Python Intro Video Placeholder",
            "quiz": {
                "question": "What is Python mainly used for?",
                "choices": [
                    "Cooking recipes",
                    "Programming and software development",
                    "Photo editing only"
                ],
                "answer": "Programming and software development"
            }
        },
        {
            "id": 2,
            "title": "Python Basics 2",
            "reading": "Variables store data in Python. You can store numbers, text, and more using variable names.",
            "video": "Variables Video Placeholder",
            "quiz": {
                "question": "What do variables do?",
                "choices": [
                    "Store data",
                    "Delete files",
                    "Style websites"
                ],
                "answer": "Store data"
            }
        }
    ]
}

# ---------------- AUTH ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["name"] = request.form["name"]
        session["role"] = request.form["role"]
        session["progress"] = {}   # { language: [completed lesson ids] }
        return redirect("/student/home")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ---------------- STUDENT ----------------
@app.route("/student/home")
def student_home():
    return render_template("student_home.html", name=session["name"])

@app.route("/student/language/<lang>")
def student_language(lang):
    lessons = LANGUAGES[lang]
    completed = session["progress"].get(lang, [])
    return render_template(
        "student_language.html",
        lessons=lessons,
        completed=completed,
        lang=lang
    )

@app.route("/student/lesson/<lang>/<int:lesson_id>", methods=["GET", "POST"])
def student_lesson(lang, lesson_id):
    lessons = LANGUAGES[lang]
    lesson = next(l for l in lessons if l["id"] == lesson_id)

    correct = False

    if request.method == "POST":
        answer = request.form["answer"]
        if answer == lesson["quiz"]["answer"]:
            session["progress"].setdefault(lang, [])
            if lesson_id not in session["progress"][lang]:
                session["progress"][lang].append(lesson_id)
            correct = True

    return render_template(
        "student_lesson.html",
        lesson=lesson,
        correct=correct,
        lang=lang
    )


if __name__ == "__main__":
    app.run(debug=True)
