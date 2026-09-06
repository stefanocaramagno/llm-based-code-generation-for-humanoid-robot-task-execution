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
    # Apertura della pinza per afferrare il bicchiere
    reachy.r_arm.r_gripper.goal_position = -60
    time.sleep(1.0)

    # Posizione per portare il bicchiere alla bocca
    drink_position = {
        reachy.r_arm.r_shoulder_pitch: -30,
        reachy.r_arm.r_shoulder_roll: 15,
        reachy.r_arm.r_arm_yaw: 0,
        reachy.r_arm.r_elbow_pitch: -30,
        reachy.r_arm.r_forearm_yaw: 0,
        reachy.r_arm.r_wrist_pitch: 0,
        reachy.r_arm.r_wrist_roll: 0,
    }

    # Movimento verso la posizione di bere
    goto(goal_positions=drink_position, duration=1.0, interpolation_mode=InterpolationMode.MINIMUM_JERK)
    time.sleep(1.0)

    # Simulazione del movimento di bere
    # Per esempio, un leggero movimento su e giù
    for _ in range(3):
        # Alza il bicchiere
        reachy.r_arm.r_wrist_pitch.goal_position += 10
        time.sleep(0.5)
        # Riporta il bicchiere giù
        reachy.r_arm.r_wrist_pitch.goal_position -= 10
        time.sleep(0.5)

    # Riportare il braccio alla posizione iniziale
    return_to_start_position()

def return_to_start_position():
    # Posizione iniziale del braccio
    initial_position = {
        reachy.r_arm.r_shoulder_pitch: 0,
        reachy.r_arm.r_shoulder_roll: 0,
        reachy.r_arm.r_arm_yaw: 0,
        reachy.r_arm.r_elbow_pitch: 0,
        reachy.r_arm.r_forearm_yaw: 0,
        reachy.r_arm.r_wrist_pitch: 0,
        reachy.r_arm.r_wrist_roll: 0,
    }
    goto(goal_positions=initial_position, duration=1.0, interpolation_mode=InterpolationMode.MINIMUM_JERK)

def drink():
    # Posizione del bicchiere (simulata)
    glass_position = np.array([0.5, -0.3, -0.2])  # Modifica le coordinate in base alla posizione del bicchiere

    # Far guardare il robot verso il bicchiere
    look_at(glass_position)

    # Muovere il braccio verso il bicchiere
    move_arm(glass_position, 2.0)

    # Eseguire il movimento di bere
    drink_movement()

    # Aggiornare lo stato del thread
    global thread_running
    thread_running = False

if __name__ == "__main__":
    # Connessione al robot Reachy
    reachy = ReachySDK(host='localhost')

    # Creare e avviare un thread per eseguire la funzione drink
    t = Thread(target=lambda: drink())
    t.daemon = True
    t.start()

    # Impostare lo stato del thread come in esecuzione
    thread_running = True

    # Loop per mostrare le immagini della telecamera destra del robot
    while thread_running:
        cv.imshow('Right camera', reachy.right_camera.last_frame)
        cv.waitKey(30)

    # Chiudere tutte le finestre di OpenCV
    cv.destroyAllWindows()

    # Spegnere il braccio destro del robot in modo graduale
    reachy.turn_off_smoothly('r_arm')

    # Uscire dal programma
    exit()