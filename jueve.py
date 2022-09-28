from flask import Flask, request, jsonify
import sqlite3
import csv
import pandas as pd
import os
import pickle
import numpy as np



os.chdir(os.path.dirname(__file__))

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def welcome():
    return "welcome to my API"

@app.route('/api/v1/all/', methods=['GET'])
def get_all():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    squal = "SELECT * FROM database"
    result = cursor.execute(squal).fetchall()
    connection.close()
    return jsonify(result)


@app.route("/prediccion/", methods=['GET'])
def predict():
    model = pickle.load(open('data/advertising_model','rb'))

    tv = request.args.get('tv', None)
    radio = request.args.get('radio', None)
    newspaper = request.args.get('newspaper', None)

    if tv is None or radio is None or newspaper is None:
        return "Missing args, the input values are needed to predict"
    else:
        prediction = model.predict([[tv,radio,newspaper]])
        return "The prediction of sales investing that amount of money in TV, radio and newspaper is: " + str(round(prediction[0],2)) + 'k €'

@app.route("/almancen/", methods=['POST','GET'])
def nuevo_registro():
    
    TV = float(request.args["TV"])
    radio = float(request.args["radio"])
    newspaper = float(request.args["newspaper"])
    sales = float(request.args["sales"])

    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    select_books = "INSERT INTO database VALUES (?,?,?,?)"
    result = cursor.execute(select_books, (TV,radio,newspaper,sales)).fetchall()
    connection.commit() 
    connection.close()
    return ("se ha añadido nuevos datos: " + str(TV) + " " + str(radio)+ " "+ str(newspaper)+ " " + str(sales))

@app.route("/reentrenar/", methods=['POST','GET'])
def reentrenar():
    model = pickle.load(open('advertising_model','rb'))
    TV = float(request.args["TV"])
    radio = float(request.args["radio"])
    newspaper = float(request.args["newspaper"])
    sales = float(request.args["sales"])

    X = []
    X.append(TV)
    X.append(radio) 
    X.append(newspaper)
    X = np.array(X).reshape(1,-1)
    y= []
    y.append(sales)
    y = np.array(y).reshape(1,-1)

    model.fit(X,y)
    pickle.dump(model, open('advertising_model_v1','wb'))

    return str(model)


app.run() 