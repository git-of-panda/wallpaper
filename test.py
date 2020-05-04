import subprocess
import os
import struct

p = subprocess.Popen("monitor.bat", stdout=subprocess.PIPE, shell=True)
stdout, stderr=p.communicate()
print(int(stdout))

