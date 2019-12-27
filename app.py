from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS
import json
import main

app = Flask(__name__)
api = Api(app)
CORS(app)

@app.route("/")

class validarArquivo(Resource):
    def post(self):
        #print(request.json)
        print("@@@@@@@@@@@@@@@@@@@@@@@@")
        #print(dir(request.data))
        retorno = main.ExecutaCheck(request.data)
        print(retorno)
        print("@@@@@@@@@@@@@@@@@@@@@@@@")
        #print(request.data)
        return retorno

api.add_resource(validarArquivo, '/validar')


if __name__ == '__main__':
     app.run(host='0.0.0.0', port='5002')
