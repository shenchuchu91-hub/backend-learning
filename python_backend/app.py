"""
极简原生 Python 后端服务 Demo
无需安装额外框架，直接使用标准库 http.server 构建。
支持 RESTful 接口与 DeepSeek 问答转发。
"""

import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.request
import urllib.error

# 健壮加载 .env 文件，兼容不同工作目录执行
def load_env(filepath=".env"):
    candidates = [
        filepath,
        os.path.join(os.path.dirname(__file__), ".env"),
        os.path.join(os.path.dirname(__file__), "..", ".env"),
    ]
    for p in candidates:
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        os.environ.setdefault(k.strip(), v.strip().strip("'\""))
            return

load_env()
PORT = int(os.environ.get("PORT", 8000))
# 默认只绑定本机，避免服务被局域网或公网访问。可用环境变量 HOST 覆盖（例如 0.0.0.0）。
HOST = os.environ.get("HOST", "127.0.0.1")

# 默认只允许本机来源。可用 CORS_ORIGINS 覆盖，多个来源以逗号分隔。
# 未写端口的条目（如 http://127.0.0.1）会同时匹配任意端口（如 http://127.0.0.1:5500）。
DEFAULT_CORS_ORIGINS = (
    "http://127.0.0.1",
    "http://localhost",
    "http://[::1]",
)


def _parse_cors_origins():
    raw = os.environ.get("CORS_ORIGINS", "").strip()
    if raw:
        return tuple(item.strip() for item in raw.split(",") if item.strip())
    return DEFAULT_CORS_ORIGINS


CORS_ORIGINS = _parse_cors_origins()


def _cors_allow_origin(origin):
    """若 Origin 被允许则返回应写回的值，否则返回 None。"""
    if not origin:
        return None
    for allowed in CORS_ORIGINS:
        if origin == allowed or origin.startswith(allowed + ":"):
            return origin
    return None


class BackendHandler(BaseHTTPRequestHandler):
    def _apply_cors_headers(self):
        allowed = _cors_allow_origin(self.headers.get("Origin", ""))
        if allowed:
            self.send_header("Access-Control-Allow-Origin", allowed)
            self.send_header("Vary", "Origin")
            self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")

    def _send_json(self, status_code, data):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self._apply_cors_headers()
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8"))

    def do_OPTIONS(self):
        origin = self.headers.get("Origin", "")
        if _cors_allow_origin(origin):
            self.send_response(204)
            self._apply_cors_headers()
            self.end_headers()
        else:
            self.send_response(403)
            self.end_headers()

    def do_GET(self):
        if self.path == "/" or self.path == "":
            self._send_json(200, {
                "status": "online",
                "message": "恭喜！你的第一个 Python 后端服务正在稳定运行！",
                "endpoints": {
                    "GET /": "服务概览",
                    "GET /health": "健康检查接口",
                    "POST /api/chat": "发送消息调用 DeepSeek (JSON: {'prompt': '...'})"
                }
            })
        elif self.path == "/health":
            self._send_json(200, {"status": "healthy", "service": "backend-learning-core"})
        else:
            self._send_json(404, {"error": "接口未找到 (404 Not Found)"})

    def do_POST(self):
        if self.path == "/api/chat":
            content_length = int(self.headers.get("Content-Length", 0))
            body_bytes = self.rfile.read(content_length)

            try:
                body = json.loads(body_bytes.decode("utf-8"))
            except Exception:
                self._send_json(400, {"error": "请求体格式错误，请传递标准 JSON"})
                return

            prompt = body.get("prompt", "")
            if not prompt:
                self._send_json(400, {"error": "缺少 'prompt' 字段"})
                return

            chosen_model = body.get("model", "deepseek").lower()

            if "gemini" in chosen_model:
                api_key = os.environ.get("GEMINI_API_KEY", "")
                if not api_key:
                    self._send_json(400, {"error": "未在 .env 中配置 GEMINI_API_KEY"})
                    return

                try:
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
                    headers = {"Content-Type": "application/json"}
                    payload = {
                        "contents": [{"parts": [{"text": prompt}]}]
                    }
                    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
                    with urllib.request.urlopen(req, timeout=30) as resp:
                        resp_data = json.loads(resp.read().decode("utf-8"))
                        answer = resp_data["candidates"][0]["content"]["parts"][0]["text"]
                        self._send_json(200, {
                            "source": "gemini-2.5-flash",
                            "prompt": prompt,
                            "reply": answer
                        })
                except Exception as e:
                    self._send_json(500, {"error": f"调用 Gemini 失败: {str(e)}"})
                return

            # 默认走 DeepSeek
            api_key = os.environ.get("DEEPSEEK_API_KEY", "")
            if not api_key or "sk-xxxx" in api_key:
                self._send_json(200, {
                    "source": "mock_response",
                    "tip": "你尚未在 .env 中配置真实的 DEEPSEEK_API_KEY",
                    "echo": f"收到你的提示词: {prompt}",
                    "reply": "后端服务已成功接收到请求！配置有效 API Key 后将自动接入真实 DeepSeek 模型。"
                })
                return

            # 调用真实 DeepSeek API
            try:
                url = "https://api.deepseek.com/chat/completions"
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {api_key}"
                }
                payload = {
                    "model": "deepseek-chat",
                    "messages": [
                        {"role": "user", "content": prompt}
                    ]
                }
                req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
                with urllib.request.urlopen(req, timeout=30) as resp:
                    resp_data = json.loads(resp.read().decode("utf-8"))
                    answer = resp_data["choices"][0]["message"]["content"]
                    self._send_json(200, {
                        "source": "deepseek-chat",
                        "prompt": prompt,
                        "reply": answer
                    })
            except Exception as e:
                self._send_json(500, {"error": f"调用 DeepSeek 失败: {str(e)}"})
        else:
            self._send_json(404, {"error": "未知 POST 路径"})

def run_server():
    server_address = (HOST, PORT)
    httpd = HTTPServer(server_address, BackendHandler)
    print(f"==================================================")
    print(f" 🚀 后端服务已启动: http://{HOST}:{PORT}")
    print(f" 默认仅监听本机。如需更改监听地址，请设置环境变量 HOST。")
    print(f" 按 Ctrl + C 可终止服务")
    print(f"==================================================")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n正在关闭后端服务...")
        httpd.server_close()
        print("服务已停止。")

if __name__ == "__main__":
    run_server()
