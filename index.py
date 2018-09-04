from flask import Flask, request, render_template, jsonify
import os
import pymongo

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/forms', methods=['GET'])
def formsPage():
    pass

@app.route('/data', methods=['GET'])
def dataPage():
    pass

@app.route('/donations')
def donationsPage():
    pass

@app.route('/onAppLoad')
def onAppLoad():
    pass

if __name__ == '__main__':
    app.run(debug = True)
