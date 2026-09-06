from reachy_sdk import ReachySDK
from reachy_sdk.trajectory import goto
from reachy_sdk.trajectory import InterpolationMode
import time
import numpy as np

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
    goto({joint: pos for joint, pos in zip(
         reachy.r_arm.joints.values(), joint_pos_ball)}, duration=duration)

# Funzione principale per muovere la pallina da basket da destra a sinistra
def move_ball():
    # Posizione iniziale della pallina (un po' a destra rispetto al centro del tavolo)
    ball_position = np.array([0.3187999 + 0.05, -0.01479991, -1.204])  # 5 cm a destra

    # Posizione finale della pallina (a sinistra rispetto al centro del tavolo)
    target_position = np.array([0.3187999 - 0.05, -0.01479991, -1.204])  # 5 cm a sinistra

    # Muovere il braccio sopra la palla
    move_arm(ball_position, 2.0)
    time.sleep(1.0)

    # Apertura della pinza per afferrare la palla
    reachy.r_arm.r_gripper.goal_position = -50
    time.sleep(1.0)

    # Muovere il braccio verso la palla
    move_arm(ball_position, 2.0)
    time.sleep(2.0)

    # Chiusura della pinza per afferrare la palla
    reachy.r_arm.r_gripper.goal_position = -40
    time.sleep(0.5)

    # Alzare il braccio con la palla
    move_arm(np.array([0.3187999, -0.01479991, -1.154]), 2.0)  # Sollevare di 5 cm
    time.sleep(1.0)

    # Muovere la pallina da destra a sinistra
    move_arm(target_position, 2.0)
    time.sleep(2.0)

    # Abbassare il braccio con la palla
    move_arm(np.array([0.3187999, -0.01479991, -1.204]), 2.0)  # Ritorna alla posizione originale
    time.sleep(1.0)

    # Apertura della pinza per rilasciare la palla
    reachy.r_arm.r_gripper.goal_position = -60
    time.sleep(1.0)

    # Spegnere il braccio destro del robot in modo graduale
    reachy.turn_off_smoothly('r_arm')

# Codice eseguibile principale
if __name__ == "__main__":
    # Connessione al robot Reachy
    reachy = ReachySDK(host='localhost')

    # Eseguire il movimento della pallina
    move_ball()

    # Uscire dal programma
    exit()