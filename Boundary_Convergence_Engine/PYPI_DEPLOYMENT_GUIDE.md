# Boundary Convergence Engine PyPI 배포 가이드

**작성일**: 2026-02-02  
**엔진 번호**: 9번  
**버전**: 1.0.0

---

## 📋 배포 준비 상태

### ✅ 완료된 항목
- [x] 패키징 파일 작성 (setup.py, pyproject.toml)
- [x] 빌드 완료 (dist/ 폴더 확인)
- [x] README.md 작성 (한국어/영어)
- [x] LICENSE 추가

---

## 🚀 PyPI 배포 단계

### Step 1: 빌드 확인
```bash
cd Engines/Independent/Boundary_Convergence_Engine/
python3 -m build
ls -la dist/
```

예상 출력:
- `boundary_convergence_engine-1.0.0.tar.gz`
- `boundary_convergence_engine-1.0.0-py3-none-any.whl`

### Step 2: PyPI 계정 준비
1. PyPI 계정 생성 (https://pypi.org/account/register/)
2. API 토큰 생성 (https://pypi.org/manage/account/token/)

### Step 3: 배포 실행
```bash
# twine 설치 (필요시)
pip install twine

# 배포
twine upload dist/*
```

또는 API 토큰을 사용:
```bash
twine upload dist/* --username __token__ --password pypi-<your-token>
```

---

## 📝 배포 후 확인

### 설치 테스트
```bash
pip install boundary-convergence-engine
python3 -c "from boundary_convergence_engine import BoundaryConvergenceEngine; print('✅ 설치 성공')"
```

### PyPI 페이지 확인
https://pypi.org/project/boundary-convergence-engine/

---

## ⚠️ 주의사항

1. **버전 관리**: 같은 버전은 재배포 불가
2. **패키지 이름**: `boundary-convergence-engine` (하이픈 사용)
3. **의존성**: 표준 라이브러리만 사용 (추가 설치 불필요)

---

**작성자**: GNJz (Qquarts)  
**버전**: 1.0.0
