# 测试指南

本文档说明如何测试 PDF to JPG 转换器的功能。

---

## 🧪 本地测试

### 前提条件

1. **安装系统依赖（poppler）**

```bash
# macOS
brew install poppler

# Ubuntu/Debian
sudo apt-get install poppler-utils

# Windows
# 下载安装：https://github.com/oschwartz10612/poppler-windows/releases/
```

2. **安装 Python 依赖**

```bash
pip install -r requirements.txt
```

---

## 🚀 启动本地开发服务器

```bash
# 进入项目目录
cd /Users/caoxinnan/repo/pdf-to-jpg

# 启动 Flask 服务器
python api/upload.py
```

**输出示例：**
```
 * Serving Flask app 'upload'
 * Debug mode: on
 * Running on http://0.0.0.0:5000
```

**访问：** http://localhost:5000

---

## ✅ 功能测试清单

### 1. 前端 UI 测试

- [ ] **页面加载**
  - 访问 http://localhost:5000
  - 页面正常显示（标题、上传区、按钮）
  - 无控制台错误

- [ ] **响应式设计**
  - 浏览器窗口缩放正常
  - 移动端模拟器显示正常
  - 所有元素对齐居中

- [ ] **拖拽区样式**
  - 虚线边框显示
  - 悬停时背景色变化
  - 图标和文字清晰可见

---

### 2. 文件上传测试

#### 测试 1：点击上传

1. 点击"选择文件"按钮
2. 选择一个 PDF 文件（如 test.pdf）
3. 验证文件选择对话框只显示 PDF 文件

**预期结果：**
- ✅ 只能选择 `.pdf` 文件
- ✅ 选择后立即开始上传

#### 测试 2：拖拽上传

1. 打开文件管理器
2. 拖拽一个 PDF 文件到上传区
3. 释放鼠标

**预期结果：**
- ✅ 拖拽时边框高亮
- ✅ 释放后立即上传

#### 测试 3：错误文件类型

1. 尝试上传非 PDF 文件（如 `.jpg`, `.docx`）

**预期结果：**
- ✅ 显示红色错误提示："只支持 PDF 文件"
- ✅ 不发送网络请求

#### 测试 4：文件过大

1. 尝试上传超过 16MB 的 PDF

**预期结果：**
- ✅ 显示错误提示："文件大小超过限制 (16MB)"

---

### 3. PDF 转换测试

#### 准备测试文件

**推荐测试文件：**

| 文件类型 | 页数 | 大小 | 测试目的 |
|---------|------|------|---------|
| 简单 PDF | 1-3 页 | < 1MB | 基础功能 |
| 多页 PDF | 10-20 页 | 2-5MB | 批量转换 |
| 大文件 PDF | 30-50 页 | 10-15MB | 性能测试 |

**创建测试 PDF（可选）：**
```bash
# macOS/Linux - 使用 LibreOffice 转换
libreoffice --headless --convert-to pdf test.docx

# 或在线工具：
# https://www.ilovepdf.com/word_to_pdf
```

#### 测试用例

**用例 1：单页 PDF**

1. 上传 1 页 PDF
2. 观察加载动画
3. 等待转换完成
4. 下载 ZIP 文件
5. 解压并查看 JPG

**预期结果：**
- ✅ 显示"正在转换..."动画
- ✅ 3-5 秒内完成
- ✅ 自动下载 `filename_converted.zip`
- ✅ ZIP 包含 1 个 JPG 文件（`page_1.jpg`）
- ✅ JPG 清晰可见，质量良好

**用例 2：多页 PDF（10 页）**

1. 上传 10 页 PDF
2. 等待转换

**预期结果：**
- ✅ 转换时间 5-10 秒
- ✅ ZIP 包含 10 个 JPG（`page_1.jpg` ~ `page_10.jpg`）
- ✅ 所有 JPG 质量一致

**用例 3：大 PDF（50 页）**

1. 上传 50 页 PDF
2. 监控转换时间

**预期结果：**
- ✅ 转换时间 < 10 秒（本地可能更长）
- ✅ ZIP 包含所有 50 页
- ✅ Vercel 部署时需注意超时（可能需要限制页数）

**用例 4：复杂 PDF（图表、图片）**

1. 上传包含复杂内容的 PDF（图表、图片、公式）
2. 检查转换质量

**预期结果：**
- ✅ 图表清晰
- ✅ 图片无失真
- ✅ 文字可读

---

### 4. 错误处理测试

#### 测试 1：无文件上传

1. 打开开发者工具
2. 使用 `fetch` 发送空请求：
```javascript
fetch('/api/upload', {method: 'POST', body: new FormData()})
  .then(r => r.json())
  .then(console.log)
```

**预期结果：**
```json
{
  "error": true,
  "message": "没有上传文件"
}
```

#### 测试 2：服务器错误模拟

1. 暂时修改 `api/upload.py`，强制抛出异常：
```python
@app.route('/api/upload', methods=['POST'])
def upload_file():
    raise Exception("测试错误")
```

2. 上传 PDF

**预期结果：**
- ✅ 显示友好错误提示
- ✅ 不显示技术栈信息（生产环境）

#### 测试 3：损坏的 PDF

1. 创建一个假的 PDF（文本文件重命名为 .pdf）
```bash
echo "fake pdf" > fake.pdf
```

2. 上传 fake.pdf

**预期结果：**
- ✅ 显示错误提示："文件处理失败"
- ✅ 临时文件被清理

---

### 5. 性能测试

#### 测试 1：并发上传

1. 打开 3 个浏览器标签页
2. 同时上传不同的 PDF

**预期结果：**
- ✅ 所有请求正常处理
- ✅ 无互相干扰
- ✅ 临时文件隔离（使用 UUID）

#### 测试 2：连续上传

1. 上传 PDF 1 → 等待完成
2. 立即上传 PDF 2 → 等待完成
3. 重复 5 次

**预期结果：**
- ✅ 每次都正常转换
- ✅ 临时文件被清理
- ✅ 无内存泄漏

---

## 🌐 Vercel 部署测试

### 部署后验证

1. **访问部署 URL**
   - 例如：`https://pdf-to-jpg-xxx.vercel.app`

2. **基础功能测试**
   - [ ] 上传 1 页 PDF
   - [ ] 下载 ZIP
   - [ ] 检查 JPG 质量

3. **Vercel 特有测试**
   - [ ] 环境检测：打开 `/` 查看 JSON 响应
   ```json
   {
     "message": "PDF to JPG 转换 API",
     "status": "运行中",
     "environment": "Vercel"  // 应该是 "Vercel" 而非 "本地"
   }
   ```
   
   - [ ] 临时文件路径：检查日志，确认使用 `/tmp` 目录

4. **超时测试**
   - 上传 50 页 PDF
   - 如果超过 10 秒，会收到 504 错误
   - 需要限制页数或优化性能

---

## 🐛 常见测试问题

### 问题 1：本地运行提示 "poppler not found"

**解决：**
```bash
# macOS
brew install poppler

# Ubuntu
sudo apt-get install poppler-utils
```

### 问题 2：转换速度很慢

**检查：**
- PDF 页数是否过多
- DPI 是否过高（默认 150）
- 本地资源是否充足

### 问题 3：ZIP 文件无法下载

**检查：**
- 浏览器控制台是否有错误
- 网络请求是否成功（200 状态码）
- `Content-Type` 是否为 `application/zip`

### 问题 4：JPG 质量不佳

**调整参数：**
- 在 `api/upload.py` 中修改 DPI：
```python
images = convert_from_path(pdf_path, dpi=200)  # 提高到 200
```

- 或提高 JPEG 质量：
```python
img.save(output_path, 'JPEG', quality=95)  # 提高到 95
```

---

## 📊 性能基准

### 本地开发环境

| PDF 页数 | 转换时间 | ZIP 大小 |
|---------|---------|---------|
| 1 页 | 1-2 秒 | ~200KB |
| 10 页 | 5-8 秒 | ~2MB |
| 50 页 | 20-30 秒 | ~10MB |

### Vercel 生产环境

| PDF 页数 | 转换时间 | 状态 |
|---------|---------|------|
| 1 页 | 2-3 秒 | ✅ 正常 |
| 10 页 | 6-10 秒 | ✅ 正常 |
| 50 页 | 可能超时 | ⚠️ 需限制 |

**建议：** 限制 PDF 页数 < 30 页，确保不超时

---

## ✅ 测试通过标准

全部测试通过后，项目可以部署到生产环境：

- [x] 前端 UI 正常显示
- [x] 文件上传功能正常（点击 + 拖拽）
- [x] PDF 转 JPG 成功
- [x] ZIP 文件正常下载
- [x] JPG 质量良好
- [x] 错误处理友好
- [x] 性能满足要求（< 10秒）
- [x] Vercel 环境适配正确
- [x] 临时文件自动清理

---

**测试完成！** 🎉

如有问题，请查看 [部署指南](DEPLOYMENT.md) 或提交 [Issue](https://github.com/yourusername/pdf-to-jpg/issues)

