"""
ThreeBodyBoundaryEngine - 기본 사용 예제

Author: GNJz (Qquarts)
Version: 1.0.0
"""

import sys
sys.path.insert(0, '../src')

from three_body_boundary_engine import (
    ThreeBodyBoundaryEngine,
    ThreeBodyConfig,
    ThreeBodySystem,
    Body,
    Point
)


def main():
    """기본 사용 예제"""
    print("=" * 60)
    print("ThreeBodyBoundaryEngine - 기본 사용 예제")
    print("=" * 60)
    
    # 엔진 생성
    config = ThreeBodyConfig()
    engine = ThreeBodyBoundaryEngine(config)
    
    # 삼체 시스템 생성 (정삼각형 배치)
    system = ThreeBodySystem(
        body1=Body(position=Point(0.0, 0.0), mass=1.0),
        body2=Body(position=Point(1.0, 0.0), mass=1.0),
        body3=Body(position=Point(0.5, 0.866), mass=1.0)
    )
    
    print("\n[1] 궤도 안정성 분석")
    print("-" * 60)
    analysis = engine.analyze_orbit_stability(system)
    
    print(f"수렴 여부: {analysis.converged}")
    print(f"불일치(Δ): {analysis.mismatch:.6f}")
    print(f"반복 횟수: {analysis.iteration}")
    print(f"경계 점 개수: {analysis.boundary_points}")
    print(f"안정성 점수: {analysis.stability_score:.3f}")
    print(f"안정 여부: {analysis.is_stable()}")
    
    print("\n[2] 라그랑주 점 경계 관찰")
    print("-" * 60)
    lagrange_analysis = engine.observe_lagrange_points(system)
    
    print(f"라그랑주 점 개수: {len(lagrange_analysis.lagrange_points)}")
    for lp in lagrange_analysis.lagrange_points:
        print(f"  {lp.lagrange_type}: {lp.stability} (안정성 점수: {lagrange_analysis.stability_map.get(lp.lagrange_type, 0.0):.3f})")
    
    print("\n[3] 안정/불안정 조건 비교")
    print("-" * 60)
    
    # 다양한 초기 조건
    systems = [
        system,  # 정삼각형
        ThreeBodySystem(
            body1=Body(position=Point(0.0, 0.0), mass=1.0),
            body2=Body(position=Point(2.0, 0.0), mass=1.0),
            body3=Body(position=Point(1.0, 1.0), mass=1.0)
        ),  # 더 멀리 떨어진 배치
    ]
    
    results = engine.compare_stability_conditions(systems)
    
    for i, result in enumerate(results):
        print(f"조건 {i+1}:")
        print(f"  안정 여부: {result.is_stable()}")
        print(f"  안정성 점수: {result.stability_score:.3f}")
        print(f"  불일치(Δ): {result.mismatch:.6f}")
    
    print("\n" + "=" * 60)
    print("원인 분석:")
    print("  ✅ 경계 정합이 실패하는 조건을 식별할 수 있습니다")
    print("  ✅ 안정/불안정 패턴을 관찰할 수 있습니다")
    print("  ❌ 이것이 '삼체 문제의 해'는 아닙니다")
    print("  ✅ 이것은 '원인 분석 데이터'입니다")
    print("=" * 60)


if __name__ == "__main__":
    main()

