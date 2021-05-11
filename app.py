import joblib
import os 

from flask import Flask, request, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import TextField
from wtforms.validators import DataRequired, NumberRange

app = Flask(__name__)
app.config['SECRET_KEY']='wP4xQ8hUljJ5oI1c'
bootstrap = Bootstrap(app)

class InputForm(FlaskForm):
    review = TextField('Review')

@app.route('/', methods=['GET', 'POST'])
def index():
    form   = InputForm(request.form)
    res_review = 'Unknow'
    if form.validate_on_submit():
       x = [[form.review]]
       #res_review = make_prediction(x)
       res_review = 'Negative'
    
    return render_template('index.html', form=form, res_review=res_review)

def make_prediction(x):
    filename = os.path.join('model', 'finalized.sav')
    model = joblib.load(filename)
    return model.predict(x)[0]