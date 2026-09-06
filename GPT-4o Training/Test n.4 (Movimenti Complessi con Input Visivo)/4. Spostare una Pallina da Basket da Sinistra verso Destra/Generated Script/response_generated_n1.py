from reachy_sdk import ReachySDK
from reachy_sdk.trajectory import goto
from reachy_sdk.trajectory import InterpolationMode
import numpy as np
import time

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
    joint_pos = reachy.r_arm.inverse_kinematics(target_matrix)

    # Accensione del braccio destro
    reachy.turn_on('r_arm')

    # Movimento del braccio verso le posizioni delle giunture calcolate
    goto({joint: pos for joint, pos in zip(reachy.r_arm.joints.values(), joint_pos)}, duration=duration)

# Funzione principale per spostare la pallina da basket
def move_basketball():
    # Coordinate della pallina da basket (iniziale e finale)
    initial_position = np.array([-0.5, 0.3187999, -0.01479991])  # A sinistra
    final_position = np.array([0.5, 0.3187999, -0.01479991])     # A destra

    # Far guardare il robot verso la pallina da basket
    reachy.head.look_at(initial_position[0], initial_position[1], initial_position[2], duration=1.0)

    # Muovere il braccio allungabile sopra la pallina
    move_arm(initial_position, 2.0)  # Posizione iniziale
    time.sleep(1.0)

    # Apertura della pinza per afferrare la pallina
    reachy.r_arm.r_gripper.goal_position = -50  # Apertura della pinza
    time.sleep(1.0)

    # Raggiungere la pallina
    move_arm(initial_position, 2.0)
    time.sleep(2.0)

    # Chiusura della pinza per afferrare la pallina
    reachy.r_arm.r_gripper.goal_position = -10  # Chiusura della pinza
    time.sleep(1.0)

    # Spostare la pallina da sinistra a destra
    move_arm(final_position, 2.0)  # Muovi verso la posizione finale
    time.sleep(2.0)

    # Apertura della pinza per rilasciare la pallina
    reachy.r_arm.r_gripper.goal_position = -50  # Apertura della pinza
    time.sleep(1.0)

    # Riportare il braccio nella posizione iniziale
    move_arm(initial_position, 2.0)
    time.sleep(1.0)

    # Spegnere il braccio destro
    reachy.turn_off_smoothly('r_arm')

# Codice eseguibile principale
if __name__ == "__main__":
    # Connessione al robot Reachy
    reachy = ReachySDK(host='localhost')

    # Eseguire il movimento della pallina da basket
    move_basketball()

    # Uscire dal programma
    exit()