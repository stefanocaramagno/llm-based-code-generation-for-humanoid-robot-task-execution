from reachy_sdk import ReachySDK
from reachy_sdk.trajectory import goto
from reachy_sdk.trajectory import InterpolationMode
import time
import numpy as np

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
    joint_pos_ball = reachy.r_arm.inverse_kinematics(target_matrix)

    # Accensione del braccio destro
    reachy.turn_on('r_arm')

    # Movimento del braccio verso le posizioni delle giunture calcolate
    goto({joint: pos for joint, pos in zip(reachy.r_arm.joints.values(), joint_pos_ball)}, duration=duration)

# Funzione per afferrare la pallina
def grasp_ball(ball_position):
    # Apertura della pinza
    reachy.r_arm.r_gripper.goal_position = -60
    time.sleep(1.0)

    # Muovere il braccio verso la posizione della pallina
    move_arm(ball_position, 2.0)
    time.sleep(1.0)

    # Chiusura della pinza per afferrare la pallina
    reachy.r_arm.r_gripper.goal_position = -40
    time.sleep(0.5)

# Funzione principale per l'afferramento della pallina
def grasp_basketball():
    # Coordinate del tavolo
    table_center = np.array([0, 0.3187999, -0.01479991])

    # Posizione della pallina (a destra e sopra il centro del tavolo)
    # Modificare le coordinate per posizionare la pallina a destra e un po' più in alto
    ball_position = np.array([0.1, 0.3187999, -0.01479991 + 0.1])  # Modificare i valori come necessario

    # Far guardare il robot verso la pallina
    look_at(ball_position)

    # Muovere il braccio sopra la pallina
    above_ball = np.array([ball_position[0], ball_position[1], ball_position[2] + 0.1])  # Sali sopra la pallina
    move_arm(above_ball, 1.0)
    time.sleep(1.0)

    # Afferramento della pallina
    grasp_ball(ball_position)

if __name__ == "__main__":
    # Connessione al robot Reachy
    reachy = ReachySDK(host='localhost')

    # Eseguire l'azione di afferramento
    grasp_basketball()

    # Spegnere il braccio destro del robot in modo graduale
    reachy.turn_off_smoothly('r_arm')

    # Uscire dal programma
    exit()