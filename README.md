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
- **result_302.txt**: 包含状态码为 302 的 URL 列表。
- **result_403.txt**: 包含状态码为 403 的 URL 列表。

所有结果文件将保存在脚本所在目录的 `./result/` 文件夹中。

## 示例

运行脚本后，控制台将显示类似以下内容：

```
less复制代码[*] Start working...
[200] http://example.com  Example Domain
[302] https://example.org  Example Domain
ERROR https://nonexistent.example  Unable to access.
[*] All tasks completed. Program finished.
Total accessible sites: 2
Please check the result file in './result'
```

## 注意事项

- 该脚本使用了 `requests` 库的 `verify=False` 参数，因此在处理 HTTPS URL 时不会验证 SSL 证书。
- 如果 URL 的 HTTP 状态码不是 200、302 或 403，则会将其标记为拒绝访问。