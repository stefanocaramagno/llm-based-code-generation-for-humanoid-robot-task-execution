from reachy_sdk import ReachySDK
from reachy_sdk.trajectory import goto
from reachy_sdk.trajectory import InterpolationMode
import time
import numpy as np

# Variabile globale per tenere traccia se il thread è in esecuzione
thread_running = False

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
    goto({joint: pos for joint, pos in zip(reachy.r_arm.joints.values(), joint_pos_ball)}, duration=duration)

# Funzione per eseguire il movimento di afferraggio
def grasp_ball():
    # Apertura della pinza
    reachy.r_arm.r_gripper.goal_position = -60
    time.sleep(1.0)

    # Coordinate della palla da basket
    ball_position = np.array([0.05, 0.3187999, -0.01479991])  # x, y, z (5 cm a destra del centro del tavolo)

    # Far guardare il robot verso la palla
    look_at(ball_position)

    # Muovere il braccio sopra la palla
    above_ball = np.array([ball_position[0], ball_position[1], ball_position[2] + 0.1])  # 10 cm sopra la palla
    move_arm(above_ball, 1.0)

    # Posizionare il braccio sopra la palla
    move_arm(ball_position, 1.0)

    # Chiusura della pinza per afferrare la palla
    reachy.r_arm.r_gripper.goal_position = -40
    time.sleep(0.5)

    # Alzare il braccio con la palla
    move_arm(np.array([ball_position[0], ball_position[1], ball_position[2] + 0.2]), 1.0)  # Alzare di 20 cm

    # Aggiornare lo stato del thread
    global thread_running
    thread_running = False

# Codice eseguibile principale
if __name__ == "__main__":
    reachy = ReachySDK(host='localhost')

    # Creare e avviare un thread per eseguire la funzione grasp_ball
    t = Thread(target=lambda: grasp_ball())
    t.daemon = True
    t.start()

    # Impostare lo stato del thread come in esecuzione
    thread_running = True

    # Loop per mantenere il programma in esecuzione fino al completamento del grasping
    while thread_running:
        time.sleep(0.1)

    # Spegnere il braccio destro del robot in modo graduale
    reachy.turn_off_smoothly('r_arm')

    # Uscire dal programma
    exit()