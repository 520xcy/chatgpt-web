from revChatGPT.V1 import Chatbot
import os
from flask import Flask, request, render_template, jsonify, session
from flask_cors import CORS
from datetime import timedelta
from pathlib import Path
import time
import logging

PROJECT_PATH = os.getcwd()


# init chatbot
chatbot = Chatbot(config={
    # "email":"",
    # "password":"",
    "access_token":os.getenv("ACCESS_TOKEN")
})

server = Flask(__name__, static_folder=os.path.join(
    PROJECT_PATH, 'templates/public'))

server.config['SECRET_KEY'] = os.urandom(24)
server.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=3)

logging.basicConfig(format='%(asctime)s  %(message)s', level=logging.INFO)
# CORS(server, resources=r'/*') # 去注释则是否允许跨域访问接口



def generate_response(prompt):
    conversation_id = session.get('conversation_id')
    prev_text = ""
    try:
        for data in chatbot.ask(prompt,conversation_id=conversation_id):
            prev_text = prev_text + data["message"][len(prev_text) :]
        session['conversation_id'] = data['conversation_id']
        session.permanent = True
    except Exception as e:
        logging.error(e)
        return {"code": 0, "msg": e}
    
    return {"code": 200, "msg": prev_text}
    
def writelog(fname, q, a):
    file_name = 'output/chat ' + fname + '.md'
    f = Path(file_name)
    f.parent.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    with open(file_name, "a", encoding="utf-8") as f:
        f.write(f"{timestamp}\nquestion: {q}\nanswer: {a}\n\n")


@server.route('/', methods=['GET', 'POST'])
def get_request_json():
    if request.method == 'POST':
        raw = request.get_json()
        question = raw['question']

        if len(question) < 1:
            return jsonify({"code": 0, "message": "问题不能为空"})

        logging.info("======================================")
        res = generate_response(question)
        logging.info(f"问题：{question}\n")
        logging.info(f"答案：{res['msg']}\n")
        writelog(request.remote_addr, question, res['msg'])
        return jsonify({"code": res['code'], "message": str(res['msg'])})

    return render_template('index.html', question=0)


if __name__ == '__main__':
    server.run(debug=True, host='0.0.0.0', port=8080)
