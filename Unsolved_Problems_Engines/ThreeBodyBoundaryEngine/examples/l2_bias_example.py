"""
ThreeBodyBoundaryEngine - L2 레이어 예제

L0 + L1 + L2 통합 예제

Author: GNJz (Qquarts)
Version: 1.1.0
"""

import sys
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from three_body_boundary_engine import (
    ThreeBodyBoundaryEngine,
    ThreeBodySystem,
    Body,
    Point,
    FailureAtlas,
    FailureBiasConverter
)


def main():
    """L0 + L1 + L2 통합 예제"""
    print("=" * 60)
    print("L0 + L1 + L2 레이어 통합 예제")
    print("=" * 60)
    
    # L0 엔진 생성
    engine = ThreeBodyBoundaryEngine()
    
    # L1 Atlas 생성
    atlas = FailureAtlas()
    
    # L2 Bias Converter 생성
    bias_converter = FailureBiasConverter(
        risk_decay_factor=0.9,
        min_risk_threshold=0.1
    )
    
    # 여러 삼체 시스템 테스트
    test_systems = [
        ("정삼각형 배치", ThreeBodySystem(
            body1=Body(position=Point(0.0, 0.0), mass=1.0),
            body2=Body(position=Point(1.0, 0.0), mass=1.0),
            body3=Body(position=Point(0.5, 0.866), mass=1.0)
        )),
        ("일직선 배치", ThreeBodySystem(
            body1=Body(position=Point(0.0, 0.0), mass=1.0),
            body2=Body(position=Point(1.0, 0.0), mass=1.0),
            body3=Body(position=Point(2.0, 0.0), mass=1.0)
        )),
        ("비대칭 배치", ThreeBodySystem(
            body1=Body(position=Point(0.0, 0.0), mass=2.0),
            body2=Body(position=Point(1.0, 0.0), mass=1.0),
            body3=Body(position=Point(0.5, 0.866), mass=1.0)
        )),
    ]
    
    print("\n[L0 분석 → L1 기록 → L2 편향 생성]")
    print("-" * 60)
    
    # 여러 시스템 분석 및 실패 기록
    for name, system in test_systems:
        # L0: 안정성 분석
        analysis = engine.analyze_orbit_stability(system)
        
        # L1: 실패 기록
        record = atlas.record_failure(
            analysis=analysis,
            system=system,
            threshold=0.1
        )
        
        if record:
            print(f"\n✅ {name}: 실패 기록됨")
            print(f"   - 조건 서명: {record.condition_signature[:50]}...")
            print(f"   - 붕괴 모드: {record.collapse_mode.value}")
            print(f"   - 심각도: {record.collapse_severity:.3f}")
    
    # L2: 실패 → 편향 변환
    print("\n" + "=" * 60)
    print("[L2: 실패 패턴 → 탐색 편향 변환]")
    print("-" * 60)
    
    bias = bias_converter.convert_failure_to_bias(atlas)
    
    print(f"총 위험도 점수: {bias.total_risk_score:.3f}")
    print(f"최대 위험도 점수: {bias.max_risk_score:.3f}")
    
    print(f"\n위험 지도 (조건 서명별 위험도):")
    for sig, risk in bias.risk_map.items():
        print(f"  - {sig[:40]}... : {risk:.3f}")
    
    print(f"\n붕괴 모드별 위험도:")
    for mode, risk in bias.collapse_mode_risk.items():
        print(f"  - {mode}: {risk:.3f}")
    
    # 위험한 조건 회피 테스트
    print("\n" + "=" * 60)
    print("[위험한 조건 회피 테스트]")
    print("-" * 60)
    
    if len(atlas.failure_records) > 0:
        test_condition = atlas.failure_records[0].condition_signature
        should_avoid = bias_converter.should_avoid_condition(
            bias=bias,
            condition_signature=test_condition,
            threshold=0.3
        )
        
        print(f"테스트 조건: {test_condition[:50]}...")
        print(f"위험도: {bias.get_risk(test_condition):.3f}")
        print(f"회피 여부: {'회피 필요' if should_avoid else '안전'}")
    
    # 안전한 조건 필터링 테스트
    print("\n" + "=" * 60)
    print("[안전한 조건 필터링 테스트]")
    print("-" * 60)
    
    candidate_conditions = [
        record.condition_signature
        for record in atlas.failure_records[:3]
    ]
    
    safe_conditions = bias_converter.get_safe_conditions(
        bias=bias,
        candidate_conditions=candidate_conditions,
        threshold=0.3
    )
    
    print(f"후보 조건 수: {len(candidate_conditions)}")
    print(f"안전한 조건 수: {len(safe_conditions)}")
    
    # 새로운 실패 기록으로 편향 업데이트
    if len(atlas.failure_records) > 0:
        print("\n" + "=" * 60)
        print("[새로운 실패 기록으로 편향 업데이트]")
        print("-" * 60)
        
        new_record = atlas.failure_records[0]
        updated_bias = bias_converter.update_bias_with_new_failure(
            bias=bias,
            new_record=new_record
        )
        
        print(f"업데이트 전 총 위험도: {bias.total_risk_score:.3f}")
        print(f"업데이트 후 총 위험도: {updated_bias.total_risk_score:.3f}")
    
    print("\n" + "=" * 60)
    print("✅ L0 + L1 + L2 통합 완료")
    print("=" * 60)
    print("\n핵심 가치:")
    print("- L0: 혼돈 원인 추적 (법칙)")
    print("- L1: 실패 패턴 구조화 (기억)")
    print("- L2: 탐색 편향 생성 (본능)")
    print("=" * 60)


if __name__ == "__main__":
    main()

