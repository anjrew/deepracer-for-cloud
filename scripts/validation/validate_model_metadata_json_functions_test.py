import validate_model_metadata_json_functions as vd


# Check Sensor properties
assert vd.check_sensor_property(["FRONT_FACING_CAMERA"])
assert vd.check_sensor_property(["FRONT_FACING_CAMERA", "LIDAR"])
assert vd.check_sensor_property(["STEREO_CAMERAS"])
assert vd.check_sensor_property(["STEREO_CAMERAS", "LIDAR"])
assert not vd.check_sensor_property(["STEREO_CAMERAS", "FRONT_FACING_CAMERA"])
assert not vd.check_sensor_property(
    ["STEREO_CAMERAS", "FRONT_FACING_CAMERA", "LIDAR"])
# assert vd.check_sensor_property(["NOT A VALID STRING"])
# assert vd.check_sensor_property("NOT AN ARRAY")


# Check neural network properties
assert vd.check_neural_network_property("DEEP_CONVOLUTIONAL_NETWORK")
assert vd.check_neural_network_property("DEEP_CONVOLUTIONAL_NETWORK_SHALLOW")
assert vd.check_neural_network_property("DEEP_CONVOLUTIONAL_NETWORK_DEEP")
# assert vd.check_neural_network_property("NOT A VALID STRING")
# assert vd.check_neural_network_property(["NOT A VALID TYPE"])


# Check action space

discrete_action_space = [
    {
        "steering_angle": -30,
        "speed": 0.6
    },
    {
        "steering_angle": -15,
        "speed": 0.6
    },
    {
        "steering_angle": 0,
        "speed": 0.6
    },
    {
        "steering_angle": 15,
        "speed": 0.6
    },
    {
        "steering_angle": 30,
        "speed": 0.6
    }
]

continuous_action_space = {
    "speed": {
        "high": 2,
        "low": 1
    },
    "steering_angle": {
        "high": 30,
        "low": -30
    }
}

assert "continuous" == vd.get_action_space_label(continuous_action_space)
assert "discrete" != vd.get_action_space_label(continuous_action_space)
assert "discrete" == vd.get_action_space_label(discrete_action_space)
assert "continuous" != vd.get_action_space_label(discrete_action_space)
assert "random" != vd.get_action_space_label(discrete_action_space)
assert vd.check_valid_action_space_property("continuous", continuous_action_space)
assert vd.check_valid_action_space_property("discrete", discrete_action_space)
# assert vd.check_valid_action_space_property("discrete", {})
