import sys
from gamecode import pyweek31
import multiprocessing as mp


MIN_VER = (3, 9)

if sys.version_info[:2] < MIN_VER:
    sys.exit(
        "This game requires Python {}.{}.".format(*MIN_VER)
    )

if __name__ == '__main__':
	requestQ = mp.Queue()
	resultQ = mp.Queue()
	
	loaderProcess = mp.Process(target=pyweek31.loader, args=(requestQ, resultQ))
	loaderProcess.start()
	pyweek31.main(requestQ, resultQ)
	sys.exit()