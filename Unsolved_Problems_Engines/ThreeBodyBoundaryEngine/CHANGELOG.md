# 변경 이력 (Changelog)

## [1.1.0] - 2026-02-02

### 변경 사항

#### 아키텍처 변경
- **원인 분석과 해결 탐색 분리**: 아키텍처 철학에 따라 엔진을 분리
- 해결 탐색 기능 제거 (별도 모듈로 분리 예정)
- 원인 분석 전용으로 명확화

#### 제거된 기능
- `recover_boundary_alignment()` - 경계 정합 복구 (프로토타입 단계)
- `stabilize_system()` - 안정화 메커니즘 (프로토타입 단계)
- `apply_dynamic_correction()` - 동적 보정 (프로토타입 단계)
- `RecoveryResult`, `StabilizationResult`, `CorrectionResult` 데이터 모델

#### 유지된 기능
- ✅ `analyze_orbit_stability()` - 궤도 안정성 분석
- ✅ `observe_boundary_formation()` - 경계 형성 과정 관찰
- ✅ `observe_lagrange_points()` - 라그랑주 점 경계 관찰
- ✅ `compare_stability_conditions()` - 안정/불안정 조건 비교

#### 문서
- 아키텍처 철학 문서 추가 (`docs/ARCHITECTURE_PHILOSOPHY.md`)
- 분리 실행 계획 문서 추가 (`docs/SEPARATION_ACTION_PLAN.md`)
- README 업데이트 (원인 분석 전용 명시)

#### 예제
- `solution_example.py` 아카이브 이동 (해결 탐색 예제)

---

## [1.0.0] - 2026-02-02

### 초기 릴리스
- 원인 분석 기능 구현
- 해결 탐색 기능 (프로토타입, v1.1.0에서 제거됨)

