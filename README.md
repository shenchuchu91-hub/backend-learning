<p align="center">
  <img src="./assets/banner.jpg" width="100%" alt="" />
</p>

<p align="center"><sub>雨还在下</sub></p>

# C / Python 练习

一边是 POSIX 套接字手写的小 HTTP，一边是标准库起的本地接口。密钥只放本机 `.env`，不进仓库。

## structure

```text
.
├── c_backend/
│   ├── server.c            # raw tcp/http with posix socket api
│   └── Makefile             # single-command build
├── python_backend/
│   ├── app.py               # stdlib http server, cors, ai gateway
│   ├── test_deepseek.py     # api connectivity check
│   ├── test_all_apis.py     # full endpoint health scan
│   ├── test_requests.http   # vscode rest client test cases
│   └── .env.example         # template — real .env stays local
├── web_frontend/
│   └── index.html           # minimal dark interface + ai console
└── deepseek_setup/
    └── continue_config_example.json
```

---

## run

**c socket server**

```bash
cd c_backend && make run
# listening on 127.0.0.1:8080
```

**python api + ai gateway**

```bash
cd python_backend
cp .env.example .env        # fill in real keys
python3 app.py
# listening on 127.0.0.1:8000
```

**web frontend**

open `web_frontend/index.html` with live server.
ai console connects to `localhost:8000`.

---

## endpoints

```text
GET   /health          →  service status
GET   /info            →  system metadata
POST  /api/chat        →  { "prompt": "...", "model": "deepseek" | "gemini" }
```

---

## key hygiene

```text
.env          →  gitignored, never committed
.env.example  →  placeholder template in repo
os.environ    →  runtime reads only, no hardcoded secrets
```

---

## notes

- c server: `socket` → `bind` → `listen` → `accept` → hand-write http response bytes
- python server: stdlib only, no flask/django — `http.server.BaseHTTPRequestHandler`
- cors: manual `Access-Control-Allow-Origin: *` header injection
- dual model: request body `model` field switches between deepseek and gemini

---

<sub>keys stay local · commits stay clean</sub>

---

<div align="center">
  <sub>雨还在下</sub>
</div>
