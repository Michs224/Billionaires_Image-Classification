from flask import Flask, request, jsonify,render_template
import Util

app=Flask(__name__)

@app.route("/Classify_image",methods=["POST"])

def Classify_image():
    image_data=request.form["image_data"]
    response=jsonify(Util.classify_image(image_data))

    response.headers.add("Access-Control-Allow-Origin","*")
    # print(image_data)
    
    return response


if __name__=="__main__":
    print("Starting Python Flask Server for Billionaires Image Classification")
    Util.load_saved_artifacts()
    app.run(host="0.0.0.0",port=5000)
