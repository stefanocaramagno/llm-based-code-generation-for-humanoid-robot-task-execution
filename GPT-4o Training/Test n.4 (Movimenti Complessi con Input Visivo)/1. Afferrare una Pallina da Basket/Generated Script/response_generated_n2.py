from reachy_sdk import ReachySDK
from reachy_sdk.trajectory import goto
from reachy_sdk.trajectory import InterpolationMode
import numpy as np
import time

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
    joint_pos = reachy.r_arm.inverse_kinematics(target_matrix)

    # Accensione del braccio destro
    reachy.turn_on('r_arm')

    # Movimento del braccio verso le posizioni delle giunture calcolate
    goto({joint: pos for joint, pos in zip(reachy.r_arm.joints.values(), joint_pos)}, duration=duration)

# Funzione per afferrare la pallina
def grasp_ball():
    # Coordinate della pallina da basket (modifica per la posizione reale)
    ball_position = np.array([0.1, 0.3187999, -0.01479991])  # Aggiungi offset x per posizionare la palla correttamente

    # Posizione sopra la palla per il movimento di afferraggio
    above_ball = np.array([ball_position[0], ball_position[1], ball_position[2] + 0.1])

    # Muovere il braccio sopra la palla
    move_arm(above_ball, 1.0)
    time.sleep(1)

    # Apertura della pinza
    reachy.r_arm.r_gripper.goal_position = -60  # Assicurati che questo valore apra la pinza
    time.sleep(1)

    # Muovere il braccio verso la palla
    move_arm(ball_position, 1.0)
    time.sleep(1)

    # Chiusura della pinza per afferrare la palla
    reachy.r_arm.r_gripper.goal_position = -20  # Modifica per chiudere la pinza attorno alla palla
    time.sleep(1)

    # Muovere il braccio verso l'alto dopo aver afferrato la palla
    move_arm(above_ball, 1.0)
    time.sleep(1)

# Codice eseguibile principale
if __name__ == "__main__":
    # Connessione al robot Reachy
    reachy = ReachySDK(host='localhost')

    # Eseguire l'azione di afferraggio
    grasp_ball()

    # Spegnere il braccio destro del robot in modo graduale
    reachy.turn_off_smoothly('r_arm')

    # Uscire dal programma
    exit()