# ros-object-mask-generator

Generate a mask of any object in the camera frame

### Currently implemented:
Color based masking. Provide HSV bounds and resultant mask is published on ROS topic `/mask` with type `sensor_msgs/Image`

### To do:
Yolo based detection and masking
