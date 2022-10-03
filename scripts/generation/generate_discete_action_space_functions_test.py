import generate_discete_action_space_functions as g

result1 = g.find_nearest_idx([1,2,3,4,5,6,9,15,24], 14)
assert result1 == 7, f"Expected 7 but recived {result1}"

result2 = g.find_remaining_angles([1,2,3,4,5,6,9,15,24], 8)
assert result2 == [9, 15, 24], f"Expected arrays to be the same but recived {result2}"

result3 = g.find_remaining_angles([1,2,3,4,5,6,9,15,24], 8)
assert result3 != [6, 9, 24], f"Expected arrays to NOT be the same but recived {result3}"