from solcx import compile_source

# Compiling our Share Data smart contract:
def compile_sol():
    # Solidity source code
    compiled_sol = compile_source(
        '''
        // SPDX-License-Identifier: GPL-3.0
        // Version of compiler
        pragma solidity >=0.7.0 <0.9.0;

        contract shareData {

            // these structs are used to represent the ROS topic data

            struct Time {
                int256 secs;
                int256 nsecs;
            }

            struct Header {
                int256 seq;
                Time stamp;
                string frame_id;
            }

            struct Data {
                int256 value;
                int256 variance;
            }

            struct Vector3 {
                int256 x;
                int256 y;
                int256 z;
            }

            struct Quaternion {
                int256 x;
                int256 y;
                int256 z;
                int256 w;
            }

            struct Pose {
                Vector3 position;
                Quaternion orientation;
                int256[36] covariance;
            }

            struct Twist {
                Vector3 linear;
                Vector3 angular;
                int256[36] covariance;
            }

            struct OdomData {
                Header header;
                string child_frame_id;
                Pose pose;
                Twist twist;
            }

            struct TemperatureData {
                Header header;
                Data data;
            }

            struct HumidityData {
                Header header;
                Data data;
            }

            struct PointCloudData {
                string IPFS_Cid;
            }

            // string that stores the place of the inspection task
            string private place;

            // string that stores the date of the inspection task
            string private date;

            // variable that stores the inspector address
            address private inspector;

            // array that stores robots adresses
            address[] private robots;

            // mapping to check valid robot addresses
            mapping (address => bool) private isRobot;

            // public variables that store robots data
            mapping (address => TemperatureData) temperatureData;
            mapping (address => HumidityData) humidityData;
            mapping (address => PointCloudData) pointCloudData;
            mapping (address => OdomData) odomData;

            // events for keeping logs
            event Temperature(TemperatureData temperature, address robot);
            event Humidity(HumidityData humidity, address robot);
            event PointCloud(PointCloudData pointCloud, address robot);
            event Odom(OdomData odom, address robot);

            constructor(string memory _place, string memory _date, address[] memory _robots) {
                place = _place;
                date = _date;
                robots = _robots;
                for (uint256 i = 0; i < robots.length; i++) {
                    isRobot[robots[i]] = true;
                }
            }

            modifier checkRobot() {
                require(isRobot[msg.sender] == true, "sender is not a robot");
                _;
            }

            function updateTemperature(TemperatureData memory _temperature) public checkRobot() {

                // updating contract variable
                temperatureData[msg.sender] = _temperature;

                // emmiting event
                emit Temperature(_temperature, msg.sender);

            }

            function updateHumidity(HumidityData memory _humidity) public checkRobot() {

                // updating contract variable
                humidityData[msg.sender] = _humidity;

                // emmiting event
                emit Humidity(_humidity, msg.sender);

            }

            function updatePointCloud(PointCloudData memory _point_cloud) public checkRobot() {

                // updating contract variable
                pointCloudData[msg.sender] = _point_cloud;

                // emmiting event
                emit PointCloud(_point_cloud, msg.sender);

            }

            function updateOdom(int256 seq,
                int256 stampSecs,
                int256 stampNsecs,
                string memory frameId,
                string memory childFrameId,
                int256[3] memory position,
                int256[4] memory orientation,
                int256[36] memory poseCovariance,
                int256[3] memory linear,
                int256[3] memory angular,
                int256[36] memory twistCovariance) public checkRobot() {

                // updating contract variable
                odomData[msg.sender] = OdomData(
                    Header(seq, Time(stampSecs, stampNsecs), frameId),
                    childFrameId,
                    Pose(Vector3(position[0], position[1], position[2]), Quaternion(orientation[0], orientation[1], orientation[2], orientation[3]), poseCovariance),
                    Twist(Vector3(linear[0], linear[1], linear[2]), Vector3(angular[0], angular[1], angular[2]), twistCovariance)
                );

                // emmiting event
                emit Odom(odomData[msg.sender], msg.sender);

            }

        }
        ''',
        output_values=['abi', 'bin']
    )
    return compiled_sol