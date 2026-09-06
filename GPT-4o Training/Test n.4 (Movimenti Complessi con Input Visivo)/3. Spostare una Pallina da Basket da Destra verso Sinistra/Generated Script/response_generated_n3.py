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
    joint_pos = reachy.r_arm.inverse_kinematics(target_matrix)

    # Accensione del braccio destro
    reachy.turn_on('r_arm')

    # Movimento del braccio verso le posizioni delle giunture calcolate
    goto({joint: pos for joint, pos in zip(reachy.r_arm.joints.values(), joint_pos)}, duration=duration)

# Funzione principale per spostare la pallina da basket
def move_ball():
    # Coordinate iniziali della pallina da basket (a destra rispetto al centro del tavolo)
    ball_position = np.array([0.1, 0.3187999, -0.01479991])  # x, y, z (con x positivo verso destra)

    # Coordinate finali della pallina da basket (a sinistra rispetto al centro del tavolo)
    target_position = np.array([-0.1, 0.3187999, -0.01479991])  # x, y, z (con x negativo verso sinistra)

    # Muovere il braccio verso la pallina da basket iniziale
    print("Muovere il braccio verso la pallina da basket iniziale...")
    move_arm(ball_position, duration=2.0)
    time.sleep(1)

    # Aprire la pinza per afferrare la pallina
    reachy.r_arm.r_gripper.goal_position = -50
    time.sleep(1)

    # Muovere il braccio verso la pallina da basket finale
    print("Spostare la pallina da basket verso sinistra...")
    move_arm(target_position, duration=2.0)
    time.sleep(1)

    # Chiudere la pinza per rilasciare la pallina
    reachy.r_arm.r_gripper.goal_position = -60
    time.sleep(1)

# Codice eseguibile principale
if __name__ == "__main__":
    # Connessione al robot Reachy
    reachy = ReachySDK(host='localhost')

    # Eseguire il movimento della pallina da basket
    move_ball()

    # Spegnere il braccio destro del robot in modo graduale
    reachy.turn_off_smoothly('r_arm')

    # Uscire dal programma
    exit()