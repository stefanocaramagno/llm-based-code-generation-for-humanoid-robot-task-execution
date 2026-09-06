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
    joint_positions = reachy.r_arm.inverse_kinematics(target_matrix)

    # Accensione del braccio destro
    reachy.turn_on('r_arm')

    # Movimento del braccio verso le posizioni delle giunture calcolate
    goto({joint: pos for joint, pos in zip(reachy.r_arm.joints.values(), joint_positions)}, duration=duration)

# Funzione per simulare il movimento di bere
def drinking_movement():
    # Posizione iniziale del bicchiere
    glass_position = np.array([0.4, -0.2, 0.1])  # Cambia le coordinate in base alla tua scena

    # Muovere il braccio verso il bicchiere
    move_arm(glass_position, duration=2.0)
    time.sleep(1.0)  # Attendere che il braccio raggiunga la posizione

    # Afferrando il bicchiere (simulazione)
    reachy.r_arm.r_gripper.goal_position = -50  # Apertura della pinza per afferrare il bicchiere
    time.sleep(1.0)

    # Portare il bicchiere alla bocca
    mouth_position = np.array([0.2, -0.1, 0.3])  # Cambia le coordinate in base alla tua scena
    move_arm(mouth_position, duration=2.0)
    time.sleep(1.0)  # Attendere che il braccio raggiunga la posizione

    # Simulazione di bere (chiudere la pinza per "bere")
    reachy.r_arm.r_gripper.goal_position = -80  # Chiusura della pinza
    time.sleep(1.0)

    # Riportare il bicchiere nella posizione iniziale
    move_arm(glass_position, duration=2.0)
    time.sleep(1.0)

    # Rilasciare il bicchiere
    reachy.r_arm.r_gripper.goal_position = -50  # Apertura della pinza
    time.sleep(1.0)

# Codice eseguibile principale
if __name__ == "__main__":
    # Connessione al robot Reachy
    reachy = ReachySDK(host='localhost')

    # Eseguire il movimento di bere
    drinking_movement()

    # Spegnere il braccio destro del robot in modo graduale
    reachy.turn_off_smoothly('r_arm')

    # Uscire dal programma
    exit()