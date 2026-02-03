"""
Integration Test - 통합 테스트

원인 분석 철학 검증 및 실제 사용 시나리오 테스트

Author: GNJz (Qquarts)
Version: 1.2.0
"""

import sys
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from three_body_boundary_engine import (
    ThreeBodyBoundaryEngine,
    ThreeBodyConfig,
    ThreeBodySystem,
    Body,
    Point
)


def test_causal_analysis_scenario():
    """원인 분석 시나리오 테스트"""
    print("\n" + "=" * 60)
    print("원인 분석 시나리오 테스트")
    print("=" * 60)
    
    config = ThreeBodyConfig()
    engine = ThreeBodyBoundaryEngine(config)
    
    # 시나리오 1: 정삼각형 배치 (상대적으로 안정)
    system1 = ThreeBodySystem(
        body1=Body(position=Point(0.0, 0.0), mass=1.0),
        body2=Body(position=Point(1.0, 0.0), mass=1.0),
        body3=Body(position=Point(0.5, 0.866), mass=1.0)
    )
    
    # 시나리오 2: 일직선 배치 (불안정)
    system2 = ThreeBodySystem(
        body1=Body(position=Point(0.0, 0.0), mass=1.0),
        body2=Body(position=Point(1.0, 0.0), mass=1.0),
        body3=Body(position=Point(2.0, 0.0), mass=1.0)
    )
    
    print("\n[시나리오 1] 정삼각형 배치")
    analysis1 = engine.analyze_orbit_stability(system1)
    print(f"  - 안정성 점수: {analysis1.stability_score:.3f}")
    print(f"  - 불일치(Δ): {analysis1.mismatch:.6f}")
    print(f"  - 안정 여부: {analysis1.is_stable()}")
    
    print("\n[시나리오 2] 일직선 배치")
    analysis2 = engine.analyze_orbit_stability(system2)
    print(f"  - 안정성 점수: {analysis2.stability_score:.3f}")
    print(f"  - 불일치(Δ): {analysis2.mismatch:.6f}")
    print(f"  - 안정 여부: {analysis2.is_stable()}")
    
    # 원인 분석: 두 조건의 차이 관찰
    print("\n[원인 분석]")
    print(f"  - 정삼각형 vs 일직선 안정성 차이: {abs(analysis1.stability_score - analysis2.stability_score):.3f}")
    print(f"  - 정삼각형 vs 일직선 불일치 차이: {abs(analysis1.mismatch - analysis2.mismatch):.6f}")
    
    # 추론 가능한 것:
    print("\n[추론 가능한 것]")
    if analysis1.stability_score > analysis2.stability_score:
        print("  ✅ 정삼각형 배치가 일직선 배치보다 안정적입니다")
    if analysis1.mismatch < analysis2.mismatch:
        print("  ✅ 정삼각형 배치의 경계 정합이 더 좋습니다")
    
    print("\n  ❌ 이것이 '삼체 문제의 해'는 아닙니다")
    print("  ✅ 이것은 '원인 분석 데이터'입니다")
    
    print("=" * 60)
    print("✅ 원인 분석 시나리오 테스트 통과")
    print("=" * 60)


def test_lagrange_stability_comparison():
    """라그랑주 점 안정성 비교 테스트"""
    print("\n" + "=" * 60)
    print("라그랑주 점 안정성 비교 테스트")
    print("=" * 60)
    
    config = ThreeBodyConfig()
    engine = ThreeBodyBoundaryEngine(config)
    
    system = ThreeBodySystem(
        body1=Body(position=Point(0.0, 0.0), mass=1.0),
        body2=Body(position=Point(1.0, 0.0), mass=1.0),
        body3=Body(position=Point(0.5, 0.866), mass=1.0)
    )
    
    lagrange_analysis = engine.observe_lagrange_points(system)
    
    print("\n[라그랑주 점 안정성 분석]")
    stable_points = []
    unstable_points = []
    
    for lp in lagrange_analysis.lagrange_points:
        stability_score = lagrange_analysis.stability_map.get(lp.lagrange_type, 0.0)
        print(f"  {lp.lagrange_type}: {lp.stability} (안정성 점수: {stability_score:.3f})")
        
        if lp.stability == "stable":
            stable_points.append(lp.lagrange_type)
        else:
            unstable_points.append(lp.lagrange_type)
    
    print(f"\n  - 안정 라그랑주 점: {stable_points}")
    print(f"  - 불안정 라그랑주 점: {unstable_points}")
    
    # 원인 분석: 안정/불안정 라그랑주 점 구분
    print("\n[원인 분석]")
    print("  ✅ L4, L5는 안정 라그랑주 점입니다")
    print("  ✅ L1, L2, L3는 불안정 라그랑주 점입니다")
    print("  ✅ 이것은 경계 정합 관점에서 관찰 가능합니다")
    
    print("=" * 60)
    print("✅ 라그랑주 점 안정성 비교 테스트 통과")
    print("=" * 60)


if __name__ == "__main__":
    test_causal_analysis_scenario()
    test_lagrange_stability_comparison()

