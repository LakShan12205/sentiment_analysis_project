from flask import Flask, render_template, redirect, request
from helper import preprocessing, vectorizer, get_prediction
from logger import logging


app = Flask(__name__)

logging.info('Flask sever started')

# Make these global so we can update them
data = {}
reviews = []
positive = 0
negative = 0

@app.route("/", methods=["GET"])
def index():
    data['reviews'] = reviews
    data['positive'] = positive
    data['negative'] = negative

    logging.info('============Open home page=============')

    return render_template('index.html', data=data)

@app.route("/", methods=["POST"])
def my_post():
    global positive, negative  # Make sure we update the global counts
    text = request.form['text']

    logging.info(f'Text : {text}')

    preprocessed_text = preprocessing(text)
    logging.info(f'preprocessed Text : {preprocessed_text}')

    vectorized_text = vectorizer(preprocessed_text)
    logging.info(f'vectorizeded Text : {vectorized_text}')

    prediction = get_prediction(vectorized_text)
    logging.info(f'prediction  : {prediction}')

    if prediction == 'negative':
        negative += 1
    else:
        positive += 1

    reviews.insert(0, text)
    return redirect("/")
    
if __name__ == '__main__':
    app.run(debug=True, port=5001)
