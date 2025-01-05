# markdown-to-website/markdown-to-website/README.md

# Markdown to Website

该项目旨在将Markdown文档集转换为静态网站。通过使用Python脚本，用户可以轻松地将Markdown文件转换为HTML格式，并使用预定义的HTML模板进行渲染。

## 项目结构

```
markdown-to-website
├── src
│   ├── md2html.py        # 转换Markdown文档为HTML的主要脚本
│   └── templates
│       └── base.html     # HTML模板，定义网站的基本结构和样式
├── requirements.txt       # 项目所需的Python库和依赖项
└── README.md              # 项目文档
```

## 安装依赖

在开始之前，请确保您已安装Python。然后，您可以使用以下命令安装项目所需的依赖项：

```
pip install -r requirements.txt
```

## 使用方法

1. 将您的Markdown文件放置在项目的适当目录中。
2. 运行以下命令以转换Markdown文件为HTML：

   ```
   python src/md2html.py <your_markdown_file.md>
   ```

3. 转换后的HTML文件将保存在指定的输出目录中。

## 特性

- 支持多种Markdown语法
- 可自定义的HTML模板
- 简单易用的命令行界面

## 贡献

欢迎任何形式的贡献！请提交问题或拉取请求以帮助改进该项目。

## 许可证

该项目采用MIT许可证，详细信息请参阅LICENSE文件。