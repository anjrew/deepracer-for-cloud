import generate_discete_action_space_functions as g
import pytest


def test_finding_index():
    result1 = g.find_nearest_idx([1, 2, 3, 4, 5, 6, 9, 15, 24], 14)
    assert result1 == 7, f"Expected 7 but recived {result1}"


def test_findin_remaining_angles():
    result2 = g.find_remaining_angles([1, 2, 3, 4, 5, 6, 9, 15, 24], 8)
    assert result2 == [
        9, 15, 24], f"Expected arrays to be the same but recived {result2}"
    result3 = g.find_remaining_angles([1, 2, 3, 4, 5, 6, 9, 15, 24], 8)
    assert result3 != [
        6, 9, 24], f"Expected arrays to NOT be the same but recived {result3}"


def test_direction_of_zero_should_throw():
    with pytest.raises(Exception) as e_info:
         g.create_direction_actions(
        [0, 2, 3, 4, 5, 6, 9, 15, 24], [1, 2], 8, 2)
         assert e_info == 'A steering range of "0" should not be used in the "create_direction_actions" to make actions'

# def test_direction_of_zero_should_throw():
#     with pytest.raises(Exception) as e_info:
#          g.create_actions_for_speeds(
#         [0, 2, 3, 4, 5, 6, 9, 15, 24], [1, 2], 8, 2)
#          assert e_info == 'A steering range of "0" should not be used in the "create_direction_actions" to make actions'
    
    

