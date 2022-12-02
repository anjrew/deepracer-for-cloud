from tensorflow.python.client import device_lib
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()

def get_available_gpus():
    local_device_protos = device_lib.list_local_devices()
    return [x.name for x in local_device_protos if x.device_type == 'GPU']

gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.05)
sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options))
print(get_available_gpus())
