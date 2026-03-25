import base64
from typing import Dict

import cv2
import mediapipe as mp
import numpy as np

mp_hands = mp.solutions.hands


class SignDetector:
    def __init__(self):
        self.hands = mp_hands.Hands(
            static_image_mode=True,
            max_num_hands=1,
            min_detection_confidence=0.6,
            min_tracking_confidence=0.6
        )

    def _decode_image(self, image_base64: str):
        encoded = image_base64.split(',', maxsplit=1)[-1]
        data = base64.b64decode(encoded)
        nparr = np.frombuffer(data, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        return image

    def _finger_count_to_text(self, count: int) -> str:
        gestures = {
            0: 'Hello',
            1: 'Yes',
            2: 'No',
            3: 'Thank you',
            4: 'Help',
            5: 'Good'
        }
        return gestures.get(count, 'Gesture detected')

    def detect(self, image_base64: str) -> Dict[str, str]:
        image = self._decode_image(image_base64)
        if image is None:
            return {'detected_text': '', 'confidence': 0.0}

        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        result = self.hands.process(rgb)

        if not result.multi_hand_landmarks:
            return {'detected_text': '', 'confidence': 0.0}

        hand = result.multi_hand_landmarks[0]
        tips = [4, 8, 12, 16, 20]
        pips = [3, 6, 10, 14, 18]

        count = 0
        for tip, pip in zip(tips[1:], pips[1:]):
            if hand.landmark[tip].y < hand.landmark[pip].y:
                count += 1

        if hand.landmark[tips[0]].x < hand.landmark[pips[0]].x:
            count += 1

        return {
            'detected_text': self._finger_count_to_text(count),
            'confidence': 0.72
        }


detector = SignDetector()
