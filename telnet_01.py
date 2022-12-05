import telnetlib
from pprint import pprint

"""
Telnet_func - take each lines sended by main_func and return with new line character
"""
def telnet_func(line):
    return f"{line}\n".encode("utf-8")

def main_func(ip, port, username, password, commands):
    with telnetlib.Telnet(ip,port) as telnet:
        
        telnet.write(b"logout\n")
        telnet.write(b"\r")

        telnet.read_until(b"Login")
        telnet.write(telnet_func(username))

        telnet.read_until(b"Password: ")
        telnet.write(telnet_func(password))
        
        telnet.read_very_eager()
        
        result = {}
        for command in commands:
            telnet.write(telnet_func(command))
            output = telnet.read_until(b"#", timeout=1).decode("utf-8")
            result[command] = output.replace("\r\n", "\n")
        
        telnet.close()
        return result

if __name__ == "__main__":
    devices = ["172.18.70.84"]
    port = "38017"
    commands = [

        "/configure router interface Loopback1",
        "/configure router interface Loopback1 address 172.16.1.1/32",
        "/configure router interface Loopback1 loopback",
        "/configure router interface Loopback2",
        "/configure router interface Loopback2 address 172.16.2.1/32",
        "/configure router interface Loopback2 loopback", "\b",
        "show router interface"

    ]
    for ip in devices:
        result = main_func(ip, port, "admin", "admin", commands)
        pprint(result, width=1024)