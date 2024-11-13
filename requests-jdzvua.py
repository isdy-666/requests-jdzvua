import hashlib
import requests
from bs4 import BeautifulSoup
import smtplib
import ssl
from email.message import EmailMessage
import re  # 新增正则表达式模块

# 登录 URL 和登录后的页面 URL
login_url = "http://教务系统ip/eams/loginExt.action"
protected_url = "http://教务系统ip/eams/homeExt.action"
fetch_url = "http://教务系统ip/eams/homeExt!main.action"

# 模拟用户凭据和盐值
username = "username"
password = "password"
salt = "76f2a3be-4267-4883-8af7-2c9160b9065f-"  # 确认是否这个salt正确

# 对密码进行加密
def encrypt_password(password, salt):
    sha1 = hashlib.sha1()
    sha1.update((salt + password).encode('utf-8'))  # 使用utf-8编码
    return sha1.hexdigest()

# 加密后的密码
encrypted_password = encrypt_password(password, salt)

# 创建一个 Session
session = requests.Session()

# 设置请求头，模拟浏览器行为
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Referer": "http://改成你自己的教务系统ip/eams/loginExt.action;jsessionid=53C488381C1E600E635BE5AD6D0E3940",  # 传递正确的referer   #改成你自己的教务系统ip
    "Host": " 改成你自己的教务系统ip",       #改成你自己的教务系统ip
    "Proxy-Connection": "keep-alive",
    "Cookie": "semester.id=102; JSESSIONID=53C488381C1E600E635BE5AD6D0E3940; GSESSIONID=53C488381C1E600E635BE5AD6D0E3940",
    # 传递登录时获得的cookie
}

# 构造登录请求的数据
data = {
    'username': username,
    'password': encrypted_password,
    'session_locale': 'zh_CN',
    'submitBtn': '登录',
}

# 登录请求
response = session.post(login_url, headers=headers, data=data)

# 检查登录是否成功
if response.status_code == 200 and "登录失败" not in response.text:
    print("登录成功")

    # 设置 fetch 请求的 headers
    headers["Referer"] = protected_url  # 需要设置 referer 为受保护的页面

    # 使用 session 发送 fetch URL 的 GET 请求
    fetch_response = session.get(fetch_url, headers=headers)

    # 检查请求是否成功
    if fetch_response.status_code == 200:
        print("成功获取数据")

        # 使用 BeautifulSoup 解析 HTML 内容
        soup = BeautifulSoup(fetch_response.text, 'html.parser')

        # --------------- 提取课程表信息 ---------------
        # 将提取到的课程信息拼接成字符串
        course_info = "今日课程：\n\n"
        schedule_div = soup.find('div', class_='jrkc-box')
        if schedule_div:
            table = schedule_div.find('table')
            if table:
                rows = table.find('tbody').find_all('tr')
                if rows:
                    for row in rows:
                        # 提取时间并去除换行和多余空格，确保破折号前后没有多余的换行或空格
                        time_td = row.find('td', class_='date')
                        time = re.sub(r'\s*-\s*', ' - ',
                                      time_td.get_text(strip=True).replace('\n', '')) if time_td else ''

                        # 提取课程名称
                        course_td = row.find('td', class_='text')
                        course_name = course_td.find('h5').get_text(strip=True) if course_td else ''

                        # 提取地点
                        location_span = course_td.find('span', class_='zt') if course_td else None
                        if location_span:
                            [s.extract() for s in location_span('i')]
                            location = location_span.get_text(strip=True)
                        else:
                            location = ''

                        # 拼接每条课程信息
                        course_info += f"{time} | {course_name} | {location}\n"
                else:
                    course_info += "今日没有课程安排。\n"
            else:
                course_info += "未找到课表的表格。\n"
        else:
            course_info += "未找到包含今日课程的内容。\n"

        # ----------------- 发送邮件 -----------------
        EMAIL_ADDRESS = 'QQ邮箱地址'  # QQ邮箱地址
        EMAIL_PASSWORD = 'QQ邮箱SMTP授权码'  # QQ邮箱SMTP授权码
        recipients = ['123456@qq.com','1231232@qq.com']  # 收件人邮箱列表

        # 创建邮件对象
        subject = "今天的课表"
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = ", ".join(recipients)
        msg.set_content(course_info)

        # 使用SSL连接QQ邮箱的SMTP服务器并发送邮件
        context = ssl.create_default_context()
        try:
            with smtplib.SMTP_SSL("smtp.qq.com", 465, context=context) as smtp:
                smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                smtp.send_message(msg)
                print("邮件发送成功！")
        except Exception as e:
            print(f"邮件发送失败，发生了异常：{e}")
    else:
        print(f"无法获取数据，状态码: {fetch_response.status_code}")
else:
    print("登录失败，检查用户名或密码")
