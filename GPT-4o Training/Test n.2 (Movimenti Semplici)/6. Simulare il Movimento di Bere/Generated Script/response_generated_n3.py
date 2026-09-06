from reachy_sdk import ReachySDK
from reachy_sdk.trajectory import goto
from reachy_sdk.trajectory import InterpolationMode
import time
import cv2 as cv
import numpy as np
from threading import Thread

# Variabile globale per tenere traccia se il thread è in esecuzione
thread_running = False

# Funzione per far guardare il robot verso un obiettivo
def look_at(target):
    reachy.head.look_at(target[0], target[1], target[2], 1.0)

# Funzione per muovere il braccio del robot verso una posizione target con una durata specificata
def move_arm(target, duration):
    target_matrix = np.array([
        [0, 0, -1, target[0]],
        [0, 1, 0, target[1]],
        [1, 0, 0, target[2]],
        [0, 0, 0, 1],
    ])

    joint_pos = reachy.r_arm.inverse_kinematics(target_matrix)
    reachy.turn_on('r_arm')
    goto({joint: pos for joint, pos in zip(reachy.r_arm.joints.values(), joint_pos)}, duration=duration)

# Funzione per simulare il movimento di bere
def drinking_movement():
    # Posizione del bicchiere (in coordinate relative a Reachy)
    glass_position = np.array([0.4, -0.2, -0.1])  # Modifica questa posizione in base alla tua configurazione

    # Far guardare il robot verso il bicchiere
    look_at(glass_position)

    # Portare il braccio verso il bicchiere
    move_arm(glass_position, 2.0)
    time.sleep(1.0)

    # Simulare il movimento di bere
    # Portare il bicchiere alla bocca
    mouth_position = np.array([0.3, -0.2, 0.0])  # Posizione della bocca
    move_arm(mouth_position, 1.0)
    time.sleep(1.0)

    # Simulare un movimento di "sorso" (piccolo movimento su e giù)
    for _ in range(3):  # Esegui il movimento di "sorso" 3 volte
        move_arm(mouth_position + np.array([0, 0, 0.05]), 0.5)  # Alzare leggermente
        time.sleep(0.5)
        move_arm(mouth_position, 0.5)  # Tornare giù
        time.sleep(0.5)

    # Riportare il braccio in una posizione neutra
    neutral_position = np.array([0.4, -0.2, -0.2])  # Posizione neutra
    move_arm(neutral_position, 2.0)

    global thread_running
    thread_running = False

# Codice eseguibile principale
if __name__ == "__main__":
    reachy = ReachySDK(host='localhost')

    t = Thread(target=lambda: drinking_movement())
    t.daemon = True
    t.start()

    thread_running = True

    # Loop per mostrare le immagini della telecamera destra del robot
    while thread_running:
        cv.imshow('Right camera', reachy.right_camera.last_frame)
        cv.waitKey(30)

    cv.destroyAllWindows()
    reachy.turn_off_smoothly('r_arm')
    exit()