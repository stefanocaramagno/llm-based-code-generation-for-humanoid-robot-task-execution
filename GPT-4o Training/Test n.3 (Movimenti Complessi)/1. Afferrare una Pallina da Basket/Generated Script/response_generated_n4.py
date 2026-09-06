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

# Funzione per eseguire il grasping
def grasp_ball():
    # Apertura della pinza
    reachy.r_arm.r_gripper.goal_position = -60  # Posizione di apertura
    time.sleep(1.0)

    # Posizione della pallina da basket (x, y, z) - aggiustata rispetto al centro del tavolo
    ball_position = np.array([0.1, 0.3187999, -0.01479991])  # Modificare x in base alla posizione della palla

    # Guardare verso la palla
    look_at(ball_position)

    # Muovere il braccio sopra la palla
    above_ball = np.array([ball_position[0], ball_position[1], ball_position[2] + 0.1])  # 10 cm sopra la palla
    move_arm(above_ball, 2.0)
    time.sleep(1.0)

    # Muovere il braccio verso la palla
    move_arm(ball_position, 2.0)
    time.sleep(1.0)

    # Chiusura della pinza per afferrare la palla
    reachy.r_arm.r_gripper.goal_position = -10  # Posizione di chiusura
    time.sleep(1.0)

    # Alzare il braccio con la palla
    move_arm(np.array([ball_position[0], ball_position[1], ball_position[2] + 0.2]), 2.0)  # Alza di 20 cm
    time.sleep(1.0)

# Codice eseguibile principale
if __name__ == "__main__":
    # Connessione al robot Reachy
    reachy = ReachySDK(host='localhost')

    # Eseguire il movimento di grasping
    grasp_ball()

    # Spegnere il braccio destro del robot in modo graduale
    reachy.turn_off_smoothly('r_arm')

    # Uscire dal programma
    exit()