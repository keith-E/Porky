import time
from pysabertooth import Sabertooth

saber = Sabertooth('/dev/ttyS0')
# Stop the motors just in case a previous run as resulted in an infinite loop.
saber.stop()

saber_min_speed = -100
saber_max_speed = 100

print('Running motors at max forward speed for 2 seconds...')
saber.drive(1, saber_max_speed)
saber.drive(2, saber_max_speed)
time.sleep(2)
saber.stop()

print('Running motors at max reverse speed for 2 seconds...')
saber.drive(1, saber_min_speed)
saber.drive(2, saber_min_speed)
time.sleep(2)
saber.stop()

print('Running left motors at half forward speed for 2 seconds...')
saber.drive(1, saber_max_speed // 2)
time.sleep(2)
saber.stop()

print('Running right motors at half forward speed for 2 seconds...')
saber.drive(2, saber_max_speed // 2)
time.sleep(2)
saber.stop()

print('Running left motors at half reverse speed for 2 seconds...')
saber.drive(1, saber_min_speed // 2)
time.sleep(2)
saber.stop()

print('Running right motors at half reverse speed for 2 seconds...')
saber.drive(2, saber_min_speed // 2)
time.sleep(2)
saber.stop()

print('Motor test has completed.')
