import os
import markdown
import re
import requests
from urllib.parse import urlparse
import shutil
import time

def download_image(url, download_dir):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        parsed_url = urlparse(url)
        image_name = os.path.basename(parsed_url.path)
        download_path = os.path.join(download_dir, image_name)
        
        # 如果文件存在，则添加时间戳
        if os.path.exists(download_path):
            timestamp = int(time.time())
            image_name = f"{os.path.splitext(image_name)[0]}_{timestamp}{os.path.splitext(image_name)[1]}"
            download_path = os.path.join(download_dir, image_name)
        
        os.makedirs(download_dir, exist_ok=True)
        with open(download_path, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        return download_path
    return None

def convert_markdown_to_html(markdown_file, output_file_path, base_template, output_dir):
    # 读取Markdown文件
    with open(markdown_file, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # 将Markdown中的本地链接后缀改为.html
    markdown_content = re.sub(r'\[([^\]]+)\]\(([^)]+\.md)\)', r'[\1](\2.html)', markdown_content)

    # 查找并处理图片链接
    image_links = re.findall(r'!\[([^\]]*)\]\(([^)]+)\)', markdown_content)
    for alt_text, image_path in image_links:
        if image_path.startswith(('http://', 'https://')):
            # 下载网络图片
            download_dir = os.path.join(output_dir, 'download', 'images')
            downloaded_image_path = download_image(image_path, download_dir)
            if downloaded_image_path:
                relative_image_path = os.path.relpath(downloaded_image_path, output_dir)
                markdown_content = markdown_content.replace(image_path, relative_image_path)
        else:
            # 复制本地图片
            abs_image_path = os.path.join(os.path.dirname(markdown_file), image_path)
            if os.path.exists(abs_image_path):
                relative_image_path = os.path.relpath(abs_image_path, os.path.dirname(markdown_file))
                target_image_path = os.path.join(output_dir, relative_image_path)
                os.makedirs(os.path.dirname(target_image_path), exist_ok=True)
                shutil.copy2(abs_image_path, target_image_path)
                markdown_content = markdown_content.replace(image_path, relative_image_path)

    # 将Markdown转换为HTML
    html_content = markdown.markdown(markdown_content)

    # 将转换后的内容插入模板
    final_html = base_template.replace('{{ content }}', html_content)

    # 写入HTML文件
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(final_html)

    print(f'Converted {markdown_file} to {output_file_path}')

def convert_directory(input_dir, output_dir):
    # 如果目标目录不存在，则创建目标目录
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 读取HTML模板
    template_path = 'src/templates/base.html'
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template file not found: {template_path}")

    with open(template_path, 'r', encoding='utf-8') as f:
        base_template = f.read()

    if '{{ content }}' not in base_template:
        raise ValueError("Template file does not contain '{{ content }}' placeholder")

    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.md'):
                markdown_file = os.path.join(root, file)
                relative_path = os.path.relpath(root, input_dir)
                output_subdir = os.path.join(output_dir, relative_path)
                os.makedirs(output_subdir, exist_ok=True)
                html_file_name = os.path.splitext(file)[0] + '.html'
                output_file_path = os.path.join(output_subdir, html_file_name)
                convert_markdown_to_html(markdown_file, output_file_path, base_template, output_dir)

if __name__ == '__main__':
    input_directory = 'path/to/your/markdown/directory'  # 替换为实际的Markdown目录路径
    output_directory = 'output'  # 输出HTML文件的目录
    convert_directory(input_directory, output_directory)