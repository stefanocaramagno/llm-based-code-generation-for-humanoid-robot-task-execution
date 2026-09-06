from reachy_sdk import ReachySDK
from reachy_sdk.trajectory import goto
from reachy_sdk.trajectory import InterpolationMode
import time
import numpy as np

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
def position_ball_above_cup():
    # Coordinate della pallina sopra la tazza
    ball_position = np.array([0.1, 0.3, 0.1])  # Un po' a destra e sopra il tavolo
    # Coordinate della tazza (centro del tavolo)
    cup_position = np.array([0, 0.3, -0.01])  # Al livello della superficie del tavolo

    # Muovere il braccio sopra la pallina
    move_arm(ball_position, duration=2.0)
    time.sleep(1)  # Attendere un momento

    # Apertura della pinza per simulare il posizionamento della pallina
    reachy.r_arm.r_gripper.goal_position = -60  # Aprire la pinza
    time.sleep(1)

    # Muovere il braccio verso la tazza
    move_arm(cup_position, duration=2.0)
    time.sleep(1)  # Attendere un momento

    # Chiusura della pinza per "posizionare" la pallina sopra la tazza
    reachy.r_arm.r_gripper.goal_position = -40  # Chiudere la pinza
    time.sleep(1)

    # Muovere il braccio per alzare il braccio dopo aver posizionato la pallina
    move_arm(cup_position + np.array([0, 0, 0.1]), duration=2.0)  # Alzare il braccio di 10 cm
    time.sleep(1)

# Codice eseguibile principale
if __name__ == "__main__":
    # Connessione al robot Reachy
    reachy = ReachySDK(host='localhost')

    # Eseguire la funzione per posizionare la pallina sopra la tazza
    position_ball_above_cup()

    # Spegnere il braccio destro del robot in modo graduale
    reachy.turn_off_smoothly('r_arm')

    # Uscire dal programma
    exit()