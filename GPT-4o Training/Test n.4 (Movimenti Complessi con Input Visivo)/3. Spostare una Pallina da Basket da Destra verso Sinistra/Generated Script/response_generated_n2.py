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
    joint_pos_ball = reachy.r_arm.inverse_kinematics(target_matrix)

    # Accensione del braccio destro
    reachy.turn_on('r_arm')

    # Movimento del braccio verso le posizioni delle giunture calcolate
    goto({joint: pos for joint, pos in zip(reachy.r_arm.joints.values(), joint_pos_ball)}, duration=duration)

# Funzione principale per spostare la pallina da basket
def move_ball():
    # Coordinate del tavolo e della pallina da basket
    table_position = np.array([0.3187999, 0, -1.204])  # Posizione del tavolo
    ball_offset = 0.1  # Offset per posizionare la pallina a destra del tavolo
    ball_position = np.array([table_position[0] + ball_offset, table_position[1], table_position[2] + 0.1])  # Posizione della pallina sopra il tavolo

    # Muovere il braccio sopra la pallina
    move_arm(ball_position, duration=2.0)
    time.sleep(1.0)  # Attendere che il braccio raggiunga la posizione

    # Posizionare il braccio sopra la pallina
    above_ball_position = np.array([ball_position[0], ball_position[1], ball_position[2] + 0.2])  # Posizione sopra la pallina
    move_arm(above_ball_position, duration=1.0)
    time.sleep(1.0)

    # Apertura della pinza per afferrare la pallina
    reachy.r_arm.r_gripper.goal_position = -50
    time.sleep(1.0)

    # Raggiungere la pallina per afferrarla
    move_arm(ball_position, duration=2.0)
    time.sleep(2.0)

    # Chiusura della pinza
    reachy.r_arm.r_gripper.goal_position = -40
    time.sleep(0.5)

    # Muovere la pallina a sinistra
    move_left_position = np.array([table_position[0] - ball_offset, table_position[1], table_position[2] + 0.1])  # Nuova posizione a sinistra
    move_arm(move_left_position, duration=2.0)
    time.sleep(1.0)

    # Apertura della pinza per rilasciare la pallina
    reachy.r_arm.r_gripper.goal_position = -60
    time.sleep(1.0)

    # Muovere il braccio sopra la posizione iniziale
    move_arm(above_ball_position, duration=1.0)
    time.sleep(1.0)

    # Spegnere il braccio destro del robot in modo graduale
    reachy.turn_off_smoothly('r_arm')

# Codice eseguibile principale
if __name__ == "__main__":
    # Connessione al robot Reachy
    reachy = ReachySDK(host='localhost')

    # Eseguire il movimento della pallina
    move_ball()

    # Uscire dal programma
    exit()