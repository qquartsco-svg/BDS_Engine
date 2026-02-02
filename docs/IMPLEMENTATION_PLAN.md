# 전체 구현 계획서

**작성일**: 2025-01-26  
**목적**: 의료 연구용 vs 엔지니어링 관점 분리 및 실제 우울증 연구 자료 기반 시뮬레이션 구현

---

## 🎯 핵심 목표

### 의료 연구용
> **"실제 우울증에 대한 연구자료로 의미있는 분석결과가 도출되는 시뮬레이션"**

- 생물학적 타당성 확보
- 임상적 관련성 확보
- 연구 재현성 확보
- 통계적 유의성 확보
- 논문용 데이터 생성

### 엔지니어링 관점
> **"동역학 메커니즘을 정확히 이해하고 확장 가능한 시스템 설계"**

- 동역학 정확성
- 모듈화 및 재사용성
- 성능 최적화
- 아키텍처 명확성

---

## 📊 현재 상태 분석

### ✅ 완료된 항목
- 우울증 시뮬레이터 기본 구조
- 공통 엔진 (NegativeBias, CognitiveControl, EnergyDepletion)
- 우울증 특화 엔진 (Motivation)
- Cookiie Brain Engine 통합
- 우울증 특화 태스크 3종
- 기본 시각화

### ⚠️ 부족한 항목 (의료 연구용)
- 신경전달물질 시스템 (도파민, 세로토닌, 노르에피네프린)
- 생체지표 매핑 (fMRI, EEG, HRV)
- 통계 분석 도구 (Seed Sweep, 통제 그룹, 효과 크기)
- 임상 스케일 통합 (HAM-D, BDI, PHQ-9)
- 연구 재현성 도구 (메타데이터, 추적성)
- 논문용 데이터 형식

### ⚠️ 부족한 항목 (엔지니어링)
- 구조 분리 (research/engineering/core)
- 동역학 문서화
- 성능 최적화
- 확장성 가이드

---

## 🏗️ Phase 1: 구조 분리 (1주)

### 1.1 디렉토리 구조 생성

```
brain_disorder_simulation/
├── research/                    # 의료 연구용 (NEW)
│   ├── __init__.py
│   ├── depression/
│   │   ├── __init__.py
│   │   ├── clinical_models.py   # 임상 모델
│   │   ├── biomarkers.py         # 생체지표 매핑
│   │   ├── validation.py         # 검증 도구
│   │   └── analysis.py           # 연구 분석 도구
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── statistical.py        # 통계 분석
│   │   └── reporting.py          # 연구 리포트
│   └── clinical_scales.py        # 임상 스케일
│
├── engineering/                 # 엔지니어링 관점 (NEW)
│   ├── __init__.py
│   ├── dynamics/                # 동역학 엔진
│   │   ├── __init__.py
│   │   └── dynamics_analysis.py
│   ├── architecture/            # 시스템 아키텍처
│   │   ├── __init__.py
│   │   └── system_design.py
│   └── optimization/            # 성능 최적화
│       ├── __init__.py
│       └── performance.py
│
└── core/                        # 공통 코어 (기존)
    ├── common/                  # 공통 엔진 (기존)
    ├── disorders/              # 질환별 엔진 (기존)
    └── unified/                 # 통합 시뮬레이터 (기존)
```

### 1.2 기존 코드 분류

**의료 연구용으로 이동:**
- `depression_simulator.py` → `research/depression/clinical_simulator.py`
- 통계 분석 관련 → `research/utils/statistical.py`
- 리포트 생성 → `research/utils/reporting.py`

**엔지니어링 관점으로 이동:**
- 동역학 분석 → `engineering/dynamics/`
- 성능 최적화 → `engineering/optimization/`

**공통 코어 유지:**
- `common/` 엔진들
- `disorders/` 질환별 엔진들
- `unified/` 통합 시뮬레이터

---

## 🔬 Phase 2: 의료 연구용 강화 (2-3주)

### 2.1 신경전달물질 시스템 통합

#### 도파민 시스템
```python
# research/depression/neurotransmitters.py

class DopamineSystem:
    """
    도파민 시스템 모델링
    
    연구 근거:
    - 우울증에서 도파민 보상 경로의 기능 저하
    - Tonic dopamine 감소
    - Phasic dopamine 반응 약화
    """
    def __init__(self):
        self.tonic_dopamine = 1.0  # 기본 도파민 수준
        self.phasic_dopamine = 1.0  # 반응성 도파민
        self.reward_sensitivity = 1.0  # 보상 민감도
        
    def update_from_depression(self, depression_level):
        """우울증 수준에 따른 도파민 변화"""
        # Tonic dopamine 감소
        self.tonic_dopamine = 1.0 - (depression_level * 0.5)
        
        # Phasic dopamine 반응 약화
        self.phasic_dopamine = 1.0 - (depression_level * 0.6)
        
        # 보상 민감도 감소
        self.reward_sensitivity = 1.0 - (depression_level * 0.7)
```

#### 세로토닌 시스템
```python
class SerotoninSystem:
    """
    세로토닌 시스템 모델링
    
    연구 근거:
    - 우울증에서 세로토닌 전달 감소
    - SSRI 효과 시뮬레이션
    """
    def __init__(self):
        self.serotonin_level = 1.0
        self.reuptake_inhibition = 0.0  # SSRI 효과
        
    def update_from_depression(self, depression_level):
        """우울증 수준에 따른 세로토닌 변화"""
        self.serotonin_level = 1.0 - (depression_level * 0.4)
        
    def apply_ssri(self, dose):
        """SSRI 투여 효과"""
        self.reuptake_inhibition = min(1.0, dose)
        self.serotonin_level = min(1.0, 
            self.serotonin_level + (dose * 0.3))
```

#### 노르에피네프린 시스템
```python
class NorepinephrineSystem:
    """
    노르에피네프린 시스템 모델링
    
    연구 근거:
    - 각성 및 에너지 조절
    - 스트레스 반응
    """
    def __init__(self):
        self.norepinephrine_level = 1.0
        self.arousal_level = 1.0
        
    def update_from_depression(self, depression_level):
        """우울증 수준에 따른 노르에피네프린 변화"""
        self.norepinephrine_level = 1.0 - (depression_level * 0.3)
        self.arousal_level = 1.0 - (depression_level * 0.4)
```

### 2.2 생체지표 매핑

#### fMRI 활성화 패턴
```python
# research/depression/biomarkers.py

class FMRIB biomarkers:
    """
    fMRI 활성화 패턴 매핑
    
    연구 근거:
    - PFC 활성화 감소
    - Amygdala 활성화 증가
    - Default Mode Network 과활성화
    """
    def extract_fmri_pattern(self, brain_state):
        """뇌 상태에서 fMRI 패턴 추출"""
        return {
            'pfc_activation': brain_state.pfc_activity,
            'amygdala_activation': brain_state.amygdala_activity,
            'hypothalamus_activation': brain_state.hypothalamus_activity,
            'default_mode_network': brain_state.dmn_activity
        }
```

#### EEG 패턴
```python
class EEGBiomarkers:
    """
    EEG 패턴 매핑
    
    연구 근거:
    - Alpha 파 감소
    - Beta 파 증가
    - Theta/Beta 비율 변화
    """
    def extract_eeg_pattern(self, brain_state):
        """뇌 상태에서 EEG 패턴 추출"""
        return {
            'alpha_power': self._calculate_alpha(brain_state),
            'beta_power': self._calculate_beta(brain_state),
            'theta_beta_ratio': self._calculate_theta_beta(brain_state)
        }
```

#### HRV (심박 변이도)
```python
class HRVBiomarkers:
    """
    HRV (Heart Rate Variability) 매핑
    
    연구 근거:
    - RMSSD 감소 (부교감 신경 활성 감소)
    - LF/HF 비율 변화
    """
    def extract_hrv(self, energy_state, stress_level):
        """에너지 상태에서 HRV 추출"""
        # 에너지가 낮으면 HRV 감소
        rmssd = energy_state.current_energy / 100.0
        return {
            'rmssd': rmssd,
            'lf_hf_ratio': 1.0 + stress_level * 0.5
        }
```

### 2.3 통계 분석 도구

#### Seed Sweep
```python
# research/utils/statistical.py

class StatisticalAnalyzer:
    """
    통계 분석 도구
    
    기능:
    - 다중 시뮬레이션 (Seed Sweep)
    - 통제 그룹 비교
    - 통계 검정 (t-test, ANOVA)
    - 효과 크기 (Cohen's d)
    """
    def seed_sweep(self, simulator_class, n_seeds=100, **params):
        """다중 시뮬레이션 실행"""
        results = []
        for seed in range(n_seeds):
            simulator = simulator_class(seed=seed, **params)
            result = simulator.simulate_full_assessment()
            results.append(result)
        return results
    
    def compare_groups(self, group1, group2):
        """두 그룹 비교"""
        from scipy import stats
        
        # t-test
        t_stat, p_value = stats.ttest_ind(group1, group2)
        
        # Cohen's d
        cohens_d = self._calculate_cohens_d(group1, group2)
        
        # 95% 신뢰구간
        ci = self._calculate_confidence_interval(group1, group2)
        
        return {
            't_statistic': t_stat,
            'p_value': p_value,
            'cohens_d': cohens_d,
            'confidence_interval': ci,
            'effect_size_interpretation': self._interpret_effect_size(cohens_d)
        }
```

### 2.4 임상 스케일 통합

#### HAM-D (Hamilton Depression Rating Scale)
```python
# research/clinical_scales.py

class HAMDMapper:
    """
    HAM-D (Hamilton Depression Rating Scale) 매핑
    
    연구 근거:
    - 표준 우울증 평가 도구
    - 17-21 항목 평가
    """
    def map_to_hamd(self, simulation_results):
        """시뮬레이션 결과를 HAM-D 점수로 매핑"""
        score = 0
        
        # 에너지 고갈 → HAM-D 항목 7 (일과성 업무 및 활동)
        if simulation_results['energy'] < 30:
            score += 3
        elif simulation_results['energy'] < 50:
            score += 2
        elif simulation_results['energy'] < 70:
            score += 1
        
        # 동기 감소 → HAM-D 항목 8 (정신 운동 지연)
        if simulation_results['motivation'] < 0.3:
            score += 3
        elif simulation_results['motivation'] < 0.5:
            score += 2
        elif simulation_results['motivation'] < 0.7:
            score += 1
        
        # 부정적 편향 → HAM-D 항목 2 (죄책감)
        if simulation_results['negative_bias'] > 0.7:
            score += 2
        elif simulation_results['negative_bias'] > 0.5:
            score += 1
        
        return {
            'hamd_score': score,
            'severity': self._interpret_severity(score)
        }
```

#### BDI (Beck Depression Inventory)
```python
class BDIMapper:
    """
    BDI (Beck Depression Inventory) 매핑
    """
    def map_to_bdi(self, simulation_results):
        """시뮬레이션 결과를 BDI 점수로 매핑"""
        # BDI는 21 항목, 각 0-3점
        # 시뮬레이션 결과를 BDI 항목에 매핑
        pass
```

#### PHQ-9 (Patient Health Questionnaire-9)
```python
class PHQ9Mapper:
    """
    PHQ-9 (Patient Health Questionnaire-9) 매핑
    """
    def map_to_phq9(self, simulation_results):
        """시뮬레이션 결과를 PHQ-9 점수로 매핑"""
        # PHQ-9는 9 항목, 각 0-3점
        # 시뮬레이션 결과를 PHQ-9 항목에 매핑
        pass
```

---

## 📈 Phase 3: 연구 논문용 데이터 생성 (1주)

### 3.1 논문용 리포트 생성

```python
# research/utils/reporting.py

class ResearchReportGenerator:
    """
    연구 논문용 리포트 생성
    
    출력:
    - 표 형식 데이터 (Table 1, Table 2)
    - 그래프 형식 데이터 (Figure 1, Figure 2)
    - 통계 분석 결과
    """
    def generate_table1(self, normal_group, depression_group):
        """표 1: 그룹별 평균 및 표준편차"""
        return {
            'normal': {
                'n': len(normal_group),
                'mean_energy': np.mean([r['energy'] for r in normal_group]),
                'sd_energy': np.std([r['energy'] for r in normal_group]),
                'ci_95': self._calculate_ci(normal_group, 'energy')
            },
            'depression': {
                'n': len(depression_group),
                'mean_energy': np.mean([r['energy'] for r in depression_group]),
                'sd_energy': np.std([r['energy'] for r in depression_group]),
                'ci_95': self._calculate_ci(depression_group, 'energy')
            }
        }
    
    def generate_statistical_report(self, comparison_result):
        """통계 분석 리포트"""
        return f"""
        주요 결과:
        - 에너지: t({comparison_result['df']}) = {comparison_result['t_statistic']:.2f}, 
          p = {comparison_result['p_value']:.4f}
        - 효과 크기: d = {comparison_result['cohens_d']:.2f} 
          ({comparison_result['effect_size_interpretation']})
        - 95% 신뢰구간: [{comparison_result['confidence_interval'][0]:.2f}, 
          {comparison_result['confidence_interval'][1]:.2f}]
        """
```

---

## ✅ Phase 4: 검증 및 문서화 (1-2주)

### 4.1 생물학적 타당성 검증

- 뇌 영역 매핑 정확성 검증
- 신경전달물질 시스템 정확성 검증
- 시간 스케일 일치 검증
- 에너지 대사 모델 정확성 검증

### 4.2 임상적 관련성 검증

- DSM-5/ICD-11 기준 매핑 검증
- 임상 스케일 통합 검증
- 증상 패턴 재현 검증
- 개인차 모델링 검증

### 4.3 연구 재현성 검증

- Seed 관리 시스템 검증
- 실험 메타데이터 검증
- 파라미터 문서화 검증
- 결과 추적성 검증

---

## 📅 전체 일정

| Phase | 기간 | 주요 작업 |
|-------|------|----------|
| Phase 1 | 1주 | 구조 분리 |
| Phase 2 | 2-3주 | 의료 연구용 강화 |
| Phase 3 | 1주 | 논문용 데이터 생성 |
| Phase 4 | 1-2주 | 검증 및 문서화 |
| **총계** | **5-7주** | **전체 구현** |

---

## 🎯 최종 목표

### 의료 연구용
- ✅ 실제 우울증 연구 자료로 의미있는 분석 결과 도출
- ✅ 연구 논문에 사용 가능한 데이터 생성
- ✅ 임상 전문가 검토 가능한 수준

### 엔지니어링 관점
- ✅ 동역학 메커니즘 정확한 이해
- ✅ 확장 가능한 시스템 설계
- ✅ 재사용 가능한 모듈

---

**작성자**: GNJz (Qquarts)  
**버전**: 1.0.0  
**최종 업데이트**: 2025-01-26

