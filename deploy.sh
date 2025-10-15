#!/bin/bash

# PDF to JPG 转换器 - Vercel 部署脚本
# 使用方法：./deploy.sh

set -e  # 遇到错误立即退出

echo "🚀 开始部署 PDF to JPG 转换器到 Vercel..."
echo ""

# 检查是否安装了 Vercel CLI
if ! command -v vercel &> /dev/null; then
    echo "❌ 错误：未找到 Vercel CLI"
    echo ""
    echo "请先安装 Vercel CLI："
    echo "  npm install -g vercel"
    echo ""
    exit 1
fi

# 检查是否已登录 Vercel
echo "📋 检查 Vercel 登录状态..."
if ! vercel whoami &> /dev/null; then
    echo "⚠️  未登录 Vercel，开始登录..."
    vercel login
else
    echo "✅ 已登录 Vercel"
fi

echo ""

# 检查必需文件
echo "📋 检查项目文件..."

required_files=(
    "api/upload.py"
    "public/index.html"
    "public/style.css"
    "public/script.js"
    "vercel.json"
    "requirements.txt"
)

missing_files=()

for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        missing_files+=("$file")
    fi
done

if [ ${#missing_files[@]} -gt 0 ]; then
    echo "❌ 错误：缺少必需文件："
    for file in "${missing_files[@]}"; do
        echo "  - $file"
    done
    echo ""
    exit 1
fi

echo "✅ 所有必需文件存在"
echo ""

# 显示项目结构
echo "📁 项目结构："
tree -L 2 -I '__pycache__|*.pyc|.git|node_modules' || ls -R

echo ""

# 询问用户确认
read -p "是否继续部署到 Vercel 生产环境？[y/N] " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ 部署已取消"
    exit 0
fi

echo ""
echo "🚀 开始部署..."
echo ""

# 执行部署
vercel --prod

echo ""
echo "✅ 部署完成！"
echo ""
echo "📌 下一步："
echo "  1. 访问上面的 Production URL"
echo "  2. 测试上传 PDF 功能"
echo "  3. 检查转换和下载是否正常"
echo ""
echo "📖 详细文档：docs/DEPLOYMENT.md"
echo ""

