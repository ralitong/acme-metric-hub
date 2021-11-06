import argparse
import sys
import time
from acme_core import AcmeCore



if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('metric_server', type=str, default='http://localhost:50000')
    parser.add_argument('--sleep', type=int, default=2)
    parser.add_argument('--send-unusual', help='Acme server will send unusual report', action='store_true')

    args = parser.parse_args()

    acme_core = AcmeCore(metric_server=args.metric_server)

    while True:
        time.sleep(args.sleep)
        if args.send_unusual:
            acme_core.post_unusual_report()
        else:
            acme_core.post_normal_report()
            

