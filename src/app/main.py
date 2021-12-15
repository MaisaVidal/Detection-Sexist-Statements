# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify
from flask_basicauth import BasicAuth
import numpy as np
import string
import pickle
import os

from datetime import datetime
from pubsub import publish_new_detect_sexism

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
    try:
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
      
      request_date = datetime.today().strftime(format="%Y-%m-%d %H:%M:%S")
      
      print('{"request_datetime":"%s", "frase":"%s", "predict":"%s", "proba":%.4f}'% (request_date, payload, is_sexist, pred_pob[0]))
      publish_new_detect_sexism('{"request_datetime":"%s", "frase":"%s", "predict":"%s", "proba":%.4f}'% (request_date, payload, is_sexist, pred_pob[0]))
      
        
      res = jsonify(frase=payload, predict=is_sexist, proba=pred_pob[0])
      print("Predição\n",res.data)

      return res
    except Exception as e:
      print("Request /detect fail:", e)

@app.route("/")
def home():
    print("Executou a rota padrão")
    return "API de detecção de frases sexistas!!"

# Subir a API
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')