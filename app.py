from flask import Flask,request,render_template
import google.generativeai as palm
import replicate
import os

os.environ["REPLICATE_API_TOKEN"] = "r8_fPLyMmEYoD6K2lNmuAmiAcW9bHP3U0Q3TigiV"

app = Flask(__name__)
model = { "model": "models/chat-bison-001"}
palm.configure(api_key="AIzaSyALcznZDR7Az8oYz0AXhLi5YfYZwh6XcEw")

name = ""
flag = 1

@app.route("/",methods=["GET","POST"])
def index():
    return(render_template("index.html"))

@app.route("/main",methods=["GET","POST"])
def main():
    global name, flag
    if flag ==1:
        name = request.form.get("q")
        flag = 0
    return(render_template("main.html",r=name))

@app.route("/text",methods=["GET","POST"])
def text():
    return(render_template("text.html"))

@app.route("/text_reply",methods=["GET","POST"])
def text_reply():
    q = request.form.get("q")
    r = palm.chat(**model, messages=q)
    return(render_template("text_reply.html",r=r.last))

@app.route("/image",methods=["GET","POST"])
def image():
    return(render_template("image.html"))

@app.route("/image_reply",methods=["GET","POST"])
def image_reply():
    q = request.form.get("q")
    r = replicate.run("stability-ai/stable-diffusion:ac732df83cea7fff18b8472768c88ad041fa750ff7682a21affe81863cbe77e4",
    input={
        "prompt": q
    })
    return(render_template("image_reply.html",r=r[0]))

@app.route("/music",methods=["GET","POST"])
def music():
    return(render_template("music.html"))

@app.route("/music_reply",methods=["GET","POST"])
def music_reply():
    q = request.form.get("q")
    r = replicate.run(
    "meta/musicgen:671ac645ce5e552cc63a54a2bbff63fcf798043055d2dac5fc9e36a837eedcfb",
    input={
        "prompt": q,
        "duration": 5
    }
    )
    return(render_template("music_reply.html",r=r))

@app.route("/video",methods=["GET","POST"])
def video():
    return(render_template("video.html"))

@app.route("/video_reply",methods=["GET","POST"])
def video_reply():
    q = request.form.get("q")
    r = replicate.run(
    "anotherjesse/zeroscope-v2-xl:9f747673945c62801b13b84701c783929c0ee784e4748ec062204894dda1a351",
    input={
        "prompt": q,
        "num_frames": 10
    }
    )
    return(render_template("video_reply.html",r=r[0]))

@app.route("/end",methods=["GET","POST"])
def end():
    return(render_template("index.html"))
    
if __name__ == "__main__":
    app.run()