"""

 Name: server.py
 Caption: Project 1 of IPK 
 Brief: Implementation of server that communicates with protocol HTTP and ensure translation of domain names 
 Author: Magdaléna Ondrušková <xondru16@stud.fit.vutbr.cz>
 Date: 03.03.2020 


"""
"""
Implementation details: 
    - TODO port numbers from makefile 
    - "\r\n\r\n"  na oddelenie hlavičky od content
"""

import socket 
import re
import string
import sys
import signal
import ipaddress

def get_result(name, op_type, operation) :
    name = name.strip()
    op_type = op_type.strip()
    get_type_match = re.match(r'(A|PTR)', op_type)
    result = ""
    header = ""
    count = 0
    ip_addr = ""
    if get_type_match == None:
        header = " 400 Bad Request \r\n\r\n"  
        return count, header  
    elif op_type == "A":
        try:
            try: 
                ip_addr = ipaddress.ip_address(name)
                header = " 400 Bad Request \r\n\r\n"
            except : 
                ip_addr= socket.gethostbyname(name)
                header = " 200 OK \r\n\r\n"
                result = name + ":" + op_type + "=" + ip_addr + "\r\n"
                count = 1
        except : 
            header = " 404 Not Found \r\n\r\n"
    elif op_type == "PTR" : 
        # check for valid IP adress 
        try:
            ip = ip = ipaddress.ip_address(name) 
            try: 
                # check if ip adress exists
                host_name, x, ip = socket.gethostbyaddr(name) 
                header = " 200 OK \r\n\r\n"
                result +=name + ":" + op_type + "=" + host_name + "\r\n"
                count=1
            except : 
                header = " 404 Not Found \r\n\r\n"
                #return header 
        except : 
            header = " 400 Bad Request \r\n\r\n"

    if operation == "GET" : 
        result = header + result
        return count, result 
    elif operation == "POST" :
        if count == 0 :
            return count, header
        else : 
            return count, result

"""

    Operation that process GET operation 
    Function RETURNS header and content 
    Doesn't need checking count, it's only there so it won't make mess 
      after returning two things from get_result. 

"""
def operation_GET(header,data):
    get_name = data.group("name")
    get_type = data.group("type")
    operation = "GET"
    result = header
    count, result_get = get_result(get_name,get_type, operation)
    result = header + result_get
    return result 

"""

    Operation that process POST operation 
    Count counts valid inputs 
        if zero from whole file => 400 Error
    Result_func is one line from content with found domain name / ip adress
    Result_post is all the results combined
    Function RETURNS header and content 

"""
def operation_POST(header, data): 
    data = data.split("\n")
    result = header
    count_all = 0
    result_post = ""
    operation = "POST"
    for line in data :
        if len(line.strip()) == 0 :
            continue 
        post_type = line.split(":")
        if len(post_type) == 1 : 
            continue 
        post_name = post_type[0]
        post_type = post_type[1]
        count, result_func = get_result(post_name,post_type,operation)
        count_all += count 
        if count != 0 :
            result_post += result_func
    if count_all > 0 :
        result +=" 200 OK \r\n\r\n" + result_post
    else :
        result += " 400 Bad Request \r\n\r\n"
    return result

##### MAIN PROGRAM ####

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = 'localhost'
PORT = sys.argv[1]
PORT=int(PORT)

#### Check for errors while binding to client - wrong port for example ####
try: 
    s.bind((HOST, PORT))
except: 
    sys.exit()
    

#### listen from client #### 
s.listen()

#### Process datas that client is sending ####
while True:
    try: 
        client_socket, adress = s.accept()
        message = client_socket.recv(1024)
        message = message.decode("utf-8") # whole message
        # check if its GET or POST
        data = message.split()
        get = re.match(r'GET', data[0])
        post = re.match(r'POST', data[0])
        url_get = re.match(r'/resolve', data[1])
        url_post = re.match(r'/dns-query', data[1])
        get_data = re.match(r'^GET /resolve\?name=(?P<name>.*)&type=(?P<type>.*) HTTP/1\.1', message)
        post_data = re.match(r'POST /dns-query HTTP/1\.1', message)
        header = "HTTP/1.1"
        result = ""
        if get == None and post == None  :
            result = header + " 405 Method Not Allowed \r\n\r\n"
        elif url_get == None and url_post == None : 
            result = header + " 400 Bad Request \r\n\r\n"
        ### operation GET ###
        elif get_data != None : 
            result = operation_GET(header,get_data)
        ### operation POST ###
        elif post_data != None : 
            ### split message to header and content ###
            data = message.split("\r\n\r\n")
            data = data[1]
            result = operation_POST(header, data)
        ### sends result and close client
        client_socket.send(result.encode())
        client_socket.close()
    except KeyboardInterrupt: 
        sys.exit()   