import random

def init_chromosome(num_pairs):
    tutors = list(range(num_pairs))
    random.shuffle(tutors)
    return tutors
