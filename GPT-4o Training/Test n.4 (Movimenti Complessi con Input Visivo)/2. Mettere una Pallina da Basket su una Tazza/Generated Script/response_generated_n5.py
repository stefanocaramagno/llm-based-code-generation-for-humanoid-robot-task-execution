from reachy_sdk import ReachySDK
from reachy_sdk.trajectory import goto, InterpolationMode
import numpy as np
import time

# Funzione per muovere il braccio del robot verso una posizione target con una durata specificata
def move_arm_to(target, duration):
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

# Funzione principale per posizionare la pallina sopra la tazza
def place_ball_on_cup():
    # Coordinate della pallina da basket
    ball_position = np.array([0.1, -0.3, -0.2])  # Adattare in base alla posizione reale
    # Coordinate della tazza
    cup_position = np.array([-0.1, -0.3, -0.2])  # Adattare in base alla posizione reale

    # Muovere il braccio sopra la pallina
    move_arm_to(ball_position, 2.0)
    time.sleep(1)

    # Apertura della pinza per afferrare la pallina
    reachy.r_arm.r_gripper.goal_position = -50  # Valore da adattare per afferrare la pallina
    time.sleep(1)

    # Muovere il braccio verso la tazza
    move_arm_to(cup_position, 2.0)
    time.sleep(1)

    # Posizionare la pallina sopra la tazza
    reachy.r_arm.r_gripper.goal_position = -60  # Valore per rilasciare la pallina
    time.sleep(1)

    # Muovere il braccio indietro dopo il rilascio
    move_arm_to(ball_position + np.array([0, 0, 0.1]), 2.0)  # Muovere verso l'alto dopo il rilascio

# Codice eseguibile principale
if __name__ == "__main__":
    # Connessione al robot Reachy
    reachy = ReachySDK(host='localhost')

    # Eseguire la funzione principale
    place_ball_on_cup()

    # Spegnere il braccio destro del robot in modo graduale
    reachy.turn_off_smoothly('r_arm')

    # Uscire dal programma
    exit()