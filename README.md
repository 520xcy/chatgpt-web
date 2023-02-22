docker运行:

```bash
version: '3'
services:
  chatgpt:
    image: 520xcy/chatgpt-web:chatgpt
    container_name: webchat
    environment:
      - OPENAI_API_KEY=前面你获取到的OpenAI API KEY
    ports:
      - "8888:8080" #8080为容器内部端口，不可更改；8888为外部映射端口，可自行更改
    restart: unless-stopped
```

本地运行:

```
cd chatgetweb
pip3 install -r requirement.txt
export OPENAI_API_KEY=获取到的openai api key
python3 main.py
```
