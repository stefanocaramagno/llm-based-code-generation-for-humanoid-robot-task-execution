from reachy_sdk import ReachySDK
from reachy_sdk.trajectory import goto
from reachy_sdk.trajectory import InterpolationMode
import time
import numpy as np

# Funzione per far guardare il robot verso un obiettivo
def look_at(target):
    reachy.head.look_at(target[0], target[1], target[2], 1.0)

# Funzione per muovere il braccio del robot verso una posizione target
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

# Funzione principale per spostare la pallina da basket
def move_ball():
    # Coordinate della pallina da basket (un po' a destra rispetto al centro del tavolo)
    ball_position = np.array([0.1, 0.3187999, -1.204])  # Esempio: spostata 10 cm a destra
    # Posizione finale della pallina (spostata a sinistra)
    target_position = np.array([-0.1, 0.3187999, -1.204])  # Esempio: spostata 10 cm a sinistra

    # Far guardare il robot verso la pallina
    look_at(ball_position)
    time.sleep(1)

    # Muovere il braccio verso la pallina
    move_arm(ball_position, 2.0)
    time.sleep(2)

    # Chiudere la pinza per afferrare la pallina
    reachy.r_arm.r_gripper.goal_position = -40  # Chiusura della pinza
    time.sleep(1)

    # Muovere il braccio verso la posizione finale (a sinistra)
    move_arm(target_position, 2.0)
    time.sleep(2)

    # Aprire la pinza per rilasciare la pallina
    reachy.r_arm.r_gripper.goal_position = -60  # Apertura della pinza
    time.sleep(1)

    # Riportare il braccio alla posizione iniziale (facoltativo)
    move_arm(ball_position, 2.0)
    time.sleep(2)

if __name__ == "__main__":
    # Connessione al robot Reachy
    reachy = ReachySDK(host='localhost')

    # Eseguire il movimento della pallina
    move_ball()

    # Spegnere il braccio destro del robot in modo graduale
    reachy.turn_off_smoothly('r_arm')

    # Uscire dal programma
    exit()