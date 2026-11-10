"""
测试直接调用 DeepSeek API 的基础脚本。
采用 Python 原生 urllib.request，无需提前 pip install 任何第三方库即可运行。
"""

import json
import os
import sys
import urllib.request
import urllib.error

def load_env_file(filepath=".env"):
    """简易加载 .env 文件到 os.environ"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(script_dir, ".env"),
        filepath,
        os.path.join("python_backend", ".env"),
        os.path.join("..", filepath)
    ]
    target = None
    for c in candidates:
        if os.path.exists(c):
            target = c
            break
    if not target:
        return

    with open(target, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            v = v.strip().strip("'\"")
            os.environ.setdefault(k.strip(), v)

def test_deepseek_call():
    load_env_file()
    api_key = os.environ.get("DEEPSEEK_API_KEY", "").strip()

    if not api_key or "sk-xxxx" in api_key:
        print("[提示] 未检测到有效的 DEEPSEEK_API_KEY！")
        print("请先在 python_backend/ 目录下创建 .env 文件，并写入：")
        print("DEEPSEEK_API_KEY=\"你的真实Key\"")
        sys.exit(1)

    url = "https://api.deepseek.com/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "你是一位资深的后端架构师导师，回答简短有力。"},
            {"role": "user", "content": "你好 DeepSeek！我正在从 Linux、C 和 Python 起步学习后端开发，请给我一句话鼓励！"}
        ],
        "temperature": 0.7
    }

    print("🚀 正在向 DeepSeek API 发送测试请求...")
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            answer = data["choices"][0]["message"]["content"]
            print("\n🎉 DeepSeek 返回响应成功：")
            print("-" * 50)
            print(answer)
            print("-" * 50)
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"❌ 请求失败 (HTTP {e.code}): {error_body}")
    except Exception as e:
        print(f"❌ 发生异常: {e}")

if __name__ == "__main__":
    test_deepseek_call()
