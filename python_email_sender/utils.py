import smtplib  # SMTP 사용을 위한 모듈
import argparse
import os
from email.mime.multipart import MIMEMultipart  # 메일의 Data 영역의 메시지를 만드는 모듈
from email.mime.text import MIMEText  # 메일의 본문 내용을 만드는 모듈
from email.mime.image import MIMEImage  # 메일의 이미지 파일을 base64 형식으로 변환하기 위한 모듈

home_directory = os.path.expanduser("~")

def parse_args():
    parser = argparse.ArgumentParser(description='Send Email')
    parser.add_argument('--sender', type=str, required=True, help='email sender')
    parser.add_argument('--smtp', type=str, default='smtp.gmail.com', help='smtp server')
    parser.add_argument('--receiver', type=str, required=True, help='email receiver')
    parser.add_argument('--password', type=str, required=False, help='email password', default=None)
    parser.add_argument('--title', type=str, required=True, help='email title')
    parser.add_argument('--content', type=str, required=False, help='email content', default='')
    parser.add_argument('--content_file', type=str, required=False, help='email content file', default='')
    parser.add_argument('--save_config', type=str, required=False, help='save configs such as sender, smtp, receiver, password at ~/.python-email-sender/config', default='')
    
    args = parser.parse_args()
    
    if len(args.content) == 0 and len(args.content_file) == 0:
        raise ValueError('content or content_file should be provided')
    elif len(args.content) > 0 and len(args.content_file) > 0:
        raise ValueError('only one of content or content_file should be provided')
    
    if len(args.content_file) > 0:
        with open(args.content_file, 'r') as f:
            args.content = f.read()
        
    if len(args.save_config) > 0 and args.password is not None:
        os.makedirs(f'{home_directory}/.python-email-sender', exist_ok=True)
        with open(f'{home_directory}/.python-email-sender/config', 'a') as f:
            f.write(f'sender={args.sender}\n')
            f.write(f'smtp={args.smtp}\n')
            f.write(f'receiver={args.receiver}\n')
            f.write(f'password={args.password}\n')
        print('Config file is saved at ~/.python-email-sender/config')
    
    if args.password is None:
        if os.path.isfile(f'{home_directory}/.python-email-sender/config'):
            with open(f'{home_directory}/.python-email-sender/config', 'r') as f:
                lines = f.readlines()
                for line in lines:
                    key, value = line.strip().split('=')
                    if key == 'password':
                        args.password = value
    
    return args

def sendmail(args):
    # smpt 서버와 연결
    gmail_smtp = args.smtp  # gmail smtp 주소
    gmail_port = 465  # gmail smtp 포트번호. 고정(변경 불가)
    smtp = smtplib.SMTP_SSL(gmail_smtp, gmail_port)
    
    # 로그인
    my_account = args.sender
    my_password = args.password
    smtp.login(my_account, my_password)
    
    # 메일을 받을 계정
    to_mail = args.receiver
    
    # 메일 기본 정보 설정
    msg = MIMEMultipart()
    msg["Subject"] = args.title  # 메일 제목
    msg["From"] = my_account
    msg["To"] = to_mail
    
    # 메일 본문 내용
    content = args.content
    content_part = MIMEText(content, "plain")
    msg.attach(content_part)
    
    def send_email(my_account, to_mail, msg):
        smtp.sendmail(my_account, to_mail, msg.as_string())
    
    # 받는 메일 유효성 검사 거친 후 메일 전송
    send_email(my_account, to_mail, msg)
    
    # smtp 서버 연결 해제
    smtp.quit()