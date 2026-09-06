from reachy_sdk import ReachySDK
from reachy_sdk.trajectory import goto
from reachy_sdk.trajectory import InterpolationMode
import time
import numpy as np

# Funzione per muovere il braccio verso una posizione target con una durata specificata
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

# Funzione per eseguire il movimento di bere
def drink_movement():
    # Posizione iniziale sopra la testa del robot
    initial_position = np.array([0.4, -0.1, 0.5])
    move_arm(initial_position, 1.0)
    time.sleep(1.0)

    # Posizione per afferrare il bicchiere
    cup_position = np.array([0.4, -0.1, 0.0])
    move_arm(cup_position, 1.0)
    time.sleep(1.0)

    # Apertura della pinza per afferrare il bicchiere
    reachy.r_arm.r_gripper.goal_position = -60  # Apertura della pinza
    time.sleep(1.0)

    # Muovere il braccio verso la bocca
    mouth_position = np.array([0.4, -0.1, 0.15])
    move_arm(mouth_position, 1.0)
    time.sleep(1.0)

    # Simulazione del bere: mantenere la posizione per un momento
    time.sleep(2.0)

    # Rimuovere il bicchiere dalla bocca
    move_arm(cup_position, 1.0)
    time.sleep(1.0)

    # Chiusura della pinza
    reachy.r_arm.r_gripper.goal_position = -10  # Chiusura della pinza
    time.sleep(1.0)

    # Tornare alla posizione iniziale
    move_arm(initial_position, 1.0)

# Codice eseguibile principale
if __name__ == "__main__":
    # Connessione al robot Reachy
    reachy = ReachySDK(host='localhost')

    # Eseguire il movimento di bere
    drink_movement()

    # Spegnere il braccio destro del robot in modo graduale
    reachy.turn_off_smoothly('r_arm')

    # Uscire dal programma
    exit()