// DOM 元素
const dropArea = document.getElementById('dropArea');
const fileInput = document.getElementById('fileInput');
const selectBtn = document.getElementById('selectBtn');
const loading = document.getElementById('loading');
const message = document.getElementById('message');

// 常量定义
const MAX_FILE_SIZE = 16 * 1024 * 1024; // 16MB
const ALLOWED_FILE_TYPES = ['application/pdf'];

// 初始化事件监听
function initEventListeners() {
    // 点击选择按钮触发文件选择
    selectBtn.addEventListener('click', () => {
        fileInput.click();
    });

    // 文件选择变化事件
    fileInput.addEventListener('change', handleFileSelect);

    // 拖拽事件
    dropArea.addEventListener('dragover', handleDragOver);
    dropArea.addEventListener('dragleave', handleDragLeave);
    dropArea.addEventListener('drop', handleDrop);

    // 点击上传区域也可以触发文件选择
    dropArea.addEventListener('click', () => {
        fileInput.click();
    });
}

// 处理文件选择
function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
        processFile(file);
    }
}

// 处理拖拽悬停
function handleDragOver(event) {
    event.preventDefault();
    event.stopPropagation();
    dropArea.classList.add('drag-over');
}

// 处理拖拽离开
function handleDragLeave(event) {
    event.preventDefault();
    event.stopPropagation();
    dropArea.classList.remove('drag-over');
}

// 处理拖拽放置
function handleDrop(event) {
    event.preventDefault();
    event.stopPropagation();
    dropArea.classList.remove('drag-over');
    
    const files = event.dataTransfer.files;
    if (files.length > 0) {
        processFile(files[0]);
    }
}

// 验证文件
function validateFile(file) {
    // 检查文件类型
    if (!ALLOWED_FILE_TYPES.includes(file.type)) {
        throw new Error('请上传 PDF 文件');
    }

    // 检查文件大小
    if (file.size > MAX_FILE_SIZE) {
        throw new Error('文件大小不能超过 16MB');
    }

    // 检查文件扩展名
    if (!file.name.toLowerCase().endsWith('.pdf')) {
        throw new Error('文件必须是 PDF 格式');
    }

    return true;
}

// 处理文件上传和转换
async function processFile(file) {
    try {
        // 验证文件
        validateFile(file);
        
        // 显示加载状态
        showLoading();
        hideMessage();
        disableUploadArea();

        // 创建 FormData
        const formData = new FormData();
        formData.append('file', file);

        // 发送请求到服务器
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });

        // 检查响应状态
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.message || `服务器错误: ${response.status}`);
        }

        // 处理下载
        await handleDownload(response);

        // 显示成功消息
        showMessage('转换成功！文件已开始下载', 'success');

    } catch (error) {
        // 显示错误消息
        showMessage(error.message, 'error');
        console.error('转换错误:', error);
    } finally {
        // 重置状态
        hideLoading();
        enableUploadArea();
        resetFileInput();
    }
}

// 处理文件下载
async function handleDownload(response) {
    try {
        const blob = await response.blob();
        
        // 检查 Blob 类型
        if (blob.type === 'application/zip' || blob.type === 'application/octet-stream') {
            // 创建下载链接
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'converted-images.zip';
            document.body.appendChild(a);
            a.click();
            
            // 清理
            setTimeout(() => {
                document.body.removeChild(a);
                window.URL.revokeObjectURL(url);
            }, 100);
        } else {
            // 如果不是 ZIP 文件，可能是错误响应
            const text = await blob.text();
            try {
                const errorData = JSON.parse(text);
                throw new Error(errorData.message || '服务器返回了错误的文件格式');
            } catch {
                throw new Error('服务器返回了错误的文件格式');
            }
        }
    } catch (error) {
        throw new Error(`下载失败: ${error.message}`);
    }
}

// 显示加载状态
function showLoading() {
    loading.classList.remove('hidden');
}

// 隐藏加载状态
function hideLoading() {
    loading.classList.add('hidden');
}

// 显示消息
function showMessage(text, type) {
    message.textContent = text;
    message.className = `message ${type}`;
    message.classList.remove('hidden');
}

// 隐藏消息
function hideMessage() {
    message.classList.add('hidden');
}

// 禁用上传区域
function disableUploadArea() {
    dropArea.style.opacity = '0.6';
    dropArea.style.pointerEvents = 'none';
    selectBtn.disabled = true;
}

// 启用上传区域
function enableUploadArea() {
    dropArea.style.opacity = '1';
    dropArea.style.pointerEvents = 'auto';
    selectBtn.disabled = false;
}

// 重置文件输入
function resetFileInput() {
    fileInput.value = '';
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', () => {
    initEventListeners();
    
    // 添加一些控制台提示（开发用）
    console.log('PDF to JPG 转换器已加载');
    console.log('支持功能：');
    console.log('- 点击上传');
    console.log('- 拖拽上传');
    console.log('- 文件验证（类型、大小）');
    console.log('- 自动下载');
    console.log('- 错误处理');
});

// 全局错误处理
window.addEventListener('error', (event) => {
    console.error('全局错误:', event.error);
    showMessage('发生未知错误，请刷新页面重试', 'error');
});

// 未处理的 Promise 拒绝
window.addEventListener('unhandledrejection', (event) => {
    console.error('未处理的 Promise 拒绝:', event.reason);
    showMessage('发生未知错误，请刷新页面重试', 'error');
    event.preventDefault();
});