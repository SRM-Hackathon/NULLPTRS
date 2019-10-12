import os
import json
import requests
import base64
import pandas as pd
import textdistance

from flask import Flask, request

app = Flask(__name__)
item_db = pd.read_csv('items.csv')
item_db['item_name']=item_db['item_name'].str.lower()
print(item_db['item_name'])
ENDPOINT_URL = 'https://vision.googleapis.com/v1/images:annotate'
API_KEY = "AIzaSyC1okP_KZw3znhozWGi6DFZ_Y_i67FcD9Q"


@app.route("/")
def hello():
    return "<html><body><h1>Use /api endpoints</h1></body></html>"

"""
@app.route('/api/get_text', methods = ['POST'])
def get_text():
    #image_base64 = request.form['image']
    image_base64=STOP_SIGN_BASE64
    return request_ocr(image_base64)
"""

def request_ocr(image_base64):
    img_request = {"requests": [{
                                'image': {'content': image_base64},
                                'features': [{
                                    'type': 'DOCUMENT_TEXT_DETECTION',
                                    'maxResults': 1
                                    }]
                                }]
                   }
    response = requests.post(ENDPOINT_URL,
                             data=json.dumps(img_request),
                             params={'key': API_KEY},
                             headers={'Content-Type': 'application/json'})
    return response.text



@app.route('/api/testbed', methods=['POST'])
def detect_hwr():
    if request.method == 'POST':
        file = request.files['pic']
        filename = file.filename
        print(filename)
        filepath = os.path.join('C:\\Users\\Madhan\\PycharmProjects\\srm_hackathon\\flask server\received_image' + filename);
        file.save(filename)
        with open(filename,"rb") as img:
            img_b64 = base64.b64encode(img.read())

        print("b64 string "+img_b64.decode('utf-8'))
        ocr_resp = request_ocr(img_b64.decode('utf-8'))
        ocr_dict = json.loads(ocr_resp)
        items=ocr_dict['responses'][0]['textAnnotations'][0]["description"]
        items=items.split("\n")
        items.pop()
        skus=[]
        for itms in items:
            itms=itms.lower()
            test = item_db[item_db['item_name'].str.contains(itms)]
            if test.empty:
                skus.append(999)
            else:
                skus.append(int((test['sku']).to_string(index=False).strip()))
            test=test.iloc[0:0]
        print(skus)




        #print(ocr_resp)
        #text = "dummy text"

        print("filepath" + filepath)
        #print(text)
        #return text
        #return ocr_resp
        return json.dumps(skus)
    else:
        return "Y U NO USE POST?"


if __name__ == '__main__':
    app.run()