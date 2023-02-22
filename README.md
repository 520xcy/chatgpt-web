docker运行:

```bash
version: '3'
services:
  chatgpt:
    image: 520xcy/chatgpt-web:chatgpt
    container_name: webchat
    environment:
      - ACCESS_TOKEN=#访问https://chat.openai.com/api/auth/session获取
    ports:
      - "8888:8080" #8080为容器内部端口，不可更改；8888为外部映射端口，可自行更改
    restart: unless-stopped
```

本地运行:

```
cd chatgetweb
pip3 install -r requirement.txt
export ACCESS_TOKEN=#访问https://chat.openai.com/api/auth/session获取
python3 main.py
```
