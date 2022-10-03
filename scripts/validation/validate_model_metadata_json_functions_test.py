import validate_model_metadata_json_functions as vd


"""Chec Sensor properties"""

["FRONT_FACING_CAMERA", "STEREO_CAMERAS"]
["LIDAR"] 
assert vd.check_sensor_property(["FRONT_FACING_CAMERA"])
assert vd.check_sensor_property(["FRONT_FACING_CAMERA", "LIDAR"])
assert vd.check_sensor_property(["STEREO_CAMERAS"])
assert vd.check_sensor_property(["STEREO_CAMERAS", "LIDAR"])
assert not vd.check_sensor_property(["STEREO_CAMERAS", "FRONT_FACING_CAMERA"])
assert not vd.check_sensor_property(["STEREO_CAMERAS", "FRONT_FACING_CAMERA", "LIDAR"])
