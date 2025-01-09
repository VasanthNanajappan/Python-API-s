import socket

HOST='localhost'
PORT=8000

def parse_request(request):
    request_lines=request.split("\r\n")
    request_line=request_lines[0]
    (request_method,path,request_version)=request_line.split(" ")

        # Return the parsed components:
    # - request_method (e.g., GET)
    # - path (e.g., /index.html)
    # - request_version (e.g., HTTP/1.1)
    # - Remaining lines (headers)
    return (request_method,path,request_version,request_lines[1:])

#It returns the response as a bytes object, which is necessary for sending the response over a network socket.
def build_response(status_code,body,content_type='text/html'):
    status_line=f"HTTP/1.1 {status_code} \r\n"
    headers=f"Content-Type:{content_type} \r\n Content-Length:{len(body)} \r\n"
    response=f"{status_line} {headers}\r\n {body}"
    return response.encode()

def handle_request(request):
    #parse the request
    (request_method,path,request_version,headers)=parse_request(request)

    #check request method
    if request_method=="GET":
        body="<html><body><h1>Hello, World!</h1></body></html>"
        respone=build_response(200,body)
    else:
        body="<html><body><h1>Method Not Allowed</h1></body></html>"
        response=build_response(405,body)
    
    return respone

#create a TCP/IP socket
server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#AF_INET -> It specifies that the socket will use the "IPV4" protocol
#SOCK_STREAM -> this argument specifies that the argument specifies the socket will use a TCP connection

server_socket.bind((HOST,PORT))
#this line binds the socket to the specified host and port

server_socket.listen()
print(f"Listening on {HOST}:{PORT}...")

while True:
    client_socket,client_address=server_socket.accept()
    #This code continuosly wait for incoming connections.