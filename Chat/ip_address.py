import socket as sk

def get_ip_address():
    """ Dynamically gets the IP Address of the server. """
    try:
        socket = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
        socket.connect(("8.8.8.8", 80))
        return socket.getsockname()[0]
    except OSError:
        return sk.gethostbyname(sk.gethostname())

