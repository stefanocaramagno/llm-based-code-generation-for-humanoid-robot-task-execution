from reachy_sdk import ReachySDK
from reachy_sdk.trajectory import goto
from reachy_sdk.trajectory import InterpolationMode
import time
import cv2 as cv
import numpy as np

from threading import Thread

# Variabile globale per tenere traccia se il thread è in esecuzione
thread_running = False

# Funzione per far guardare il robot verso un obiettivo
def look_at(target):
    reachy.head.look_at(
        target[0], target[1], target[2], 1.0)

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
    goto({joint: pos for joint, pos in zip(
         reachy.r_arm.joints.values(), joint_pos_ball)}, duration=duration)

# Funzione per eseguire il movimento di lancio
def throw_movement():

    # Apertura della pinza
    reachy.r_arm.r_gripper.goal_position = -60

    # Posizione angolare del braccio destro per il lancio
    right_angled_position = {
        reachy.r_arm.r_shoulder_pitch: -90,
        reachy.r_arm.r_shoulder_roll: 0,
        reachy.r_arm.r_arm_yaw: 0,
        reachy.r_arm.r_elbow_pitch: 0,
        reachy.r_arm.r_forearm_yaw: 0,
        reachy.r_arm.r_wrist_pitch: 0,
        reachy.r_arm.r_wrist_roll: 10,
    }

    # Movimento del braccio verso la posizione di lancio
    goto(
        goal_positions=right_angled_position,
        duration=0.2,
        interpolation_mode=InterpolationMode.MINIMUM_JERK
    )

# Funzione principale per il movimento di basket
def basketball():

    # Position Basket Ball (3) 
    # ball_position = np.array([-0.356,0.832,-0.29]) # In riferimento al centro della scena (0,0,0)
    ball_position = np.array([0.3478,-0.1248,-0.3719999]) # In riferimento a Reachy

    # Far guardare il robot verso la palla
    look_at(ball_position)

    # Muovere il braccio allungabile sopra la palla evitando la palla
    avoid_ball = np.array([ball_position[0]-0.05, ball_position[1]-0.10, 0])
    move_arm(avoid_ball, 1.0)

    # Posizionare il braccio sopra la palla
    above_ball = np.array([ball_position[0]-0.05, ball_position[1], 0])
    move_arm(above_ball, 1.0)

    # Apertura della pinza
    reachy.r_arm.r_gripper.goal_position = -50
    time.sleep(1.0)

    # Raggiungere la palla
    move_arm(ball_position, 4.0)
    time.sleep(2.0)

    # Chiusura della pinza
    reachy.r_arm.r_gripper.goal_position = -40
    time.sleep(0.5)

    # Alzare il braccio e lanciare la palla
    move_arm(above_ball, 4.0)

    # Eseguire il movimento di lancio
    throw_movement()
    time.sleep(1)

    # Aggiornare lo stato del thread
    global thread_running
    thread_running = False

# Codice eseguibile principale
if __name__ == "__main__":
    
    # Connessione al robot Reachy
    reachy = ReachySDK(host='localhost')
    
    # Creare e avviare un thread per eseguire la funzione basketball
    t = Thread(target=lambda: basketball())
    t.daemon = True
    t.start()
    
    # Impostare lo stato del thread come in esecuzione
    thread_running = True

    # Loop per mostrare le immagini della telecamera destra del robot
    while (thread_running):
        cv.imshow('Right camera', reachy.right_camera.last_frame)
        cv.waitKey(30)
    
    # Chiudere tutte le finestre di OpenCV
    cv.destroyAllWindows()
    
    # Spegnere il braccio destro del robot in modo graduale
    reachy.turn_off_smoothly('r_arm')

    # Uscire dal programma
    exit()