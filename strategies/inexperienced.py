"""
Random strategy functionality
"""
import random


# Decides action - hit or stand
def take_action():
    action = random.choice(["hit", "stand"])
    return action
