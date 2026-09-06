from reachy_sdk import ReachySDK
from reachy_sdk.trajectory import goto
from reachy_sdk.trajectory import InterpolationMode
import time
import numpy as np

# Definizione delle coordinate della pallina da basket
# La pallina è situata a destra rispetto al centro
basketball_position = np.array([0.3187999 + 0.1, -0.01479991, -1.204])  # Aggiungere 0.1 metri a x per spostare a destra
target_position = np.array([0.3187999 - 0.3, -0.01479991, -1.204])  # Spostamento a sinistra di 0.3 metri

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

    joint_pos_ball = reachy.r_arm.inverse_kinematics(target_matrix)
    reachy.turn_on('r_arm')
    goto({joint: pos for joint, pos in zip(reachy.r_arm.joints.values(), joint_pos_ball)}, duration=duration)

# Funzione principale per spostare la pallina
def move_basketball():
    # Far guardare il robot verso la pallina
    look_at(basketball_position)

    # Muovere il braccio verso la posizione della pallina
    move_arm(basketball_position, 2.0)
    time.sleep(1.0)  # Attendere che il movimento sia completato

    # Apertura della pinza per afferrare la pallina
    reachy.r_arm.r_gripper.goal_position = -50
    time.sleep(1.0)

    # Muovere il braccio verso la posizione target (spostamento a sinistra)
    move_arm(target_position, 2.0)
    time.sleep(1.0)  # Attendere che il movimento sia completato

    # Chiusura della pinza per rilasciare la pallina
    reachy.r_arm.r_gripper.goal_position = -60
    time.sleep(1.0)

    # Spegnere il braccio destro in modo graduale
    reachy.turn_off_smoothly('r_arm')

if __name__ == "__main__":
    # Connessione al robot Reachy
    reachy = ReachySDK(host='localhost')

    # Eseguire il movimento di spostamento della pallina
    move_basketball()

    # Uscire dal programma
    exit()