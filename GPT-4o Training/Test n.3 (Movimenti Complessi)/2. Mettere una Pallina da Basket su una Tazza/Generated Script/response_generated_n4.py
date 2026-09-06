from reachy_sdk import ReachySDK
from reachy_sdk.trajectory import goto
from reachy_sdk.trajectory import InterpolationMode
import time
import numpy as np

# Funzione per far guardare il robot verso un obiettivo
def look_at(target):
    reachy.head.look_at(target[0], target[1], target[2], 1.0)

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
    goto({joint: pos for joint, pos in zip(reachy.r_arm.joints.values(), joint_pos_ball)}, duration=duration)

# Funzione principale per posizionare la pallina sopra la tazza
def place_ball_on_cup():
    # Coordinate della pallina da basket
    ball_position = np.array([0.1, 0.4, -0.1])  # Modifica le coordinate in base alla tua scena
    # Coordinate della tazza (posizionata sopra il tavolo)
    cup_position = np.array([0.0, 0.3, -0.1])  # Modifica le coordinate in base alla tua scena

    # Far guardare il robot verso la pallina
    look_at(ball_position)

    # Muovere il braccio sopra la pallina
    move_arm(ball_position + np.array([0, 0, 0.1]), 1.0)  # Muovi sopra la pallina

    # Apertura della pinza
    reachy.r_arm.r_gripper.goal_position = -50
    time.sleep(1.0)

    # Muovere il braccio verso la pallina
    move_arm(ball_position, 2.0)
    time.sleep(1.0)

    # Chiusura della pinza
    reachy.r_arm.r_gripper.goal_position = -40
    time.sleep(0.5)

    # Muovere sopra la tazza
    move_arm(cup_position + np.array([0, 0, 0.1]), 1.0)  # Muovi sopra la tazza

    # Muovere giù sopra la tazza
    move_arm(cup_position, 1.0)
    time.sleep(1.0)

    # Rilasciare la pallina
    reachy.r_arm.r_gripper.goal_position = -60  # Aggiusta la posizione per rilasciare
    time.sleep(1.0)

    # Muovere il braccio indietro
    move_arm(cup_position + np.array([0, -0.2, 0]), 1.0)  # Muovi indietro dal tavolo
    time.sleep(1.0)

    # Spegnere il braccio destro del robot in modo graduale
    reachy.turn_off_smoothly('r_arm')

if __name__ == "__main__":
    # Connessione al robot Reachy
    reachy = ReachySDK(host='localhost')

    # Eseguire la funzione per posizionare la pallina sopra la tazza
    place_ball_on_cup()