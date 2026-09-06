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

# Funzione principale per posizionare la pallina sopra la tazza
def position_ball_over_cup():
    # Coordinate della pallina da basket
    ball_position = np.array([0.1, 0.35, 0.1])  # Modifica in base alla scena
    # Coordinate della tazza
    cup_position = np.array([0.0, 0.35, -0.1])  # Modifica in base alla scena

    # Muovere il braccio sopra la tazza
    move_arm(cup_position + np.array([0, 0, 0.1]), 2.0)  # Muovi sopra la tazza
    time.sleep(1.0)

    # Posizionare la pallina da basket sopra la tazza
    move_arm(ball_position, 2.0)  # Muovi alla posizione della pallina
    time.sleep(1.0)

    # Eseguire l'azione di rilascio della pallina (opzionale, a seconda della configurazione)
    reachy.r_arm.r_gripper.goal_position = -60  # Apertura della pinza per rilasciare
    time.sleep(1.0)

    # Chiusura della pinza (facoltativo, se necessario)
    reachy.r_arm.r_gripper.goal_position = -40  # Chiusura della pinza
    time.sleep(1.0)

    # Spegnere il braccio destro del robot in modo graduale
    reachy.turn_off_smoothly('r_arm')

# Codice eseguibile principale
if __name__ == "__main__":
    # Connessione al robot Reachy
    reachy = ReachySDK(host='localhost')

    # Eseguire la funzione per posizionare la pallina sopra la tazza
    position_ball_over_cup()