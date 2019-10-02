# CentOS 7에 Khaiii 설치하기

Linux CentOS 7 계열에  Khaiii 형태소 분석기를 설치하고 사용하는 방법

## Python 3.x 설치

Khaiii 형태소 분석기를 설치하기 위해서는 python 3 이상이 깔려 있어야한다.

```bash
yum install -y https://centos7.iuscommunity.org/ius-release.rpm

yum install -y python36u python36u-libs python36u-devel python36u-pip
```

이 상태에서 ```python``` 을 실행시키면 구 버전인 2.xx 버전이 실행되므로 alias 를 변경하여 3.6 버전이 실행되도록 해야한다.

```bash
# root 권한이 필요한 경우 sudo 명령과 함께 사용

unlink /bin/python
ln -s /bin/python3.6 /bin/python3
ln -s /bin/pip3.6 /bin/pip
```

여기 까지 진행하면 python 이 3.6  버전으로 잘 실행 되지만 `yum` 에서 에러가 발생한다. yum 이 python 2.x 버전의 문법을 사용하기 때문이다. 그래서 yum 이 phython 2.x 버전을 사용하도록 2 가지 파일의 설정을 바꿔 줘야한다.

```bash
vim /usr/bin/yum
#!/usr/bin/python
==>
#!/usr/bin/python2
```

