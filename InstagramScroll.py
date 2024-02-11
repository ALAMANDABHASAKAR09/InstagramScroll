import cv2
import mediapipe as mp
import pyautogui as pg
pg.FAILSAFE = False

cap = cv2.VideoCapture(0)
hands = mp.solutions.hands.Hands(
    min_detection_confidence=0.5, min_tracking_confidence=0.5, max_num_hands=1
)
drawing_utils= mp.solutions.drawing_utils
screen_width, screen_height = pg.size()

alpha = 0.9
window_size = 5

index_x_history = [0] * window_size
index_y_history = [0] * window_size

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb_frame)
    if results.multi_hand_landmarks:
        for hand in results.multi_hand_landmarks:
            drawing_utils.draw_landmarks(frame, hand)
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * screen_width)
                y = int(landmark.y * screen_height)

                if id == 4:
                    index_x_history.append(x)
                    index_x_history = index_x_history[-window_size:]
                    smoothed_x = int(sum(index_x_history) / window_size)

                    index_y_history.append(y)
                    index_y_history = index_y_history[-window_size:]
                    smoothed_y = int(sum(index_y_history) / window_size)

                    pg.moveTo(smoothed_x, smoothed_y)

                if id == 8:
                    thumb_x = x
                    thumb_y = y
                    click_dist = abs(thumb_y - index_y_history[-1])
                    if click_dist<5:
                        pg.scroll(-200)
                        pg.sleep(1)
                        
                elif id == 12:
                    thumb_x = x
                    thumb_y = y
                    click_dist = abs(thumb_y - index_y_history[-1])

                    if click_dist<5:
                        pg.scroll(100)
                        pg.sleep(1)                        
    cv2.imshow('Virtual Mouse', frame)
    cv2.waitKey(1)

