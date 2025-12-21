from flask import Flask, render_template, request
import pandas as pd
import joblib
import numpy as np

app = Flask(__name__)

# Load your brains (models)
view_model = joblib.load('view_model.pkl')
like_model = joblib.load('like_model.pkl')
comment_model = joblib.load('comment_model.pkl')

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    if request.method == 'POST':
        
        user_title = request.form.get('title')
        day = request.form.get('day')
        hour = int(request.form.get('hour'))

        
        input_df = pd.DataFrame({
            'title': [user_title],
            'title_length': [len(user_title)],
            'day_of_week': [day],
            'hour': [hour]
        })

        
        v = float(view_model.predict(input_df)[0])
        l = float(like_model.predict(input_df)[0])
        c = float(comment_model.predict(input_df)[0])
        eng = ((l + c) / v * 100) if v > 0 else 0

        prediction = {
            'title': user_title,
            'views': f"{v:,}",
            'likes': f"{l:,}",
            'comments': f"{c:,}",
            'engagement': f"{eng:.2f}"
        }

    return render_template('index.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)