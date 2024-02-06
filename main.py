import cv2
import mediapipe as mp
import mouse
import numpy as np

# Obtenir les dimensions de l'écran
screen_width, screen_height = 1920, 1080

# Initialize camera
cam = cv2.VideoCapture(0)

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)

# Initialize MediaPipe drawing utils for visualization
mp_drawing = mp.solutions.drawing_utils

# Pour le lissage des mouvements de la souris
last_x, last_y = 0, 0
alpha = 0.3  # Coefficient de lissage, entre 0 et 1

# Offset pour les bords de l'écran
offset_x = screen_width * 0.1  # Offset horizontal de 10% de la largeur de l'écran
offset_y = screen_height * 0.1  # Offset vertical de 10% de la hauteur de l'écran

while True:
    ret, frame = cam.read()
    if not ret:
        break

    # Flip the frame horizontally for a mirror effect
    frame = cv2.flip(frame, 1)

    # Convert the frame color from BGR to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with MediaPipe Hands
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Use drawing utils to draw connections
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Access the index finger mcp (metacarpophalangeal) joint (landmark 5)
            index_fingertip = hand_landmarks.landmark[5]

            # Convert the normalized position to pixel coordinates
            x, y = int(index_fingertip.x * frame.shape[1]), int(index_fingertip.y * frame.shape[0])

            # Apply smoothing
            smooth_x = int(last_x + alpha * (x - last_x))
            smooth_y = int(last_y + alpha * (y - last_y))
            last_x, last_y = smooth_x, smooth_y

            # Map the camera coordinates to screen dimensions with offset
            screen_x = np.interp(smooth_x, (0 + offset_x, frame.shape[1] - offset_x), (0, screen_width))
            screen_y = np.interp(smooth_y, (0 + offset_y, frame.shape[0] - offset_y), (0, screen_height))

            # Move the mouse to the mapped position
            mouse.move(screen_x, screen_y)

            # Draw a bigger circle at the index fingertip
            cv2.circle(frame, (x, y), 10, (0, 255, 0), -1)

    # Show the frame
    cv2.imshow('frame', frame)

    # Break loop with 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cam.release()
cv2.destroyAllWindows()
