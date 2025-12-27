import cv2
from django.shortcuts import redirect
import mediapipe as mp
import pickle
import numpy as np
import pyttsx3
import time

def detection():
    import cv2
    import pickle
    import mediapipe as mp
    import numpy as np
    import time
    from deep_translator import GoogleTranslator
    from gtts import gTTS
    from playsound import playsound
    import os

    # ==============================
    # Load the trained model
    # ==============================
    with open(r"D:\ISLtranslator\ISLtranslator\data\isl_model.pkl", "rb") as f:
        model = pickle.load(f)

    # ==============================
    # Mediapipe setup
    # ==============================
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.7
    )
    mp_drawing = mp.solutions.drawing_utils

    # ==============================
    # Translator (English → Malayalam)
    # ==============================
    translator = GoogleTranslator(source='en', target='ml')

    # ==============================
    # Sentence variables
    # ==============================
    sentence = ""
    last_sign = None
    same_sign_counter = 0
    last_spoken_time = time.time()

    cap = cv2.VideoCapture(0)

    print("🖐️ Starting Real-Time ISL Recognition...")
    print("Press 'q' to exit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)

        sign_label = None

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                landmarks = []
                for lm in hand_landmarks.landmark:
                    landmarks.extend([lm.x, lm.y, lm.z])

                X = np.array(landmarks).reshape(1, -1)
                sign_label = model.predict(X)[0]

                mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS
                )

        # ==============================
        # Sentence formation logic
        # ==============================
        if sign_label is not None:
            if sign_label == last_sign:
                same_sign_counter += 1
            else:
                same_sign_counter = 0

            # Add confirmed sign
            if same_sign_counter == 30:
                if sign_label == "space":
                    sentence += " "
                else:
                    sentence += sign_label

                print("🆕 Added to sentence:", sentence)
                same_sign_counter = 0

            last_sign = sign_label
            last_spoken_time = time.time()

        else:
            print("-------------")
            # ==============================
            # Speak Malayalam after pause
            # ==============================
            if time.time() - last_spoken_time > 3 and sentence.strip() != "":
                print("🔤 English Text:", sentence)

                # Translate English → Malayalam
                malayalam_text = translator.translate(sentence)
                print("🌐 Malayalam Text---------:", malayalam_text)

                # Malayalam Audio
                tts = gTTS(text=malayalam_text, lang="ml")
                tts.save("malayalam_output.mp3")
                playsound("malayalam_output.mp3")
                os.remove("malayalam_output.mp3")

                sentence = ""
                last_spoken_time = time.time()

        # ==============================
        # Display
        # ==============================
        cv2.putText(
            frame, f"Current: {sign_label}",
            (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
            (0, 255, 0), 2
        )

        cv2.putText(
            frame, f"Sentence: {sentence}",
            (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
            (255, 255, 255), 2
        )

        cv2.imshow("ISL Real-Time Recognition", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return redirect('userdash')

