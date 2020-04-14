# -*-coding:utf-8-*-
from flask import Flask, render_template
from Nlp.main import speechRecorder
import time
from Nlp.main import xunFei_aip

app = Flask(__name__)


# 首页面
@app.route("/")
def index():
	return render_template("index.html")


# 开始录音
@app.route("/speech", methods=['GET', 'POST'])
def beginRecorder():
	begin = time.time()
	speechRecorder.run()
	return "200"


# 结束录音
@app.route("/stopSpeech", methods=["GET", "POST"])
def stopRecorder():
	print("停止录音……")
	speechRecorder.stop()
	end = time.time()
	return "200"


# 开始识别
@app.route("/recognize", methods=['GET', 'POST'])
def recognize():
	return xunFei_aip.xunFeiAPI()     # 讯飞语音识别接口


if __name__ == '__main__':
	# 启动多线程参数，加快资源请求，快速响应用户
	app.run(debug=True, host="127.0.0.1", threaded=True)