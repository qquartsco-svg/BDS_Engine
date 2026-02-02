# 엔진 분리 실행 계획

**작성일**: 2026-02-02  
**목적**: ThreeBodyBoundaryEngine에서 해결 탐색 기능 제거 및 원인 분석만 남기기

---

## 🎯 목표

### 현재 상태
- ThreeBodyBoundaryEngine에 원인 분석 + 해결 탐색이 섞여 있음
- 해결 탐색 기능은 프로토타입 단계, 작동하지 않음

### 목표 상태
- ThreeBodyBoundaryEngine: 원인 분석만 (완성)
- 해결 탐색 기능: 별도 모듈로 분리 (나중에 구현)

---

## 📋 작업 계획

### Phase 1: 해결 탐색 기능 제거 (즉시)

**작업 내용**:
1. `recover_boundary_alignment()` 메서드 제거
2. `stabilize_system()` 메서드 제거
3. `apply_dynamic_correction()` 메서드 제거
4. 관련 데이터 모델 제거:
   - `RecoveryResult`
   - `StabilizationResult`
   - `CorrectionResult`

**파일 수정**:
- `src/three_body_boundary_engine/three_body_boundary_engine.py`
- `src/three_body_boundary_engine/models.py`
- `src/three_body_boundary_engine/__init__.py`

**예상 시간**: 1-2시간

---

### Phase 2: 문서 업데이트 (즉시)

**작업 내용**:
1. README.md 업데이트
   - 해결 탐색 기능 언급 제거
   - 원인 분석만 강조
2. API 문서 업데이트
3. 예제 코드 정리
   - `solution_example.py` 제거 또는 별도 폴더로 이동

**파일 수정**:
- `README.md`
- `examples/basic_usage.py`
- `examples/solution_example.py` (제거 또는 이동)

**예상 시간**: 1시간

---

### Phase 3: 테스트 업데이트 (즉시)

**작업 내용**:
1. 해결 탐색 관련 테스트 제거
2. 원인 분석 테스트만 유지
3. 테스트 실행 및 검증

**파일 수정**:
- `tests/test_three_body_boundary_engine.py`
- 기타 해결 탐색 관련 테스트

**예상 시간**: 1시간

---

### Phase 4: 버전 업데이트 (즉시)

**작업 내용**:
1. 버전 번호 업데이트
   - v1.0.0 → v1.1.0 (원인 분석 전용)
2. CHANGELOG 작성
3. GitHub 태그 생성

**예상 시간**: 30분

---

## 🔧 구체적 작업 내용

### 1. three_body_boundary_engine.py 수정

**제거할 메서드**:
```python
# 제거
def recover_boundary_alignment(...) -> RecoveryResult
def stabilize_system(...) -> StabilizationResult
def apply_dynamic_correction(...) -> CorrectionResult
```

**유지할 메서드**:
```python
# 유지
def analyze_orbit_stability(...) -> StabilityAnalysis
def observe_boundary_formation(...) -> BoundaryDynamics
def observe_lagrange_points(...) -> LagrangeAnalysis
def compare_stability_conditions(...) -> List[StabilityAnalysis]
```

---

### 2. models.py 수정

**제거할 클래스**:
```python
# 제거
@dataclass
class RecoveryResult
@dataclass
class StabilizationResult
@dataclass
class CorrectionResult
```

**유지할 클래스**:
```python
# 유지
@dataclass
class StabilityAnalysis
@dataclass
class BoundaryDynamics
@dataclass
class LagrangeAnalysis
```

---

### 3. __init__.py 수정

**제거할 export**:
```python
# 제거
RecoveryResult
StabilizationResult
CorrectionResult
```

**유지할 export**:
```python
# 유지
ThreeBodyBoundaryEngine
ThreeBodyConfig
ThreeBodySystem
StabilityAnalysis
BoundaryDynamics
LagrangeAnalysis
Body
Point
```

---

## 📝 체크리스트

### Phase 1: 코드 제거
- [ ] `recover_boundary_alignment()` 제거
- [ ] `stabilize_system()` 제거
- [ ] `apply_dynamic_correction()` 제거
- [ ] `RecoveryResult` 제거
- [ ] `StabilizationResult` 제거
- [ ] `CorrectionResult` 제거
- [ ] `__init__.py` 업데이트

### Phase 2: 문서 업데이트
- [ ] README.md 업데이트
- [ ] API 문서 업데이트
- [ ] `solution_example.py` 제거/이동
- [ ] 주석 업데이트

### Phase 3: 테스트 업데이트
- [ ] 해결 탐색 테스트 제거
- [ ] 원인 분석 테스트만 유지
- [ ] 테스트 실행 및 검증

### Phase 4: 버전 업데이트
- [ ] 버전 번호 업데이트
- [ ] CHANGELOG 작성
- [ ] GitHub 태그 생성

---

## 🚀 실행 순서

1. **백업 생성**
   ```bash
   git checkout -b backup-before-separation
   git push origin backup-before-separation
   ```

2. **Phase 1 실행**: 코드 제거
3. **Phase 2 실행**: 문서 업데이트
4. **Phase 3 실행**: 테스트 업데이트
5. **Phase 4 실행**: 버전 업데이트

6. **검증**
   - 모든 테스트 통과 확인
   - 예제 코드 실행 확인
   - 문서 일관성 확인

7. **커밋 및 푸시**
   ```bash
   git add .
   git commit -m "Separate causal analysis from solution exploration

   - Remove solution exploration methods (prototype stage)
   - Keep only causal analysis methods (production ready)
   - Update documentation and examples
   - Version: 1.1.0 (causal analysis only)"
   git push origin main
   ```

---

## ⚠️ 주의사항

1. **해결 탐색 기능은 완전히 제거하지 말고 별도 브랜치에 보관**
   - 나중에 별도 모듈로 구현할 때 참고

2. **원인 분석 기능은 절대 손상시키지 않음**
   - 모든 원인 분석 메서드는 그대로 유지

3. **문서는 철학을 반영하여 업데이트**
   - "원인 분석 전용" 명확히 표시
   - 해결 탐색은 "별도 모듈로 예정" 표시

---

## 📊 예상 결과

### Before (현재)
```
ThreeBodyBoundaryEngine
├── 원인 분석 (완성) ✅
└── 해결 탐색 (프로토타입) ❌
```

### After (목표)
```
ThreeBodyBoundaryEngine (v1.1.0)
└── 원인 분석만 (완성) ✅

SolutionExplorationEngine (미래)
└── 해결 탐색 (별도 모듈로 구현 예정)
```

---

**작성자**: GNJz (Qquarts)  
**버전**: 1.0.0  
**실행 예정일**: 즉시

