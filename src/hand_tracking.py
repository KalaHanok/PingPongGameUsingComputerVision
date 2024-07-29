import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.mp_drawing = mp.solutions.drawing_utils

    def get_hand_position(self, frame):
        flipped_frame = cv2.flip(frame, 1)
        
        image = cv2.cvtColor(flipped_frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        hand_x = None
        gesture = None

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                for id, lm in enumerate(hand_landmarks.landmark):
                    if id == 9:
                        hand_x = int(lm.x * frame.shape[1])
                
                gesture = self.classify_gesture(hand_landmarks.landmark)

        return hand_x, gesture, image

    def classify_gesture(self, landmarks):
        wrist = landmarks[mp.solutions.hands.HandLandmark.WRIST]
        thumb_tip = landmarks[mp.solutions.hands.HandLandmark.THUMB_TIP]
        index_tip = landmarks[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP]
        middle_tip = landmarks[mp.solutions.hands.HandLandmark.MIDDLE_FINGER_TIP]
        ring_tip = landmarks[mp.solutions.hands.HandLandmark.RING_FINGER_TIP]
        pinky_tip = landmarks[mp.solutions.hands.HandLandmark.PINKY_TIP]

        thumb_ip = landmarks[mp.solutions.hands.HandLandmark.THUMB_IP]
        index_pip = landmarks[mp.solutions.hands.HandLandmark.INDEX_FINGER_PIP]
        middle_pip = landmarks[mp.solutions.hands.HandLandmark.MIDDLE_FINGER_PIP]
        ring_pip = landmarks[mp.solutions.hands.HandLandmark.RING_FINGER_PIP]
        pinky_pip = landmarks[mp.solutions.hands.HandLandmark.PINKY_PIP]

        thumb_mcp = landmarks[mp.solutions.hands.HandLandmark.THUMB_MCP]
        index_mcp = landmarks[mp.solutions.hands.HandLandmark.INDEX_FINGER_MCP]
        middle_mcp = landmarks[mp.solutions.hands.HandLandmark.MIDDLE_FINGER_MCP]
        ring_mcp = landmarks[mp.solutions.hands.HandLandmark.RING_FINGER_MCP]
        pinky_mcp = landmarks[mp.solutions.hands.HandLandmark.PINKY_MCP]

        def distance(point1, point2):
            return ((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2) ** 0.5

        # Pause: All fingers are curled into the palm (fist)
        if (thumb_tip.y > thumb_ip.y and
            index_tip.y > index_pip.y and
            middle_tip.y > middle_pip.y and
            ring_tip.y > ring_pip.y and
            pinky_tip.y > pinky_pip.y):
            return "pause"

        # Setting: All fingers are open
        if (thumb_tip.y < thumb_ip.y and
            index_tip.y < index_pip.y and
            middle_tip.y < middle_pip.y and
            ring_tip.y < ring_pip.y and
            pinky_tip.y < pinky_pip.y):
            return "settings"

        # Pointing: Index finger is higher than thumb tip, other fingers lower than thumb tip
        if (index_tip.y < thumb_tip.y and
            middle_tip.y > thumb_tip.y and
            ring_tip.y > thumb_tip.y and
            pinky_tip.y > thumb_tip.y):
            return "game"

        # MouseClick: Index and middle fingers open, other fingers closed, separation less than middle-thumb separation
        if (index_tip.y < thumb_tip.y and
            middle_tip.y < thumb_tip.y and
            ring_tip.y > thumb_tip.y and
            pinky_tip.y > thumb_tip.y and
            distance(index_tip, middle_tip) < distance(middle_tip, thumb_tip)):
            return "click"

        # MouseMove: Index and middle fingers are parallel with similar distances between corresponding nodes
        if (index_tip.y < thumb_tip.y and
            middle_tip.y < thumb_tip.y and
            ring_tip.y > thumb_tip.y and
            pinky_tip.y > thumb_tip.y and
            abs(distance(landmarks[14], landmarks[18]) - distance(landmarks[15], landmarks[19])) < 0.02):
            return "MouseMove"

        return "Unknown"
