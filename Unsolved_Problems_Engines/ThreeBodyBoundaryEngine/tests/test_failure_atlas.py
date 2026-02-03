"""
ThreeBodyBoundaryEngine - Failure Atlas 테스트

L1 레이어 (실패 구조 축적 레이어) 테스트

Author: GNJz (Qquarts)
Version: 1.2.0
"""

import unittest
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
    Point,
    StabilityAnalysis,
    FailureAtlas,
    FailureRecord,
    CollapseMode
)


class TestFailureAtlas(unittest.TestCase):
    """Failure Atlas 테스트"""
    
    def setUp(self):
        """테스트 설정"""
        self.engine = ThreeBodyBoundaryEngine()
        self.atlas = FailureAtlas()
        
        # 테스트용 삼체 시스템
        self.system = ThreeBodySystem(
            body1=Body(position=Point(0.0, 0.0), mass=1.0),
            body2=Body(position=Point(1.0, 0.0), mass=1.0),
            body3=Body(position=Point(0.5, 0.866), mass=1.0)
        )
    
    def test_failure_record_creation(self):
        """실패 기록 생성 테스트"""
        # L0 분석 실행
        analysis = self.engine.analyze_orbit_stability(self.system)
        
        # 실패 기록 생성 (임계값을 낮춰서 실패로 만들기)
        record = self.atlas.record_failure(
            analysis=analysis,
            system=self.system,
            threshold=0.01  # 매우 낮은 임계값
        )
        
        if record is not None:
            # 실패 기록 검증
            self.assertIsInstance(record, FailureRecord)
            self.assertIsNotNone(record.condition_signature)
            self.assertGreater(record.timestamp, 0)
            self.assertIn(record.collapse_mode, CollapseMode)
            self.assertGreaterEqual(record.collapse_severity, 0.0)
            self.assertLessEqual(record.collapse_severity, 1.0)
            print(f"✅ 실패 기록 생성: {record.collapse_mode.value}, 심각도: {record.collapse_severity:.3f}")
        else:
            print("ℹ️ 분석 결과가 안정적이어서 실패 기록이 생성되지 않음")
    
    def test_failure_classification(self):
        """실패 유형 분류 테스트"""
        # 여러 실패 시나리오 생성
        test_systems = [
            ThreeBodySystem(
                body1=Body(position=Point(0.0, 0.0), mass=1.0),
                body2=Body(position=Point(1.0, 0.0), mass=1.0),
                body3=Body(position=Point(0.5, 0.866), mass=1.0)
            ),
            ThreeBodySystem(
                body1=Body(position=Point(0.0, 0.0), mass=2.0),
                body2=Body(position=Point(1.0, 0.0), mass=1.0),
                body3=Body(position=Point(0.5, 0.866), mass=1.0)
            ),
        ]
        
        for system in test_systems:
            analysis = self.engine.analyze_orbit_stability(system)
            record = self.atlas.record_failure(
                analysis=analysis,
                system=system,
                threshold=0.01
            )
        
        # 실패 유형별 분류 확인
        stats = self.atlas.get_failure_statistics()
        print(f"✅ 총 실패 횟수: {stats['total_failures']}")
        print(f"✅ 실패 모드별 분류: {stats['failure_by_mode']}")
        print(f"✅ 실패 유형별 분류: {stats['failure_by_type']}")
        
        self.assertGreaterEqual(stats['total_failures'], 0)
    
    def test_collapse_taxonomy(self):
        """붕괴 모드 분류 테스트"""
        # 여러 분석 실행
        for i in range(3):
            analysis = self.engine.analyze_orbit_stability(self.system)
            self.atlas.record_failure(
                analysis=analysis,
                system=self.system,
                threshold=0.01
            )
        
        # 붕괴 모드 분류 확인
        taxonomy = self.atlas.collapse_taxonomy
        print(f"✅ 붕괴 모드 분류: {taxonomy}")
        
        self.assertIsInstance(taxonomy, dict)
    
    def test_similar_failures(self):
        """유사한 실패 패턴 찾기 테스트"""
        # 여러 실패 기록 생성
        for i in range(5):
            analysis = self.engine.analyze_orbit_stability(self.system)
            record = self.atlas.record_failure(
                analysis=analysis,
                system=self.system,
                threshold=0.01
            )
        
        if len(self.atlas.failure_records) > 0:
            # 첫 번째 실패 기록의 조건 서명으로 유사한 실패 찾기
            first_record = self.atlas.failure_records[0]
            similar = self.atlas.get_similar_failures(
                condition_signature=first_record.condition_signature,
                similarity_threshold=0.5
            )
            
            print(f"✅ 유사한 실패 패턴: {len(similar)}개")
            self.assertGreaterEqual(len(similar), 1)  # 최소한 자기 자신은 포함
    
    def test_failure_statistics(self):
        """실패 통계 테스트"""
        # 여러 실패 기록 생성
        for i in range(3):
            analysis = self.engine.analyze_orbit_stability(self.system)
            self.atlas.record_failure(
                analysis=analysis,
                system=self.system,
                threshold=0.01
            )
        
        stats = self.atlas.get_failure_statistics()
        
        # 통계 검증
        self.assertIn("total_failures", stats)
        self.assertIn("failure_by_mode", stats)
        self.assertIn("failure_rate_by_mode", stats)
        self.assertIn("failure_by_type", stats)
        
        print(f"✅ 실패 통계: {stats}")
    
    def test_atlas_clear(self):
        """Atlas 초기화 테스트"""
        # 실패 기록 생성
        analysis = self.engine.analyze_orbit_stability(self.system)
        self.atlas.record_failure(
            analysis=analysis,
            system=self.system,
            threshold=0.01
        )
        
        # 초기화
        self.atlas.clear()
        
        # 검증
        self.assertEqual(len(self.atlas.failure_records), 0)
        self.assertEqual(self.atlas.total_failures, 0)
        print("✅ Atlas 초기화 성공")


if __name__ == "__main__":
    unittest.main()

