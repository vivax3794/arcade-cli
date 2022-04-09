from socket import socket

JWT = "OAUTH:eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NDg0MzAzOTAsIm9wYXF1ZV91c2VyX2lkIjoiVTQ2ODEwNjcyMyIsInJvbGUiOiJicm9hZGNhc3RlciIsInB1YnN1Yl9wZXJtcyI6eyJsaXN0ZW4iOlsiYnJvYWRjYXN0IiwiZ2xvYmFsIl0sInNlbmQiOlsiYnJvYWRjYXN0Il19LCJjaGFubmVsX2lkIjoiNDY4MTA2NzIzIiwidXNlcl9pZCI6IjQ2ODEwNjcyMyIsImlhdCI6MTY0ODM0Mzk5MH0.JvErIhUSyzeI7FxZ3AroeLUPiPyKzs754gc-xsoWmm0"
NICK = "matissetec"

# connect to twitch
s = socket()
s.connect(("irc.chat.twitch.tv", 6667))
s.send(bytes("PASS " + JWT + "\r\n", "UTF-8"))
s.send(bytes("NICK " + NICK + "\r\n", "UTF-8"))
s.send(bytes("JOIN #" + NICK + "\r\n", "UTF-8"))

# print response
while True:
    response = s.recv(1024).decode("UTF-8")
    print(response)
