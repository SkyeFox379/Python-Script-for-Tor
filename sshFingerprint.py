#!/usr/bin/python

import paramiko
import socks
import sys

PROXYHOST = "127.0.0.1"
PROXYPORT = 9050

sshPort = 22

CONNECTION_TIMEOUT=30

urls = []

with open('onionLinks.txt', 'r') as handle:
	for line in handle:
		if line.strip("\n"):
			urls.append(line.strip("\n"))

for url in urls:
	print('[*] Requesting %s' % url)

	try:
		s = socks.socksocket()

		s.set_proxy(
			proxy_type=socks.SOCKS5,
			addr=PROXYHOST,
			port=PROXYPORT,
		)

		s.settimeout(CONNECTION_TIMEOUT)

		sshHost = url

		if url.startswith("http://"):
			sshHost = url[len("http://"): -1]
		elif url.startswith("https://"):
			sshHost = url[len("https://"): -1]

		s.connect((sshHost, sshPort))


		#fingerprint = s.get_fingerprint()
		#print(fingerprint)


		transport = paramiko.Transport(s)
		transport.connect(username=" ",password=" ")


		conn = paramiko.SSHClient.from_transport(transport)

		conn.close()
		transport.close()

	except KeyboardInterrupt:
		sys.exit()

	except (paramiko.ssh_exception.AuthenticationException):
		print("[*] Connected! Bad password.")


		f = open("workingLinks.txt","w")
		with f as handle:
			f.write(url)
		f.close()


	except:
		print("[*] Cannot connect")
 
print('[*] Done')
