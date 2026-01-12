# 🚀 Quick Heroku Deployment Guide (빠른 배포 가이드)

## 배포 준비 완료! ✅

모든 Heroku 배포 파일이 준비되었습니다. 이제 배포만 하면 됩니다!

---

## 방법 1: GitHub 연동으로 배포 (가장 쉬움! 추천 👍)

### 1단계: Heroku 계정 생성 및 로그인
1. https://signup.heroku.com/ 에서 무료 계정 생성
2. 이메일 인증 완료

### 2단계: 새 앱 생성
1. Heroku Dashboard로 이동: https://dashboard.heroku.com/
2. "New" → "Create new app" 클릭
3. 앱 이름 입력 (예: `chamjoheum-erp`) 또는 자동 생성
4. Region: United States 선택
5. "Create app" 클릭

### 3단계: GitHub 연동
1. "Deploy" 탭 클릭
2. Deployment method에서 "GitHub" 선택
3. "Connect to GitHub" 클릭하고 인증
4. Repository 검색: `ParkChongsam/awesome-flutter`
5. "Connect" 클릭
6. Branch 선택: `claude/flask-erp-project-setup-yVcfM`

### 4단계: PostgreSQL 데이터베이스 추가
1. "Resources" 탭 클릭
2. Add-ons 검색창에 "postgres" 입력
3. "Heroku Postgres" 선택
4. Plan: "Essential 0" (무료) 선택
5. "Submit Order Form" 클릭

### 5단계: 환경 변수 설정
1. "Settings" 탭 클릭
2. "Reveal Config Vars" 클릭
3. 다음 변수 추가:
   ```
   KEY                VALUE
   FLASK_ENV          production
   SECRET_KEY         [Generate strong random key - 아래 참조]
   COMPANY_NAME       참좋은복사기
   COMPANY_NAME_EN    Very Good Copy Machine
   ```

**SECRET_KEY 생성 방법:**
```python
# Python에서 실행
import secrets
print(secrets.token_hex(32))
```
또는 온라인: https://randomkeygen.com/

### 6단계: 배포 실행
1. "Deploy" 탭으로 돌아가기
2. "Manual deploy" 섹션에서
3. Branch: `claude/flask-erp-project-setup-yVcfM` 선택
4. "Deploy Branch" 클릭 🚀
5. 배포 로그를 확인하며 대기 (2-3분 소요)
6. "View" 버튼 클릭하여 앱 열기

### 7단계: 데이터베이스 초기화
1. "More" → "Run console" 클릭
2. 다음 명령어 입력:
   ```bash
   flask init-db
   ```
3. "Run" 클릭
4. 초기 데이터가 생성됩니다 (admin 계정 포함)

### 8단계: 앱 접속 및 로그인
1. 앱 URL로 이동 (예: https://chamjoheum-erp.herokuapp.com)
2. 기본 관리자 계정으로 로그인:
   - Username: `admin`
   - Password: `admin123`
3. **즉시 비밀번호 변경!**

---

## 방법 2: Heroku CLI로 배포 (개발자용)

### 1단계: Heroku CLI 설치

**macOS:**
```bash
brew tap heroku/brew && brew install heroku
```

**Ubuntu/Debian:**
```bash
curl https://cli-assets.heroku.com/install-ubuntu.sh | sh
```

**Windows:**
- https://devcenter.heroku.com/articles/heroku-cli 에서 설치

### 2단계: 로그인
```bash
heroku login
```

### 3단계: 프로젝트로 이동
```bash
cd flask-erp-system
```

### 4단계: Heroku 앱 생성
```bash
# 자동 이름 생성
heroku create

# 또는 특정 이름으로
heroku create chamjoheum-erp
```

### 5단계: PostgreSQL 추가
```bash
heroku addons:create heroku-postgresql:essential-0
```

### 6단계: 환경 변수 설정
```bash
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
heroku config:set COMPANY_NAME="참좋은복사기"
heroku config:set COMPANY_NAME_EN="Very Good Copy Machine"
```

### 7단계: 배포
```bash
# Heroku remote 추가 (이미 create 했다면 생략)
heroku git:remote -a your-app-name

# 배포
git push heroku claude/flask-erp-project-setup-yVcfM:main
```

### 8단계: 데이터베이스 초기화
```bash
heroku run flask init-db
```

### 9단계: 앱 열기
```bash
heroku open
```

---

## 배포 후 확인사항 ✓

- [ ] 앱이 정상적으로 열림
- [ ] 로그인 페이지 표시
- [ ] admin/admin123으로 로그인 가능
- [ ] 대시보드 표시
- [ ] 데이터베이스 연결 정상
- [ ] 모든 메뉴 접근 가능

---

## 유용한 명령어

```bash
# 로그 확인
heroku logs --tail

# 앱 재시작
heroku restart

# 데이터베이스 정보
heroku pg:info

# 환경 변수 확인
heroku config

# 앱 정보
heroku info

# 데이터베이스 백업
heroku pg:backups:capture

# 콘솔 접속
heroku run flask shell
```

---

## 문제 해결

### "Application Error" 발생 시
```bash
heroku logs --tail
heroku restart
```

### 데이터베이스 연결 오류
```bash
heroku pg:info
heroku config:get DATABASE_URL
```

### 앱이 느리게 응답
- 무료 dyno는 30분 비활성 후 sleep 모드
- 첫 요청 시 15-30초 소요 (정상)
- Hobby dyno로 업그레이드 고려 ($7/월)

---

## 배포 파일 목록 ✅

모든 필수 파일이 준비되었습니다:

- ✅ **Procfile** - Gunicorn 웹 서버 설정
- ✅ **runtime.txt** - Python 3.11.7
- ✅ **app.json** - Heroku 앱 메타데이터
- ✅ **requirements.txt** - gunicorn 포함
- ✅ **.slugignore** - 불필요한 파일 제외
- ✅ **config.py** - DATABASE_URL 호환성 수정
- ✅ **DEPLOY.md** - 상세 배포 가이드

---

## 다음 단계

1. ⚠️ **admin 비밀번호 변경** (매우 중요!)
2. 샘플 데이터 입력 및 테스트
3. 사용자 계정 추가
4. 커스텀 도메인 연결 (선택)
5. SSL 인증서 설정 (Heroku 자동 제공)
6. 정기 백업 설정

---

## 추가 리소스

- 📖 상세 배포 가이드: `DEPLOY.md`
- 📚 Heroku 문서: https://devcenter.heroku.com/
- 🆘 Heroku 지원: https://help.heroku.com/

---

**배포 준비 완료! 이제 위의 방법 중 하나를 선택하여 배포하세요! 🚀**

**참좋은복사기 (Very Good Copy Machine) ERP System**
