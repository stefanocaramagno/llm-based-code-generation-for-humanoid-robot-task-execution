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

    joint_pos_ball = reachy.r_arm.inverse_kinematics(target_matrix)

    reachy.turn_on('r_arm')

    goto({joint: pos for joint, pos in zip(
         reachy.r_arm.joints.values(), joint_pos_ball)}, duration=duration)

# Funzione principale per posizionare la pallina sopra la tazza
def place_ball_over_cup():
    # Coordinate della pallina e della tazza
    ball_position = np.array([0.1, 0.35, 0.1])  # Posizione della pallina
    cup_position = np.array([-0.2, 0.3187999, 0])  # Posizione della tazza

    # Far guardare il robot verso la pallina
    look_at(ball_position)

    # Muovere il braccio sopra la pallina
    move_arm(ball_position, duration=2.0)
    time.sleep(2)

    # Apertura della pinza per afferrare la pallina (supponendo che la pinza possa afferrare)
    reachy.r_arm.r_gripper.goal_position = -60  # Aprire la pinza
    time.sleep(1.0)

    # Muovere il braccio verso il tavolo sopra la tazza
    above_cup = np.array([cup_position[0], cup_position[1], cup_position[2] + 0.1])  # Posizione sopra la tazza
    move_arm(above_cup, duration=2.0)
    time.sleep(2)

    # Abbassare il braccio sopra la tazza
    move_arm(cup_position, duration=2.0)
    time.sleep(2)

    # Chiusura della pinza per rilasciare la pallina
    reachy.r_arm.r_gripper.goal_position = -40  # Chiudere la pinza
    time.sleep(1.0)

    # Muovere il braccio indietro dopo aver posizionato la pallina
    move_arm(above_cup, duration=2.0)
    time.sleep(2)

    # Spegnere il braccio destro del robot in modo graduale
    reachy.turn_off_smoothly('r_arm')

# Codice eseguibile principale
if __name__ == "__main__":
    # Connessione al robot Reachy
    reachy = ReachySDK(host='localhost')

    # Eseguire la funzione per posizionare la pallina sopra la tazza
    place_ball_over_cup()