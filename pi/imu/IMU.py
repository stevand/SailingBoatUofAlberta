from XdaCallback import XdaCallback
from builtins import *
import xsensdeviceapi as xda

from time import perf_counter, sleep

class IMU:
    def __init__(self):
        control = xda.XsControl_construct()

        #finding the port the imu is connected to
        imu_port = None
        for port in xda.XsScanner_scanPorts():
            if port.deviceId().isMti() or port.deviceId().isMtig():
                imu_port = port
                break
        else:
            raise RuntimeError('IMU not found')

        #opening port
        control.openPort(port.portName(), port.baudrate())

        #getting the device object from the id
        device = control.device(imu_port.deviceId())

        #setting up callback handler
        self._callback = XdaCallback()
        device.addCallbackHandler(self._callback)

        #configuring the device
        device.gotoConfig()
        configArray = xda.XsOutputConfigurationArray()
        configArray.push_back(xda.XsOutputConfiguration(xda.XDI_PacketCounter, 0))
        configArray.push_back(xda.XsOutputConfiguration(xda.XDI_SampleTimeFine, 0))
        configArray.push_back(xda.XsOutputConfiguration(xda.XDI_Quaternion, 0))

        #putting device into measurement mode
        device.gotoMeasurement()

    def orientation(self):
        start = perf_counter()
        #process will wait half a second at most
        while perf_counter() - start < 0.5:
            if self._callback.packetAvailable():
                orientation = self._callback.getNextPacket().orientationEuler()
                return orientation
    
    def heading():
        yaw = self.orientation().yaw()
        return yaw + 180

if __name__ == '__main__':
    imu = IMU()
    while True:
        sleep(0.1)
        euler = imu.orientation()
        print('roll: {} yaw: {} pitch: {}'.format(euler.roll(), euler.yaw(), euler.pitch()))