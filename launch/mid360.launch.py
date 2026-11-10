import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    package_share = get_package_share_directory("roboparty_lidar")
    default_config = os.path.join(package_share, "config", "MID360_config.json")

    config_file = LaunchConfiguration("config_file")
    frame_id = LaunchConfiguration("frame_id")
    publish_freq = LaunchConfiguration("publish_freq")
    xfer_format = LaunchConfiguration("xfer_format")
    multi_topic = LaunchConfiguration("multi_topic")
    data_src = LaunchConfiguration("data_src")
    output_data_type = LaunchConfiguration("output_data_type")
    lvx_file_path = LaunchConfiguration("lvx_file_path")
    cmdline_bd_code = LaunchConfiguration("cmdline_bd_code")
    publish_tf = LaunchConfiguration("publish_tf")
    base_frame = LaunchConfiguration("base_frame")

    driver = Node(
        package="livox_ros_driver2",
        executable="livox_ros_driver2_node",
        name="livox_lidar_publisher",
        output="screen",
        parameters=[
            {"xfer_format": ParameterValue(xfer_format, value_type=int)},
            {"multi_topic": ParameterValue(multi_topic, value_type=int)},
            {"data_src": ParameterValue(data_src, value_type=int)},
            {"publish_freq": ParameterValue(publish_freq, value_type=float)},
            {"output_data_type": ParameterValue(output_data_type, value_type=int)},
            {"frame_id": frame_id},
            {"lvx_file_path": lvx_file_path},
            {"user_config_path": config_file},
            {"cmdline_input_bd_code": cmdline_bd_code},
        ],
    )

    static_tf = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        name="livox_frame_publisher",
        arguments=[
            "--x", LaunchConfiguration("x"),
            "--y", LaunchConfiguration("y"),
            "--z", LaunchConfiguration("z"),
            "--roll", LaunchConfiguration("roll"),
            "--pitch", LaunchConfiguration("pitch"),
            "--yaw", LaunchConfiguration("yaw"),
            "--frame-id", base_frame,
            "--child-frame-id", frame_id,
        ],
        condition=IfCondition(publish_tf),
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "config_file",
                default_value=default_config,
                description="Livox MID-360 JSON configuration",
            ),
            DeclareLaunchArgument(
                "frame_id",
                default_value="livox_frame",
                description="Lidar frame id",
            ),
            DeclareLaunchArgument(
                "publish_freq",
                default_value="10.0",
                description="Lidar publish frequency in Hz",
            ),
            DeclareLaunchArgument(
                "xfer_format",
                default_value="0",
                description="0: PointCloud2, 1: CustomMsg",
            ),
            DeclareLaunchArgument(
                "multi_topic",
                default_value="0",
                description="0: shared topic, 1: one topic per lidar",
            ),
            DeclareLaunchArgument(
                "data_src",
                default_value="0",
                description="0: lidar",
            ),
            DeclareLaunchArgument(
                "output_data_type",
                default_value="0",
                description="0: publish, other values: write LVX",
            ),
            DeclareLaunchArgument(
                "lvx_file_path",
                default_value="/tmp/livox_test.lvx",
                description="LVX output path when output_data_type is not 0",
            ),
            DeclareLaunchArgument(
                "cmdline_bd_code",
                default_value="livox0000000001",
                description="Livox broadcast code",
            ),
            DeclareLaunchArgument(
                "publish_tf",
                default_value="true",
                description="Publish base_link -> lidar static TF",
            ),
            DeclareLaunchArgument(
                "base_frame",
                default_value="base_link",
                description="Parent frame for the lidar static TF",
            ),
            DeclareLaunchArgument("x", default_value="0.0"),
            DeclareLaunchArgument("y", default_value="0.0"),
            DeclareLaunchArgument("z", default_value="0.0"),
            DeclareLaunchArgument("roll", default_value="0.0"),
            DeclareLaunchArgument("pitch", default_value="0.0"),
            DeclareLaunchArgument("yaw", default_value="0.0"),
            driver,
            static_tf,
        ]
    )
