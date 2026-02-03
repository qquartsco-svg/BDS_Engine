"""
ThreeBodyBoundaryEngine - 실패 구조 축적 레이어 (L1)

엔진 번호: UP-1
레이어: L1 (실패 구조 축적)
역할: 실패 패턴을 구조화하여 저장하고 분류하는 레이어

핵심 철학:
- "혼돈은 랜덤이 아니다"
- 실패 패턴의 구조적 유사성 발견
- 반복되는 붕괴 메커니즘 식별

레이어 원칙:
- L0의 출력(StabilityAnalysis)을 입력으로 받음
- L0의 정체성 유지 (L0는 건드리지 않음)
- 실패를 "기억"으로 변환

Author: GNJz (Qquarts)
Version: 1.2.0
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from enum import Enum
from .models import StabilityAnalysis, ThreeBodySystem
from .point import Point


class CollapseMode(Enum):
    """붕괴 모드 분류"""
    DIVERGENCE = "divergence"  # 발산 (convergence_rate < 0)
    MISMATCH = "mismatch"  # 불일치 (mismatch > threshold)
    CONVERGENCE_FAILURE = "convergence_failure"  # 수렴 실패 (converged = False)
    UNKNOWN = "unknown"  # 알 수 없음


@dataclass
class FailureRecord:
    """실패 기록
    
    L0의 StabilityAnalysis 결과를 실패 기록으로 변환.
    실패 패턴의 구조적 특징을 저장.
    """
    # 기본 정보
    condition_signature: str  # 조건 서명 (구조적 특징)
    timestamp: float  # 발생 시점
    
    # L0 출력 데이터
    delta_threshold_crossed: float  # Δ 임계값 초과
    mismatch: float  # 경계 불일치
    convergence_rate: float  # 수렴 속도
    converged: bool  # 수렴 여부
    stability_score: float  # 안정성 점수
    
    # 붕괴 정보
    collapse_mode: CollapseMode  # 붕괴 모드
    collapse_severity: float  # 붕괴 심각도 (0.0 ~ 1.0)
    
    # 공간 패턴 (선택적)
    spatial_pattern: Optional[Dict[str, float]] = None  # 공간 패턴 (위치별 밀도 등)
    
    # 메타데이터
    iteration: int = 0  # 반복 횟수
    boundary_points: int = 0  # 경계 점 개수
    
    def __post_init__(self):
        """검증 및 자동 계산"""
        # 붕괴 심각도 자동 계산
        if self.collapse_severity == 0.0:
            self.collapse_severity = self._calculate_severity()
    
    def _calculate_severity(self) -> float:
        """붕괴 심각도 계산"""
        # mismatch와 convergence_rate를 기반으로 심각도 계산
        mismatch_component = min(self.mismatch / 1.0, 1.0)  # 1.0 이상이면 1.0
        convergence_component = 0.0
        if self.convergence_rate < 0:
            convergence_component = min(abs(self.convergence_rate) / 0.1, 1.0)  # -0.1 이상이면 1.0
        
        # 두 컴포넌트의 가중 평균
        severity = (mismatch_component * 0.6 + convergence_component * 0.4)
        return min(severity, 1.0)
    
    def get_failure_type(self) -> str:
        """실패 유형 반환"""
        if self.collapse_mode == CollapseMode.DIVERGENCE:
            return "divergence"
        elif self.collapse_mode == CollapseMode.MISMATCH:
            return "mismatch"
        elif self.collapse_mode == CollapseMode.CONVERGENCE_FAILURE:
            return "convergence_failure"
        else:
            return "unknown"


@dataclass
class FailureAtlas:
    """실패 지도 (Failure Atlas)
    
    L1 레이어의 핵심 클래스.
    실패 패턴을 구조화하여 저장하고 분류.
    
    핵심 질문:
    - 실패는 어떤 유형으로 반복되는가?
    - 붕괴는 항상 같은 방식인가?
    - 실패에는 "형태"가 있는가?
    """
    
    # 실패 기록 저장소
    failure_records: List[FailureRecord] = field(default_factory=list)
    
    # 실패 유형별 분류 (Failure Manifold)
    failure_manifold: Dict[str, List[FailureRecord]] = field(default_factory=dict)
    
    # 붕괴 모드 분류 (Collapse Taxonomy)
    collapse_taxonomy: Dict[str, int] = field(default_factory=dict)
    
    # 통계 정보
    total_failures: int = 0
    failure_rate_by_mode: Dict[str, float] = field(default_factory=dict)
    
    def record_failure(
        self,
        analysis: StabilityAnalysis,
        system: ThreeBodySystem,
        threshold: float = 0.1
    ) -> FailureRecord:
        """실패 기록 추가
        
        L0의 StabilityAnalysis 결과를 받아서 실패 기록으로 변환.
        
        Args:
            analysis: L0의 안정성 분석 결과
            system: 삼체 시스템
            threshold: 실패 임계값
        
        Returns:
            생성된 실패 기록
        """
        # 실패 여부 확인
        is_failure = not analysis.is_stable(threshold)
        
        if not is_failure:
            # 실패가 아니면 기록하지 않음
            return None
        
        # 붕괴 모드 판정
        collapse_mode = self._determine_collapse_mode(analysis, threshold)
        
        # 조건 서명 생성 (구조적 특징)
        condition_signature = self._generate_condition_signature(system, analysis)
        
        # 실패 기록 생성
        failure_record = FailureRecord(
            condition_signature=condition_signature,
            timestamp=datetime.now().timestamp(),
            delta_threshold_crossed=analysis.mismatch - threshold,
            mismatch=analysis.mismatch,
            convergence_rate=analysis.convergence_rate,
            converged=analysis.converged,
            stability_score=analysis.stability_score,
            collapse_mode=collapse_mode,
            collapse_severity=0.0,  # 자동 계산됨
            iteration=analysis.iteration,
            boundary_points=analysis.boundary_points
        )
        
        # 기록 추가
        self.failure_records.append(failure_record)
        self.total_failures += 1
        
        # 실패 유형별 분류
        self._classify_failure(failure_record)
        
        # 붕괴 모드 분류 업데이트
        self._update_collapse_taxonomy(failure_record)
        
        return failure_record
    
    def _determine_collapse_mode(
        self,
        analysis: StabilityAnalysis,
        threshold: float
    ) -> CollapseMode:
        """붕괴 모드 판정"""
        # 발산 모드 (convergence_rate < 0)
        if analysis.convergence_rate < 0:
            return CollapseMode.DIVERGENCE
        
        # 불일치 모드 (mismatch > threshold)
        if analysis.mismatch > threshold:
            return CollapseMode.MISMATCH
        
        # 수렴 실패 모드 (converged = False)
        if not analysis.converged:
            return CollapseMode.CONVERGENCE_FAILURE
        
        # 알 수 없음
        return CollapseMode.UNKNOWN
    
    def _generate_condition_signature(
        self,
        system: ThreeBodySystem,
        analysis: StabilityAnalysis
    ) -> str:
        """조건 서명 생성
        
        시스템의 구조적 특징을 문자열로 인코딩.
        유사한 조건을 식별하기 위한 서명.
        """
        bodies = system.get_all_bodies()
        
        # 질량 비율
        masses = [b.mass for b in bodies]
        mass_ratio = tuple(sorted(masses, reverse=True))
        
        # 위치 패턴 (정규화된 거리)
        positions = [b.position for b in bodies]
        distances = []
        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                dist = ((positions[i].x - positions[j].x) ** 2 + 
                       (positions[i].y - positions[j].y) ** 2) ** 0.5
                distances.append(round(dist, 2))
        
        # 서명 생성
        signature = f"mass_{mass_ratio}_dist_{tuple(sorted(distances))}_mismatch_{analysis.mismatch:.3f}"
        return signature
    
    def _classify_failure(self, failure_record: FailureRecord):
        """실패 유형별 분류"""
        failure_type = failure_record.get_failure_type()
        
        if failure_type not in self.failure_manifold:
            self.failure_manifold[failure_type] = []
        
        self.failure_manifold[failure_type].append(failure_record)
    
    def _update_collapse_taxonomy(self, failure_record: FailureRecord):
        """붕괴 모드 분류 업데이트"""
        mode_key = failure_record.collapse_mode.value
        
        if mode_key not in self.collapse_taxonomy:
            self.collapse_taxonomy[mode_key] = 0
        
        self.collapse_taxonomy[mode_key] += 1
        
        # 실패율 업데이트
        self._update_failure_rate()
    
    def _update_failure_rate(self):
        """실패율 업데이트"""
        if self.total_failures == 0:
            return
        
        self.failure_rate_by_mode = {}
        for mode, count in self.collapse_taxonomy.items():
            self.failure_rate_by_mode[mode] = count / self.total_failures
    
    def get_similar_failures(
        self,
        condition_signature: str,
        similarity_threshold: float = 0.8
    ) -> List[FailureRecord]:
        """유사한 실패 패턴 찾기
        
        조건 서명이 유사한 실패 기록들을 반환.
        
        Args:
            condition_signature: 비교할 조건 서명
            similarity_threshold: 유사도 임계값 (0.0 ~ 1.0)
        
        Returns:
            유사한 실패 기록 리스트
        """
        similar_failures = []
        
        for record in self.failure_records:
            similarity = self._calculate_signature_similarity(
                condition_signature,
                record.condition_signature
            )
            
            if similarity >= similarity_threshold:
                similar_failures.append(record)
        
        return similar_failures
    
    def _calculate_signature_similarity(
        self,
        sig1: str,
        sig2: str
    ) -> float:
        """서명 유사도 계산 (간단한 문자열 유사도)"""
        # 간단한 구현: 공통 부분 비율
        if sig1 == sig2:
            return 1.0
        
        # 더 정교한 유사도 계산은 나중에 구현 가능
        # 지금은 간단히 조건 서명의 구조적 유사성만 확인
        common_parts = 0
        total_parts = 0
        
        parts1 = sig1.split('_')
        parts2 = sig2.split('_')
        
        for p1, p2 in zip(parts1, parts2):
            total_parts += 1
            if p1 == p2:
                common_parts += 1
        
        if total_parts == 0:
            return 0.0
        
        return common_parts / total_parts
    
    def get_failure_statistics(self) -> Dict:
        """실패 통계 반환"""
        return {
            "total_failures": self.total_failures,
            "failure_by_mode": self.collapse_taxonomy.copy(),
            "failure_rate_by_mode": self.failure_rate_by_mode.copy(),
            "failure_by_type": {
                failure_type: len(records)
                for failure_type, records in self.failure_manifold.items()
            }
        }
    
    def clear(self):
        """모든 기록 초기화"""
        self.failure_records.clear()
        self.failure_manifold.clear()
        self.collapse_taxonomy.clear()
        self.total_failures = 0
        self.failure_rate_by_mode.clear()

