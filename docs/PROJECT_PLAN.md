# PDF to JPG 转换网站 - 任务分配表

**项目名称：** PDF to JPG Converter  
**生成日期：** 2025-10-15  
**目标：** 开发一个Vercel部署的网站，实现PDF上传并转换为JPG图片（打包下载）

---

## 📋 核心需求

1. **上传功能**：用户上传单个PDF文件
2. **转换功能**：每页转成一张JPG（适中质量，150 DPI）
3. **下载功能**：所有JPG打包成ZIP文件供下载
4. **部署平台**：Vercel（Serverless环境）

---

## 🎯 任务拆分与分配

### Task-001: 技术方案设计与架构规划
- **复杂度：** `critical`
- **执行者：** Cursor（CEO亲自做）
- **模型：** Cursor AI
- **成本：** ¥0.30
- **内容：**
  - 确定技术栈（Flask + pdf2image + Pillow）
  - Vercel部署适配方案（Serverless Functions + /tmp目录）
  - 文件处理流程设计
  - 前后端接口设计
- **输出：** `docs/ARCHITECTURE.md`

---

### Task-002: 后端API开发（PDF转JPG核心逻辑）
- **复杂度：** `complex`
- **执行者：** DeepSeek Reasoner（牛马）
- **模型：** `deepseek:deepseek-reasoner`
- **成本：** ¥0.05
- **原因：** 涉及Vercel平台适配、文件系统限制（/tmp）、异步处理、错误处理
- **任务规范：** `tasks/task-002-backend-api.txt`
- **内容：**
  - Flask API 路由设计
  - PDF上传接收（/api/upload）
  - PDF转JPG核心函数（pdf2image + Pillow）
  - Vercel环境适配（判断 `VERCEL` 环境变量）
  - /tmp 目录文件处理
  - ZIP打包逻辑
  - 错误处理和日志
- **输出：** `src/api/convert.py`

---

### Task-003: 前端页面开发（上传界面 + 下载）
- **复杂度：** `simple`
- **执行者：** DeepSeek Chat（牛马）
- **模型：** `deepseek:deepseek-chat`
- **成本：** ¥0.02
- **原因：** 独立的HTML/CSS/JS，无复杂状态管理
- **任务规范：** `tasks/task-003-frontend.txt`
- **内容：**
  - HTML5 文件上传界面
  - 拖拽上传支持
  - 上传进度条
  - 下载按钮
  - 简洁现代的UI设计
- **输出：** `src/templates/index.html`, `src/static/style.css`, `src/static/script.js`

---

### Task-004: Vercel部署配置
- **复杂度：** `simple`
- **执行者：** DeepSeek Chat（牛马）
- **模型：** `deepseek:deepseek-chat`
- **成本：** ¥0.02
- **任务规范：** `tasks/task-004-vercel-config.txt`
- **内容：**
  - `vercel.json` 配置
  - `requirements.txt` 依赖管理
  - 环境变量说明
  - Serverless Function 配置
- **输出：** `vercel.json`, `requirements.txt`

---

### Task-005: 测试与优化
- **复杂度：** `complex`
- **执行者：** Cursor（CEO）
- **模型：** Cursor AI
- **成本：** ¥0.20
- **内容：**
  - 本地测试
  - Vercel部署测试
  - 错误处理验证
  - 性能优化
  - 用户体验优化

---

## 💰 成本预估

| 任务 | 模型 | 成本 |
|------|------|------|
| Task-001 架构设计 | Cursor | ¥0.30 |
| Task-002 后端API | DeepSeek Reasoner | ¥0.05 |
| Task-003 前端页面 | DeepSeek Chat | ¥0.02 |
| Task-004 部署配置 | DeepSeek Chat | ¥0.02 |
| Task-005 测试优化 | Cursor | ¥0.20 |
| **总计** | - | **¥0.59** |

**节省对比：**
- 纯Cursor开发：约 ¥1.50
- 混合策略：¥0.59
- **节省：60.7%**

---

## 📌 技术栈

### 后端
- **框架：** Flask（轻量级，适合Vercel）
- **PDF处理：** pdf2image（基于poppler）
- **图片处理：** Pillow（压缩、质量调整）
- **打包：** zipfile（标准库）

### 前端
- **纯HTML/CSS/JavaScript**（无框架，保持简单）
- **上传：** FormData + Fetch API

### 部署
- **平台：** Vercel
- **函数类型：** Serverless Functions
- **存储：** /tmp 临时目录（Vercel限制）

---

## ⚠️ Vercel 特殊注意事项

1. **文件系统只读** → 使用 `/tmp` 目录
2. **Serverless 超时限制** → 控制PDF页数（建议 < 50页）
3. **依赖安装** → `requirements.txt` 需包含 `poppler-utils`
4. **环境变量** → 通过 `os.environ.get('VERCEL')` 判断环境

---

## 🚀 执行顺序

```
Task-001 (架构设计) 
    ↓
Task-002 (后端API) 
    ↓
Task-003 (前端页面) 
    ↓
Task-004 (部署配置) 
    ↓
Task-005 (测试优化)
```

---

## ✅ 验收标准

1. ✅ 本地可运行（`flask run`）
2. ✅ 上传PDF文件成功
3. ✅ 转换为JPG（150 DPI，适中质量）
4. ✅ 下载ZIP文件包含所有页面
5. ✅ Vercel部署成功
6. ✅ 线上环境正常工作

---

**生成者：** Cursor AI  
**批准状态：** 待用户确认

