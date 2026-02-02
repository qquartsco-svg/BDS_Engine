# 우울증 연구용 시뮬레이션 요구사항

**작성일**: 2025-01-26  
**목적**: 실제 우울증 연구 자료로 의미있는 분석 결과 도출을 위한 요구사항 정의

---

## 🎯 핵심 목표

> **"실제 우울증에 대한 연구자료로 의미있는 분석결과가 도출되는 시뮬레이션"**

이것은 단순한 시뮬레이션이 아니라, **연구 논문에 사용 가능한 데이터를 생성하는 도구**여야 합니다.

---

## 📚 실제 우울증 연구 자료 기반 요구사항

### 1. 신경생물학적 기전

#### 도파민 시스템
- **연구 근거**: 우울증에서 도파민 보상 경로의 기능 저하
- **필수 구현**:
  - Tonic dopamine 감소
  - Phasic dopamine 반응 약화
  - 보상 민감도 감소
  - 무쾌감증 (anhedonia) 모델링

#### 세로토닌 시스템
- **연구 근거**: 우울증에서 세로토닌 전달 감소
- **필수 구현**:
  - 세로토닌 농도 모델
  - SSRI 효과 시뮬레이션
  - 기분 조절 메커니즘

#### 노르에피네프린 시스템
- **연구 근거**: 각성 및 에너지 조절
- **필수 구현**:
  - 각성 수준 모델
  - 에너지 대사 연동
  - 스트레스 반응

### 2. 뇌 영역별 기능

#### 전전두엽 피질 (PFC)
- **연구 근거**: 인지 제어, 부정적 편향, 반추
- **필수 구현**:
  - 인지 제어 기능 저하
  - 부정적 편향 강화
  - 반추 루프 지속

#### 편도체 (Amygdala)
- **연구 근거**: 부정적 감정 처리 과활성화
- **필수 구현**:
  - 부정적 자극 과민 반응
  - 공포/불안 반응 증가
  - 감정 조절 실패

#### 시상하부 (Hypothalamus)
- **연구 근거**: 에너지 대사, 수면-각성 조절
- **필수 구현**:
  - 에너지 고갈 모델
  - 수면 장애
  - 항상성 조절 실패

#### 선조체 (Basal Ganglia)
- **연구 근거**: 동기, 보상 처리
- **필수 구현**:
  - 동기 감소
  - 보상 민감도 감소
  - 행동 시작 어려움

### 3. 시간 스케일

#### 단기 (초-분)
- **연구 근거**: 즉각적 인지 반응, 감정 조절
- **필수 구현**:
  - 실시간 인지 처리
  - 감정 반응 시간
  - 의사결정 과정

#### 중기 (시간-일)
- **연구 근거**: 기분 변화, 에너지 변동
- **필수 구현**:
  - 일일 에너지 변동
  - 기분 변화 패턴
  - 수면-각성 주기

#### 장기 (주-월)
- **연구 근거**: 우울증 발병, 회복 과정
- **필수 구현**:
  - 우울증 발병 과정
  - 치료 반응
  - 재발 패턴

---

## 📊 연구 분석 결과 도출 요구사항

### 1. 통계적 유의성

**필수 요소:**
- 충분한 샘플 수 (N ≥ 30 권장)
- 통제 그룹 비교
- 통계 검정 (t-test, ANOVA, etc.)
- 효과 크기 (Cohen's d)
- 신뢰 구간

**구현 방법:**
- Seed sweep (다중 시뮬레이션)
- 통계 분석 모듈
- 결과 리포트 생성

### 2. 생물학적 타당성 검증

**필수 요소:**
- 뇌 영역 활성화 패턴
- 신경전달물질 농도
- 에너지 대사 패턴
- 시간 스케일 일치

**검증 방법:**
- 기존 연구 자료와 비교
- 생물학적 제약 조건 검증
- 물리적 타당성 테스트

### 3. 임상적 관련성

**필수 요소:**
- DSM-5/ICD-11 기준 매핑
- 임상 스케일 (HAM-D, BDI, PHQ-9)
- 증상 패턴 재현
- 개인차 모델링

**검증 방법:**
- 실제 환자 데이터와 비교
- 임상 전문가 검토
- 통계적 유의성 검증

---

## 🔬 의미있는 분석 결과 도출을 위한 필수 기능

### 1. 다중 시뮬레이션 (Seed Sweep)

**목적**: 통계적 유의성 확보

**구현:**
```python
# 연구용 시뮬레이션
results = []
for seed in range(100):  # N=100
    simulator = DepressionSimulator(seed=seed)
    result = simulator.simulate_full_assessment()
    results.append(result)

# 통계 분석
statistical_analysis = StatisticalValidator(results)
print(f"평균 에너지: {statistical_analysis.mean_energy:.2f}")
print(f"95% 신뢰구간: {statistical_analysis.confidence_interval}")
print(f"효과 크기: {statistical_analysis.cohens_d}")
```

### 2. 통제 그룹 비교

**목적**: 정상 vs 우울증 비교

**구현:**
```python
# 정상 그룹
normal_group = []
for seed in range(50):
    simulator = DepressionSimulator(
        seed=seed,
        initial_energy=100.0,  # 정상
        recovery_inhibition=1.0  # 정상 회복
    )
    normal_group.append(simulator.simulate())

# 우울증 그룹
depression_group = []
for seed in range(50):
    simulator = DepressionSimulator(
        seed=seed,
        initial_energy=60.0,  # 우울증
        recovery_inhibition=0.7  # 회복 억제
    )
    depression_group.append(simulator.simulate())

# 통계 비교
comparison = StatisticalComparison(normal_group, depression_group)
print(f"t-test p-value: {comparison.t_test_p}")
print(f"Cohen's d: {comparison.cohens_d}")
```

### 3. 생체지표 매핑

**목적**: 실제 연구 자료와 비교 가능

**구현:**
```python
# 생체지표 추출
biomarkers = simulator.extract_biomarkers()

# fMRI 활성화 패턴
fmri_pattern = biomarkers.get_fmri_pattern()
# PFC 활성화 감소
# Amygdala 활성화 증가

# EEG 패턴
eeg_pattern = biomarkers.get_eeg_pattern()
# Alpha 파 감소
# Beta 파 증가

# HRV (심박 변이도)
hrv = biomarkers.get_hrv()
# RMSSD 감소 (부교감 신경 활성 감소)
```

### 4. 시간 경과 분석

**목적**: 우울증 발병/회복 과정 관찰

**구현:**
```python
# 장기 추적
long_term_tracking = simulator.track_long_term(
    duration_days=30,
    sampling_interval_hours=1
)

# 에너지 변동 패턴
energy_trajectory = long_term_tracking.get_energy_trajectory()
# 일일 변동
# 주간 변동
# 회복/악화 패턴

# 시각화
visualizer.plot_trajectory(energy_trajectory)
```

### 5. 개인차 모델링

**목적**: 우울증 하위 유형 분석

**구현:**
```python
# 에너지 기반 우울증
energy_based = DepressionSimulator(
    energy_depletion_rate=0.8,  # 높은 에너지 고갈
    negative_bias_strength=0.4  # 낮은 부정적 편향
)

# 인지 기반 우울증
cognitive_based = DepressionSimulator(
    energy_depletion_rate=0.3,  # 낮은 에너지 고갈
    negative_bias_strength=0.9  # 높은 부정적 편향
)

# 혼합형
mixed = DepressionSimulator(
    energy_depletion_rate=0.6,
    negative_bias_strength=0.7
)
```

---

## 📈 연구 논문용 데이터 형식

### 1. 표 형식 데이터

```python
# 연구용 리포트 생성
report = ResearchReport(simulator)

# 표 1: 그룹별 평균 및 표준편차
table1 = report.generate_table1()
# | 그룹 | N | 평균 에너지 | SD | 95% CI |
# |------|---|------------|----|--------|
# | 정상 | 50 | 85.2 | 12.3 | [81.7, 88.7] |
# | 우울증 | 50 | 45.8 | 15.2 | [41.5, 50.1] |

# 표 2: 통계 검정 결과
table2 = report.generate_table2()
# | 변수 | t-value | p-value | Cohen's d | 95% CI |
```

### 2. 그래프 형식 데이터

```python
# 그림 1: 에너지 변동 패턴
figure1 = report.generate_figure1()
# 시간 경과에 따른 에너지 변화
# 정상 그룹 vs 우울증 그룹

# 그림 2: 뇌 영역 활성화 패턴
figure2 = report.generate_figure2()
# PFC, Amygdala, Hypothalamus 활성화 비교
```

### 3. 통계 분석 결과

```python
# 통계 분석 리포트
stats_report = report.generate_statistical_report()

# 주요 결과
print(f"주요 결과:")
print(f"  - 에너지: t({stats_report.df}) = {stats_report.t_value:.2f}, p = {stats_report.p_value:.4f}")
print(f"  - 효과 크기: d = {stats_report.cohens_d:.2f} ({stats_report.effect_size_interpretation})")
print(f"  - 95% 신뢰구간: [{stats_report.ci_lower:.2f}, {stats_report.ci_upper:.2f}]")
```

---

## ✅ 검증 체크리스트

### 생물학적 타당성
- [ ] 뇌 영역 매핑 정확성
- [ ] 신경전달물질 시스템 정확성
- [ ] 시간 스케일 일치
- [ ] 에너지 대사 모델 정확성

### 임상적 관련성
- [ ] DSM-5/ICD-11 기준 매핑
- [ ] 임상 스케일 통합
- [ ] 증상 패턴 재현
- [ ] 개인차 모델링

### 연구 재현성
- [ ] Seed 관리 시스템
- [ ] 실험 메타데이터
- [ ] 파라미터 문서화
- [ ] 결과 추적성

### 통계적 유의성
- [ ] 충분한 샘플 수
- [ ] 통제 그룹 비교
- [ ] 통계 검정
- [ ] 효과 크기 계산

---

## 🎯 최종 목표

**"실제 우울증 연구 자료로 의미있는 분석 결과 도출"**

이를 위해:
1. ✅ 생물학적 타당성 확보
2. ✅ 임상적 관련성 확보
3. ✅ 통계적 유의성 확보
4. ✅ 연구 재현성 확보
5. ✅ 논문용 데이터 형식 제공

---

**작성자**: GNJz (Qquarts)  
**버전**: 1.0.0  
**최종 업데이트**: 2025-01-26

