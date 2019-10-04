# CentOS 7에 Khaiii 설치하기

Linux CentOS 7 계열에  Khaiii 형태소 분석기를 설치하고 사용하는 방법

## Python 3.6 설치

### python 설치

Khaiii 형태소 분석기를 설치하기 위해서는 python 3 이상이 깔려 있어야한다.

```bash
yum install -y https://centos7.iuscommunity.org/ius-release.rpm
yum install -y python36u python36u-libs python36u-devel python36u-pip
```

위 상태에서 ```python``` 을 실행시키면 구 버전인 2.xx 버전이 실행되므로 alias 를 변경하여 3.6 버전이 실행되도록 해야한다.

```bash
# root 권한이 필요한 경우 sudo 명령과 함께 사용

unlink /bin/python
ln -s /bin/python3.6 /bin/python3
ln -s /bin/pip3.6 /bin/pip
```

### yum 에러 해결

위까지 진행하면 python 이 3.6  버전으로 잘 실행 되지만 `yum` 에서 에러가 발생한다. yum 이 python 2.x 버전의 문법을 사용하기 때문이다. 그래서 yum 이 phython 2.x 버전을 사용하도록 2 가지 파일의 설정을 바꿔 줘야한다.

```bash
vim /usr/bin/yum

#!/usr/bin/python
==>
#!/usr/bin/python2
```

```bash
vim /usr/libexec/urlgrabber-ext-down

#!/usr/bin/python
==>
#!/usr/bin/python2
```

여기까지 진행하면 Python 3.x 설치와 관련된 모든 작업을 완료한 것이다.

### CMake 설치

나중에 khaiii 소스를 컴파일하기 위한 빌드 툴인 CMake 를 설치한다.

```bash
# /usr/local 디렉토리에 쓰기 권한이 있어야한다. 없다면 sudo 와 함께 사용.

pip intall cmake
```

## gcc 4.9+ 설치

khaiii 소스를 받아서 컴파일 하려면 gcc 가 필요하다. 그 중에서도 4.9 이상의 버전이 필요하므로 아래와 같이 설치한다.

### gcc 설치

```bash
sudo yum install -y centos-release-scl-rh
sudo yum install -y devtoolset-4-gcc devtoolset-4-gcc-c++
```

### 활성화 및 버전 확인

설치가 되었다고 바로 되는 것은 아니고 아래와 같이 활성화 시켜줘야 한다. 계정 혹은 터미널이 바뀌거나 재접속 할시에는 다시 활성화 시켜줘야한다- 쓸 이 있다면. ~~매번 자동으로 활성화 시키는 방법은 알아보기 귀찮아요.~~

```bash
scl enable devtoolset-4 bash
gcc --version
gcc (GCC) 5.2.1 20150902 (Red Hat 5.2.1-2)
Copyright (C) 2015 Free Software Foundation, Inc.
This is free software; see the source for copying conditions. There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
```

## git 설치 및 Khaiii 소스 다운로드

이제 모든 도구들이 갖추어졌으므로 khaiii 소스를 다운받기위해 git를 설치한다.

### git 설치

```bash
sudo yum install git
```

### khaiii 소스 다운로드

적당한 디렉토리로 이동하여 소스를 클론 뜬다.

```bash
git clone https://github.com/kakao/khaiii.git
```

### 설치 준비

```bash
cd khaiii
mkdir build
cd build
```

## 설치 시작!

이제 모든 준비가 되었으므로 설치를 시작한다. 

설치 과정은 정식 문서인 :point_right:[이곳](https://github.com/kakao/khaiii/wiki/%EB%B9%8C%EB%93%9C-%EB%B0%8F-%EC%84%A4%EC%B9%98#%EB%B9%8C%EB%93%9C)을 참조 하도록 한다.

```-끝-```
