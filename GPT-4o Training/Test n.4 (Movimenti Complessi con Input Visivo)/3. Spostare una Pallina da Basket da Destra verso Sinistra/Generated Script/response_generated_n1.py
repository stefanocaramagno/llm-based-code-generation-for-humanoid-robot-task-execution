from reachy_sdk import ReachySDK
from reachy_sdk.trajectory import goto
from reachy_sdk.trajectory import InterpolationMode
import time
import numpy as np

# Funzione per muovere il braccio di Reachy verso una posizione target
def move_arm(target, duration):
    # Creazione della matrice target per la cinematica inversa
    target_matrix = np.array([
        [0, 0, -1, target[0]],
        [0, 1, 0, target[1]],
        [1, 0, 0, target[2]],
        [0, 0, 0, 1],
    ])

    # Calcolo delle posizioni delle giunture usando la cinematica inversa
    joint_pos = reachy.r_arm.inverse_kinematics(target_matrix)

    # Accensione del braccio destro
    reachy.turn_on('r_arm')

    # Movimento del braccio verso le posizioni delle giunture calcolate
    goto({joint: pos for joint, pos in zip(reachy.r_arm.joints.values(), joint_pos)}, duration=duration)

# Funzione principale per spostare la pallina da basket
def move_ball():
    # Coordinate iniziali della pallina (a destra del centro del tavolo)
    ball_position = np.array([0.5, 0.3187999, -0.01479991])  # Modifica x per la posizione iniziale a destra
    # Coordinate finali della pallina (a sinistra del centro del tavolo)
    target_position = np.array([-0.5, 0.3187999, -0.01479991])  # Modifica x per la posizione finale a sinistra

    # Muovere il braccio verso la pallina
    move_arm(ball_position, duration=2.0)
    time.sleep(2.0)  # Attendere che il braccio raggiunga la posizione

    # Apertura della pinza per afferrare la pallina
    reachy.r_arm.r_gripper.goal_position = -50  # Aprire la pinza
    time.sleep(1.0)

    # Raggiungere la pallina
    move_arm(ball_position, duration=2.0)
    time.sleep(2.0)  # Attendere che il braccio raggiunga la posizione

    # Chiusura della pinza per afferrare la pallina
    reachy.r_arm.r_gripper.goal_position = -40  # Chiudere la pinza
    time.sleep(0.5)

    # Muovere il braccio verso la posizione finale a sinistra
    move_arm(target_position, duration=2.0)
    time.sleep(2.0)  # Attendere che il braccio raggiunga la posizione

    # Rilasciare la pallina
    reachy.r_arm.r_gripper.goal_position = -60  # Aprire la pinza
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