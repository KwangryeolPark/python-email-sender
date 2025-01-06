from setuptools import setup, find_packages

setup(
    name='python-email-sender',
    version='0.0.4',
    description='Python package for sending email',
    author='Kwangryeol Park',
    author_email='pkr7098@gmail.com',
    url='',
    packages=find_packages(),  # 이 부분을 수정하여 모든 패키지를 자동으로 찾도록 함
    package_data={},
)
