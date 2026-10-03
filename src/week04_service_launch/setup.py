from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'week04_service_launch'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'),
            glob(os.path.join('launch', '*.launch.py'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='shnoh',
    maintainer_email='awake_noh@naver.com',
    description='ROS2 연습 week02',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'rectangle_driver = week04_service_launch.rectangle_driver:main',
            'start_stop_client = week04_service_launch.start_stop_client:main'
        ],
    },
)
