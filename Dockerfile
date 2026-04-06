# 파이썬 경량화 버전(slim) 사용
FROM python:3.11-slim

# 환경 변수 설정
# PYTHONDONTWRITEBYTECODE: 파이썬이 .pyc 파일을 쓰지 않도록 설정
# PYTHONUNBUFFERED: 파이썬 출력을 버퍼링 없이 즉시 출력하도록 설정
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TZ=Asia/Seoul

# 작업 디렉토리 설정
WORKDIR /app

# Docker 레이어 캐싱을 활용해 빌드 속도를 높이기 위해 requirements.txt를 먼저 복사
COPY requirements.txt .

# 패키지 설치
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 나머지 소스 코드 복사
COPY . .

# 컨테이너 외부로 노출할 포트 설정 (FastAPI 기본 8000)
EXPOSE 8000

# 앱 실행 명령어
# 외부 접속이 가능하도록 --host 0.0.0.0 으로 설정
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
