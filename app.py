import joblib
import os 
import re
from nltk.corpus import stopwords
stopwords_en = stopwords.words("english")
import spacy
nlp = spacy.load('en_core_web_sm')

from flask import Flask, request, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import TextField
from wtforms.validators import DataRequired, NumberRange

app = Flask(__name__)
app.config['SECRET_KEY']='wP4xQ8hUljJ5oI1c'
bootstrap = Bootstrap(app)

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[\W\d_]+", " ", text)
    text = [word for word in text.split() if word not in stopwords_en]
    nlp_text = nlp(" ".join(text))
    tokens = [word.lemma_ if word.lemma_ != "-PRON-" else word.lower_ for word in nlp_text]
    return " ".join(tokens)

class InputForm(FlaskForm):
    review = TextField('Review')

@app.route('/', methods=['GET', 'POST'])
def index():
    form   = InputForm(request.form)
    res_review = 'Unknow'
    if form.validate_on_submit():
       x = form.review.data
       res_review = make_prediction(x)
       #res_review = 'Negative'
    
    return render_template('index.html', form=form, res_review=res_review)

def make_prediction(text):

    # clean_text_file = os.path.join('model', 'clean_text.joblib')
    vectorizer_file = os.path.join('model', 'vectorizer.joblib')
    model_file = os.path.join('model', 'model.joblib')  

    
    # clean = joblib.load(clean_text_file)
    vectorizer = joblib.load(vectorizer_file)
    model = joblib.load(model_file)

    text = clean_text(text)
    text = vectorizer.transform([text])
    label = model.predict(text)[0]

    if label == 0:
        return "Negative"
    elif label == 1:
        return "Positive"
    else:
        return "Neutro"
