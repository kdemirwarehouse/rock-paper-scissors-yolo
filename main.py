"""
Rock-Paper-Scissors — Real-Time Hand Gesture Recognition with YOLO
===================================================================
A game that detects hand gestures via webcam and plays against the computer.

Controls:
    Q : Quit
    R : Reset score
"""

import cv2
import random
import time
from ultralytics import YOLO


# ---------- Settings ----------
MODEL_PATH = "best.pt"
CAMERA_INDEX = 0
CONFIDENCE_THRESHOLD = 0.6
COOLDOWN_TIME = 2  # seconds

# ---------- Model and camera ----------
model = YOLO(MODEL_PATH)
cap = cv2.VideoCapture(CAMERA_INDEX)

# ---------- Game state ----------
# NOTE: The class names below ("tas", "kagit", "makas") match the labels
# used when training the YOLO model. Do not rename them unless you retrain
# the model with English labels.
score = {"Player": 0, "Computer": 0}
choices = ["tas", "kagit", "makas"]  # rock, paper, scissors
last_game_time = 0
computer_choice = None
result = None


def get_winner(player, computer):
    """Determine the round result and update the score."""
    if player == computer:
        return "Draw"

    winning_combinations = [("tas", "makas"), ("kagit", "tas"), ("makas", "kagit")]
    if (player, computer) in winning_combinations:
        score["Player"] += 1
        return "You Win!"

    score["Computer"] += 1
    return "You Lose!"


# ---------- Main loop ----------
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    detections = model(frame, verbose=False)[0]

    player_choice = None
    for detection in detections.boxes.data.tolist():
        x1, y1, x2, y2, conf, class_id = detection
        if conf > CONFIDENCE_THRESHOLD:
            x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
            class_name = detections.names[int(class_id)].lower()

            if class_name in choices:
                player_choice = class_name
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, class_name.upper(), (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                break

    current_time = time.time()
    if player_choice and (current_time - last_game_time > COOLDOWN_TIME):
        computer_choice = random.choice(choices)
        result = get_winner(player_choice, computer_choice)
        last_game_time = current_time

    if computer_choice and (current_time - last_game_time < COOLDOWN_TIME):
        cv2.putText(frame, f"Computer: {computer_choice}", (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        cv2.putText(frame, f"Result: {result}", (10, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        remaining = COOLDOWN_TIME - (current_time - last_game_time)
        cv2.putText(frame, f"Next round: {remaining:.1f}s", (10, 150),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 200, 200), 2)
    else:
        cv2.putText(frame, "Show your hand!", (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    cv2.putText(frame,
                f"Score - You: {score['Player']}  PC: {score['Computer']}",
                (10, frame.shape[0] - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow("Rock Paper Scissors", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    elif key == ord("r"):
        score = {"Player": 0, "Computer": 0}

cap.release()
cv2.destroyAllWindows()
