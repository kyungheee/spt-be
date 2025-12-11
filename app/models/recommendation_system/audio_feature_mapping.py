from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Iterable, Tuple
from app.models.llm.mood_condition_schema import Mood, MoodInfo

# 0~1 스케일 피처 + tempo(BPM)을 기분으로 사용
AudioFeatureRange = Dict[str, Tuple[float, float]]

# 기분별 기본 오디오 피처 범위 지정
MOOD_TO_FEATURE: Dict[Mood, AudioFeatureRange] = {
    Mood.anger: {
        "valence": (0.1, 0.4),
        "energy": (0.7, 1.0),
        "tempo": (130.0, 170.0),
        "acousticness": (0.0, 0.3),
        "danceability": (0.4, 0.8),
    },
    Mood.sadness: {
        "valence": (0.0, 0.3),
        "energy": (0.0, 0.5),
        "tempo": (60.0, 110.0),
        "acousticness": (0.4, 1.0),
        "danceability": (0.0, 0.6),
    },
    Mood.pain: {
        "valence": (0.1, 0.4),
        "energy": (0.0, 0.5),
        "tempo": (60.0, 100.0),
        "acousticness": (0.5, 1.0),
        "danceability": (0.0, 0.5),
    },
    Mood.anxiety: {
        "valence": (0.1, 0.5),
        "energy": (0.4, 0.8),
        "tempo": (90.0, 140.0),
        "acousticness": (0.0, 0.6),
        "danceability": (0.3, 0.7),
    },
    Mood.shame: {
        "valence": (0.2, 0.6),
        "energy": (0.2, 0.7),
        "tempo": (90.0, 130.0),
        "acousticness": (0.2, 0.7),
        "danceability": (0.3, 0.7),
    },
    Mood.joy: {
        "valence": (0.7, 1.0),
        "energy": (0.5, 1.0),
        "tempo": (110.0, 160.0),
        "acousticness": (0.0, 0.6),
        "danceability": (0.6, 1.0),
    },
    Mood.love: {
        "valence": (0.6, 1.0),
        "energy": (0.2, 0.8),
        "tempo": (80.0, 140.0),
        "acousticness": (0.3, 0.9),
        "danceability": (0.4, 0.8),
    },
}
# 이거 사용자의 경험에 따라 조정 가능하게(업데이트 가능하게)


# spotify 오디오 피처 한 세트
@dataclass
class AudioFeature:
    valence: float
    energy: float
    tempo: float
    acousticness: float
    danceability: float
    
    def clip(self) -> AudioFeature:
        self.valence = _clamp(self.valence)
        self.energy = _clamp(self.energy)
        self.tempo = max(0.0, self.tempo)
        self.acousticness = _clamp(self.acousticness)
        self.danceability = _clamp(self.danceability)
        return self
    
    def as_dict(self) -> Dict[str, float]:
        return {
            "valence": self.valence,
            "energy": self.energy,
            "tempo": self.tempo,
            "acousticness": self.acousticness,
            "danceability": self.danceability,
        }
    
DEFAULT_FEATURE = AudioFeature(0.5, 0.5, 120.0, 0.5, 0.5)

def _clamp(value: float) -> float:
    return max(0.0, min(1.0, value))

def _midpoint(low: float, high: float) -> float:
    return (low + high) / 2.0   

def _feature_midpoint(ranges: AudioFeatureRange) -> AudioFeature:
    return AudioFeature(
        valence = _midpoint(*ranges["valence"]),
        energy = _midpoint(*ranges["envergy"]),
        tempo = _midpoint(*ranges["tempo"]),
        acusticeness = _midpoint(*ranges["acousticness"]),
        danceability = _midpoint(*ranges["danceability"])
    )