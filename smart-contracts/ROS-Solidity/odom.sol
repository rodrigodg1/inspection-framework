// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.9.0;

contract OdomData {

    uint public constant DATASIZE = 9;

    struct Time {
        uint32 secs;
        uint32 nsecs;
    }

    struct Vector3 {
        uint32 x;
        uint32 y;
        uint32 z;
    }

    struct Quaternion {
        uint32 x;
        uint32 y;
        uint32 z;
        uint32 w;
    }

    struct Pose {
        Vector3 position;
        Quaternion orientation;
    }

    struct Twist {
        Vector3 linear;
        Vector3 angular;
    }

    struct Header {
        uint32 seq;
        Time stamp;
        string frame_id;
    }

    struct PoseWithCovariance {
        Pose pose;
        uint32[36] covariance;
    }

    struct TwistWithCovariance {
        Twist twist;
        uint32[36] covariance;
    }

    struct Odom {
        Header header;
        string child_frame_id;
        PoseWithCovariance pose;
        TwistWithCovariance twist;
    }

    Odom odom;

    function updateOdom(
        uint32 seq,
        uint32 stampSecs,
        uint32 stampNsecs,
        string memory frameId,
        string memory childFrameId,
        uint32[3] memory position,
        uint32[4] memory orientation,
        uint32[36] memory poseCovariance,
        uint32[3] memory linear,
        uint32[3] memory angular,
        uint32[36] memory twistCovariance
    ) public {
        //for (uint j = 0; j < DATASIZE; j++) {
            odom.header.seq = seq;
            odom.header.stamp.secs = stampSecs;
            odom.header.stamp.nsecs = stampNsecs;
            odom.header.frame_id = frameId;

            odom.child_frame_id = childFrameId;

            odom.pose.pose.position.x = position[0];
            odom.pose.pose.position.y = position[1];
            odom.pose.pose.position.z = position[2];

            odom.pose.pose.orientation.x = orientation[0];
            odom.pose.pose.orientation.y = orientation[1];
            odom.pose.pose.orientation.z = orientation[2];
            odom.pose.pose.orientation.w = orientation[3];

            for (uint256 i = 0; i < 36; i++) {
                odom.pose.covariance[i] = poseCovariance[i];
            }

            odom.twist.twist.linear.x = linear[0];
            odom.twist.twist.linear.y = linear[1];
            odom.twist.twist.linear.z = linear[2];

            odom.twist.twist.angular.x = angular[0];
            odom.twist.twist.angular.y = angular[1];
            odom.twist.twist.angular.z = angular[2];

            for (uint256 i = 0; i < 36; i++) {
                odom.twist.covariance[i] = twistCovariance[i];
            }
        //}
    }
}
