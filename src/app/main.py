# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify
from flask_basicauth import BasicAuth
import numpy as np
import string
import pickle
import os

# Criação de uma app
app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = os.environ.get('BASIC_AUTH_USERNAME')
app.config['BASIC_AUTH_PASSWORD'] = os.environ.get('BASIC_AUTH_PASSWORD')

# Habilitando autenticação na app
basic_auth = BasicAuth(app)

# Carregar modelo
with open('models/model_naive_bayes.pkl', 'rb') as f:
    model = pickle.load(f)


@app.route("/detect", methods=['POST'])
def detect():
    # Pegar o JSON da requisição
    dados = request.get_json()
    payload = dados['frase']
    
    print("A frase recebida foi: "+payload)
    # Fazer predição
    pred = model.predict([payload])
    pred_pob = model.predict_proba([payload])[:,1]
    
    print("predict_proba:",pred_pob)
    if pred == 1:
      is_sexist = 'sexista'

    else:
      is_sexist = 'neutra/ambígua'
      
    res = jsonify(frase=payload, predict=is_sexist, proba=pred_pob[0])
    print("Predição\n",res.data)

    return res

@app.route("/")
def home():
    print("Executou a rota padrão")
    return "API de detecção de frases sexistas!!"

# Subir a API
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')