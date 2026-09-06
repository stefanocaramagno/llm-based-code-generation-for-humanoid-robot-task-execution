from reachy_sdk import ReachySDK
import numpy as np

def look_at(target):
    reachy.head.look_at(target[0], target[1], target[2], 1.0)

if __name__ == "__main__":
    # Connessione al robot Reachy
    reachy = ReachySDK(host='localhost')

    # Posizione del target (basketball) verso cui far guardare la testa 
    target_position = np.array([0.5, -0.3, -0.2])

    # Far guardare la testa del robot verso il target (basketball)
    look_at(target_position)
