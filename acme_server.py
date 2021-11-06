from acme_core import AcmeCore
import sys
import time


if __name__ == '__main__':
    metric_server = sys.argv[1]
    send_unusual = ''

    if(len(sys.argv) > 2):
        send_unusual = sys.argv[2]

    acme_core = AcmeCore(metric_server=metric_server)

    while True:
        time.sleep(2)
        if send_unusual == 'send_unusual':
            acme_core.post_unusual_report()
        else:
            acme_core.post_normal_report()
            

