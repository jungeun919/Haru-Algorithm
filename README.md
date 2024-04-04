# 하루 알고리즘 (팀명: DA풀어)

![image](./static/haru.gif)

## 프로젝트 소개
haru algorithm은 로그인 과정 없이 간단하게 하루마다 하나의 랜덤 알고리즘 문제를 제공하여 채점을 받아볼 수 있습니다.<br>
정답 풀이는 포인트 사용 및 다른 패널티 없이 언제든 누구나 확인 가능합니다.<br>
또한 문제풀이 시 카테고리를 제공하지 않아서 다양한 접근법으로 문제를 풀 수 있습니다.<br>
어떤 문제를 먼저 풀어야 할지 고민할 필요 없이 하루 한 문제씩 지속적으로 다양한 유형의 문제를 학습해 보세요!<br>

<br>

## 개발 환경
* Frontend: HTML/CSS, Javascript
* Backend: Django, sqlite3
* Infra: Naver Cloud Platform

<br>

## 팀원
* Frontend : 김지연, 박미란
* Backend : 이지수, 최정은
* Design : 박근영

<br>

## 실행 방법
1. 가상 환경 생성 및 활성화
```bash
# macOS user의 경우
python3 -m venv [가상환경명]
source [가상환경명]/bin/activate

# window user의 경우
python -m venv [가상환경명]
source [가상환경명]/scripts/activate
```

2. 관련 패키지 설치
```bash
pip3 install -r requirements.txt
```

3. 마이그레이션 적용 후 서버 실행
```bash
python3 manage.py migrate
python3 manage.py runserver
```
