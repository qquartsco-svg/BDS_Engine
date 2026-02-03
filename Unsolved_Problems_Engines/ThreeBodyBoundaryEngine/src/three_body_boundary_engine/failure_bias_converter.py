"""
ThreeBodyBoundaryEngine - 실패 학습 레이어 (L2)

엔진 번호: UP-1
레이어: L2 (실패 학습)
역할: 실패 패턴을 탐색 편향으로 변환하는 레이어

핵심 철학:
- "이 방향은 위험하다"라는 내부 지형 생성
- 학습이 아니라 편향 생성
- 탐색 효율 기하급수적 향상

레이어 원칙:
- L0 + L1의 출력(FailureAtlas)을 입력으로 받음
- 실패 패턴을 탐색 편향으로 변환
- 탐색 공간에서 위험 영역 식별

⚠️ 중요:
- 이건 성공 학습이 아니다
- 실패 확률을 줄이는 학습
- 탐색 공간을 깎아내리는 학습
- STDP와 유사하지만 보상이 아니라 파괴 회피

Author: GNJz (Qquarts)
Version: 1.1.0
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from .failure_atlas import FailureAtlas, FailureRecord
from .point import Point


@dataclass
class SearchBias:
    """탐색 편향
    
    실패 패턴을 기반으로 생성된 탐색 편향.
    "이 방향은 위험하다"라는 내부 지형.
    """
    # 위험 영역 (조건 서명별 위험도)
    risk_map: Dict[str, float] = field(default_factory=dict)
    
    # 붕괴 모드별 위험도
    collapse_mode_risk: Dict[str, float] = field(default_factory=dict)
    
    # 공간 패턴별 위험도 (선택적)
    spatial_risk_pattern: Optional[Dict[Tuple[float, float], float]] = None
    
    # 전체 위험도 통계
    total_risk_score: float = 0.0
    max_risk_score: float = 0.0
    
    def get_risk(self, condition_signature: str) -> float:
        """조건 서명에 대한 위험도 반환"""
        return self.risk_map.get(condition_signature, 0.0)
    
    def is_risky(self, condition_signature: str, threshold: float = 0.5) -> bool:
        """위험한 조건인지 판정"""
        return self.get_risk(condition_signature) >= threshold


class FailureBiasConverter:
    """실패 → 편향 변환기
    
    L1의 FailureAtlas를 받아서 탐색 편향(SearchBias)을 생성.
    
    핵심 원리:
    - 실패 빈도가 높은 구간의 밀도 가중치를 낮춤
    - 탐색 공간에서 위험 영역 식별
    - "이 방향은 가지 마라"라는 직관 생성
    """
    
    def __init__(
        self,
        risk_decay_factor: float = 0.9,
        min_risk_threshold: float = 0.1
    ):
        """
        Args:
            risk_decay_factor: 위험도 감쇠 계수 (0.0 ~ 1.0)
                - 높을수록 실패 기록이 오래 유지됨
            min_risk_threshold: 최소 위험도 임계값
                - 이 값 이하는 위험도로 간주하지 않음
        """
        self.risk_decay_factor = risk_decay_factor
        self.min_risk_threshold = min_risk_threshold
    
    def convert_failure_to_bias(
        self,
        failure_atlas: FailureAtlas
    ) -> SearchBias:
        """실패 패턴을 탐색 편향으로 변환
        
        L1의 FailureAtlas를 받아서 탐색 편향을 생성.
        
        Args:
            failure_atlas: L1의 실패 지도
        
        Returns:
            탐색 편향
        """
        if failure_atlas.total_failures == 0:
            # 실패 기록이 없으면 빈 편향 반환
            return SearchBias()
        
        # 위험 지도 생성
        risk_map = self._build_risk_map(failure_atlas)
        
        # 붕괴 모드별 위험도 계산
        collapse_mode_risk = self._calculate_collapse_mode_risk(failure_atlas)
        
        # 전체 위험도 통계
        total_risk = sum(risk_map.values())
        max_risk = max(risk_map.values()) if risk_map else 0.0
        
        return SearchBias(
            risk_map=risk_map,
            collapse_mode_risk=collapse_mode_risk,
            total_risk_score=total_risk,
            max_risk_score=max_risk
        )
    
    def _build_risk_map(
        self,
        failure_atlas: FailureAtlas
    ) -> Dict[str, float]:
        """위험 지도 생성
        
        조건 서명별 위험도를 계산.
        실패 빈도가 높을수록 위험도가 높음.
        """
        risk_map = {}
        
        # 조건 서명별 실패 빈도 계산
        condition_counts: Dict[str, int] = {}
        condition_severities: Dict[str, List[float]] = {}
        
        for record in failure_atlas.failure_records:
            sig = record.condition_signature
            
            # 실패 횟수 카운트
            if sig not in condition_counts:
                condition_counts[sig] = 0
                condition_severities[sig] = []
            
            condition_counts[sig] += 1
            condition_severities[sig].append(record.collapse_severity)
        
        # 위험도 계산
        max_count = max(condition_counts.values()) if condition_counts else 1
        
        for sig, count in condition_counts.items():
            # 빈도 기반 위험도 (0.0 ~ 1.0)
            frequency_risk = count / max_count
            
            # 심각도 기반 위험도 (평균)
            avg_severity = sum(condition_severities[sig]) / len(condition_severities[sig])
            
            # 최종 위험도 (빈도 60% + 심각도 40%)
            risk = frequency_risk * 0.6 + avg_severity * 0.4
            
            # 최소 임계값 적용
            if risk >= self.min_risk_threshold:
                risk_map[sig] = risk
        
        return risk_map
    
    def _calculate_collapse_mode_risk(
        self,
        failure_atlas: FailureAtlas
    ) -> Dict[str, float]:
        """붕괴 모드별 위험도 계산"""
        if failure_atlas.total_failures == 0:
            return {}
        
        collapse_mode_risk = {}
        
        # 각 붕괴 모드별 실패율
        for mode, count in failure_atlas.collapse_taxonomy.items():
            # 실패율 = 해당 모드 실패 횟수 / 전체 실패 횟수
            failure_rate = count / failure_atlas.total_failures
            
            # 위험도 = 실패율 (0.0 ~ 1.0)
            collapse_mode_risk[mode] = failure_rate
        
        return collapse_mode_risk
    
    def update_bias_with_new_failure(
        self,
        bias: SearchBias,
        new_record: FailureRecord
    ) -> SearchBias:
        """새로운 실패 기록으로 편향 업데이트
        
        기존 편향에 새로운 실패 기록을 반영하여 업데이트.
        STDP 유사 메커니즘: 최근 실패일수록 더 큰 영향.
        
        Args:
            bias: 기존 탐색 편향
            new_record: 새로운 실패 기록
        
        Returns:
            업데이트된 탐색 편향
        """
        # 기존 위험도에 감쇠 적용
        updated_risk_map = {
            sig: risk * self.risk_decay_factor
            for sig, risk in bias.risk_map.items()
        }
        
        # 새로운 실패 기록의 위험도 계산
        new_risk = new_record.collapse_severity
        
        # 기존 위험도와 새 위험도 중 큰 값 선택
        sig = new_record.condition_signature
        if sig in updated_risk_map:
            updated_risk_map[sig] = max(updated_risk_map[sig], new_risk)
        else:
            updated_risk_map[sig] = new_risk
        
        # 최소 임계값 적용
        updated_risk_map = {
            sig: risk
            for sig, risk in updated_risk_map.items()
            if risk >= self.min_risk_threshold
        }
        
        # 통계 업데이트
        total_risk = sum(updated_risk_map.values())
        max_risk = max(updated_risk_map.values()) if updated_risk_map else 0.0
        
        return SearchBias(
            risk_map=updated_risk_map,
            collapse_mode_risk=bias.collapse_mode_risk.copy(),
            total_risk_score=total_risk,
            max_risk_score=max_risk
        )
    
    def should_avoid_condition(
        self,
        bias: SearchBias,
        condition_signature: str,
        threshold: float = 0.5
    ) -> bool:
        """조건을 회피해야 하는지 판정
        
        Args:
            bias: 탐색 편향
            condition_signature: 조건 서명
            threshold: 회피 임계값
        
        Returns:
            회피 여부
        """
        return bias.is_risky(condition_signature, threshold)
    
    def get_safe_conditions(
        self,
        bias: SearchBias,
        candidate_conditions: List[str],
        threshold: float = 0.5
    ) -> List[str]:
        """안전한 조건 필터링
        
        후보 조건 중에서 안전한 조건만 반환.
        
        Args:
            bias: 탐색 편향
            candidate_conditions: 후보 조건 서명 리스트
            threshold: 안전 임계값 (이 값 미만이면 안전)
        
        Returns:
            안전한 조건 리스트
        """
        safe_conditions = []
        
        for condition in candidate_conditions:
            risk = bias.get_risk(condition)
            if risk < threshold:
                safe_conditions.append(condition)
        
        return safe_conditions

