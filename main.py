"""
Semi-automatic CSR generator.
"""

__author__ = "ringobouya"
__status__ = "alpha"
__version__ = "0.1"
__date__    = "13 June 2019"

import sys
import random
import string
import subprocess

# 2048 or 4096
PK_BITS = 2048
PK_SEED = 10000

# -----------------------------------------------------------------------------

# for private key use only
def randomname(n):
   randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
   return ''.join(randlst)


#TODO: CHECKING SYSTEM
# strip spaces, upper keyname, 
def shaping(subj):
    spr = [i.strip() for i in subj.split(',')]
    subj = ""
    for c in spr:
        subj += "/" + c
        if c.startswith('CN='):
            name = c.split('=')[1]
    return name, subj


def keygen(name, subj):
    # create random data.
    with open('./rand.dat', mode='w') as f:
        f.write(randomname(PK_SEED))
    # DES3
    #keygencmd = "openssl genrsa -out server.key -rand ./rand.dat -des3 %d" % (PK_BITS)
    # NOENCRYPT
    keygencmd = "openssl genrsa -out %s.key -rand ./rand.dat %d" % (name, PK_BITS)
    subprocess.call(keygencmd, shell=True)
    # print
    with open(name + '.key', 'r') as f:
        for row in f:
            print(row, end="")


def csrgen(name, subj):
    req_cmd='openssl req -new -sha256 -key %s.key -out %s.csr '\
            '-subj \'%s\'' % (name, name, subj)
    subprocess.call(req_cmd, shell=True)
    # print
    with open(name + '.csr', 'r') as f:
        for row in f:
            print(row, end="")


def main(subject):
    name, subj = shaping(subjcet)
    keygen(name, subj)
    csrgen(name, subj)


if __name__ == "__main__":
    args = sys.argv
    if len(args) >= 2:
        subject = args[1]
    else:
        # Example mode
        subject = "CN=www.example.com, OU=Example Unit, O=Example Company, ST=Tokyo, C=JP"
    main(subject)

