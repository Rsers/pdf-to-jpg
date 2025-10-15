# PDF to JPG 转换网站 - 技术架构文档

**版本：** 1.0  
**日期：** 2025-10-15  
**设计者：** Cursor AI

---

## 🎯 系统概述

一个轻量级的PDF转JPG在线转换工具，部署在Vercel Serverless平台上。

**核心功能：**
- 用户上传PDF文件
- 后端转换为JPG图片（每页一张）
- 打包成ZIP文件供下载

---

## 🏗️ 技术架构

### 整体架构图

```
用户浏览器
    ↓ (上传PDF)
前端页面 (index.html)
    ↓ (POST /api/upload)
Flask API (Vercel Serverless Function)
    ↓
PDF处理模块 (pdf2image)
    ↓
图片压缩 (Pillow)
    ↓
ZIP打包 (zipfile)
    ↓ (返回ZIP文件)
用户下载
```

---

## 🔧 技术栈选型

### 后端框架：Flask

**选择理由：**
- ✅ 轻量级，适合Serverless环境
- ✅ Vercel原生支持Python
- ✅ 简单直接，无需复杂配置

**替代方案对比：**
- ❌ FastAPI：过于复杂（本项目不需要异步）
- ❌ Django：太重（违反SS原则）

### PDF处理：pdf2image + poppler

**选择理由：**
- ✅ 成熟稳定的PDF渲染方案
- ✅ 支持高质量转换
- ✅ poppler是开源PDF渲染引擎

**工作原理：**
```python
from pdf2image import convert_from_path

# 转换PDF为PIL Image对象列表
images = convert_from_path(
    pdf_path,
    dpi=150,  # 分辨率
    fmt='jpeg'
)
```

### 图片处理：Pillow

**选择理由：**
- ✅ Python标准图片处理库
- ✅ 支持质量压缩
- ✅ 与pdf2image完美兼容

**质量设置：**
```python
image.save(
    jpg_path,
    'JPEG',
    quality=85,  # 0-100，85为平衡点
    optimize=True  # 优化文件大小
)
```

### 打包：zipfile (标准库)

**选择理由：**
- ✅ Python标准库，无需额外依赖
- ✅ 足够简单

---

## 📁 项目目录结构

```
pdf-to-jpg/
├── docs/                      # 项目文档
│   ├── PROJECT_PLAN.md        # 任务分配表
│   └── ARCHITECTURE.md        # 架构文档（本文件）
├── tasks/                     # DeepSeek任务规范
│   ├── task-002-backend-api.txt
│   ├── task-003-frontend.txt
│   └── task-004-vercel-config.txt
├── api/                       # Vercel Serverless Functions
│   └── upload.py              # 上传转换API
├── public/                    # 静态文件（Vercel自动服务）
│   ├── index.html             # 前端页面
│   ├── style.css              # 样式
│   └── script.js              # 交互逻辑
├── vercel.json                # Vercel配置
├── requirements.txt           # Python依赖
└── README.md                  # 项目说明
```

---

## 🔄 核心流程设计

### 1. 文件上传流程

```
前端 (script.js)
    ↓
FormData.append('file', pdfFile)
    ↓
fetch('/api/upload', {method: 'POST', body: formData})
    ↓
后端接收 (Flask request.files['file'])
```

### 2. PDF转换流程

```python
# 伪代码
def convert_pdf_to_jpg(pdf_path):
    # Step 1: 转换PDF为图片列表
    images = pdf2image.convert_from_path(
        pdf_path, 
        dpi=150,
        fmt='jpeg'
    )
    
    # Step 2: 保存为JPG文件
    jpg_paths = []
    for i, image in enumerate(images):
        jpg_path = f'/tmp/page_{i+1}.jpg'
        image.save(jpg_path, 'JPEG', quality=85, optimize=True)
        jpg_paths.append(jpg_path)
    
    # Step 3: 打包成ZIP
    zip_path = '/tmp/output.zip'
    with zipfile.ZipFile(zip_path, 'w') as zf:
        for jpg_path in jpg_paths:
            zf.write(jpg_path, os.path.basename(jpg_path))
    
    return zip_path
```

### 3. 文件下载流程

```python
# Flask返回文件
return send_file(
    zip_path,
    mimetype='application/zip',
    as_attachment=True,
    download_name='converted.zip'
)
```

---

## 🌍 Vercel 平台适配

### 关键限制与解决方案

| 限制 | 影响 | 解决方案 |
|------|------|---------|
| **文件系统只读** | 无法写入项目目录 | 使用 `/tmp` 目录 |
| **函数超时（10秒）** | 大PDF转换超时 | 限制页数 < 50页 |
| **内存限制（1GB）** | 大文件处理 | 控制DPI=150 |
| **无持久化存储** | 文件临时存在 | 转换后立即返回，清理临时文件 |

### 环境判断逻辑

```python
import os

# 判断是否在Vercel环境
IS_VERCEL = os.environ.get('VERCEL') is not None

# 根据环境选择存储路径
UPLOAD_FOLDER = '/tmp' if IS_VERCEL else './uploads'
```

### vercel.json 配置要点

```json
{
  "functions": {
    "api/upload.py": {
      "maxDuration": 10,
      "memory": 1024
    }
  },
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/api/$1"
    },
    {
      "src": "/(.*)",
      "dest": "/public/$1"
    }
  ]
}
```

---

## 🎨 前端设计

### UI原则：简洁现代

**核心元素：**
1. 文件拖拽上传区（虚线边框）
2. 上传进度条（转换时显示）
3. 下载按钮（转换完成后显示）
4. 错误提示（红色）

**用户体验：**
- ✅ 拖拽上传 + 点击上传
- ✅ 实时进度反馈
- ✅ 一键下载
- ✅ 清晰的错误提示

---

## 🔒 安全考虑

### 1. 文件验证
```python
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
```

### 2. 文件大小限制
```python
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
```

### 3. 临时文件清理
```python
import atexit
import shutil

def cleanup():
    if os.path.exists('/tmp/pdf_convert'):
        shutil.rmtree('/tmp/pdf_convert')

atexit.register(cleanup)
```

---

## 📊 性能优化

### 1. DPI选择（150）
- 平衡质量和速度
- 适合网页查看
- 减少内存占用

### 2. JPEG压缩（quality=85）
- 视觉质量几乎无损
- 文件大小减少约50%

### 3. ZIP压缩级别
```python
# 使用默认压缩级别（平衡速度和大小）
zipfile.ZIP_DEFLATED
```

---

## 🐛 错误处理

### 错误类型与处理

| 错误 | 原因 | 处理 |
|------|------|------|
| **400 Bad Request** | 无文件/非PDF | 返回错误提示 |
| **413 Payload Too Large** | 文件超过16MB | Vercel自动拦截 |
| **500 Internal Error** | 转换失败 | 捕获异常，返回友好提示 |
| **504 Timeout** | PDF页数过多 | 提示"文件过大" |

### 错误响应格式

```json
{
  "error": true,
  "message": "错误描述"
}
```

---

## 📦 依赖管理

### requirements.txt

```
Flask==3.0.0
pdf2image==1.16.3
Pillow==10.1.0
```

**注意：** `poppler-utils` 需要通过系统包安装（Vercel构建时自动处理）

---

## 🚀 部署流程

### 本地开发
```bash
# 安装依赖
pip install -r requirements.txt

# 运行开发服务器
python -m flask --app api/upload run

# 访问
open http://localhost:5000
```

### Vercel部署
```bash
# 安装Vercel CLI
npm i -g vercel

# 部署
vercel --prod
```

---

## ✅ 架构优势

1. **轻量化（LL原则）**
   - 无框架依赖（前端）
   - 最小化后端（仅Flask + 2个库）
   
2. **简单性（SS原则）**
   - 单一API端点
   - 清晰的处理流程
   
3. **成本效益**
   - Vercel免费额度足够
   - 无需服务器维护
   
4. **可维护性**
   - 代码量 < 500行
   - 逻辑清晰直观

---

## 📌 下一步

- [x] Task-001: 架构设计（已完成）
- [ ] Task-002: 后端API开发（DeepSeek Reasoner）
- [ ] Task-003: 前端页面开发（DeepSeek Chat）
- [ ] Task-004: Vercel配置（DeepSeek Chat）
- [ ] Task-005: 测试与部署

---

**设计者：** Cursor AI  
**状态：** ✅ 已完成并审核

