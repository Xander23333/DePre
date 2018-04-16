from flask import Flask
from flask import make_response
app = Flask(__name__)

@app.route("/")
def hello():
    resp = make_response("haha")
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp
if __name__ == '__main__':  
    app.run()