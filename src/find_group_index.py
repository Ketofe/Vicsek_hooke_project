#Made using chat gpt
def find_group_index(Index_limit_of_each_group, particle_index):
    for n, limit in enumerate(Index_limit_of_each_group):
        if particle_index < limit:  # If the particle index is less than the current limit
            return n
    return len(Index_limit_of_each_group) - 1  # If index exceeds all limits, assign to the last group