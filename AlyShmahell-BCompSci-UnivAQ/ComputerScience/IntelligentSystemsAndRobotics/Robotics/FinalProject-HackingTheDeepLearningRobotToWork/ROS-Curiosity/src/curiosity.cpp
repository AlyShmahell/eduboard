#include <vector>
#include <string>
#include <math.h>
#include <ros/ros.h>
#include <nav_msgs/Odometry.h>
#include <geometry_msgs/Twist.h>
#include <curiosity/LandMarkDistance.h>

using std::vector;
using std::string;
using namespace curiosity;

ros::Publisher pub;

class LandMark
{
public:
    LandMark(string Name, double X, double Y):name(Name),x(X),y(Y) {}
    string name;
    double x,y;
};

class LandMarkMonitor
{
public:

    vector<LandMark> LandmarkVector;
    LandMarkDistance vacinity;

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
        ROS_INFO("closest to: %s, within: %f",vacinity.name.c_str(),vacinity.distance);

        geometry_msgs::Twist twist;
        twist.angular.z = 5;
        twist.linear.x = 5;
        pub.publish(twist);
    }
};




int main(int argc, char** argv)
{
    ros::init(argc, argv, "curiosity");
    ros::NodeHandle node;
    LandMarkMonitor monitor;
    pub = node.advertise<geometry_msgs::Twist>("/mobile_base/commands/velocity", 1);
    ros::Subscriber sub = node.subscribe("odom", 10, &LandMarkMonitor::OdometryCallBack, &monitor);
    ros::spin();
    return 0;
}
