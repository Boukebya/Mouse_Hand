import argparse
import cv2
import mediapipe as mp
import os
import pandas as pd

# Initialisation de MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, max_num_hands=1, min_detection_confidence=0.5)


def create_landmark_dataset(dataset_path, save_path):
    # Liste pour stocker les données
    data = []

    # Itérer sur chaque classe dans le dataset
    for label in os.listdir(dataset_path):
        class_path = os.path.join(dataset_path, label)
        if not os.path.isdir(class_path):
            continue

        # Itérer sur chaque fichier dans le dossier de la classe
        for file_name in os.listdir(class_path):
            file_path = os.path.join(class_path, file_name)
            image = cv2.imread(file_path)
            if image is None:
                continue
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(image)

            # Extraire les landmarks
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    landmarks = [lm for lm in hand_landmarks.landmark]
                    row = [label]
                    for lm in landmarks:
                        row.extend([lm.x, lm.y, lm.z])
                    data.append(row)

    # Convertir en DataFrame
    df = pd.DataFrame(data)
    # Sauvegarder en CSV
    df.to_csv(save_path, index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create Landmark Dataset for each Classes")
    parser.add_argument("-i", "--dataset", required=True, help="Path to Dataset")
    parser.add_argument("-o", "--save", required=True, help="Path to save CSV file")

    args = parser.parse_args()

    create_landmark_dataset(args.dataset, args.save)
