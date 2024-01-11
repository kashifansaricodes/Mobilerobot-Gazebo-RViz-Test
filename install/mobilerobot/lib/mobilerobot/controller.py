import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from sensor_msgs.msg import Imu
import math
import time
import matplotlib.pyplot as plt

class controller (Node) :
    def _init_ (self) :
        super()._init_('control_node')

        #Publisher for velocity and position control
        self.publisher_vel = self.create_publisher( Float64MultiArray , '/velocity_controller/commands' , 10)
        self.publisher_pos = self.create_publisher( Float64MultiArray , '/position_controller/commands' , 10)

        #subscribe to IMU
        qos_profile = QoSProfile( reliability=ReliabilityPolicy.BEST_EFFORT, history=HistoryPolicy.KEEP_LAST, depth=10)
        self.pose_subscriber = self.create_subscription(Imu , '/imu_plugin/out' , self.callback , qos_profile)

        self.orientation = 0.0
        self.target_x = 10
        self.target_y = 10
        self.x = 0.0001
        self.y = 0.0001
        self.linear_vel = 3.0
        self.steering = 0.0
        self.wheelbase = 20
        self.error_angular = 0.0
        self.stop = 0.1
        self.kp = 0.1
        self.velocity = Float64MultiArray()
        self.position = Float64MultiArray()
        self.error = []
        self.timer =[]

    def callback (self , msg) :
        distance = math.sqrt((self.target_x - self.x) * 2 + (self.target_y - self.y) * 2)
        if distance > 1.5 :
            #velocity
            self.velocuty = Float64MultiArray(data=[self.linear_vel])
            #position
            orientation_q = msg.orientation
            self.orientation = 2.0 * math.atan2(orientation_q.z, orientation_q.w)
            self.error_angular = math.atan2(self.target_y-self.y, self.target_x-self.x)
            self.error.append(self.error_angular)
            self.timer.append(time.time())
            position_req = self.kp * self.error_angular
            self.position = Float64MultiArray(data=[position_req, position_req])
            #publish
            self.publisher_vel.publish(self.velocity)
            self.publisher_pos.publish(self.position)

            #Update position
            delta_x = self.linear_vel * math.cos(self.orientation+self.linear_vel/self.wheelbase*math.tan(self.steer_angle))
            delta_y = self.linear_vel * math.sin(self.orientation+self.linear_vel/self.wheelbase*math.tan(self.steer_angle))
            self.x = self.x + delta_x * 0.01
            self.y = self.y + delta_y * 0.01
        else :
            self.velocity.data = [0]
            self.position.data = [0 , 0]

        plt.plot(self.timer , self.error)
        plt.xlabel('time')
        plt.ylabel('value')
        plt.grid(True)
        plt.savefig('plot.png')


def main(args=None):
    rclpy.init(args=args)
    Controller = controller(node_name='custom_keyboard_control_node')

    try:
        rclpy.spin(Controller)
    except KeyboardInterrupt:
        pass

    Controller.destroy_node()
    rclpy.shutdown()

    plt.plot(Controller.timer , Controller.error)
    plt.xlabel('time')
    plt.ylabel('value')
    plt.grid(True)
    plt.savefig('plot3.png')

if __name__ == '__main__':
    main()