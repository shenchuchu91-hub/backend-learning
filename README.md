# 后端进阶之路：从 Linux、C 到 Python、Web 成果展与 AI 接入

欢迎来到后端与全栈开发的个人实践仓库！这里包含了从底层网络套接字（C 语言）到现代应用层 API（Python 原生服务）、个人成果展示网页以及接入 **DeepSeek 大模型** 的完整工作流。

---

## 目录结构

```text
.
├── .gitignore              # 严防密钥、二进制缓存泄漏的配置（保护 GitHub 安全）
├── .vscode/
│   ├── extensions.json     # VS Code 推荐插件清单（Continue、Live Server、Prettier、Ruff 等）
│   └── settings.json       # 编辑器自动保存与多语言格式化规范
├── deepseek_setup/
│   └── continue_config_example.json # Continue 插件接入 DeepSeek 的现成配置模板
├── c_backend/              # 底层网络核心（C 语言 POSIX Socket）
│   ├── server.c            # 纯 C 编写的 HTTP 网络服务端
│   └── Makefile            # 编译脚本（make 一键编译）
├── python_backend/         # 业务服务核心（Python 原生 HTTP 服务与 DeepSeek 接入）
│   ├── app.py              # 后端 API 服务主程序（支持 CORS，供网页前端直接调用）
│   ├── test_deepseek.py    # 单独测试 DeepSeek API 通信脚本
│   ├── test_requests.http  # VS Code 接口测试用例（免装 Postman）
│   └── .env.example        # 敏感信息模板（真实 .env 已被安全忽略）
└── web_frontend/           # 个人成果展示网站与 AI 交互控制台
    └── index.html          # 现代化响应式个人网站（支持 Live Server 一键本地预览）
```

---

## 快速上手与功能体验

### 1. VS Code 智能辅助与 DeepSeek 接入
- **所有开发插件已全部自动安装**：Continue、Python、C/C++、Ruff、Live Server、Prettier、GitLens。
- **需在 `.env` 中配置自己的 Key**：
  - 将 `python_backend/.env.example` 复制为 `python_backend/.env`，填入你自己申请的 `DEEPSEEK_API_KEY`（如需 Gemini，再填写 `GEMINI_API_KEY`）。不要把真实 Key 提交到仓库。
  - 若使用 Continue 插件，请按 `deepseek_setup/continue_config_example.json` 自行填写密钥后，即可在侧边栏使用 **DeepSeek-V3** 做代码补全与对话，或使用 **DeepSeek-R1** 进行复杂逻辑深度推理。

### 2. 本地网站实时预览（Live Server）
- 在 VS Code 资源管理器中，**右键点击 `web_frontend/index.html`**；
- 选择 **`Open with Live Server`**；
- 浏览器会自动打开你的个人网站，修改 HTML/CSS 代码时浏览器会自动实时刷新！

### 3. 运行 Python 后端让网页与 DeepSeek 联动
- 先配置密钥与监听参数：
  ```bash
  cp python_backend/.env.example python_backend/.env
  # 在 .env 中填入你自己的 DEEPSEEK_API_KEY
  ```
- 默认只监听本机 `127.0.0.1:8000`，CORS 也只允许 `http://127.0.0.1`、`http://localhost`、`http://[::1]`（含任意端口，例如 Live Server 的 `:5500`）。可用环境变量覆盖：
  ```bash
  # 监听地址（默认 127.0.0.1；改为 0.0.0.0 会暴露到局域网，不推荐）
  HOST=127.0.0.1
  PORT=8000
  # 额外允许的浏览器来源，逗号分隔（可选）
  # CORS_ORIGINS=http://127.0.0.1:5500,http://localhost:5500
  ```
- 在终端启动后端服务：
  ```bash
  python3 python_backend/app.py
  # 或临时覆盖监听地址：HOST=127.0.0.1 PORT=8000 python3 python_backend/app.py
  ```
- 刷新或打开你的个人网页，在下方的“**AI 实时交互区**”输入任何问题，点击发送，网页就会通过你本地的 Python 后端实时向 DeepSeek 发起提问并展示回答！

### 4. C 语言底层 Socket 服务器体验
- 在终端中运行：
  ```bash
  cd c_backend && make run
  ```
- 服务绑定在 `127.0.0.1:8080`（仅本机可访问）。在浏览器访问 `http://127.0.0.1:8080`，通过源码直观理解操作系统内核底层的 Socket、Bind、Listen、Accept 机制。

---

## 如何发布网页到 GitHub Pages（免费公网展示）

你可以让全世界任何人通过公网链接访问你的个人主页：
1. 打开你的 GitHub 仓库：[https://github.com/shenchuchu91-hub/backend-learning](https://github.com/shenchuchu91-hub/backend-learning)
2. 点击仓库顶部的 **`Settings` -> `Pages`**；
3. 在 **Branch** 下选择 `main`，文件夹选择 `/ (root)` 或 `/web_frontend`；
4. 点击 **Save**，稍等 1-2 分钟，GitHub 会生成一个专属链接（例如 `https://shenchuchu91-hub.github.io/backend-learning/web_frontend/`），你就能把它发给任何人看你的项目作品！
