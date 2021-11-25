import psutil
import time
import DockerConfig
import HostConfig
import subprocess


def monitor(
        process: subprocess.Popen,
        timeLimit: float,
        memoryLimit: float,
        frequency=10000,
        bits=2
):
    runningTime = 0
    runningMem = 0
    maxRunningTime = 0
    maxRunningMem = 0

    pst = psutil.Process(process.pid)
    # Check whether process has fulfilled
    while True:
        exitcode = process.poll()
        if exitcode==0:
            print('############Normal Exit!#############')
            return HostConfig.ProcessStatus.NORMALLY_EXIT, maxRunningTime, maxRunningMem
        elif exitcode is None:
            pass
        else:
            print('##terminated##')
            return HostConfig.ProcessStatus.TERMINATED, 0, 0

        # Choose User time as programme running time(User, System)
        # cpu_times().user is in second unit, times by 1000 to ms
        runningTime = round(float(pst.cpu_times().user + pst.cpu_times().system)*1000, bits)
        maxRunningTime = max(maxRunningTime, runningTime)

        # Choose Virtual memory as programme running memory(Virtual, Real)
        # memory_info().vms is in Byte unit, divided into 1024*1024 to MB
        runningMem = round(float(pst.memory_info().rss)/(1024*1024), bits)
        maxRunningMem = max(maxRunningMem, runningMem)

        if runningTime > timeLimit:
            process.kill()
            print('########Time Limit Exceeded!########')
            return HostConfig.ProcessStatus.TIME_LIMIT_EXCEEDED, 0, 0

        if runningMem > memoryLimit:
            process.kill()
            print('#######Memory Limit Exceeded!#######')
            return HostConfig.ProcessStatus.MEMORY_LIMIT_EXCEEDED, 0, 0

        time.sleep(0.001)





