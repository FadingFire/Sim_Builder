import bluesky as bs
from bluesky import stack, sim, traf

bs.stack.stack('CRE KL204 B744 EHAM/RW27')
print('Latitudes:', bs.traf.lat)
