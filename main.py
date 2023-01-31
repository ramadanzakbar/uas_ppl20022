import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

# Create flask app
flask_app = Flask(__name__)
model = pickle.load(open("model.pkl", "rb"))

@flask_app.route("/")
def Home():
    return render_template("index.html")

@flask_app.route("/predict", methods = ["POST"])
def predict():
    tiket_terjual,rivalitas,suporter_lawan,suporter_team = [x for x in request.form.values()]
   
    tiket_terjual = int(tiket_terjual) / 100
    suporter_lawan = int(suporter_lawan) / 100
    suporter_team = int(suporter_team) / 100

    if rivalitas == "Sangat Rendah":
        tingkat_rivalitas = 1
    elif rivalitas == "Rendah":
        tingkat_rivalitas = 2
    elif rivalitas == "Sedang":
        tingkat_rivalitas = 3
    elif rivalitas == "Tinggi":
        tingkat_rivalitas = 4
    elif rivalitas == "Sangat Tinggi":
        tingkat_rivalitas = 5
    data = [[tiket_terjual,tingkat_rivalitas,suporter_lawan,suporter_team]]
    data = np.array(data,dtype=float)
    prediction = model.predict(data)
    if prediction == 1:
        prediction_text = "Keamanan Biasa"
    elif prediction == 2:
        prediction_text = "Keamanan Maksimal"
    elif prediction == 3:
        prediction_text = "Keamanan Super Maksimal"
    return render_template("index.html", prediction_text = "{}".format(prediction_text),prediction = prediction,
    tiket_terjual = int(tiket_terjual *100), rivalitas = rivalitas, suporter_lawan = int(suporter_lawan*100), suporter_team = int(suporter_team*100)
    )

if __name__ == "__main__":
    flask_app.run(debug=True)