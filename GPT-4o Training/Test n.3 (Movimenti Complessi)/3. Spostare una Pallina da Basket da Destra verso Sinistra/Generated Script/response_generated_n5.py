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

# Funzione principale per spostare la pallina da basket
def move_basketball():
    # Coordinate del tavolo e posizione iniziale della pallina
    table_position = np.array([0.3187999, -1.204, -0.01479991])  # (x, y, z)
    ball_offset = 0.1  # Offset per posizionare la pallina un po' a destra

    # Posizione iniziale della pallina
    ball_position = np.array([table_position[0] + ball_offset, table_position[1], table_position[2]])

    # Spostamento della pallina verso sinistra
    target_position = np.array([table_position[0] - ball_offset, table_position[1], table_position[2]])

    # Muovere il braccio sopra la pallina
    move_arm(ball_position, duration=2.0)  # Muovi sopra la pallina
    time.sleep(1)

    # Afferrando la pallina (simulazione di chiusura della pinza)
    reachy.r_arm.r_gripper.goal_position = -40  # Chiudi la pinza
    time.sleep(1)

    # Muovere il braccio verso la posizione target (sinistra)
    move_arm(target_position, duration=2.0)  # Sposta la pallina verso sinistra
    time.sleep(1)

    # Rilasciare la pallina (simulazione di apertura della pinza)
    reachy.r_arm.r_gripper.goal_position = -60  # Apri la pinza
    time.sleep(1)

    # Tornare alla posizione iniziale
    move_arm(ball_position, duration=2.0)  # Torna sopra la pallina
    time.sleep(1)

if __name__ == "__main__":
    # Connessione al robot Reachy
    reachy = ReachySDK(host='localhost')

    # Eseguire il movimento della pallina
    move_basketball()

    # Spegnere il braccio destro del robot in modo graduale
    reachy.turn_off_smoothly('r_arm')

    # Uscire dal programma
    exit()