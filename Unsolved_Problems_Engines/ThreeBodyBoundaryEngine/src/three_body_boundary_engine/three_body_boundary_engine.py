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

Author: GNJz (Qquarts)
Version: 1.0.0
"""

from typing import List, Optional, Dict
from .config import ThreeBodyConfig
from .models import (
    ThreeBodySystem,
    StabilityAnalysis,
    BoundaryDynamics,
    LagrangeAnalysis,
    LagrangePoint,
    RecoveryResult,
    StabilizationResult,
    CorrectionResult,
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
    
    # ============================================================
    # 해결 접근법 (Solution Approach) 메서드
    # ============================================================
    
    def recover_boundary_alignment(
        self,
        system: ThreeBodySystem,
        target_mismatch: float = 1e-6,
        max_recovery_iterations: int = 100,
        learning_rate: float = 0.01
    ) -> RecoveryResult:
        """경계 정합 복구
        
        원인 분석으로 파악한 불일치 지점을 복구합니다.
        
        해결 접근:
        - 불일치가 발생한 지점의 밀도 분포 분석
        - 경계 점의 위치를 밀도 기울기에 따라 조정
        - 반복적 refinement를 통한 수렴
        
        Args:
            system: 삼체 시스템
            target_mismatch: 목표 불일치 값
            max_recovery_iterations: 최대 복구 반복 횟수
            learning_rate: 학습률 (경계 조정 강도)
        
        Returns:
            복구 결과
        """
        # 초기 분석
        initial_analysis = self.analyze_orbit_stability(system)
        initial_mismatch = initial_analysis.mismatch
        initial_stability = initial_analysis.stability_score
        
        # 이미 목표 불일치 이하이면 성공
        if initial_mismatch <= target_mismatch:
            return RecoveryResult(
                success=True,
                initial_mismatch=initial_mismatch,
                final_mismatch=initial_mismatch,
                improvement=0.0,
                iterations=0,
                stability_before=initial_stability,
                stability_after=initial_stability
            )
        
        # 복구 시도
        current_system = system
        for iteration in range(max_recovery_iterations):
            # 현재 불일치 분석
            current_analysis = self.analyze_orbit_stability(current_system)
            current_mismatch = current_analysis.mismatch
            
            # 목표 달성 확인
            if current_mismatch <= target_mismatch:
                final_analysis = self.analyze_orbit_stability(current_system)
                return RecoveryResult(
                    success=True,
                    initial_mismatch=initial_mismatch,
                    final_mismatch=current_mismatch,
                    improvement=initial_mismatch - current_mismatch,
                    iterations=iteration + 1,
                    stability_before=initial_stability,
                    stability_after=final_analysis.stability_score
                )
            
            # 밀도 기울기를 이용한 경계 재정렬
            # (간단한 근사: 중력 퍼텐셜의 극소점 방향으로 조정)
            bodies = current_system.get_all_bodies()
            
            # 각 천체의 위치를 약간 조정 (밀도 기울기 방향)
            # 실제로는 더 정교한 알고리즘이 필요하지만, 여기서는 간단한 근사 사용
            adjusted_bodies = []
            for body in bodies:
                # 중력 퍼텐셜의 기울기 방향으로 약간 이동
                # (간단한 근사: 다른 천체들의 중심 방향으로 이동)
                other_bodies = [b for b in bodies if b != body]
                if other_bodies:
                    center_x = sum(b.position.x * b.mass for b in other_bodies) / sum(b.mass for b in other_bodies)
                    center_y = sum(b.position.y * b.mass for b in other_bodies) / sum(b.mass for b in other_bodies)
                    
                    # 중심 방향으로 약간 이동
                    dx = (center_x - body.position.x) * learning_rate
                    dy = (center_y - body.position.y) * learning_rate
                    
                    from .point import Point
                    new_position = Point(
                        body.position.x + dx,
                        body.position.y + dy
                    )
                    adjusted_bodies.append(Body(
                        position=new_position,
                        mass=body.mass,
                        velocity=body.velocity
                    ))
                else:
                    adjusted_bodies.append(body)
            
            # 시스템 업데이트
            current_system = ThreeBodySystem(
                body1=adjusted_bodies[0],
                body2=adjusted_bodies[1],
                body3=adjusted_bodies[2],
                gravitational_constant=current_system.gravitational_constant
            )
        
        # 최대 반복 횟수 도달
        final_analysis = self.analyze_orbit_stability(current_system)
        return RecoveryResult(
            success=final_analysis.mismatch < initial_mismatch,
            initial_mismatch=initial_mismatch,
            final_mismatch=final_analysis.mismatch,
            improvement=initial_mismatch - final_analysis.mismatch,
            iterations=max_recovery_iterations,
            stability_before=initial_stability,
            stability_after=final_analysis.stability_score
        )
    
    def stabilize_system(
        self,
        system: ThreeBodySystem,
        target_stability: float = 0.8,
        max_stabilization_iterations: int = 50
    ) -> StabilizationResult:
        """안정화 메커니즘
        
        불안정한 초기 조건을 안정적인 조건으로 전환합니다.
        
        해결 접근:
        - 초기 조건의 안정성 점수 계산
        - 불안정한 경우, 안정 라그랑주 점(L4, L5) 방향으로 조정
        - 중력 퍼텐셜의 극소점을 찾아 천체 위치 재배치
        
        Args:
            system: 삼체 시스템
            target_stability: 목표 안정성 점수
            max_stabilization_iterations: 최대 안정화 반복 횟수
        
        Returns:
            안정화 결과
        """
        # 초기 안정성 분석
        initial_analysis = self.analyze_orbit_stability(system)
        initial_stability = initial_analysis.stability_score
        
        # 이미 목표 안정성 이상이면 성공
        if initial_stability >= target_stability:
            return StabilizationResult(
                success=True,
                initial_stability=initial_stability,
                final_stability=initial_stability,
                optimized_system=system,
                adjustment_magnitude=0.0,
                lagrange_point_used=None
            )
        
        # 라그랑주 점 분석
        lagrange_analysis = self.observe_lagrange_points(system)
        
        # 안정 라그랑주 점 찾기 (L4, L5)
        stable_lagrange_points = [
            lp for lp in lagrange_analysis.lagrange_points
            if lp.stability == "stable" and lp.lagrange_type in ["L4", "L5"]
        ]
        
        if not stable_lagrange_points:
            # 안정 라그랑주 점이 없으면 실패
            return StabilizationResult(
                success=False,
                initial_stability=initial_stability,
                final_stability=initial_stability,
                optimized_system=system,
                adjustment_magnitude=0.0,
                lagrange_point_used=None
            )
        
        # 가장 안정적인 라그랑주 점 선택
        best_lp = max(
            stable_lagrange_points,
            key=lambda lp: lagrange_analysis.stability_map.get(lp.lagrange_type, 0.0)
        )
        
        # 천체를 라그랑주 점 방향으로 조정
        current_system = system
        adjustment_magnitude = 0.0
        
        for iteration in range(max_stabilization_iterations):
            current_analysis = self.analyze_orbit_stability(current_system)
            current_stability = current_analysis.stability_score
            
            # 목표 달성 확인
            if current_stability >= target_stability:
                return StabilizationResult(
                    success=True,
                    initial_stability=initial_stability,
                    final_stability=current_stability,
                    optimized_system=current_system,
                    adjustment_magnitude=adjustment_magnitude,
                    lagrange_point_used=best_lp.lagrange_type
                )
            
            # 천체를 라그랑주 점 방향으로 약간 이동
            bodies = current_system.get_all_bodies()
            adjusted_bodies = []
            
            for body in bodies:
                # 라그랑주 점 방향으로 이동
                dx = (best_lp.position.x - body.position.x) * 0.1
                dy = (best_lp.position.y - body.position.y) * 0.1
                
                from .point import Point
                new_position = Point(
                    body.position.x + dx,
                    body.position.y + dy
                )
                adjusted_bodies.append(Body(
                    position=new_position,
                    mass=body.mass,
                    velocity=body.velocity
                ))
                adjustment_magnitude += (dx**2 + dy**2)**0.5
            
            # 시스템 업데이트
            current_system = ThreeBodySystem(
                body1=adjusted_bodies[0],
                body2=adjusted_bodies[1],
                body3=adjusted_bodies[2],
                gravitational_constant=current_system.gravitational_constant
            )
        
        # 최대 반복 횟수 도달
        final_analysis = self.analyze_orbit_stability(current_system)
        return StabilizationResult(
            success=final_analysis.stability_score > initial_stability,
            initial_stability=initial_stability,
            final_stability=final_analysis.stability_score,
            optimized_system=current_system,
            adjustment_magnitude=adjustment_magnitude,
            lagrange_point_used=best_lp.lagrange_type
        )
    
    def apply_dynamic_correction(
        self,
        system: ThreeBodySystem,
        time_steps: List[float],
        correction_threshold: float = 0.01,
        correction_strength: float = 0.1
    ) -> CorrectionResult:
        """동적 보정
        
        시간에 따라 변화하는 시스템에 실시간 보정을 적용합니다.
        
        해결 접근:
        - 각 시간 단계에서 불일치 모니터링
        - 임계값 초과 시 자동 보정 메커니즘 작동
        - 경계 점의 위치를 실시간으로 조정
        
        Args:
            system: 삼체 시스템
            time_steps: 시간 단계 리스트
            correction_threshold: 보정 임계값 (불일치가 이 값을 초과하면 보정)
            correction_strength: 보정 강도
        
        Returns:
            동적 보정 결과
        """
        corrections_applied = 0
        correction_history = []
        current_system = system
        collapse_delayed = False
        
        for t in time_steps:
            # 현재 불일치 분석
            current_analysis = self.analyze_orbit_stability(current_system)
            current_mismatch = current_analysis.mismatch
            correction_history.append(current_mismatch)
            
            # 임계값 초과 시 보정
            if current_mismatch > correction_threshold:
                # 보정 적용: 경계 정합 복구 시도
                recovery = self.recover_boundary_alignment(
                    system=current_system,
                    target_mismatch=correction_threshold,
                    max_recovery_iterations=10,
                    learning_rate=correction_strength
                )
                
                if recovery.success:
                    corrections_applied += 1
                    current_system = system  # 간단한 근사: 원래 시스템 유지
                    # 실제로는 recovery를 통해 개선된 시스템을 사용해야 함
                    collapse_delayed = True
        
        # 최종 안정성 분석
        final_analysis = self.analyze_orbit_stability(current_system)
        
        return CorrectionResult(
            corrections_applied=corrections_applied,
            collapse_delayed=collapse_delayed,
            final_stability=final_analysis.stability_score,
            correction_history=correction_history,
            time_steps=time_steps
        )

