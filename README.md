# 🧠 AI Health Risk Predictor

A Flask-based web app that uses machine learning to predict:
- ❤️ Heart Disease Risk
- 💪 Muscle Weakness Risk

Built with Python, Flask, and scikit-learn.

---

## 🚀 Features

- 🔍 Predicts health risks based on user input
- 📊 Saves prediction history to CSV
- 🧾 View history by category (Heart or Muscle)
- 🗑️ Clear history with one click
- 🎨 Clean, responsive UI with animations

---

## 🛠️ Tech Stack

| Layer        | Tools Used                     |
|--------------|--------------------------------|
| Frontend     | HTML, CSS, Jinja2              |
| Backend      | Flask, Python                  |
| ML Models    | RandomForest, DecisionTree     |
| Data Storage | CSV (history.csv)              |

---

## 📂 Project Structure
project/ │ ├── app.py                  # Main Flask app ├── history.csv             # Stores prediction logs ├── templates/ │   ├── base.html │   ├── home.html │   ├── result.html │   ├── history.html │   └── health_tips.html ├── static/ │   └── style.css ├── models/ │   ├── heart_model.pkl │   └── muscle_model.pkl └── README.md

📌 Future Improvements
- Add login/authentication
- Export history to Excel or PDF
- Dynamic health tips based on prediction
- Deploy to Render or Vercel

🙌 Author
Built with ❤️ by [Goodness]

# health-risk-predictor-
