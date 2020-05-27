from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/home', methods=['GET'])
def home():
    return {'respone':'hello world'}

if __name__ == '__main__':
    app.run(debug=True)