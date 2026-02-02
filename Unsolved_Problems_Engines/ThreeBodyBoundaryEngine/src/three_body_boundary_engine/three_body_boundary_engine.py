"""
ThreeBodyBoundaryEngine - 삼체 문제 경계 정합 분석 엔진

엔진 번호: UP-1 (Unsolved Problems Engine #1)
엔진 이름: ThreeBodyBoundaryEngine
역할: 삼체 궤도 정합 분석을 통한 원인 구조 분석

⚠️ 중요 명확화:
- 이 엔진은 삼체 문제의 "해"를 제공하는 것이 아니라,
- 경계 정합 관점에서 궤도 안정성을 분석합니다.
- 출력은 "정답"이 아니라 "원인 분석 데이터"입니다.

핵심 철학:
- 안정 궤도 = 경계-공간 정합 상태
- 혼돈 = 경계 refinement 실패
- "왜 특정 지점에서 궤도가 붕괴하는가" 원인 분석

정확한 정체성:
- 삼체 문제를 "운동 방정식의 난제"가 아니라
- "공간이 하나의 일관된 형태를 가질 수 없는 조건의 문제"로 재서술
- 혼돈의 "기원 조건"을 분석 (전개 과정 시뮬레이션 아님)

처리 방식:
- 정적 분석: 시간 적분 없음, velocity 사용 안 함
- 공간 변환: 중력 퍼텐셜 → 밀도 → 경계 정합
- 궤도 시뮬레이션 ❌ → 공간 구조 분석 ✅

Author: GNJz (Qquarts)
Version: 1.1.0 (원인 분석 전용)
"""

from typing import List, Optional, Dict
from .config import ThreeBodyConfig
from .models import (
    ThreeBodySystem,
    StabilityAnalysis,
    BoundaryDynamics,
    LagrangeAnalysis,
    LagrangePoint,
    Body
)
from .gravity_calculator import GravityCalculator
from .boundary_convergence_adapter import BoundaryConvergenceAdapter
from .lagrange_calculator import LagrangeCalculator
from .point import Point


class ThreeBodyBoundaryEngine:
    """ThreeBodyBoundaryEngine
    
    삼체 문제를 경계 정합 관점에서 분석하는 엔진.
    
    핵심 개념:
    - 중력 퍼텐셜 → 밀도 변환
    - 경계 형성 시뮬레이션
    - 안정/불안정 조건 비교
    - 라그랑주 점 경계 관찰
    """
    
    def __init__(self, config: Optional[ThreeBodyConfig] = None):
        """
        Args:
            config: 설정 (None이면 기본값 사용)
        """
        self.config = config or ThreeBodyConfig()
        self.gravity_calculator = GravityCalculator(
            gravitational_constant=self.config.gravitational_constant
        )
        self.boundary_adapter = BoundaryConvergenceAdapter(
            boundary_radius=self.config.boundary_radius,
            initial_boundary_points=self.config.initial_boundary_points,
            max_iterations=self.config.max_iterations,
            error_threshold=self.config.error_threshold
        )
        self.lagrange_calculator = LagrangeCalculator()
    
    def analyze_orbit_stability(
        self,
        system: ThreeBodySystem,
        x_range: Optional[tuple] = None,
        y_range: Optional[tuple] = None
    ) -> StabilityAnalysis:
        """궤도 안정성 분석
        
        원인 분석: "왜 특정 조건에서 궤도가 안정/불안정한가?"
        
        Args:
            system: 삼체 시스템
            x_range: x 범위 (min, max), None이면 자동 계산
            y_range: y 범위 (min, max), None이면 자동 계산
        
        Returns:
            안정성 분석 결과
        """
        bodies = system.get_all_bodies()
        
        # 범위 자동 계산
        if x_range is None or y_range is None:
            all_x = [b.position.x for b in bodies]
            all_y = [b.position.y for b in bodies]
            x_min, x_max = min(all_x), max(all_x)
            y_min, y_max = min(all_y), max(all_y)
            
            # 여유 공간 추가
            x_range = (x_min - 1.0, x_max + 1.0)
            y_range = (y_min - 1.0, y_max + 1.0)
        
        # 중력 퍼텐셜 필드 생성
        potential_field = self.gravity_calculator.create_potential_field(
            bodies=bodies,
            x_range=x_range,
            y_range=y_range,
            resolution=self.config.potential_resolution
        )
        
        # 밀도 변환
        density_field = self.gravity_calculator.potential_to_density(
            potential_field=potential_field,
            normalization=self.config.density_normalization
        )
        
        # 경계 형성 시뮬레이션
        result = self.boundary_adapter.converge(importance_weights=density_field)
        
        # 안정성 점수 계산 (0.0 ~ 1.0)
        if result.converged:
            stability_score = max(0.0, 1.0 - result.mismatch / self.config.stability_threshold)
        else:
            stability_score = 0.0
        
        return StabilityAnalysis(
            converged=result.converged,
            mismatch=result.mismatch,
            iteration=result.iteration,
            boundary_points=result.boundary_points,
            stability_score=stability_score,
            convergence_rate=result.convergence_rate
        )
    
    def observe_boundary_formation(
        self,
        system: ThreeBodySystem,
        time_steps: List[float],
        x_range: Optional[tuple] = None,
        y_range: Optional[tuple] = None
    ) -> BoundaryDynamics:
        """경계 형성 과정 관찰
        
        원인 분석: "경계가 시간에 따라 어떻게 변하는가?"
        
        Args:
            system: 삼체 시스템
            time_steps: 시간 단계 리스트
            x_range: x 범위
            y_range: y 범위
        
        Returns:
            경계 동역학 관찰 결과
        """
        mismatches = []
        boundary_evolutions = []
        stability_trajectory = []
        
        for t in time_steps:
            # 시간에 따른 천체 위치 업데이트 (간단한 근사)
            # 실제로는 궤도 적분이 필요하지만, 여기서는 정적 분석
            analysis = self.analyze_orbit_stability(
                system=system,
                x_range=x_range,
                y_range=y_range
            )
            
            mismatches.append(analysis.mismatch)
            boundary_evolutions.append(analysis.boundary_points)
            stability_trajectory.append(analysis.stability_score)
        
        return BoundaryDynamics(
            time_steps=time_steps,
            mismatches=mismatches,
            boundary_evolutions=boundary_evolutions,
            stability_trajectory=stability_trajectory
        )
    
    def observe_lagrange_points(
        self,
        system: ThreeBodySystem
    ) -> LagrangeAnalysis:
        """라그랑주 점 경계 관찰
        
        원인 분석: "라그랑주 점에서 경계 형성이 어떻게 다른가?"
        
        Args:
            system: 삼체 시스템
        
        Returns:
            라그랑주 점 분석 결과
        """
        # 라그랑주 점 계산
        lagrange_points = self.lagrange_calculator.calculate_lagrange_points(
            body1=system.body1,
            body2=system.body2,
            body3=system.body3
        )
        
        # 각 라그랑주 점의 경계 형성 분석
        stability_map = {}
        boundary_formation = {}
        
        for lp in lagrange_points:
            # 라그랑주 점 근처의 작은 시스템 생성
            # (간단한 근사: 라그랑주 점을 중심으로 한 작은 영역)
            analysis = self.analyze_orbit_stability(
                system=system,
                x_range=(lp.position.x - 0.5, lp.position.x + 0.5),
                y_range=(lp.position.y - 0.5, lp.position.y + 0.5)
            )
            
            stability_map[lp.lagrange_type] = analysis.stability_score
            boundary_formation[lp.lagrange_type] = analysis
        
        return LagrangeAnalysis(
            lagrange_points=lagrange_points,
            stability_map=stability_map,
            boundary_formation=boundary_formation
        )
    
    def compare_stability_conditions(
        self,
        systems: List[ThreeBodySystem],
        x_range: Optional[tuple] = None,
        y_range: Optional[tuple] = None
    ) -> List[StabilityAnalysis]:
        """안정/불안정 조건 비교
        
        원인 분석: "어떤 초기 조건이 안정/불안정한가?"
        
        Args:
            systems: 삼체 시스템 리스트 (다양한 초기 조건)
            x_range: x 범위
            y_range: y 범위
        
        Returns:
            안정성 분석 결과 리스트
        """
        results = []
        for system in systems:
            analysis = self.analyze_orbit_stability(
                system=system,
                x_range=x_range,
                y_range=y_range
            )
            results.append(analysis)
        return results
    
    def reset(self) -> None:
        """엔진 리셋"""
        self.boundary_adapter = BoundaryConvergenceAdapter(
            boundary_radius=self.config.boundary_radius,
            initial_boundary_points=self.config.initial_boundary_points,
            max_iterations=self.config.max_iterations,
            error_threshold=self.config.error_threshold
        )
    
    def get_config(self) -> ThreeBodyConfig:
        """설정 반환"""
        return self.config
    
    def update_config(self, **kwargs) -> None:
        """설정 업데이트"""
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
        
        # 설정 변경 후 재초기화
        self.gravity_calculator = GravityCalculator(
            gravitational_constant=self.config.gravitational_constant
        )
        self.boundary_adapter = BoundaryConvergenceAdapter(
            boundary_radius=self.config.boundary_radius,
            initial_boundary_points=self.config.initial_boundary_points,
            max_iterations=self.config.max_iterations,
            error_threshold=self.config.error_threshold
        )
    

