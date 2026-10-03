from share_server import ShareServer


FILE = "output/apex_ai_portrait.png"


server = ShareServer()

url = server.start(FILE)

print()
print("======================================")
print("APEX SHARE TEST")
print("======================================")
print()
print("Open this URL on your phone:")
print()
print(url)
print()
print("Press ENTER to stop the server...")

input()

server.stop()
