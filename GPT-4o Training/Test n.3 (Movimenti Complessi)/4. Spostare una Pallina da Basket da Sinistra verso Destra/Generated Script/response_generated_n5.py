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
    goto({joint: pos for joint, pos in zip(
         reachy.r_arm.joints.values(), joint_pos)}, duration=duration)

# Funzione principale per spostare la pallina da basket
def move_ball():
    # Coordinate iniziali della pallina da basket
    ball_initial_position = np.array([-0.2, 0.3187999, -1.204])  # Un po' a sinistra rispetto al centro
    # Coordinate finali della pallina da basket (spostata a destra)
    ball_final_position = np.array([0.2, 0.3187999, -1.204])  # Spostata a destra

    # Far guardare il robot verso la palla inizialmente
    reachy.head.look_at(ball_initial_position[0], ball_initial_position[1], ball_initial_position[2], 1.0)
    time.sleep(1.0)

    # Muovere il braccio sopra la palla
    move_arm(ball_initial_position, 2.0)
    time.sleep(1.0)

    # Apertura della pinza per afferrare la palla
    reachy.r_arm.r_gripper.goal_position = -50  # Apertura della pinza
    time.sleep(1.0)

    # Raggiungere la palla
    move_arm(ball_initial_position, 2.0)
    time.sleep(1.0)

    # Chiusura della pinza per afferrare la palla
    reachy.r_arm.r_gripper.goal_position = -40  # Chiusura della pinza
    time.sleep(1.0)

    # Sollevare la palla sopra il tavolo
    above_ball_position = np.array([-0.2, 0.3187999, -1.154])  # Un po' più in alto
    move_arm(above_ball_position, 2.0)
    time.sleep(1.0)

    # Muovere il braccio verso la posizione finale della pallina
    move_arm(ball_final_position, 2.0)
    time.sleep(1.0)

    # Abbassare il braccio per posizionare la pallina
    drop_position = np.array([0.2, 0.3187999, -1.204])  # Posizione finale
    move_arm(drop_position, 2.0)
    time.sleep(1.0)

    # Apertura della pinza per rilasciare la palla
    reachy.r_arm.r_gripper.goal_position = -60  # Apertura della pinza
    time.sleep(1.0)

    # Spegnere il braccio destro del robot in modo graduale
    reachy.turn_off_smoothly('r_arm')

# Codice eseguibile principale
if __name__ == "__main__":
    # Connessione al robot Reachy
    reachy = ReachySDK(host='localhost')

    # Eseguire la funzione per spostare la pallina
    move_ball()

    # Uscire dal programma
    exit()