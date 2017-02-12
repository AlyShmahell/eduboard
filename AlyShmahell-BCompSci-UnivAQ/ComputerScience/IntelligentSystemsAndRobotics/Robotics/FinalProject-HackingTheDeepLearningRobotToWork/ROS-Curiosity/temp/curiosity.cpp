#include <vector>
#include <string>
#include <math.h>
#include <ros/ros.h>
#include <nav_msgs/Odometry.h>
#include <geometry_msgs/Twist.h>
#include "tf/tf.h"
#include <tf/transform_listener.h>


ros::Publisher velocityPublisher;
ros::Subscriber poseSubscriber;

nav_msgs::Odometry odometryPose;
std::pair<double,double> targetCoordinates;
double targetBearing;

void thinkFunction();
void moveLinear(double speed, double distance, bool isForward);
void rotateRadian(double ang_vel, double angle_radian, bool isClockwise);
double degreeToradian(double degreeAngle);
double radianTodegree(double radianAngle);
double calculateBearing( double x1, double y1, double x2,double y2);


struct LandMarkDistance
{
    std::string name;
    float distance;
} vacinity;

class LandMark
{
public:
    LandMark(std::string Name, double X, double Y):name(Name),x(X),y(Y) {}
    std::string name;
    double x,y;
};

class LandMarkMonitor
{
public:

    std::vector<LandMark> LandmarkVector;

    LandMarkMonitor()
    {
        LandmarkVector.push_back(LandMark("cube",1.44,-0.98));
        LandmarkVector.push_back(LandMark("dumpster",0.99,-3.44));
        LandmarkVector.push_back(LandMark("cylinder",-2.00,-3.48));
        LandmarkVector.push_back(LandMark("barrier",-4.00,-1.00));
        LandmarkVector.push_back(LandMark("bookshelf",0.00,-1.53));
    }

    void OdometryCallBack(const nav_msgs::Odometry::ConstPtr& msg)
    {
        vacinity.distance=-1;
        for(size_t i=0; i<LandmarkVector.size(); i++)
        {
            double distance = sqrt((LandmarkVector[i].x-msg->pose.pose.position.x)*(LandmarkVector[i].x-msg->pose.pose.position.x)+(LandmarkVector[i].y-msg->pose.pose.position.y)*(LandmarkVector[i].y-msg->pose.pose.position.y));

            if(vacinity.distance==-1||distance<vacinity.distance)
            {
                vacinity.distance = distance;
                vacinity.name = LandmarkVector[i].name;
            }
        }
        odometryPose.pose.pose.position.x = msg->pose.pose.position.x;
        odometryPose.pose.pose.position.y = msg->pose.pose.position.y;

        ROS_INFO("closest to: %s, within: %f, Bearing: %f",vacinity.name.c_str(),vacinity.distance,targetBearing);
    }
};




int main(int argc, char** argv)
{
    ros::init(argc, argv, "curiosity");
    ros::NodeHandle node;
    LandMarkMonitor monitor;
    velocityPublisher = node.advertise<geometry_msgs::Twist>("/cmd_vel_mux/input/teleop", 1000);
    poseSubscriber = node.subscribe("odom", 10, &LandMarkMonitor::OdometryCallBack, &monitor);
    ros::spinOnce();
    while(true)
    {
        thinkFunction();
    }
    return 0;
}


void thinkFunction()
{
    if(fabs(vacinity.distance)<0.5)
    {
        targetCoordinates.first = fabs(rand()%5);
        targetCoordinates.second = fabs(rand()%5);
        targetBearing = calculateBearing(odometryPose.pose.pose.position.x,odometryPose.pose.pose.position.y,targetCoordinates.first,targetCoordinates.second);
        rotateRadian(0.4,degreeToradian(targetBearing),true);
        moveLinear(1.0,3.0,true);
    }
    else if(fabs(vacinity.distance)>10.0)
    {
        moveLinear(1.0,10.0,false);
        rotateRadian(0.4,degreeToradian(180),true);
    }
    else
    {
        targetBearing = calculateBearing(odometryPose.pose.pose.position.x,odometryPose.pose.pose.position.y,targetCoordinates.first,targetCoordinates.second);
        rotateRadian(0.4,degreeToradian(targetBearing),true);
        moveLinear(1.0,5.0,true);
    }
}

void moveLinear(double speed, double distance, bool isForward)
{
    geometry_msgs::Twist VelocityMessage;
    nav_msgs::Odometry initial_odometryPose = odometryPose;

    if (isForward)
        VelocityMessage.linear.x =abs(speed);
    else
        VelocityMessage.linear.x =-abs(speed);

    VelocityMessage.linear.y = VelocityMessage.linear.z =VelocityMessage.angular.x =VelocityMessage.angular.y =VelocityMessage.angular.z =0;

    double distance_moved = 0.0;

    ros::Rate rate(1024);
    while(true)
    {
        ros::spinOnce();
        rate.sleep();
        velocityPublisher.publish(VelocityMessage);
        distance_moved = sqrt(pow((odometryPose.pose.pose.position.x-initial_odometryPose.pose.pose.position.x), 2) +
                              pow((odometryPose.pose.pose.position.y-initial_odometryPose.pose.pose.position.y), 2));
        if(abs(distance_moved)>abs(distance))
        {
            VelocityMessage.linear.x =0;
            velocityPublisher.publish(VelocityMessage);
            break;
        }
    }
}

void rotateRadian(double angular_velocity, double radians,  bool clockwise)
{
    geometry_msgs::Twist VelocityMessage;

    tf::StampedTransform initTransform;
    tf::StampedTransform currentTransform;
    tf::TransformListener tfListener;

    tfListener.waitForTransform("base_footprint", "odom", ros::Time(0), ros::Duration(1.0));
    tfListener.lookupTransform("base_footprint", "odom", ros::Time(0), initTransform);


    angular_velocity=((angular_velocity>0.4)?angular_velocity:0.4);

    while(radians < 0) radians += 2*M_PI;
    while(radians > 2*M_PI) radians -= 2*M_PI;

    VelocityMessage.linear.x = VelocityMessage.linear.y = 0.0;
    VelocityMessage.angular.z = angular_velocity;

    if (clockwise)
        VelocityMessage.angular.z = -VelocityMessage.angular.z;

    ros::Rate rate(1024);
    while (true)
    {
        velocityPublisher.publish(VelocityMessage);

        tfListener.waitForTransform("base_footprint", "odom", ros::Time(0), ros::Duration(1.0));
        tfListener.lookupTransform("base_footprint", "odom", ros::Time(0), currentTransform);

        tf::Transform relative_transform = initTransform.inverse() * currentTransform;
        double angle_turned = relative_transform.getRotation().getAngle();

        if (fabs(angle_turned) < 1.0e-2) continue;

        if (fabs(angle_turned) > radians)
        {
            VelocityMessage.angular.z = 0;
            velocityPublisher.publish(VelocityMessage);
            rate.sleep();
            break;
        }
        rate.sleep();
    }
}

double calculateBearing( double x1, double y1, double x2,double y2)
{
    return (atan2((y2 - y1),(x2 - x1))*180.0) / M_PI;
}

double radianTodegree(double radianAngle)
{
    return radianAngle*57.2957795;
}

double degreeToradian(double degreeAngle)
{
    return degreeAngle/57.2957795;
}




