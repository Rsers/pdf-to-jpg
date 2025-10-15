# 部署指南

本文档详细说明如何将 PDF to JPG 转换器部署到 Vercel。

---

## 🚀 部署前准备

### 1. 确认文件结构

确保项目包含以下文件：

```
pdf-to-jpg/
├── api/
│   └── upload.py          ✅ 必需
├── public/
│   ├── index.html         ✅ 必需
│   ├── style.css          ✅ 必需
│   └── script.js          ✅ 必需
├── vercel.json            ✅ 必需
└── requirements.txt       ✅ 必需
```

### 2. 验证配置文件

**vercel.json** 必须包含：
```json
{
  "version": 2,
  "builds": [...],
  "routes": [...],
  "functions": {
    "api/upload.py": {
      "maxDuration": 10,
      "memory": 1024
    }
  }
}
```

**requirements.txt** 必须包含：
```
Flask==3.0.0
pdf2image==1.16.3
Pillow==10.1.0
```

---

## 📦 部署方式一：GitHub + Vercel（推荐）

### 步骤 1: 推送到 GitHub

```bash
# 初始化 Git 仓库（如果还没有）
git init

# 添加所有文件
git add .

# 提交
git commit -m "feat: 初始化 PDF to JPG 转换器项目"

# 添加远程仓库（替换为你的仓库地址）
git remote add origin https://github.com/yourusername/pdf-to-jpg.git

# 推送到 GitHub
git push -u origin main
```

### 步骤 2: 在 Vercel 导入项目

1. **访问 Vercel**
   - 打开 [vercel.com](https://vercel.com)
   - 使用 GitHub 账号登录

2. **导入项目**
   - 点击 "New Project"
   - 选择你的 GitHub 仓库 `pdf-to-jpg`
   - 点击 "Import"

3. **配置项目（可选）**
   - **Project Name:** pdf-to-jpg（或自定义）
   - **Framework Preset:** Other
   - **Root Directory:** ./
   - **Build Command:** 留空（Vercel 自动处理）
   - **Output Directory:** public
   - **Install Command:** 留空（Vercel 自动处理）

4. **部署**
   - 点击 "Deploy"
   - 等待构建完成（约 1-2 分钟）

5. **完成！**
   - 获得部署 URL：`https://pdf-to-jpg-xxx.vercel.app`
   - 访问并测试

---

## 🖥️ 部署方式二：Vercel CLI

### 步骤 1: 安装 Vercel CLI

```bash
npm install -g vercel
```

### 步骤 2: 登录 Vercel

```bash
vercel login
```

按提示选择登录方式（GitHub/Email）

### 步骤 3: 部署

```bash
# 进入项目目录
cd /path/to/pdf-to-jpg

# 部署到生产环境
vercel --prod
```

**首次部署会询问：**
```
? Set up and deploy "~/pdf-to-jpg"? [Y/n] y
? Which scope do you want to deploy to? (你的用户名)
? Link to existing project? [y/N] n
? What's your project's name? pdf-to-jpg
? In which directory is your code located? ./
```

**部署输出示例：**
```
🔍  Inspect: https://vercel.com/xxx/pdf-to-jpg/xxx
✅  Production: https://pdf-to-jpg-xxx.vercel.app [copied to clipboard]
```

### 步骤 4: 验证部署

访问生成的 URL，测试功能：
1. 上传一个 PDF 文件
2. 等待转换
3. 下载 ZIP 文件
4. 检查 JPG 图片

---

## 🔍 部署验证清单

部署完成后，请验证以下功能：

### ✅ 前端访问
- [ ] 访问主页正常加载
- [ ] UI 显示正常（标题、上传区、按钮）
- [ ] 响应式布局正常（移动端）

### ✅ 文件上传
- [ ] 点击上传可以选择文件
- [ ] 拖拽上传正常工作
- [ ] 只能选择 PDF 文件
- [ ] 非 PDF 文件显示错误提示

### ✅ PDF 转换
- [ ] 上传 PDF 后显示"正在转换..."
- [ ] 转换完成后自动下载 ZIP
- [ ] ZIP 文件包含所有页面的 JPG
- [ ] JPG 图片质量正常

### ✅ 错误处理
- [ ] 上传超大文件（>16MB）显示错误
- [ ] 上传非 PDF 文件显示错误
- [ ] 服务器错误显示友好提示

---

## 🐛 部署问题排查

### 问题 1: 构建失败 - "No Python files found"

**原因：** `api/upload.py` 文件缺失或路径错误

**解决：**
```bash
# 检查文件是否存在
ls api/upload.py

# 确保文件在正确位置
tree -L 2
```

### 问题 2: 运行时错误 - "Module not found: pdf2image"

**原因：** `requirements.txt` 缺失或依赖未正确安装

**解决：**
```bash
# 检查 requirements.txt
cat requirements.txt

# 确保包含 pdf2image==1.16.3
```

### 问题 3: 500 错误 - "poppler not found"

**原因：** Vercel 环境缺少 poppler（理论上不应出现，Vercel 自动安装）

**解决：**
- 检查 Vercel 构建日志
- 确认 `pdf2image` 版本正确

### 问题 4: 静态文件 404

**原因：** `vercel.json` 路由配置错误

**解决：**
```json
// 确保 vercel.json 包含静态文件路由
{
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/api/$1"
    },
    {
      "src": "/(.*)",
      "dest": "/public/$1"  // 注意 /public/ 前缀
    }
  ]
}
```

### 问题 5: Serverless Timeout（10秒超时）

**原因：** PDF 页数过多或文件过大

**解决：**
- 限制 PDF 页数（< 50 页）
- 优化转换参数（降低 DPI）
- 或升级 Vercel 套餐（增加超时限制）

---

## 📊 Vercel 环境变量

本项目无需配置环境变量，但如果需要，可以在 Vercel 控制台设置：

**Settings → Environment Variables**

示例变量（如果需要）：
```
MAX_FILE_SIZE=16777216  # 16MB
MAX_PAGES=50
DPI=150
JPEG_QUALITY=85
```

然后在代码中读取：
```python
import os
MAX_FILE_SIZE = int(os.environ.get('MAX_FILE_SIZE', 16 * 1024 * 1024))
```

---

## 🔄 更新部署

### 通过 GitHub（自动部署）

1. 修改代码
2. 提交并推送到 GitHub
```bash
git add .
git commit -m "fix: 修复XXX问题"
git push
```
3. Vercel 自动触发重新部署

### 通过 CLI（手动部署）

```bash
# 部署到生产环境
vercel --prod

# 部署到预览环境（测试用）
vercel
```

---

## 📈 监控和日志

### 查看部署日志

**Vercel 控制台：**
1. 打开 [vercel.com/dashboard](https://vercel.com/dashboard)
2. 选择项目 `pdf-to-jpg`
3. 点击 "Deployments" → 选择部署
4. 查看 "Build Logs" 和 "Function Logs"

**CLI 方式：**
```bash
# 查看实时日志
vercel logs
```

### 监控函数性能

**Vercel 控制台 → Analytics**
- 函数调用次数
- 平均响应时间
- 错误率
- 带宽使用

---

## 💰 成本优化

### Vercel 免费额度

- **带宽：** 100GB/月
- **函数运行时间：** 100GB-Hours/月
- **函数调用：** 无限制（免费）

### 预计使用量

假设每次转换：
- PDF 大小：5MB
- ZIP 大小：3MB
- 函数运行时间：3 秒

**每月可免费处理：**
- 带宽限制：100GB ÷ 8MB ≈ 12,500 次
- 时间限制：100GB-Hours ÷ 3秒 ≈ 120,000 次

**结论：** 对于个人或小型项目，完全免费！

---

## 🌐 自定义域名（可选）

### 步骤 1: 在 Vercel 添加域名

1. 打开项目 → Settings → Domains
2. 输入你的域名（如 `pdf2jpg.example.com`）
3. 点击 "Add"

### 步骤 2: 配置 DNS

在你的域名提供商（如 Cloudflare）添加记录：

**A 记录：**
```
Type: A
Name: pdf2jpg (或 @)
Value: 76.76.21.21
```

**或 CNAME 记录：**
```
Type: CNAME
Name: pdf2jpg
Value: cname.vercel-dns.com
```

### 步骤 3: 等待 DNS 生效

通常 5-30 分钟，最长 48 小时。

---

## ✅ 部署完成！

恭喜！你的 PDF to JPG 转换器已成功部署到 Vercel！

**下一步：**
- 🎉 分享你的网站链接
- 📊 监控使用情况
- 🔧 根据用户反馈优化
- ⭐ 给项目加个 Star

---

**有问题？** 查看 [常见问题](../README.md#常见问题) 或提交 [Issue](https://github.com/yourusername/pdf-to-jpg/issues)

