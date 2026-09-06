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
def place_ball_over_cup():
    # Coordinate della pallina e della tazza
    ball_position = np.array([0.4, -1.2, -0.014])  # Posizione della pallina
    cup_position = np.array([0.3, -1.2, -0.014])   # Posizione della tazza

    # Muovere il braccio sopra la pallina
    move_arm(ball_position, 2.0)
    time.sleep(1)

    # Apertura della pinza per afferrare la pallina
    reachy.r_arm.r_gripper.goal_position = -50
    time.sleep(1)

    # Muovere il braccio verso la tazza
    move_arm(cup_position, 2.0)
    time.sleep(1)

    # Posizionare la pallina sopra la tazza
    place_above_cup = np.array([cup_position[0], cup_position[1], cup_position[2] + 0.1])  # Alzare di 10 cm
    move_arm(place_above_cup, 2.0)
    time.sleep(1)

    # Chiudere la pinza per rilasciare la pallina
    reachy.r_arm.r_gripper.goal_position = -60
    time.sleep(1)

    # Riportare il braccio in una posizione neutra
    neutral_position = np.array([0, -1.5, 0])  # Posizione neutra arbitraria
    move_arm(neutral_position, 2.0)

if __name__ == "__main__":
    # Connessione al robot Reachy
    reachy = ReachySDK(host='localhost')

    # Eseguire la funzione per posizionare la pallina sopra la tazza
    place_ball_over_cup()

    # Spegnere il braccio destro del robot in modo graduale
    reachy.turn_off_smoothly('r_arm')