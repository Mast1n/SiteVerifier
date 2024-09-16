# SiteVerifier

通过 HTTP 请求检测 URL 是否存活，并将结果输出到指定的文件中。

## 功能

- 从文件中加载 URL 列表
- 验证 URL 的可访问性
- 支持多线程处理
- 处理不同的 HTTP 状态码
- 将结果输出到文件中，包括按状态码分类的文件

## 安装

你可以使用以下命令安装依赖库：

```
pip install -r requirements.txt
```

## 使用

1. **准备 URL 文件**

   创建一个文本文件，其中每行包含一个 URL

   ```
   http://example.com
   https://example.org
   ```

2. **运行脚本**

   使用以下命令运行 `SiteVerifier.py`，并指定 URL 文件路径和线程数量（可选）：

   ```
   python SiteVerifier.py -f <file> [-t <threads>]
   ```

   - `-f <file>`: 指定包含 URL 的输入文件路径（必需）。
   - `-t <threads>`: 指定要使用的最大线程数（默认值为 25）。

   示例：

   ```
   python SiteVerifier.py -f urls.txt -t 10
   ```

## 输出

- **result.txt**: 包含所有 URL 的详细结果。
- **result_200.txt**: 包含状态码为 200 的 URL 列表。
- **result_403.txt**: 包含状态码为 403 的 URL 列表。

所有结果文件将保存在脚本所在目录的 `./result/` 文件夹中。
