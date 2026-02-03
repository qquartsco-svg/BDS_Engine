"""
ThreeBodyBoundaryEngine - 성능 벤치마크

L1, L2, 통합 파이프라인 성능 측정

Author: GNJz (Qquarts)
Version: 1.2.0
"""

import time
import sys
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from three_body_boundary_engine import (
    ThreeBodyBoundaryEngine,
    FailureAtlas,
    FailureBiasConverter,
    ThreeBodySystem,
    Body,
    Point
)


def benchmark_l0_analysis(num_iterations=100):
    """L0 안정성 분석 성능 벤치마크"""
    engine = ThreeBodyBoundaryEngine()
    
    system = ThreeBodySystem(
        body1=Body(position=Point(0.0, 0.0), mass=1.0),
        body2=Body(position=Point(1.0, 0.0), mass=1.0),
        body3=Body(position=Point(0.5, 0.866), mass=1.0)
    )
    
    start_time = time.time()
    
    for _ in range(num_iterations):
        analysis = engine.analyze_orbit_stability(system)
    
    end_time = time.time()
    elapsed = end_time - start_time
    
    avg_time = elapsed / num_iterations
    
    print(f"L0 안정성 분석:")
    print(f"  반복 횟수: {num_iterations}")
    print(f"  총 시간: {elapsed:.3f}초")
    print(f"  평균 시간: {avg_time*1000:.3f}ms")
    print(f"  초당 처리량: {num_iterations/elapsed:.1f}회/초")
    
    return avg_time


def benchmark_l1_recording(num_iterations=100):
    """L1 실패 기록 성능 벤치마크"""
    engine = ThreeBodyBoundaryEngine()
    atlas = FailureAtlas()
    
    system = ThreeBodySystem(
        body1=Body(position=Point(0.0, 0.0), mass=1.0),
        body2=Body(position=Point(1.0, 0.0), mass=1.0),
        body3=Body(position=Point(0.5, 0.866), mass=1.0)
    )
    
    start_time = time.time()
    
    for _ in range(num_iterations):
        analysis = engine.analyze_orbit_stability(system)
        atlas.record_failure(analysis, system, threshold=0.01)
    
    end_time = time.time()
    elapsed = end_time - start_time
    
    avg_time = elapsed / num_iterations
    
    print(f"\nL1 실패 기록:")
    print(f"  반복 횟수: {num_iterations}")
    print(f"  총 시간: {elapsed:.3f}초")
    print(f"  평균 시간: {avg_time*1000:.3f}ms")
    print(f"  초당 처리량: {num_iterations/elapsed:.1f}회/초")
    print(f"  총 실패 기록 수: {atlas.total_failures}")
    
    return avg_time


def benchmark_l2_conversion(num_iterations=10):
    """L2 편향 생성 성능 벤치마크"""
    engine = ThreeBodyBoundaryEngine()
    atlas = FailureAtlas()
    converter = FailureBiasConverter()
    
    # 실패 기록 생성
    system = ThreeBodySystem(
        body1=Body(position=Point(0.0, 0.0), mass=1.0),
        body2=Body(position=Point(1.0, 0.0), mass=1.0),
        body3=Body(position=Point(0.5, 0.866), mass=1.0)
    )
    
    for _ in range(100):  # 100개 실패 기록 생성
        analysis = engine.analyze_orbit_stability(system)
        atlas.record_failure(analysis, system, threshold=0.01)
    
    start_time = time.time()
    
    for _ in range(num_iterations):
        bias = converter.convert_failure_to_bias(atlas)
    
    end_time = time.time()
    elapsed = end_time - start_time
    
    avg_time = elapsed / num_iterations
    
    print(f"\nL2 편향 생성:")
    print(f"  반복 횟수: {num_iterations}")
    print(f"  총 시간: {elapsed:.3f}초")
    print(f"  평균 시간: {avg_time*1000:.3f}ms")
    print(f"  초당 처리량: {num_iterations/elapsed:.1f}회/초")
    print(f"  실패 기록 수: {atlas.total_failures}")
    
    return avg_time


def benchmark_integrated_pipeline(num_iterations=50):
    """통합 파이프라인 성능 벤치마크"""
    engine = ThreeBodyBoundaryEngine()
    atlas = FailureAtlas()
    converter = FailureBiasConverter()
    
    system = ThreeBodySystem(
        body1=Body(position=Point(0.0, 0.0), mass=1.0),
        body2=Body(position=Point(1.0, 0.0), mass=1.0),
        body3=Body(position=Point(0.5, 0.866), mass=1.0)
    )
    
    start_time = time.time()
    
    for _ in range(num_iterations):
        # L0: 분석
        analysis = engine.analyze_orbit_stability(system)
        
        # L1: 기록
        record = atlas.record_failure(analysis, system, threshold=0.01)
        
        # L2: 편향 생성 (주기적으로)
        if atlas.total_failures % 10 == 0:
            bias = converter.convert_failure_to_bias(atlas)
    
    end_time = time.time()
    elapsed = end_time - start_time
    
    avg_time = elapsed / num_iterations
    
    print(f"\n통합 파이프라인 (L0+L1+L2):")
    print(f"  반복 횟수: {num_iterations}")
    print(f"  총 시간: {elapsed:.3f}초")
    print(f"  평균 시간: {avg_time*1000:.3f}ms")
    print(f"  초당 처리량: {num_iterations/elapsed:.1f}회/초")
    print(f"  총 실패 기록 수: {atlas.total_failures}")
    
    return avg_time


def benchmark_similarity_search(num_records=1000, num_searches=100):
    """유사도 검색 성능 벤치마크"""
    engine = ThreeBodyBoundaryEngine()
    atlas = FailureAtlas()
    
    system = ThreeBodySystem(
        body1=Body(position=Point(0.0, 0.0), mass=1.0),
        body2=Body(position=Point(1.0, 0.0), mass=1.0),
        body3=Body(position=Point(0.5, 0.866), mass=1.0)
    )
    
    # 실패 기록 생성
    for _ in range(num_records):
        analysis = engine.analyze_orbit_stability(system)
        atlas.record_failure(analysis, system, threshold=0.01)
    
    # 검색 대상 선택
    if len(atlas.failure_records) > 0:
        target_sig = atlas.failure_records[0].condition_signature
        
        start_time = time.time()
        
        for _ in range(num_searches):
            similar = atlas.get_similar_failures(
                condition_signature=target_sig,
                similarity_threshold=0.5
            )
        
        end_time = time.time()
        elapsed = end_time - start_time
        
        avg_time = elapsed / num_searches
        
        print(f"\n유사도 검색:")
        print(f"  실패 기록 수: {num_records}")
        print(f"  검색 횟수: {num_searches}")
        print(f"  총 시간: {elapsed:.3f}초")
        print(f"  평균 시간: {avg_time*1000:.3f}ms")
        print(f"  초당 처리량: {num_searches/elapsed:.1f}회/초")
        
        return avg_time
    
    return 0.0


def main():
    """메인 벤치마크 실행"""
    print("=" * 60)
    print("ThreeBodyBoundaryEngine 성능 벤치마크")
    print("=" * 60)
    
    # L0 벤치마크
    l0_time = benchmark_l0_analysis(100)
    
    # L1 벤치마크
    l1_time = benchmark_l1_recording(100)
    
    # L2 벤치마크
    l2_time = benchmark_l2_conversion(10)
    
    # 통합 파이프라인 벤치마크
    integrated_time = benchmark_integrated_pipeline(50)
    
    # 유사도 검색 벤치마크
    similarity_time = benchmark_similarity_search(1000, 100)
    
    # 요약
    print("\n" + "=" * 60)
    print("성능 요약")
    print("=" * 60)
    print(f"L0 안정성 분석: {l0_time*1000:.3f}ms")
    print(f"L1 실패 기록: {l1_time*1000:.3f}ms")
    print(f"L2 편향 생성: {l2_time*1000:.3f}ms")
    print(f"통합 파이프라인: {integrated_time*1000:.3f}ms")
    print(f"유사도 검색: {similarity_time*1000:.3f}ms")
    print("=" * 60)


if __name__ == "__main__":
    main()

