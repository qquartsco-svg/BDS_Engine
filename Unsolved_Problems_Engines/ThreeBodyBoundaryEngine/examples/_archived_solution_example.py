"""
해결 접근법 사용 예제

Author: GNJz (Qquarts)
Version: 1.0.0
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


def main():
    """해결 접근법 예제"""
    print("=" * 60)
    print("ThreeBodyBoundaryEngine - 해결 접근법 예제")
    print("=" * 60)
    
    # 엔진 생성
    config = ThreeBodyConfig()
    engine = ThreeBodyBoundaryEngine(config)
    
    # 불안정한 초기 조건 (일직선 배치)
    print("\n[초기 조건] 일직선 배치 (불안정)")
    unstable_system = ThreeBodySystem(
        body1=Body(position=Point(0.0, 0.0), mass=1.0),
        body2=Body(position=Point(1.0, 0.0), mass=1.0),
        body3=Body(position=Point(2.0, 0.0), mass=1.0)
    )
    
    initial_analysis = engine.analyze_orbit_stability(unstable_system)
    print(f"  - 초기 안정성 점수: {initial_analysis.stability_score:.3f}")
    print(f"  - 초기 불일치: {initial_analysis.mismatch:.6f}")
    print(f"  - 안정 여부: {initial_analysis.is_stable()}")
    
    # ============================================================
    # 해결 접근법 1: 경계 정합 복구
    # ============================================================
    print("\n" + "=" * 60)
    print("[해결 접근법 1] 경계 정합 복구")
    print("=" * 60)
    
    recovery = engine.recover_boundary_alignment(
        system=unstable_system,
        target_mismatch=1e-5,
        max_recovery_iterations=30,
        learning_rate=0.05
    )
    
    print(f"\n복구 결과:")
    print(f"  - 성공: {recovery.success}")
    print(f"  - 초기 불일치: {recovery.initial_mismatch:.6f}")
    print(f"  - 최종 불일치: {recovery.final_mismatch:.6f}")
    print(f"  - 개선: {recovery.improvement:.6f}")
    print(f"  - 개선율: {recovery.improvement_rate():.2%}")
    print(f"  - 반복 횟수: {recovery.iterations}")
    print(f"  - 안정성 변화: {recovery.stability_before:.3f} → {recovery.stability_after:.3f}")
    
    # ============================================================
    # 해결 접근법 2: 안정화 메커니즘
    # ============================================================
    print("\n" + "=" * 60)
    print("[해결 접근법 2] 안정화 메커니즘")
    print("=" * 60)
    
    stabilization = engine.stabilize_system(
        system=unstable_system,
        target_stability=0.6,
        max_stabilization_iterations=20
    )
    
    print(f"\n안정화 결과:")
    print(f"  - 성공: {stabilization.success}")
    print(f"  - 초기 안정성: {stabilization.initial_stability:.3f}")
    print(f"  - 최종 안정성: {stabilization.final_stability:.3f}")
    print(f"  - 안정성 개선: {stabilization.stability_improvement():.3f}")
    print(f"  - 조정 크기: {stabilization.adjustment_magnitude:.3f}")
    print(f"  - 사용된 라그랑주 점: {stabilization.lagrange_point_used}")
    
    if stabilization.optimized_system:
        optimized_analysis = engine.analyze_orbit_stability(stabilization.optimized_system)
        print(f"\n최적화된 시스템 분석:")
        print(f"  - 안정성 점수: {optimized_analysis.stability_score:.3f}")
        print(f"  - 불일치: {optimized_analysis.mismatch:.6f}")
        print(f"  - 안정 여부: {optimized_analysis.is_stable()}")
    
    # ============================================================
    # 해결 접근법 3: 동적 보정
    # ============================================================
    print("\n" + "=" * 60)
    print("[해결 접근법 3] 동적 보정")
    print("=" * 60)
    
    time_steps = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    correction = engine.apply_dynamic_correction(
        system=unstable_system,
        time_steps=time_steps,
        correction_threshold=0.01,
        correction_strength=0.1
    )
    
    print(f"\n동적 보정 결과:")
    print(f"  - 적용된 보정 횟수: {correction.corrections_applied}")
    print(f"  - 붕괴 지연: {correction.collapse_delayed}")
    print(f"  - 최종 안정성: {correction.final_stability:.3f}")
    print(f"  - 평균 불일치: {correction.average_mismatch():.6f}")
    
    print(f"\n보정 이력 (처음 5개):")
    for i, mismatch in enumerate(correction.correction_history[:5]):
        print(f"  - t={correction.time_steps[i]:.1f}: 불일치={mismatch:.6f}")
    
    # ============================================================
    # 종합 결과
    # ============================================================
    print("\n" + "=" * 60)
    print("종합 결과")
    print("=" * 60)
    
    print(f"\n원인 분석 → 해결 접근:")
    print(f"  1. 원인 파악: 초기 불일치 = {initial_analysis.mismatch:.6f}")
    print(f"  2. 경계 정합 복구: 개선율 = {recovery.improvement_rate():.2%}")
    print(f"  3. 안정화 메커니즘: 안정성 개선 = {stabilization.stability_improvement():.3f}")
    print(f"  4. 동적 보정: 붕괴 지연 = {correction.collapse_delayed}")
    
    print("\n" + "=" * 60)
    print("✅ 해결 접근법 예제 완료")
    print("=" * 60)
    print("\n핵심 통찰:")
    print("  ✅ 원인 분석으로 파악한 불일치를 복구할 수 있습니다")
    print("  ✅ 불안정한 초기 조건을 안정적으로 전환할 수 있습니다")
    print("  ✅ 동적 보정을 통해 붕괴를 지연시킬 수 있습니다")
    print("  ⚠️ 이것은 '완전한 해'가 아니라 '안정화 메커니즘'입니다")
    print("=" * 60)


if __name__ == "__main__":
    main()

