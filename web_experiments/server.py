import select
import socket

def server() -> None:
    host = socket.gethostname()
    port = 12345
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setblocking(0)
        s.bind((host, port))
        s.listen(5)
        print('Server listening....')
        inputs = [s]
        outputs = []

        while inputs:
            readable, writable, exceptional = select.select(inputs, outputs, inputs)
            for r in readable:
                if r is s:
                    conn, addr = s.accept()
                    print('Connected by', addr)
                    conn.setblocking(0)
                    inputs.append(conn)
                else:
                    data = r.recv(1024)
                    if not data:
                        inputs.remove(r)
                        r.close()
                    else:
                        data = r.recv(1024)
                        if data:
                            print('Received', data)
                        else:
                            inputs.remove(r)
                            r.close()