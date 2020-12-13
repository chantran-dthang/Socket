import socket
import mimetypes
import os
import os.path
import time

# PORT = 8080
# HOST = 'localhost'
PORT = 80
HOST = socket.gethostbyname(socket.gethostname())
code_files = '<!doctype html><html lang="en"><head><title>FILES</title><!-- Required meta tags --><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no"><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"><link rel="shortcut icon" href="#"></head><body><style type="text/css">table {border-collapse: collapse;}th{font-size: 20px;color: blue;text-decoration: underline;border-bottom: 1px solid black;vertical-align: bottom;padding: 15px;}td{padding: 5px;}.btn-link {border: none;outline: none;background: none;cursor: pointer;color: #0000EE;padding: 0;text-decoration: underline;font-family: inherit;font-size: inherit;}</style><table><tr><th>Name</th><br><th>Last modified</th><th>Size</th><th>Description</th></tr><tr><form action="/index.html" method="POST"><td></i><i class="fa fa-arrow-left"><input class ="btn-link" type="submit" value="[Parent Directory]" /></form></tr>'

# socket.gethostbyname(socket.getfqdn(socket.gethostname()))
my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.bind((HOST, PORT))
my_socket.listen(1)
print('Host:', HOST)
print('Serving on port ', PORT)

# check = True
# header = "HTTP/1.1 301 Moved Permanently\n" + "Location: /" + myfile
# print(header)
# final_response = header.encode('utf-8')
# connection.send(final_response)
# connection.close()
# continue
# else:
# myfile = '404.html'
# check = False

# header = 'HTTP/1.1 404 Not Found\n\n'
#         file2 = open('404.html', 'r')
#         response = file2.read()
#         file2.close()
#         response = response.encode('utf-8')

# header = 'HTTP/1.1 200 OK\n'
# mimetype = 'text/html'
# header += 'Content-Type: ' + str(mimetype) + '\n\n'
# print('Server response: ', header)
# final_response = header.encode('utf-8')
# final_response += code_files.encode('utf-8')
# connection.send(final_response)
# connection.close()


def MovePage(filename, connector):
    # content = "".encode('utf-8')
    header = "HTTP/1.1 301 Moved Permanently\n" + "Location: /" + filename
    print(header)
    if(filename == "404.html"):
        header = 'HTTP/1.1 404 Not Found\n\n'
        file = open('404.html', 'rb')
        content = file.read()
        file.close()
        respone = header.encode('utf-8') + content
    elif(filename == "files.html"):
        header = 'HTTP/1.1 200 OK\n'
        mimetype = 'text/html'
        header += 'Content-Type: ' + str(mimetype) + '\n\n'
        print('Server response: ', header)
        respone = header.encode('utf-8')
        respone += code_files.encode('utf-8')
    else:
        respone = header.encode('utf-8')
    connector.send(respone)
    connector.close()


check = False  # True when username password accepted
while True:
    connection, address = my_socket.accept()
    request = connection.recv(1024).decode('utf-8')
    if (request == ""):
        connection.close()
        continue
    string_list = request.split(' ')  # Split request from spaces
    method = string_list[0]
    requesting_file = string_list[1]
    print('Client request ', method, requesting_file, "??")

    myfile = requesting_file.split('?')[0]  # After the "?" symbol not relevent here
    myfile = myfile.lstrip('/')
    if (method == 'GET'):
        # Load index file as default
        # Check info, prevent connect to info.html when don't enter username-password
        if (myfile == '' or (myfile == 'info.html' and check == False)):
            myfile = 'index.html'
            # header = "HTTP/1.1 301 Moved Permanently\n" + "Location: /" + myfile
            # print(header)
            # final_response = header.encode('utf-8')
            # connection.send(final_response)
            # connection.close()
            # continue
            MovePage(myfile, connection)
            continue
        if (myfile == 'index.html'):
            check = False
        if (myfile == 'files.html'):
            pathF = 'files'
            listfile = os.listdir(pathF)
            # code_files = '<!doctype html><html lang="en"><head><title>FILES</title><!-- Required meta tags --><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no"><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"><link rel="shortcut icon" href="#"></head><body><style type="text/css">table {border-collapse: collapse;}th{font-size: 20px;color: blue;text-decoration: underline;border-bottom: 1px solid black;vertical-align: bottom;padding: 15px;}td{padding: 5px;}.btn-link {border: none;outline: none;background: none;cursor: pointer;color: #0000EE;padding: 0;text-decoration: underline;font-family: inherit;font-size: inherit;}</style><table><tr><th>Name</th><br><th>Last modified</th><th>Size</th><th>Description</th></tr><tr><form action="/index.html" method="POST"><td></i><i class="fa fa-arrow-left"><input class ="btn-link" type="submit" value="[Parent Directory]" /></form></tr>'
            for i in listfile:
                dirF = pathF + "/"
                dirF = dirF + i
                day_m = os.path.getmtime(dirF)
                code_files += '<tr><form action="' + dirF + '" method="POST"><td></i><i class="fa fa-file-o"><input class ="btn-link" type="submit" value="' + i + '" /></form>'
                day_m2 = time.localtime(day_m)
                size = os.path.getsize(dirF)
                code_files += '<td>' + str(day_m2.tm_year) + '-' + str(day_m2.tm_mon) + '-' + str(
                    day_m2.tm_mday) + ' ' + str(day_m2.tm_hour) + ':' + str(day_m2.tm_min) + '</td>'
                code_files += '<td>' + str(round(size / 1024, 1)) + 'M</td></tr>'
            # header = 'HTTP/1.1 200 OK\n'
            # mimetype = 'text/html'
            # header += 'Content-Type: ' + str(mimetype) + '\n\n'
            # print('Server response: ', header)
            # final_response = header.encode('utf-8')
            # final_response += code_files.encode('utf-8')
            # connection.send(final_response)
            # connection.close()
            MovePage(myfile, connection)
            continue

    elif (method == 'POST'):
        if (myfile == 'info.html'):
            pass_and_user = string_list[-1].split('username=')[1]
            _username = pass_and_user.split('&password=')[0]
            _password = pass_and_user.split('&password=')[1]
            print('Username: ', _username)
            print('Password: ', _password)
            if (_username == 'admin' and _password == 'admin'):
                check = True
                # header = "HTTP/1.1 301 Moved Permanently\n" + "Location: /" + myfile
                # print(header)
                # final_response = header.encode('utf-8')
                # connection.send(final_response)
                # connection.close()
                # continue
                MovePage(myfile, connection)
                continue
            else:
                myfile = '404.html'
                check = False

        else:
            # header = "HTTP/1.1 301 Moved Permanently\n" + "Location: /" + myfile
            # print(header)
            # final_response = header.encode('utf-8')
            # connection.send(final_response)
            # connection.close()
            MovePage(myfile, connection)
            continue
    else:
        connection.close()
        continue
    try:
        file = open(myfile, 'rb')  # open file , r => read , b => byte format
        response = file.read()
        file.close()
        if (myfile == '404.html'):
            # header = 'HTTP/1.1 404 Not Found\n\n'
            # file2 = open(myfile, 'r')
            # response = file2.read()
            # file2.close()
            # print('Server response: ', header)
            # final_response = header.encode('utf-8')
            # final_response += response.encode('utf-8')
            # connection.send(final_response)
            # connection.close()
            MovePage(myfile, connection)
            continue

        else:
            header = 'HTTP/1.1 200 OK\n'

        # -- library not support pptx ...
        if (myfile.endswith(".jpg") or myfile.endswith('.jpeg')):
            mimetype = 'image/jpg'
        elif (myfile.endswith(".png")):
            mimetype = 'image/png'
        elif (myfile.endswith(".css")):
            mimetype = 'text/css'
        elif (myfile.endswith('.html') or myfile.endswith('.htm')):
            mimetype = 'text/html'
        elif (myfile.endswith(".pdf")):
            mimetype = 'application/pdf'
        elif (myfile.endswith(".ppt")):
            mimetype = 'application/vnd.ms-powerpoint'
        elif (myfile.endswith(".pptx")):
            mimetype = 'application/vnd.openxmlformats-officedocument.presentationml.presentation'
        elif (myfile.endswith(".rar")):
            mimetype = 'application/vnd.rar'
        elif (myfile.endswith(".xls")):
            mimetype = 'application/vnd.ms-excel'
        elif (myfile.endswith(".xlsx")):
            mimetype = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        elif (myfile.endswith(".doc")):
            mimetype = 'application/msword'
        elif (myfile.endswith(".docx")):
            mimetype = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        elif (myfile.endswith(".zip")):
            mimetype = 'application/zip'
        elif (myfile.endswith(".csv")):
            mimetype = 'text/csv'
        elif (myfile.endswith(".php")):
            mimetype = 'application/x-httpd-php'
        elif (myfile.endswith(".mp3")):
            mimetype = 'audio/mpeg'

        # mimetype = mimetypes.MimeTypes().guess_type(myfile)[0] -- library not support pptx...

        header += 'Content-Type: ' + str(mimetype) + '\n\n'

    except Exception as e:
        header = 'HTTP/1.1 404 Not Found\n\n'
        file2 = open('404.html', 'r')
        response = file2.read()
        file2.close()
        response = response.encode('utf-8')

    print('Server response: ', header)
    final_response = header.encode('utf-8')
    final_response += response
    connection.send(final_response)
    connection.close()
