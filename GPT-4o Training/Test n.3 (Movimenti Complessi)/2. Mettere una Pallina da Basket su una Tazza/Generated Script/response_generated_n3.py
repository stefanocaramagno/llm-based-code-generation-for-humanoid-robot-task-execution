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
    goto({joint: pos for joint, pos in zip(
         reachy.r_arm.joints.values(), joint_pos)}, duration=duration)

# Funzione principale per posizionare la pallina sopra la tazza
def place_ball_above_cup():
    # Coordinate della pallina da basket (si presume che siano più a destra e sopra il centro del tavolo)
    ball_position = np.array([0.05, 0.3187999, -0.01479991])  # Aggiunta di 5 cm in x rispetto al centro
    cup_position = np.array([-0.1, 0.3187999, -0.01479991])  # Posizione della tazza a sinistra della pallina

    # Muovere il braccio sopra la palla per afferrarla
    above_ball_position = np.array([ball_position[0], ball_position[1], ball_position[2] + 0.1])  # 10 cm sopra la palla
    move_arm(above_ball_position, duration=1.0)
    time.sleep(1)

    # Raggiungere la pallina da basket
    move_arm(ball_position, duration=2.0)
    time.sleep(2)

    # Apertura della pinza per afferrare la pallina
    reachy.r_arm.r_gripper.goal_position = -50  # Apertura della pinza
    time.sleep(1)

    # Chiudere la pinza per afferrare la pallina
    reachy.r_arm.r_gripper.goal_position = -20  # Chiudere la pinza
    time.sleep(1)

    # Muovere il braccio sopra la tazza
    above_cup_position = np.array([cup_position[0], cup_position[1], cup_position[2] + 0.1])  # 10 cm sopra la tazza
    move_arm(above_cup_position, duration=1.0)
    time.sleep(1)

    # Posizionare la pallina sopra la tazza
    move_arm(cup_position, duration=1.0)
    time.sleep(1)

    # Rilasciare la pallina
    reachy.r_arm.r_gripper.goal_position = -60  # Apertura della pinza
    time.sleep(1)

    # Spegnere il braccio destro del robot in modo graduale
    reachy.turn_off_smoothly('r_arm')

# Codice eseguibile principale
if __name__ == "__main__":
    # Connessione al robot Reachy
    reachy = ReachySDK(host='localhost')

    # Eseguire la funzione di posizionamento
    place_ball_above_cup()