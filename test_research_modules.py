#!/usr/bin/env python3
"""
연구 모듈 통합 테스트

의료 연구용 모듈들의 통합 테스트 및 데모
- 신경전달물질 시스템
- 생체지표 매핑
- 통계 분석
- 임상 스케일
- 리포트 생성
- 검증

Author: GNJz (Qquarts)
Version: 1.0.0
"""

import sys
import os
from pathlib import Path

# 프로젝트 경로 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / 'brain_disorder_simulation'))

import numpy as np
from typing import Dict, Any

print("=" * 70)
print("🧪 연구 모듈 통합 테스트")
print("=" * 70)
print()

# ======================================================================
# 1. 신경전달물질 시스템 테스트
# ======================================================================
print("=" * 70)
print("1. 신경전달물질 시스템 테스트")
print("=" * 70)

try:
    from research.depression.neurotransmitters import NeurotransmitterSystem
    
    nt_system = NeurotransmitterSystem()
    
    # 우울증 수준에 따른 신경전달물질 변화 시뮬레이션
    depression_level = 0.7  # 중증 우울증
    
    nt_system.update_from_depression(depression_level)
    
    print(f"✅ NeurotransmitterSystem 초기화 성공")
    print(f"   우울증 수준: {depression_level:.1f}")
    print(f"   도파민 (Tonic): {nt_system.dopamine.state.tonic_dopamine:.3f}")
    print(f"   도파민 (Phasic): {nt_system.dopamine.state.phasic_dopamine:.3f}")
    print(f"   세로토닌: {nt_system.serotonin.state.serotonin_level:.3f}")
    print(f"   노르에피네프린: {nt_system.norepinephrine.state.norepinephrine_level:.3f}")
    print()
except Exception as e:
    print(f"❌ 오류: {e}")
    import traceback
    traceback.print_exc()
    print()

# ======================================================================
# 2. 생체지표 매핑 테스트
# ======================================================================
print("=" * 70)
print("2. 생체지표 매핑 테스트")
print("=" * 70)

try:
    from research.depression.biomarkers import BiomarkerExtractor
    
    extractor = BiomarkerExtractor()
    
    # 시뮬레이션 뇌 상태
    brain_state = {
        'pfc_activity': 0.5,  # PFC 활성화 감소
        'amygdala_activity': 1.5,  # Amygdala 활성화 증가
        'hypothalamus_activity': 0.6,
        'basal_ganglia_activity': 0.4,
        'negative_bias': 0.7,
        'rumination': 0.6,
        'energy_level': 0.3,
        'executive_control': 0.5,
        'arousal_level': 0.8,
        'sleep_quality': 0.4
    }
    
    energy_state = {
        'current_energy': 30.0,
        'recovery_rate': 0.02
    }
    
    biomarkers = extractor.extract_all_biomarkers(
        brain_state=brain_state,
        energy_state=energy_state,
        stress_level=0.6,
        sleep_quality=0.4
    )
    
    print(f"✅ BiomarkerExtractor 테스트 성공")
    print(f"   fMRI - PFC 활성화: {biomarkers['fmri']['pfc_activation']:.3f}")
    print(f"   fMRI - Amygdala 활성화: {biomarkers['fmri']['amygdala_activation']:.3f}")
    print(f"   EEG - Alpha 파워: {biomarkers['eeg']['alpha_power']:.3f}")
    print(f"   EEG - Theta/Beta 비율: {biomarkers['eeg']['theta_beta_ratio']:.3f}")
    print(f"   HRV - RMSSD: {biomarkers['hrv']['rmssd']:.3f}")
    print()
except Exception as e:
    print(f"❌ 오류: {e}")
    import traceback
    traceback.print_exc()
    print()

# ======================================================================
# 3. 임상 스케일 테스트
# ======================================================================
print("=" * 70)
print("3. 임상 스케일 테스트")
print("=" * 70)

try:
    from research.clinical_scales import ClinicalScaleMapper
    
    mapper = ClinicalScaleMapper()
    
    # 시뮬레이션 결과 (우울증 패턴)
    simulation_results = {
        'negative_bias': 0.75,
        'rumination': 0.65,
        'final_energy': 25.0,
        'final_motivation': 0.2,
        'sleep_quality': 0.3,
        'cognitive_control': 0.4,
        'stress_level': 0.5
    }
    
    scales = mapper.map_all_scales(simulation_results)
    
    print(f"✅ ClinicalScaleMapper 테스트 성공")
    print(f"   HAM-D 점수: {scales['hamd'].total_score} / 52")
    print(f"   HAM-D 심각도: {scales['hamd'].severity}")
    print(f"   BDI 점수: {scales['bdi'].total_score} / 63")
    print(f"   BDI 심각도: {scales['bdi'].severity}")
    print(f"   PHQ-9 점수: {scales['phq9'].total_score} / 27")
    print(f"   PHQ-9 심각도: {scales['phq9'].severity}")
    print()
    
    # 리포트 생성
    report = mapper.generate_clinical_report(simulation_results)
    print(report)
    
except Exception as e:
    print(f"❌ 오류: {e}")
    import traceback
    traceback.print_exc()
    print()

# ======================================================================
# 4. 통계 분석 테스트
# ======================================================================
print("=" * 70)
print("4. 통계 분석 테스트")
print("=" * 70)

try:
    from research.utils.statistical import StatisticalAnalyzer
    
    analyzer = StatisticalAnalyzer()
    
    # 가상의 그룹 데이터
    normal_group = [
        {'energy': 85.0, 'motivation': 0.8, 'negative_bias': 0.2},
        {'energy': 90.0, 'motivation': 0.85, 'negative_bias': 0.15},
        {'energy': 88.0, 'motivation': 0.82, 'negative_bias': 0.18},
    ]
    
    depression_group = [
        {'energy': 30.0, 'motivation': 0.3, 'negative_bias': 0.75},
        {'energy': 25.0, 'motivation': 0.25, 'negative_bias': 0.8},
        {'energy': 35.0, 'motivation': 0.35, 'negative_bias': 0.7},
    ]
    
    # 그룹 비교
    comparison = analyzer.compare_groups(
        normal_group, 
        depression_group, 
        'energy'
    )
    
    print(f"✅ StatisticalAnalyzer 테스트 성공")
    print(f"   t-통계량: {comparison.t_statistic:.3f}")
    print(f"   p-값: {comparison.p_value:.6f}")
    print(f"   Cohen's d: {comparison.cohens_d:.3f}")
    print(f"   효과 크기: {comparison.effect_size_interpretation}")
    print()
    
    # 리포트 생성
    report = analyzer.generate_statistical_report(comparison, "에너지 수준")
    print(report)
    
except Exception as e:
    print(f"❌ 오류: {e}")
    import traceback
    traceback.print_exc()
    print()

# ======================================================================
# 5. 검증 테스트
# ======================================================================
print("=" * 70)
print("5. 검증 테스트")
print("=" * 70)

try:
    from research.depression.validation import ComprehensiveValidator
    
    validator = ComprehensiveValidator()
    
    # 시뮬레이션 결과
    simulation_results = {
        'pfc_activity': 0.5,
        'amygdala_activity': 1.5,
        'hypothalamus_activity': 0.6,
        'basal_ganglia_activity': 0.4,
        'negative_bias': 0.75,
        'rumination': 0.65,
        'final_energy': 25.0,
        'final_motivation': 0.2,
        'sleep_quality': 0.3,
        'cognitive_control': 0.4,
        'stress_level': 0.5,
        'hamd_score': 24,
        'bdi_score': 35,
        'phq9_score': 18
    }
    
    # 실험 설정
    experiment_config = {
        'seed': 42,
        'experiment_id': 'test_001',
        'date': '2025-01-26',
        'version': '1.0.0',
        'author': 'GNJz',
        'n_steps': 100,
        'dt': 0.1
    }
    
    validation_results = validator.validate_all(simulation_results, experiment_config)
    
    print(f"✅ ComprehensiveValidator 테스트 성공")
    print(f"   전체 점수: {validation_results['overall_score']:.2%}")
    print(f"   전체 통과: {'✅ 통과' if validation_results['overall_passed'] else '❌ 미통과'}")
    print()
    
    # 리포트 생성
    report = validator.generate_validation_report(validation_results)
    print(report)
    
except Exception as e:
    print(f"❌ 오류: {e}")
    import traceback
    traceback.print_exc()
    print()

# ======================================================================
# 6. 통합 테스트
# ======================================================================
print("=" * 70)
print("6. 통합 테스트: 전체 파이프라인")
print("=" * 70)

try:
    # 전체 파이프라인 테스트
    print("🔄 전체 파이프라인 실행 중...")
    print()
    
    # 1. 신경전달물질 시스템
    nt_system = NeurotransmitterSystem()
    nt_system.update_from_depression(0.7)
    
    # 2. 생체지표 추출
    extractor = BiomarkerExtractor()
    biomarkers = extractor.extract_all_biomarkers(
        brain_state=brain_state,
        energy_state=energy_state,
        stress_level=0.6,
        sleep_quality=0.4
    )
    
    # 3. 임상 스케일 매핑
    mapper = ClinicalScaleMapper()
    scales = mapper.map_all_scales(simulation_results)
    
    # 4. 통계 분석 (간단한 예시)
    analyzer = StatisticalAnalyzer()
    
    # 5. 검증
    validator = ComprehensiveValidator()
    validation = validator.validate_all(simulation_results, experiment_config)
    
    print("✅ 전체 파이프라인 테스트 성공!")
    print()
    print("📊 최종 결과 요약:")
    print(f"   - HAM-D: {scales['hamd'].total_score}점 ({scales['hamd'].severity})")
    print(f"   - BDI: {scales['bdi'].total_score}점 ({scales['bdi'].severity})")
    print(f"   - PHQ-9: {scales['phq9'].total_score}점 ({scales['phq9'].severity})")
    print(f"   - 검증 점수: {validation['overall_score']:.2%}")
    print()
    
except Exception as e:
    print(f"❌ 오류: {e}")
    import traceback
    traceback.print_exc()
    print()

print("=" * 70)
print("🎉 모든 테스트 완료!")
print("=" * 70)
print()
print("📁 실행 파일 위치:")
print(f"   {Path(__file__).absolute()}")
print()
print("🚀 실행 방법:")
print("   python3 test_research_modules.py")
print()

