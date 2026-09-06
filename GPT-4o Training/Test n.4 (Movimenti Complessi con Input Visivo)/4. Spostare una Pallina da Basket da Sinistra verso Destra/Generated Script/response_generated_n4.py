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
def move_basketball():
    # Coordinate della pallina (partenza a sinistra)
    initial_position = np.array([-0.2, 0.3187999, -0.01479991])  # Modifica l'asse x per la posizione iniziale
    # Coordinate della pallina (arrivo a destra)
    final_position = np.array([0.2, 0.3187999, -0.01479991])  # Modifica l'asse x per la posizione finale

    # Muovere il braccio alla posizione iniziale sopra la pallina
    move_arm(initial_position, 2.0)
    time.sleep(1.0)  # Attendere un attimo

    # Afferrare la pallina (apertura della pinza)
    reachy.r_arm.r_gripper.goal_position = -50
    time.sleep(1.0)

    # Raggiungere la pallina
    move_arm(initial_position, 2.0)
    time.sleep(2.0)  # Attendere per il movimento

    # Chiudere la pinza per afferrare la pallina
    reachy.r_arm.r_gripper.goal_position = -40
    time.sleep(0.5)

    # Muovere il braccio alla posizione finale a destra
    move_arm(final_position, 2.0)
    time.sleep(1.0)  # Attendere un attimo

    # Rilasciare la pallina
    reachy.r_arm.r_gripper.goal_position = -60
    time.sleep(1.0)

    # Spegnere il braccio destro del robot in modo graduale
    reachy.turn_off_smoothly('r_arm')

if __name__ == "__main__":
    # Connessione al robot Reachy
    reachy = ReachySDK(host='localhost')

    # Eseguire il movimento di spostamento della pallina da basket
    move_basketball()

    # Uscire dal programma
    exit()