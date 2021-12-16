import base64

from flask import Flask, request, make_response
from flask_cors import CORS, cross_origin
from extract import extract_text

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/', methods=['GET', 'POST'])
@cross_origin()
def index():
	with open("./examples/imageToSave.png", "wb") as fh:
		fh.write(base64.decodebytes((request.json['body'][22:]).encode('utf-8')))
	v = extract_text(None, None, "./examples/imageToSave.png")
	v = " ".join(v.split("\n")).strip()
	print(v)
	response = make_response()
	response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
	response.data = f'"{v}"'
	return response
