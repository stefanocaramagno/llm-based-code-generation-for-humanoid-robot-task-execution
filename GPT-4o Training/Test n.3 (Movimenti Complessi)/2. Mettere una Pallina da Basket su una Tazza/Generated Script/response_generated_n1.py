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
    target_matrix = np.array([
        [0, 0, -1, target[0]],
        [0, 1, 0, target[1]],
        [1, 0, 0, target[2]],
        [0, 0, 0, 1],
    ])

    joint_pos = reachy.r_arm.inverse_kinematics(target_matrix)
    reachy.turn_on('r_arm')
    goto({joint: pos for joint, pos in zip(reachy.r_arm.joints.values(), joint_pos)}, duration=duration)

# Funzione principale per posizionare la pallina sopra la tazza
def place_ball_on_cup():
    # Coordinate della pallina da basket (modifica in base alla tua scena)
    ball_position = np.array([0.1, 0.3187999, -0.01479991])  # Un po' a destra e sopra il centro del tavolo

    # Coordinate della tazza (da modificare in base alla posizione effettiva della tazza)
    cup_position = np.array([-0.1, 0.3187999, -0.01479991])  # Un po' più a sinistra rispetto alla pallina

    # Far guardare il robot verso la pallina
    look_at(ball_position)
    time.sleep(1)

    # Muovere il braccio sopra la pallina
    move_arm(ball_position + np.array([0, 0, 0.2]), duration=2.0)  # Posizione sopra la pallina
    time.sleep(1)

    # Apertura della pinza per afferrare la pallina
    reachy.r_arm.r_gripper.goal_position = -50  # Aprire la pinza
    time.sleep(1)

    # Muovere il braccio verso la pallina
    move_arm(ball_position, duration=2.0)
    time.sleep(2)

    # Chiusura della pinza per afferrare la pallina
    reachy.r_arm.r_gripper.goal_position = -40  # Chiudere la pinza
    time.sleep(1)

    # Muovere il braccio verso la tazza
    move_arm(cup_position + np.array([0, 0, 0.2]), duration=2.0)  # Posizione sopra la tazza
    time.sleep(1)

    # Abbassare il braccio per posizionare la pallina sulla tazza
    move_arm(cup_position, duration=2.0)
    time.sleep(1)

    # Apertura della pinza per rilasciare la pallina
    reachy.r_arm.r_gripper.goal_position = -60  # Aprire la pinza
    time.sleep(1)

    # Alzare il braccio dopo aver posizionato la pallina
    move_arm(cup_position + np.array([0, 0, 0.2]), duration=2.0)  # Alzare il braccio
    time.sleep(1)

if __name__ == "__main__":
    # Connessione al robot Reachy
    reachy = ReachySDK(host='localhost')

    # Eseguire la funzione per posizionare la pallina sopra la tazza
    place_ball_on_cup()

    # Spegnere il braccio destro del robot in modo graduale
    reachy.turn_off_smoothly('r_arm')

    # Uscire dal programma
    exit()