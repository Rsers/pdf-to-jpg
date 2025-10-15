#!/bin/bash

# PDF to JPG 转换器 - 腾讯云服务器部署脚本
# 服务器：txy-2c2g-13 (122.51.216.13)
# 端口：3000

set -e  # 遇到错误立即退出

echo "🚀 开始部署 PDF to JPG 转换器到腾讯云服务器..."
echo ""

# 配置
SERVER_HOST="txy-2c2g-13"
PROJECT_DIR="/home/ubuntu/pdf-to-jpg"
PORT=3000

echo "📋 部署配置："
echo "  服务器：$SERVER_HOST"
echo "  项目目录：$PROJECT_DIR"
echo "  端口：$PORT"
echo ""

# Step 1: 连接服务器并创建项目目录
echo "📂 Step 1: 创建项目目录..."
ssh $SERVER_HOST "mkdir -p $PROJECT_DIR"
echo "✅ 项目目录已创建"
echo ""

# Step 2: 上传代码到服务器
echo "📤 Step 2: 上传代码到服务器..."
rsync -avz --progress \
  --exclude='.git' \
  --exclude='__pycache__' \
  --exclude='*.pyc' \
  --exclude='.DS_Store' \
  --exclude='uploads' \
  --exclude='src' \
  --exclude='tasks' \
  --exclude='docs' \
  --exclude='.gitignore' \
  --exclude='CHECKLIST.md' \
  --exclude='deploy.sh' \
  --exclude='rule1.md' \
  ./ $SERVER_HOST:$PROJECT_DIR/
echo "✅ 代码已上传"
echo ""

# Step 3: 安装系统依赖和 Python 包
echo "📦 Step 3: 安装依赖..."
ssh $SERVER_HOST << 'EOF'
set -e
cd /home/ubuntu/pdf-to-jpg

# 安装 poppler-utils（PDF 转换必需）
echo "安装 poppler-utils..."
sudo apt-get update
sudo apt-get install -y poppler-utils

# 安装 Python 依赖
echo "安装 Python 依赖..."
pip3 install -r requirements.txt

echo "✅ 依赖安装完成"
EOF
echo ""

# Step 4: 配置 systemd 服务
echo "⚙️  Step 4: 配置 systemd 服务..."
ssh $SERVER_HOST << 'EOF'
set -e

# 创建 systemd 服务文件
sudo tee /etc/systemd/system/pdf-to-jpg.service > /dev/null << 'SERVICE'
[Unit]
Description=PDF to JPG Converter
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/pdf-to-jpg
Environment="PORT=3000"
ExecStart=/usr/bin/python3 /home/ubuntu/pdf-to-jpg/api/upload.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
SERVICE

echo "✅ systemd 服务配置已创建"
EOF
echo ""

# Step 5: 重新加载 systemd 并启动服务
echo "🔄 Step 5: 启动服务..."
ssh $SERVER_HOST << 'EOF'
set -e

# 重新加载 systemd
sudo systemctl daemon-reload

# 停止旧服务（如果存在）
sudo systemctl stop pdf-to-jpg 2>/dev/null || true

# 启动服务
sudo systemctl start pdf-to-jpg

# 设置开机自启
sudo systemctl enable pdf-to-jpg

echo "✅ 服务已启动并设置为开机自启"
EOF
echo ""

# Step 6: 检查服务状态
echo "🔍 Step 6: 检查服务状态..."
ssh $SERVER_HOST "sudo systemctl status pdf-to-jpg --no-pager" || true
echo ""

# Step 7: 测试服务
echo "🧪 Step 7: 测试服务..."
sleep 3  # 等待服务完全启动
ssh $SERVER_HOST "curl -s http://localhost:3000/ | jq" || echo "注意：服务可能需要几秒钟启动"
echo ""

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║          ✅ 部署完成！PDF to JPG 转换器已上线！             ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "🌐 访问地址：http://122.51.216.13:3000"
echo ""
echo "📊 常用命令："
echo "  查看日志：ssh $SERVER_HOST 'sudo journalctl -u pdf-to-jpg -f'"
echo "  重启服务：ssh $SERVER_HOST 'sudo systemctl restart pdf-to-jpg'"
echo "  停止服务：ssh $SERVER_HOST 'sudo systemctl stop pdf-to-jpg'"
echo "  查看状态：ssh $SERVER_HOST 'sudo systemctl status pdf-to-jpg'"
echo ""

