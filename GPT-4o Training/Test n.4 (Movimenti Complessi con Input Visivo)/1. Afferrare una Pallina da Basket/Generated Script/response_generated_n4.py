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

    joint_positions = reachy.r_arm.inverse_kinematics(target_matrix)

    reachy.turn_on('r_arm')

    goto({joint: pos for joint, pos in zip(reachy.r_arm.joints.values(), joint_positions)}, duration=duration)

# Funzione per eseguire il movimento di grasping
def grasp_ball():
    # Posizione della pallina da basket (x, y, z) rispetto a Reachy
    ball_position = np.array([0.1, 0.3187999, -0.01479991])  # Un po' a destra e sopra il centro del tavolo

    # Far guardare il robot verso la palla
    look_at(ball_position)

    # Muovere il braccio sopra la palla
    above_ball = np.array([ball_position[0], ball_position[1], ball_position[2] + 0.1])  # 10 cm sopra la palla
    move_arm(above_ball, 1.0)
    time.sleep(1.0)

    # Apertura della pinza
    reachy.r_arm.r_gripper.goal_position = -60  # Apertura della pinza
    time.sleep(1.0)

    # Muovere il braccio verso la palla
    move_arm(ball_position, 2.0)
    time.sleep(2.0)

    # Chiusura della pinza
    reachy.r_arm.r_gripper.goal_position = -40  # Chiusura della pinza
    time.sleep(0.5)

    # Alzare il braccio con la palla afferrata
    above_ball_after_grasp = np.array([ball_position[0], ball_position[1], ball_position[2] + 0.2])  # Alzare di 20 cm
    move_arm(above_ball_after_grasp, 2.0)
    time.sleep(1.0)

    # Spegnere il braccio destro del robot in modo graduale
    reachy.turn_off_smoothly('r_arm')

if __name__ == "__main__":
    # Connessione al robot Reachy
    reachy = ReachySDK(host='localhost')

    # Eseguire il movimento di afferramento
    grasp_ball()