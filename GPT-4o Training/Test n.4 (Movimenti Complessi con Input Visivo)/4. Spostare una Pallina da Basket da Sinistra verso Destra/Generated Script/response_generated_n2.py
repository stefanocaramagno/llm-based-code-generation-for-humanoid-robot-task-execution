from reachy_sdk import ReachySDK
from reachy_sdk.trajectory import goto
from reachy_sdk.trajectory import InterpolationMode
import time
import numpy as np

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

# Funzione principale per spostare la pallina da basket
def move_basketball():
    # Coordinate iniziali della pallina da basket (sinistra)
    ball_initial_position = np.array([-0.2, 0.3187999, -0.01479991])  # Modifica x per posizionarla a sinistra

    # Coordinate finali della pallina da basket (destra)
    ball_final_position = np.array([0.2, 0.3187999, -0.01479991])  # Modifica x per posizionarla a destra

    # Muovere il braccio sopra la palla
    move_arm(ball_initial_position, duration=2.0)
    time.sleep(1.0)  # Attendere che il braccio raggiunga la posizione

    # Apertura della pinza per afferrare la palla
    reachy.r_arm.r_gripper.goal_position = -50
    time.sleep(1.0)  # Attendere che la pinza si apra

    # Muovere il braccio verso la palla
    move_arm(ball_initial_position, duration=2.0)
    time.sleep(2.0)  # Attendere che il braccio raggiunga la posizione

    # Chiusura della pinza per afferrare la palla
    reachy.r_arm.r_gripper.goal_position = -40
    time.sleep(0.5)

    # Muovere il braccio verso la posizione finale a destra
    move_arm(ball_final_position, duration=2.0)
    time.sleep(2.0)  # Attendere che il braccio raggiunga la posizione finale

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
    move_basketball()

    # Uscire dal programma
    exit()