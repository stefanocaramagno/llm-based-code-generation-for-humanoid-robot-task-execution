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
    goto({joint: pos for joint, pos in zip(
         reachy.r_arm.joints.values(), joint_pos_ball)}, duration=duration)

# Funzione per afferrare la pallina
def grasp_ball():
    # Apertura della pinza
    reachy.r_arm.r_gripper.goal_position = -60  # Valore per aprire la pinza
    time.sleep(1.0)

    # Posizione della pallina da basket (sopra il tavolo)
    ball_position = np.array([0.1, 0.3187999, -0.01479991])  # Modifica x per la posizione a destra

    # Muovere il braccio verso la posizione della pallina
    move_arm(ball_position, 2.0)
    time.sleep(2.0)

    # Chiusura della pinza per afferrare la pallina
    reachy.r_arm.r_gripper.goal_position = -40  # Valore per chiudere la pinza
    time.sleep(1.0)

    # Alzare il braccio con la pallina
    above_ball_position = np.array([0.1, 0.3187999, 0.1])  # Alzare di qualche cm
    move_arm(above_ball_position, 2.0)
    time.sleep(2.0)

if __name__ == "__main__":
    # Connessione al robot Reachy
    reachy = ReachySDK(host='localhost')

    # Far guardare il robot verso la palla
    look_at([0.1, 0.3187999, -0.01479991])  # Target per il movimento della testa
    time.sleep(1.0)

    # Eseguire l'azione di afferraggio
    grasp_ball()

    # Spegnere il braccio destro del robot in modo graduale
    reachy.turn_off_smoothly('r_arm')