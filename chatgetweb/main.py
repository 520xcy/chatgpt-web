import openai
import os
from flask import Flask, request, render_template, jsonify, session
from flask_cors import CORS
from datetime import timedelta
from pathlib import Path
import time
import logging

PROJECT_PATH = os.getcwd()

openai.api_key = os.getenv('OPENAI_API_KEY')

server = Flask(__name__, static_folder=os.path.join(
    PROJECT_PATH, 'templates/public'))

server.config['SECRET_KEY'] = os.urandom(24)
server.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)

logging.basicConfig(format='%(asctime)s  %(message)s', level=logging.INFO)
# CORS(server, resources=r'/*') # 去注释则是否允许跨域访问接口


def set_userid(users: dict):
    session['turns'] = users['turns']
    session['text'] = users['text']
    session.permanent = True


def get_session():
    return {
        'text': session.get('text', ''),
        'turns': session.get('turns', [])
    }


def get_completion(question):
    users = get_session()

    question = users['text'] + "\nHuman: " + question
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"{question}\n",
            temperature=0.5,
            max_tokens=2045,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stop=None
        )
    except Exception as e:
        logging.error(e)
        return {"code": 0, "msg": e}

    result = response["choices"][0]["text"].strip()
    users['turns'] += [question] + [result]  # 只有这样迭代才能连续提问理解上下文

    if len(users['turns']) <= 5:  # 为了防止超过字数限制程序会爆掉，所以提交的话轮语境为10次。
        users['text'] = " ".join(users['turns'])
    else:
        users['text'] = " ".join(users['turns'][-5:])
    set_userid(users)
    return {"code": 200, "msg": result}


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
        res = get_completion(question)
        logging.info(f"问题：{question}\n")
        logging.info(f"答案：{res['msg']}\n")
        writelog(request.remote_addr, question, res['msg'])
        return jsonify({"code": res['code'], "message": str(res['msg'])})

    return render_template('index.html', question=0)


if __name__ == '__main__':
    server.run(debug=False, host='0.0.0.0', port=8080)
