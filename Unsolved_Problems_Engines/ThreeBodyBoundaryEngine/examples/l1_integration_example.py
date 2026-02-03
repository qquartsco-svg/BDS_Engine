"""
ThreeBodyBoundaryEngine - L1 레이어 통합 예제

L0 (ThreeBodyBoundaryEngine) + L1 (FailureAtlas) 통합 예제

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
    ThreeBodySystem,
    Body,
    Point,
    FailureAtlas
)


def main():
    """L0 + L1 통합 예제"""
    print("=" * 60)
    print("L0 + L1 레이어 통합 예제")
    print("=" * 60)
    
    # L0 엔진 생성
    engine = ThreeBodyBoundaryEngine()
    
    # L1 Atlas 생성
    atlas = FailureAtlas()
    
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
    
    print("\n[L0 분석 실행 및 L1 실패 기록]")
    print("-" * 60)
    
    for name, system in test_systems:
        # L0: 안정성 분석
        analysis = engine.analyze_orbit_stability(system)
        
        # L1: 실패 기록 (임계값 0.1)
        record = atlas.record_failure(
            analysis=analysis,
            system=system,
            threshold=0.1
        )
        
        if record:
            print(f"\n✅ {name}: 실패 기록됨")
            print(f"   - 붕괴 모드: {record.collapse_mode.value}")
            print(f"   - 심각도: {record.collapse_severity:.3f}")
            print(f"   - mismatch: {record.mismatch:.6f}")
            print(f"   - 수렴 여부: {record.converged}")
        else:
            print(f"\n✅ {name}: 안정적 (실패 기록 없음)")
            print(f"   - mismatch: {analysis.mismatch:.6f}")
            print(f"   - 안정성 점수: {analysis.stability_score:.3f}")
    
    # L1 통계 출력
    print("\n" + "=" * 60)
    print("[L1 실패 통계]")
    print("-" * 60)
    
    stats = atlas.get_failure_statistics()
    print(f"총 실패 횟수: {stats['total_failures']}")
    print(f"\n붕괴 모드별 분류:")
    for mode, count in stats['failure_by_mode'].items():
        rate = stats['failure_rate_by_mode'].get(mode, 0.0)
        print(f"  - {mode}: {count}회 ({rate*100:.1f}%)")
    
    print(f"\n실패 유형별 분류:")
    for failure_type, count in stats['failure_by_type'].items():
        print(f"  - {failure_type}: {count}회")
    
    # 유사한 실패 패턴 찾기
    if len(atlas.failure_records) > 0:
        print("\n" + "=" * 60)
        print("[유사한 실패 패턴 찾기]")
        print("-" * 60)
        
        first_record = atlas.failure_records[0]
        similar = atlas.get_similar_failures(
            condition_signature=first_record.condition_signature,
            similarity_threshold=0.5
        )
        
        print(f"첫 번째 실패 기록의 조건 서명:")
        print(f"  {first_record.condition_signature}")
        print(f"\n유사한 실패 패턴: {len(similar)}개 발견")
    
    print("\n" + "=" * 60)
    print("✅ L0 + L1 통합 완료")
    print("=" * 60)


if __name__ == "__main__":
    main()

