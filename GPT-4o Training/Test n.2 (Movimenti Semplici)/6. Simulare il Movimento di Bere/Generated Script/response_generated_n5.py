from reachy_sdk import ReachySDK
from reachy_sdk.trajectory import goto
from reachy_sdk.trajectory import InterpolationMode
import time
import numpy as np
from threading import Thread

# Variabile globale per tenere traccia se il thread è in esecuzione
thread_running = False

def look_at(target):
    reachy.head.look_at(target[0], target[1], target[2], 1.0)

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

def drink_movement():
    # Posizione del bicchiere (ipotetica)
    glass_position = np.array([0.4, -0.2, -0.1])  # Coordinate XYZ del bicchiere

    # Far guardare il robot verso il bicchiere
    look_at(glass_position)

    # Muovere il braccio verso la posizione del bicchiere
    move_arm(glass_position, 2.0)
    time.sleep(1.0)

    # Posizione per avvicinare il bicchiere alla bocca
    mouth_position = np.array([0.4, -0.2, 0.1])  # Coordinate XYZ per portare il bicchiere alla bocca
    move_arm(mouth_position, 1.0)
    time.sleep(1.0)

    # Simulazione di "bere" (un movimento di su e giù)
    for _ in range(3):
        move_arm(mouth_position + np.array([0, 0, 0.05]), 0.5)  # Alzare il bicchiere
        time.sleep(0.5)
        move_arm(mouth_position, 0.5)  # Riportare il bicchiere alla bocca
        time.sleep(0.5)

    # Riportare il braccio alla posizione iniziale
    initial_position = np.array([0.5, -0.3, 0])  # Posizione iniziale del braccio
    move_arm(initial_position, 2.0)

    global thread_running
    thread_running = False

if __name__ == "__main__":
    reachy = ReachySDK(host='localhost')

    # Creare e avviare un thread per eseguire il movimento di bere
    t = Thread(target=drink_movement)
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