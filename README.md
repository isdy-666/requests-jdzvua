# 景艺大-自动课程表获取及邮件通知脚本-树维教务系统爬虫

本 Python 脚本用于自动登录 景德镇艺术职业大学 教务管理系统，其他的树维的教务系统同样适用，获取当天的课程表信息，并将格式化后的课程表发送至指定邮箱，实现了课程表的自动化查询和邮件提醒功能。

## 功能说明

- **自动登录**：使用提供的账号和加密后的密码登录教务管理系统。
- **课程表抓取**：获取当天的课程表信息，包括上课时间、课程名称和上课地点。
- **信息格式化**：将课程表信息格式化为清晰易读的文本。
- **邮件发送**：通过 QQ 邮箱的 SMTP 服务，将格式化后的课程表发送到多个指定的收件人邮箱。

## 使用场景

适用于需要每日查看课程表的学生用户，通过该脚本可以自动获取当天课程信息并及时推送到邮箱中，实现课程表的自动化提醒功能。

## 环境依赖

- **Python 3.x**
- **requests** - 用于发送 HTTP 请求。
- **beautifulsoup4** - 用于解析 HTML 页面。
- **smtplib** - Python 内置库，用于发送邮件。
- **ssl** - Python 内置库，用于建立安全的邮件连接。

## 安装步骤

1. **克隆项目代码**：

    ```bash
    git clone https://github.com/isdy-666/requests-jdzvua.git
    cd requests-jdzvua
    ```

2. **安装所需的 Python 包**：

    ```bash
    pip install requests beautifulsoup4
    ```
3. **安装所需的 Python 包**：

    ```bash
    python requests-jdzvua.py
    ```

## 参数配置

在运行脚本前，需要根据实际情况配置以下参数：

- **username** 和 **password**：将这些字段替换为您的教务管理系统账号和密码。
- **salt**：用于密码加密的盐值，请根据教务系统的要求确认该值是否正确。
- **EMAIL_ADDRESS** 和 **EMAIL_PASSWORD**：发送方的 QQ 邮箱地址及 SMTP 授权码（不是 QQ 邮箱密码）。
- **recipients**：一个包含收件人邮箱的列表，可以添加多个接收邮箱。


### 修改示例

```python
# 模拟用户凭据和盐值
username = "您的学号"
password = "您的密码"
salt = "您的salt值"  # 确认是否这个salt正确

# QQ邮箱信息
EMAIL_ADDRESS = '您的QQ邮箱@qq.com'  # 替换为您的邮箱地址
EMAIL_PASSWORD = '您的SMTP授权码'  # 替换为您的QQ邮箱SMTP授权码

# 收件人邮箱列表
recipients = [
    '收件人1@qq.com',
    '收件人2@qq.com',
    '收件人3@qq.com',
    # 添加更多收件人邮箱
]
