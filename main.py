import os
import sys
import random
import string
import subprocess
from logging import getLogger, StreamHandler, Formatter
import logging

"""
Semi-automatic CSR generator.
"""

__author__ = "ringobouya"
__status__ = "alpha"
__version__ = "0.2"
__date__ = "8 Dec 2020"

MY_LOG_LEVEL = logging.INFO

# 2048 or 4096
PK_BITS = 2048
PK_SEED = 10000


def randomname(n):
    randlst = [
        random.choice(string.ascii_letters + string.digits) for i in range(n)
        ]
    return ''.join(randlst)


# TODO: CHECKING SYSTEM
# strip spaces, upper keyname.
def shaping(subj, logger=None):
    spr = [i.strip() for i in subj.split(',')]
    subj = ""
    for c in spr:
        subj += "/" + c
        if c.startswith('CN='):
            name = c.split('=')[1]
            # find a wildcard
            if(name.find("*") >= 0):
                logger.debug("remove asterisk.: %s", name)
                name = name[2:]

    return name, subj


def keygen(name, subj, logger=None):
    # create random data.
    # with open('./rand.dat', mode='w') as f:
    randfile = os.getcwd() + "/rand.dat"
    logger.debug(randfile)
    with open(randfile, mode='w') as f:
        f.write(randomname(PK_SEED))
    # DES3
    # "openssl genrsa -out %s.key -rand ./rand.dat -des3 %d" % (PK_BITS)
    # NOENCRYPT
    keygencmd = "openssl genrsa -out %s.key -rand ./rand.dat %d" \
                % (name, PK_BITS)
    subprocess.call(keygencmd, shell=True)
    # print
    with open(name + '.key', 'r') as f:
        for row in f:
            print(row, end="")


def csrgen(name, subj, logger=None):
    req_cmd = 'openssl req -new -sha256 -key %s.key -out %s.csr '\
            '-subj \'%s\'' % (name, name, subj)
    subprocess.call(req_cmd, shell=True)
    # print
    with open(name + '.csr', 'r') as f:
        for row in f:
            print(row, end="")


def main(subject, logger=None):
    name, subj = shaping(subject, logger)
    keygen(name, subj, logger)
    csrgen(name, subj, logger)


if __name__ == "__main__":
    logger = getLogger(__name__)
    logger.setLevel(MY_LOG_LEVEL)
    stream_handler = StreamHandler()
    stream_handler.setLevel(MY_LOG_LEVEL)
    handler_format = Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    stream_handler.setFormatter(handler_format)
    logger.addHandler(stream_handler)

    args = sys.argv
    if len(args) >= 2:
        subject = args[1]
    else:
        # Keywords:
        # emailAddress=hoge@example.com
        # CN=www.example.com
        # OU=Example Unit
        # O=Example Company
        # ST=Tokyo
        # C=JP

        # Example mode
        subject = "CN=www.example.com, OU=Example Unit, " \
                    "O=Example Company, ST=Tokyo, C=JP"

        logger.info("@@@@ Demo mode @@@@")
        logger.info("python main.py + \"" + subject + "\"")

    main(subject, logger=logger)
