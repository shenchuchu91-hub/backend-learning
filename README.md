# 后端进阶之路：从 Linux、C 到 Python 与 AI 接入

欢迎来到后端开发的实践起步仓库！这里包含了从底层网络套接字（C 语言）到现代应用层 API（Python 原生服务）以及接入 **DeepSeek 大模型** 的完整工作流。

---

## 目录结构

```text
.
├── .gitignore              # 严防密钥、二进制缓存泄漏的配置（保护 GitHub 安全）
├── .vscode/
│   ├── extensions.json     # VS Code 推荐插件清单（一键安装 Continue、Python、Ruff、REST Client 等）
│   └── settings.json       # 编辑器自动保存与代码格式化规范
├── deepseek_setup/
│   └── continue_config_example.json # VS Code Continue 插件接入 DeepSeek 的现成配置模板
├── c_backend/              # 底层网络核心（C 语言 POSIX Socket）
│   ├── server.c            # 纯 C 编写的 HTTP 网络服务端
│   └── Makefile            # 编译脚本（make 一键编译）
└── python_backend/         # 业务服务核心（Python 原生 HTTP 服务与 DeepSeek 接入）
    ├── app.py              # 后端 API 服务主程序
    ├── test_deepseek.py    # 单独测试 DeepSeek API 通信脚本
    ├── test_requests.http  # VS Code 接口测试用例（免装 Postman）
    └── .env.example        # 敏感信息模板（复制为 .env 填入你的 Key）
```

---

## 快速上手

### 1. VS Code 插件一键安装与 DeepSeek 接入
1. **用 VS Code 打开此项目文件夹**：
   - 右下角会自动弹出提示：`This workspace has extension recommendations`（此工作区有推荐插件）。
   - 点击 **`Install All`（全部安装）**，即可自动安装 **Continue (AI助手)**、**Python**、**Ruff**、**REST Client** 等后端套件。
2. **配置 Continue 接入 DeepSeek**：
   - 打开 VS Code 左侧的 **Continue** 图标，点击底部的 ⚙️ 设置按钮进入配置。
   - 参考 `deepseek_setup/continue_config_example.json`，把你的 DeepSeek API Key 填进去即可实现侧边栏 AI 答疑与代码补全。

---

### 2. Python 后端与 DeepSeek 对话体验

1. **配置环境变量**：
   ```bash
   cd python_backend
   cp .env.example .env
   # 用编辑器打开 .env 填入你的 DeepSeek API Key
   ```
2. **启动后端服务**：
   ```bash
   python3 app.py
   ```
   服务将运行在 `http://127.0.0.1:8000`。
3. **测试接口**：
   - 在 VS Code 中打开 `python_backend/test_requests.http` 文件，在请求上方直接点击 **`Send Request`** 即可在编辑器右侧查看返回结果。

---

### 3. C 语言底层 Socket 服务器体验

1. **编译并启动**：
   ```bash
   cd c_backend
   make run
   ```
   服务将监听 `http://127.0.0.1:8080`。
2. **在浏览器或终端测试**：
   ```bash
   curl http://127.0.0.1:8080/
   ```
   通过阅读 `c_backend/server.c`，你将直观理解操作系统内核是如何通过套接字（Socket）接收网络字节流并返回 HTTP 报文的。

---

## 如何将本仓库提交并发布到你的 GitHub

你已经配置好了 GitHub 身份信息，只需在 GitHub 网页上新建一个仓库，然后执行：

```bash
# 1. 提交本地所有初始代码
git add .
git commit -m "feat: 初始化后端学习路线工作区与 DeepSeek 接入模板"

# 2. 关联你的远程仓库并推送 (将下方仓库地址替换为你自己的)
git remote add origin https://github.com/shenchuchu91-hub/backend-learning-roadmap.git
git branch -M main
git push -u origin main
```
