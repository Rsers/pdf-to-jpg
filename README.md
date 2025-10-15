# PDF to JPG 转换器

一个简洁现代的在线 PDF 转 JPG 工具，部署在 Vercel Serverless 平台上。

[![部署状态](https://img.shields.io/badge/deploy-vercel-black)](https://vercel.com)
[![Python](https://img.shields.io/badge/python-3.9+-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

---

## ✨ 功能特性

- 📤 **拖拽上传** - 支持拖拽或点击上传 PDF 文件
- 🖼️ **批量转换** - 每页转换为一张 JPG 图片
- 📦 **打包下载** - 所有 JPG 自动打包成 ZIP 文件
- ⚡ **快速响应** - Serverless 架构，按需运行
- 🎨 **现代 UI** - 简洁美观的用户界面
- 📱 **响应式设计** - 支持移动端访问

---

## 🚀 快速开始

### 在线使用

访问部署好的网站：[待部署后填写]

### 本地开发

#### 1. 克隆项目

```bash
git clone https://github.com/yourusername/pdf-to-jpg.git
cd pdf-to-jpg
```

#### 2. 安装依赖

**系统依赖（必须）：**

```bash
# macOS
brew install poppler

# Ubuntu/Debian
sudo apt-get install poppler-utils

# Windows
# 下载并安装 poppler: https://github.com/oschwartz10612/poppler-windows/releases/
```

**Python 依赖：**

```bash
pip install -r requirements.txt
```

#### 3. 运行开发服务器

```bash
python api/upload.py
```

访问：http://localhost:5000

---

## 📁 项目结构

```
pdf-to-jpg/
├── api/                      # Vercel Serverless Functions
│   └── upload.py             # PDF 转换 API
├── public/                   # 静态文件（前端）
│   ├── index.html            # 主页面
│   ├── style.css             # 样式
│   └── script.js             # 交互逻辑
├── docs/                     # 项目文档
│   ├── PROJECT_PLAN.md       # 任务分配表
│   └── ARCHITECTURE.md       # 架构设计文档
├── tasks/                    # DeepSeek 任务规范
│   ├── task-002-backend-api.txt
│   ├── task-003-frontend.txt
│   └── task-004-vercel-config.txt
├── vercel.json               # Vercel 部署配置
├── requirements.txt          # Python 依赖
└── README.md                 # 项目说明（本文件）
```

---

## 🔧 技术栈

### 后端
- **Flask** - 轻量级 Web 框架
- **pdf2image** - PDF 转图片（基于 poppler）
- **Pillow** - 图片处理与压缩

### 前端
- **纯 HTML/CSS/JavaScript** - 无框架，保持简单
- **Fetch API** - 文件上传
- **响应式设计** - 移动端适配

### 部署
- **Vercel** - Serverless Functions 平台
- **环境适配** - 自动检测 Vercel 环境，使用 `/tmp` 目录

---

## ⚙️ 部署到 Vercel

### 方式一：通过 GitHub（推荐）

1. **Fork 本仓库到你的 GitHub**

2. **在 Vercel 导入项目**
   - 访问 [vercel.com](https://vercel.com)
   - 点击 "New Project"
   - 导入你的 GitHub 仓库
   - 点击 "Deploy"

3. **完成！**
   - Vercel 会自动构建和部署
   - 获得一个 `.vercel.app` 域名

### 方式二：通过 Vercel CLI

```bash
# 安装 Vercel CLI
npm i -g vercel

# 登录
vercel login

# 部署
vercel --prod
```

---

## 📊 转换参数

| 参数 | 值 | 说明 |
|------|----|----|
| **DPI** | 150 | 适中质量，网页查看足够 |
| **JPEG 质量** | 85 | 平衡质量和文件大小 |
| **最大文件大小** | 16MB | Vercel 限制 |
| **最大页数** | 50 | 避免 Serverless 超时 |

---

## 🐛 常见问题

### Q1: 转换失败，显示 500 错误？

**A:** 可能原因：
- PDF 文件损坏
- 文件页数过多（> 50 页）
- PDF 包含特殊加密

**解决方案：**
- 尝试更小的 PDF
- 检查 PDF 是否正常打开
- 查看控制台日志

### Q2: 本地运行提示 "poppler not found"？

**A:** 需要安装系统依赖 `poppler-utils`

```bash
# macOS
brew install poppler

# Ubuntu/Debian
sudo apt-get install poppler-utils
```

### Q3: Vercel 部署后无法访问？

**A:** 检查：
1. `vercel.json` 配置是否正确
2. `requirements.txt` 依赖是否完整
3. Vercel 构建日志是否有错误

---

## 🔐 安全与限制

- ✅ 只接受 `.pdf` 文件
- ✅ 文件大小限制：16MB
- ✅ Serverless 超时：10 秒
- ✅ 临时文件自动清理
- ✅ 无数据持久化（隐私保护）

---

## 💰 成本说明

### 开发成本（Cursor + DeepSeek 混合策略）

| 任务 | 执行者 | 成本 |
|------|--------|------|
| 架构设计 | Cursor | ¥0.30 |
| 后端 API | DeepSeek Reasoner | ¥0.05 |
| 前端页面 | DeepSeek Chat | ¥0.02 |
| 部署配置 | DeepSeek Chat | ¥0.02 |
| 测试优化 | Cursor | ¥0.20 |
| **总计** | - | **¥0.59** |

**对比：** 纯 Cursor 开发约 ¥1.50，节省 **60.7%**

### 运行成本（Vercel）

- **免费额度：** 每月 100GB 带宽 + 100GB-Hours 函数运行时间
- **预计：** 数百到数千次转换/月 完全免费
- **超出额度：** $0.40/GB 带宽，$0.60/100万 次函数调用

---

## 📝 开发日志

- **2025-10-15** - 项目初始化，完成架构设计
- **2025-10-15** - 后端 API 开发完成（DeepSeek Reasoner）
- **2025-10-15** - 前端页面开发完成（DeepSeek Chat）
- **2025-10-15** - Vercel 配置完成，准备部署

---

## 📄 许可证

MIT License - 自由使用、修改和分发

---

## 🙏 致谢

- [pdf2image](https://github.com/Belval/pdf2image) - PDF 转图片库
- [Pillow](https://python-pillow.org/) - Python 图片处理库
- [Vercel](https://vercel.com) - Serverless 部署平台
- [DeepSeek](https://www.deepseek.com/) - AI 代码生成

---

## 📧 联系方式

如有问题或建议，请提交 [Issue](https://github.com/yourusername/pdf-to-jpg/issues)

---

**⭐ 如果这个项目对你有帮助，请给个 Star！**
