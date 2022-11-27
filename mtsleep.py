import threading
from time import sleep, ctime

loops = [4, 2]


def loop1(nloop, nsec):
    print("start loop " + str(nloop) + " at " + str(ctime()))
    sleep(nsec)
    print("loop " + str(nloop) + " done at " + str(ctime()))


def main1():
    print("starting at:" + str(ctime()))
    threads = []
    nloops = range(len(loops))
    for i in nloops:
        t = threading.Thread(target=loop1, args=(i, loops[i]))
        threads.append(t)
    for i in nloops:
        threads[i].start()
    for i in nloops:
        threads[i].join()
    print("all done at " + str(ctime()))


if __name__ == '__main__':
    main1()
