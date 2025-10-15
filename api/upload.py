import os
import zipfile
import tempfile
import atexit
from flask import Flask, request, send_file, jsonify, send_from_directory
from pdf2image import convert_from_path
from PIL import Image
import io

# 初始化 Flask 应用
app = Flask(__name__, static_folder="public", static_url_path="")

# 环境配置
UPLOAD_FOLDER = "./uploads"
MAX_CONTENT_LENGTH = 20 * 1024 * 1024  # 20MB（腾讯云服务器无限制）
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

# 确保上传目录存在
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# 存储临时文件路径，用于清理
temp_files = []


def cleanup_temp_files():
    """清理所有临时文件"""
    print("开始清理临时文件...")
    for file_path in temp_files:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"已删除临时文件: {file_path}")
        except Exception as e:
            print(f"删除临时文件失败 {file_path}: {str(e)}")
    temp_files.clear()


# 注册退出时的清理函数
atexit.register(cleanup_temp_files)


def allowed_file(filename):
    """检查文件扩展名是否为 PDF"""
    return "." in filename and filename.rsplit(".", 1)[1].lower() == "pdf"


def convert_pdf_to_jpg(pdf_path, output_dir):
    """
    将 PDF 文件转换为 JPG 图片

    Args:
        pdf_path: PDF 文件路径
        output_dir: 输出目录

    Returns:
        list: 生成的 JPG 文件路径列表
    """
    try:
        print(f"开始转换 PDF: {pdf_path}")

        # 使用 pdf2image 转换 PDF
        images = convert_from_path(
            pdf_path,
            dpi=150,  # 控制内存占用，适合网页查看
            fmt="jpeg",
            output_folder=output_dir,
            paths_only=True,
        )

        print(f"PDF 转换完成，共 {len(images)} 页")
        return images

    except Exception as e:
        print(f"PDF 转换失败: {str(e)}")
        raise


def compress_and_save_images(image_paths, quality=85):
    """
    使用 Pillow 压缩图片并保存

    Args:
        image_paths: 原始图片路径列表
        quality: JPEG 质量 (1-100)

    Returns:
        list: 压缩后的图片路径列表
    """
    compressed_paths = []

    for i, image_path in enumerate(image_paths):
        try:
            # 打开图片
            with Image.open(image_path) as img:
                # 转换为 RGB 模式（确保 JPEG 兼容）
                if img.mode != "RGB":
                    img = img.convert("RGB")

                # 生成输出文件名
                base_name = os.path.splitext(os.path.basename(image_path))[0]
                output_path = os.path.join(
                    os.path.dirname(image_path), f"{base_name}_compressed.jpg"
                )

                # 保存压缩后的图片
                img.save(output_path, "JPEG", quality=quality, optimize=True)

                compressed_paths.append(output_path)
                temp_files.append(output_path)  # 添加到清理列表

                print(f"第 {i+1} 页压缩完成: {output_path}")

        except Exception as e:
            print(f"图片压缩失败 {image_path}: {str(e)}")
            raise

    return compressed_paths


def create_zip_file(image_paths, zip_filename):
    """
    将图片文件打包成 ZIP

    Args:
        image_paths: 图片路径列表
        zip_filename: 输出的 ZIP 文件名

    Returns:
        str: ZIP 文件路径
    """
    zip_path = os.path.join(UPLOAD_FOLDER, zip_filename)

    try:
        print(f"开始创建 ZIP 文件: {zip_path}")

        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for i, image_path in enumerate(image_paths):
                # 在 ZIP 中为每页使用有意义的文件名
                page_num = i + 1
                arcname = f"page_{page_num}.jpg"
                zipf.write(image_path, arcname)
                print(f"已添加第 {page_num} 页到 ZIP")

        # 获取 ZIP 文件大小
        zip_size = os.path.getsize(zip_path)
        print(f"ZIP 文件创建完成: {zip_path} ({zip_size} 字节)")

        temp_files.append(zip_path)  # 添加到清理列表
        return zip_path

    except Exception as e:
        print(f"ZIP 文件创建失败: {str(e)}")
        raise


@app.route("/api/upload", methods=["POST"])
def upload_file():
    """处理 PDF 文件上传和转换"""

    # 初始化临时文件列表（为本次请求）
    request_temp_files = []

    try:
        # 检查是否有文件上传
        if "file" not in request.files:
            return jsonify({"error": True, "message": "没有上传文件"}), 400

        file = request.files["file"]

        # 检查文件名是否为空
        if file.filename == "":
            return jsonify({"error": True, "message": "文件名为空"}), 400

        # 检查文件类型
        if not allowed_file(file.filename):
            return jsonify({"error": True, "message": "只支持 PDF 文件"}), 400

        print(f"开始处理文件: {file.filename}")

        # 生成唯一的文件名
        import uuid

        file_id = str(uuid.uuid4())
        pdf_filename = f"{file_id}.pdf"
        pdf_path = os.path.join(UPLOAD_FOLDER, pdf_filename)

        # 保存上传的 PDF 文件
        file.save(pdf_path)
        request_temp_files.append(pdf_path)
        temp_files.append(pdf_path)

        print(f"PDF 文件已保存: {pdf_path}")

        # 转换 PDF 为 JPG
        image_paths = convert_pdf_to_jpg(pdf_path, UPLOAD_FOLDER)

        # 检查页数（Vercel 超时限制）
        if len(image_paths) > 50:
            print(
                f"警告: PDF 页数较多 ({len(image_paths)} 页)，可能超过 Vercel 超时限制"
            )

        # 添加到临时文件列表
        request_temp_files.extend(image_paths)
        temp_files.extend(image_paths)

        # 压缩图片
        compressed_paths = compress_and_save_images(image_paths, quality=85)
        request_temp_files.extend(compressed_paths)

        # 创建 ZIP 文件
        zip_filename = f"{file_id}_converted.zip"
        zip_path = create_zip_file(compressed_paths, zip_filename)
        request_temp_files.append(zip_path)

        # 准备返回 ZIP 文件
        original_name = os.path.splitext(file.filename)[0]
        download_name = f"{original_name}_converted.zip"

        print(f"转换完成，准备返回文件: {download_name}")

        return send_file(
            zip_path,
            as_attachment=True,
            download_name=download_name,
            mimetype="application/zip",
        )

    except Exception as e:
        print(f"处理过程中发生错误: {str(e)}")

        # 清理本次请求的临时文件
        for file_path in request_temp_files:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    if file_path in temp_files:
                        temp_files.remove(file_path)
            except Exception as cleanup_error:
                print(f"清理临时文件失败 {file_path}: {str(cleanup_error)}")

        return jsonify({"error": True, "message": f"文件处理失败: {str(e)}"}), 500


@app.errorhandler(413)
def too_large(e):
    """处理文件过大错误"""
    return jsonify({"error": True, "message": "文件大小超过限制 (20MB)"}), 413


@app.errorhandler(500)
def internal_server_error(e):
    """处理服务器内部错误"""
    return jsonify({"error": True, "message": "服务器内部错误"}), 500


@app.route("/")
def home():
    # 根路径直接返回前端页面
    return send_from_directory("public", "index.html")


# 用于生产环境运行
if __name__ == "__main__":
    # 从环境变量读取端口，默认 3000
    port = int(os.environ.get("PORT", 3000))
    app.run(debug=False, host="0.0.0.0", port=port)
