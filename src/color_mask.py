#!/usr/bin/env python2.7

import numpy as np
import cv2 as cv
import rospy
from sensor_msgs.msg import Image
from std_msgs.msg import Header
from cv_bridge import CvBridge


def generate_color_mask(ros_image):

    # Convert ROS Image to CV2 image
    img = bridge.imgmsg_to_cv2(ros_image, desired_encoding='bgr8')

    # Create mask
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    mask = cv.inRange(hsv, lower, upper)

    # Filter mask
    if filter:
        mask = cv.medianBlur(mask, window_size)

    # Convert CV2 image to ROS Image
    ros_mask = bridge.cv2_to_imgmsg(mask, encoding="mono8")
    
    header = Header()
    header.stamp = rospy.Time.now()
    ros_mask.header = header

    # Publish mask
    pub.publish(ros_mask)


if __name__ == '__main__':
    rospy.init_node('mask_generation', anonymous=False)
    
    # Read params
    source_topic = rospy.get_param("/color_mask/image_source")
    output_topic = rospy.get_param("/color_mask/output")
    lower = np.array([rospy.get_param("/color_mask/lower_h"), rospy.get_param("/color_mask/lower_s"), rospy.get_param("/color_mask/lower_v")])
    upper = np.array([rospy.get_param("/color_mask/upper_h"), rospy.get_param("/color_mask/upper_s"), rospy.get_param("/color_mask/upper_v")])
    filter = rospy.get_param("/color_mask/filter")
    if filter:
        window_size = rospy.get_param("/color_mask/window_size")

    # Defaults
    if source_topic == "":
        source_topic = "/usb_cam/image_raw"
    if output_topic == "":
        output_topic = "/mask"
    if filter == None:
        filter = False

    rospy.Subscriber(source_topic, Image, generate_color_mask)
    pub = rospy.Publisher(output_topic, Image, queue_size=10)
    
    bridge = CvBridge()

    rospy.spin()