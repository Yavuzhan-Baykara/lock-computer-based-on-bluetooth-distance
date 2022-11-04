import bluetooth
import subprocess
from subprocess import sys
from multiprocessing import Pool


def discover_devices():
    nearby_devices = bluetooth.discover_devices()
    return nearby_devices
    

def activate():
    target_name = "My Phone"
    target_address = "7c:fd:6b:79:da:56"    
    pool = Pool(20)
    multiple_results = [pool.apply_async(discover_devices,) for i in range(10)]

    for bdaddr in multiple_results[-1].get():
        if target_name == bluetooth.lookup_name( bdaddr ):
            target_address = bdaddr
            break
    values = bluetooth.find_service(address=target_address)
    pool.close()
    return values

if __name__ == "__main__":
    while True:
        if not activate() == []:
            USER = None
            PASSWORD = None
            proc = subprocess.Popen(['runas',f'/user:{USER}',sys.argv[0]], stdin=subprocess.PIPE) 
            proc.stdin.write(PASSWORD)
            print("Bluetooth is active")
        else:
            print(activate())
            cmd='rundll32.exe user32.dll, LockWorkStation'
            subprocess.call(cmd)

