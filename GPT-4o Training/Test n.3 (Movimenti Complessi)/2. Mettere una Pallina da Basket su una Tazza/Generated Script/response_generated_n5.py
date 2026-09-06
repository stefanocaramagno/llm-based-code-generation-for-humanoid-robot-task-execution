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
    joint_positions = reachy.r_arm.inverse_kinematics(target_matrix)

    # Accensione del braccio destro
    reachy.turn_on('r_arm')

    # Movimento del braccio verso le posizioni delle giunture calcolate
    goto({joint: pos for joint, pos in zip(reachy.r_arm.joints.values(), joint_positions)}, duration=duration)

# Funzione principale per posizionare la pallina sopra la tazza
def place_ball_on_cup():
    # Coordinate della pallina da basket
    ball_position = np.array([0.2, 0.3187999, -0.01479991])

    # Muovere il braccio verso la pallina
    move_arm(ball_position, duration=2.0)
    time.sleep(2)

    # Apertura della pinza per afferrare la pallina
    reachy.r_arm.r_gripper.goal_position = -60  # valore per afferrare
    time.sleep(1.0)

    # Sollevare la pallina sopra la tazza
    above_cup_position = np.array([0.1, 0.3187999, 0.05])  # altezza sopra la tazza
    move_arm(above_cup_position, duration=2.0)
    time.sleep(2)

    # Posizionare la pallina sopra la tazza
    cup_position = np.array([0.1, 0.3187999, -0.01479991])
    move_arm(cup_position, duration=1.0)
    time.sleep(2)

    # Rilasciare la pallina
    reachy.r_arm.r_gripper.goal_position = -10  # valore per rilasciare
    time.sleep(1.0)

    # Spegnere il braccio destro del robot in modo graduale
    reachy.turn_off_smoothly('r_arm')

# Codice eseguibile principale
if __name__ == "__main__":
    # Connessione al robot Reachy
    reachy = ReachySDK(host='localhost')

    # Eseguire il posizionamento della pallina sulla tazza
    place_ball_on_cup()

    # Uscire dal programma
    exit()