from flask import Flask, request, jsonify
import Util

app=Flask(__name__)

@app.route("/Classify_image", methods=["GET","POST"])

def Classify_image():
    image_data=request.form["image_data"]

    response=jsonify(Util.classify_image(image_data))

    response.headers.add("Access-Control-Allow-Origin","*")

    return response

if __name__=="__main__":
    print("Starting Python Flask Server for Sports Celebrity Image Classification")
    Util.load_saved_artifacts()
    app.run(port=5000)
