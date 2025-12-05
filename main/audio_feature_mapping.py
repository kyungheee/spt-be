from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Tuple
from mood_schema import Mood, MoodInfo, Weather, ConditionInput

# 0~1 스케일 피처 + tempo(BPM)을 기분으로 사용
AudioFeatureRange = Dict[str, Tuple[float, float]]

# 기분별 기본 오디오 피처 범위 지정
MOOD_TO_FEATURE: Dict[Mood, AudioFeatureRange] = {
    Mood.ANGER: {
        "valence": (0.1, 0.4),
        "energy": (0.7, 1.0),
        "tempo": (130.0, 170.0),
        "acousticness": (0.0, 0.3),
        "danceability": (0.4, 0.8),
    },
    Mood.SADNESS: {
        "valence": (0.0, 0.3),
        "energy": (0.0, 0.5),
        "tempo": (60.0, 110.0),
        "acousticness": (0.4, 1.0),
        "danceability": (0.0, 0.6),
    },
    Mood.PAIN: {
        "valence": (0.1, 0.4),
        "energy": (0.0, 0.5),
        "tempo": (60.0, 100.0),
        "acousticness": (0.5, 1.0),
        "danceability": (0.0, 0.5),
    },
    Mood.ANXIETY: {
        "valence": (0.1, 0.5),
        "energy": (0.4, 0.8),
        "tempo": (90.0, 140.0),
        "acousticness": (0.0, 0.6),
        "danceability": (0.3, 0.7),
    },
    Mood.SHAME: {
        "valence": (0.2, 0.6),
        "energy": (0.2, 0.7),
        "tempo": (90.0, 130.0),
        "acousticness": (0.2, 0.7),
        "danceability": (0.3, 0.7),
    },
    Mood.JOY: {
        "valence": (0.7, 1.0),
        "energy": (0.5, 1.0),
        "tempo": (110.0, 160.0),
        "acousticness": (0.0, 0.6),
        "danceability": (0.6, 1.0),
    },
    Mood.LOVE: {
        "valence": (0.6, 1.0),
        "energy": (0.2, 0.8),
        "tempo": (80.0, 140.0),
        "acousticness": (0.3, 0.9),
        "danceability": (0.4, 0.8),
    },
}

# spotify 오디오 피처 한 세트
@dataclass
class AudioFeature:
    valence: float
    energy: float
    tempo: float
    acousticness: float
    danceability: float
    
    def clip(self)
    