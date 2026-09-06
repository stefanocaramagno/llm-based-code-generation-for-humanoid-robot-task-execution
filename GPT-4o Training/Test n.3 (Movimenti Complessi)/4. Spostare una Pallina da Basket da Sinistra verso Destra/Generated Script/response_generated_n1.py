from reachy_sdk import ReachySDK
from reachy_sdk.trajectory import goto
from reachy_sdk.trajectory import InterpolationMode
import numpy as np
import time

# Funzione per muovere il braccio del robot verso una posizione target
def move_arm(target, duration):
    target_matrix = np.array([
        [0, 0, -1, target[0]],
        [0, 1, 0, target[1]],
        [1, 0, 0, target[2]],
        [0, 0, 0, 1],
    ])

    # Calcolo delle posizioni delle giunture usando la cinematica inversa
    joint_positions = reachy.r_arm.inverse_kinematics(target_matrix)

    # Accensione del braccio destro
    reachy.turn_on('r_arm')

    # Movimento del braccio verso le posizioni delle giunture calcolate
    goto({joint: pos for joint, pos in zip(reachy.r_arm.joints.values(), joint_positions)}, duration=duration)

def move_ball(start_position, end_position, duration):
    # Muovere il braccio verso la posizione iniziale della palla
    move_arm(start_position, duration / 2)  # Muovi verso la palla
    time.sleep(1.0)  # Attendi un attimo

    # Chiusura della pinza per afferrare la palla
    reachy.r_arm.r_gripper.goal_position = -50  # Apri la pinza
    time.sleep(1.0)

    # Muovi verso l'alto per afferrare
    above_ball = np.array([start_position[0], start_position[1], start_position[2] + 0.1])
    move_arm(above_ball, duration / 2)
    time.sleep(1.0)

    # Muovere il braccio verso la posizione finale
    move_arm(end_position, duration / 2)  # Muovi verso la posizione finale
    time.sleep(1.0)

    # Alzare il braccio per rilasciare la palla
    move_arm(above_ball, duration / 2)
    reachy.r_arm.r_gripper.goal_position = -60  # Rilascia la palla
    time.sleep(1.0)

if __name__ == "__main__":
    # Connessione al robot Reachy
    reachy = ReachySDK(host='localhost')

    # Coordinate della palla (posizione iniziale)
    ball_start_position = np.array([-0.1, 0.3187999, -1.204])  # A sinistra del centro
    # Coordinate della palla (posizione finale)
    ball_end_position = np.array([0.1, 0.3187999, -1.204])  # A destra del centro

    # Sposta la pallina da sinistra a destra in 4 secondi
    move_ball(ball_start_position, ball_end_position, duration=4.0)

    # Spegnere il braccio destro del robot in modo graduale
    reachy.turn_off_smoothly('r_arm')