#!/usr/bin/env python
import rospy
import random
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseWithCovarianceStamped, Twist

class PubCmd():
    
    def __init__(self):
        self.odom_subscriber = rospy.Subscriber('/odometry/filtered', Odometry, self.odom_callback)
        self.cmd_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        self.odom_msg = Odometry()
        self.pub_msg = Twist()
        self.ctrl_c = False
        rospy.on_shutdown(self.shutdownhook)
        self.rate = rospy.Rate(10)
    
    def shutdownhook(self):
        # works better than the rospy.is_shut_down()
        self.ctrl_c = True
        self.pub_msg.linear.x = 0.0
        self.pub_msg.linear.y = 0.0
        self.pub_msg.angular.z = 0.0
        self.cmd_publisher.publish(self.pub_msg)

    def odom_callback(self, msg):
        self.odom_msg = msg
    
    # def pub_first(self):
    #     rand_float = random.uniform(-0.5,0.5)
    #     self.pub_msg.linear.x = 0.5
    #     self.pub_msg.linear.y = 0.0
    #     self.pub_msg.angular.z = 0.5

    def pub_prepare(self):
        self.pub_msg.linear.x = self.odom_msg.twist.twist.linear.x
        self.pub_msg.linear.y = self.odom_msg.twist.twist.linear.y
        self.pub_msg.linear.z = self.odom_msg.twist.twist.linear.z
        self.pub_msg.angular.x = self.odom_msg.twist.twist.angular.x
        self.pub_msg.angular.y = self.odom_msg.twist.twist.angular.y
        self.pub_msg.angular.z = self.odom_msg.twist.twist.angular.z
        
    def publish_cmd(self):
        # loop to publish the odometry values
        while not rospy.is_shutdown():
            # self.pub_first()
            # self.cmd_publisher.publish(self.pub_msg)
            self.pub_prepare()
            self.cmd_publisher.publish(self.pub_msg)
            self.rate.sleep()
            
if __name__ == '__main__':
    rospy.init_node('pub_cmd', anonymous=True)
    cmd_object = PubCmd()
    try:
        cmd_object.publish_cmd()
    except rospy.ROSInterruptException:
        pass
