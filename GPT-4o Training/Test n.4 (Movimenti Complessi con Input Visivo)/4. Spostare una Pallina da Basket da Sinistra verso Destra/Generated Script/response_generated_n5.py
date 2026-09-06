from reachy_sdk import ReachySDK
from reachy_sdk.trajectory import goto
from reachy_sdk.trajectory import InterpolationMode
import numpy as np
import time

# Funzione per far guardare il robot verso un obiettivo
def look_at(target):
    reachy.head.look_at(target[0], target[1], target[2], 1.0)

# Funzione per muovere il braccio del robot verso una posizione target con una durata specificata
def move_arm(target, duration):
    # Creazione della matrice target per la cinematica inversa
    target_matrix = np.array([
        [0, 0, -1, target[0]],
        [0, 1, 0, target[1]],
        [1, 0, 0, target[2]],
        [0, 0, 0, 1],
    ])

    # Calcolo delle posizioni delle giunture usando la cinematica inversa
    joint_pos_target = reachy.r_arm.inverse_kinematics(target_matrix)

    # Accensione del braccio destro
    reachy.turn_on('r_arm')

    # Movimento del braccio verso le posizioni delle giunture calcolate
    goto({joint: pos for joint, pos in zip(reachy.r_arm.joints.values(), joint_pos_target)}, duration=duration)

# Funzione principale per spostare la pallina da basket
def move_basketball():
    # Coordinate del tavolo e della pallina
    table_position = np.array([0.3187999, -1.204, -0.01479991])  # Posizione del tavolo
    ball_position_left = np.array([table_position[0] - 0.1, table_position[1], table_position[2] + 0.1])  # Posizione iniziale della pallina (a sinistra)
    ball_position_right = np.array([table_position[0] + 0.1, table_position[1], table_position[2] + 0.1])  # Posizione finale della pallina (a destra)

    # Far guardare il robot verso la pallina
    look_at(ball_position_left)

    # Muovere il braccio sopra la pallina
    move_arm(ball_position_left, 1.0)
    time.sleep(1.0)

    # Apertura della pinza per afferrare la pallina
    reachy.r_arm.r_gripper.goal_position = -50  # Aprire la pinza
    time.sleep(1.0)

    # Raggiungere la pallina
    move_arm(ball_position_left, 2.0)
    time.sleep(2.0)

    # Chiusura della pinza per afferrare la pallina
    reachy.r_arm.r_gripper.goal_position = -40  # Chiudere la pinza
    time.sleep(0.5)

    # Sollevare la pallina
    move_arm(np.array([ball_position_left[0], ball_position_left[1], ball_position_left[2] + 0.1]), 2.0)
    time.sleep(1.0)

    # Muovere la pallina verso destra
    move_arm(ball_position_right, 2.0)
    time.sleep(2.0)

    # Abbassare la pallina nella nuova posizione
    move_arm(np.array([ball_position_right[0], ball_position_right[1], ball_position_right[2] - 0.1]), 2.0)
    time.sleep(1.0)

    # Aprire la pinza per rilasciare la pallina
    reachy.r_arm.r_gripper.goal_position = -50  # Aprire la pinza
    time.sleep(1.0)

    # Spegnere il braccio destro del robot
    reachy.turn_off_smoothly('r_arm')

# Codice eseguibile principale
if __name__ == "__main__":
    # Connessione al robot Reachy
    reachy = ReachySDK(host='localhost')

    # Eseguire la funzione per muovere la pallina da basket
    move_basketball()