# 변경 이력 (Changelog)

**엔진 번호**: UP-1  
**프로젝트**: ThreeBodyBoundaryEngine

---

## [1.2.0] - 2026-02-03

### 추가됨 (Added)
- **L1 레이어 (실패 추적 레이어)**: `FailureAtlas` 구현
  - 실패 기록 생성 및 구조화
  - Condition Signature 생성
  - 붕괴 모드 분류
  - 유사한 실패 패턴 찾기
- **L2 레이어 (실패 학습 레이어)**: `FailureBiasConverter` 구현
  - 실패 → 위험 지형 변환
  - SearchBias 생성
  - STDP-like 감쇠 메커니즘
- **문서화**:
  - 전력 효율 분석 문서
  - 신경생물학적 기초 분석 문서
  - 개념 및 수식 참조 가이드
  - 실험적 상태 명시 문서
- **테스트**: L1, L2 레이어 테스트 추가 (총 21개 테스트)

### 변경됨 (Changed)
- **언어 정제**:
  - 확정적 표현 제거 ("완벽히 일치" → "구조적으로 유사함")
  - 수치 과신 금지 ("구조적으로 가능한 상한" 명시)
  - "LLM 개선" 표현 제거
  - 실험적 상태 명시 추가
- **버전 관리**:
  - 모든 파일을 1.2.0으로 통일
  - Single Source of Truth 구현 (setup.py가 __init__.py에서 버전 읽기)
  - author_email 제거 (가짜 이메일 방지)

### 개선됨 (Improved)
- **주석 및 개념**:
  - 모든 소스 파일의 주석 정확성 확인
  - 개념 명확성 확인
  - 수식 정확성 확인
  - 문서와 코드의 일관성 확인

### 문서화
- `EXPERIMENTAL_STATUS.md`: 실험적 소프트웨어 상태 명시
- `COMMENT_CONCEPT_REVIEW.md`: 주석 및 개념 점검 보고서
- `NEXT_WORK_CHECKLIST.md`: 다음 작업 체크리스트
- `WORK_STATUS_SUMMARY.md`: 작업 상황 정리

---

## [1.2.1] - 2026-02-03

### 추가됨 (Added)
- **통합 API(Facade Pattern)**: `ThreeBodyBoundaryEngine.run()` 추가
  - L0 → L1 → L2 파이프라인을 단일 진입점으로 실행
  - `enable_l1`, `enable_l2` 스위치로 레이어 on/off 지원
  - L2 활성화 시 FailureAtlas 미존재 상황은 `ValueError`로 명시적 차단
- **표준 결과 모델**: `EngineRunResult`
  - `analysis(L0)`, `failure_atlas(L1)`, `search_bias(L2)`, `last_failure_record` 고정 구조 제공

### 변경됨 (Changed)
- README / API_REFERENCE의 퀵스타트 예제를 `run()` 기반으로 동기화

### 테스트 (Tests)
- `run()` 경로 및 스위치 조합 테스트 추가
- 전체 테스트 23개 통과

## [1.1.0] - 2026-02-02

### 추가됨 (Added)
- **L0 레이어 (원인 분석 레이어)**: `ThreeBodyBoundaryEngine` 구현
  - 중력 퍼텐셜 계산
  - 경계 정합 분석
  - 안정성 판정
- **기본 문서화**:
  - README.md (한국어/영어)
  - API Reference
  - 사용 가이드
  - 레이어 아키텍처 문서

---

## [1.0.0] - 2026-02-01

### 추가됨 (Added)
- **초기 릴리즈**:
  - ThreeBodyBoundaryEngine 기본 구조
  - 경계 정합 관점 도입
  - 기본 수식 구현

---

**형식**: [Keep a Changelog](https://keepachangelog.com/ko/1.0.0/)  
**버전 관리**: [Semantic Versioning](https://semver.org/lang/ko/)
