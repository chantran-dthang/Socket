import socket
import mimetypes
import os
import os.path
import time

PORT = 80
HOST = socket.gethostbyname(socket.gethostname())
files_html = '<!doctype html><html lang="en"><head><title>FILES</title><!-- Required meta tags --><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no"><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"><link rel="shortcut icon" href="#"></head><body><style type="text/css">table {border-collapse: collapse;}th{font-size: 20px;color: blue;text-decoration: underline;border-bottom: 1px solid black;vertical-align: bottom;padding: 15px;}td{padding: 5px;}.btn-link {border: none;outline: none;background: none;cursor: pointer;color: #0000EE;padding: 0;text-decoration: underline;font-family: inherit;font-size: inherit;}</style><table><tr><th>Name</th><br><th>Last modified</th><th>Size</th><th>Description</th></tr><tr><form action="/index.html" method="POST"><td></i><i class="fa fa-arrow-left"><input class ="btn-link" type="submit" value="[Parent Directory]" /></form></tr>'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(1)
print('Host:', HOST)
print('Serving on port ', PORT)


def MovePage(filename, connector):
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
        respone += files_html.encode('utf-8')
    else:
        respone = header.encode('utf-8')
    connector.send(respone)
    connector.close()

checkPwd = False  # True when username password accepted
while True:
    connector, address = server.accept()
    request = connector.recv(1024).decode('utf-8')
    if (request == ""):
        connector.close()
        continue
    string_list = request.split(' ')  # Split request from spaces
    method = string_list[0]
    file_request = string_list[1]
    print('Client request ', method, file_request, "??")

    filename = file_request.split('?')[0]  # After the "?" symbol not relevent here
    filename = filename.lstrip('/')
    if (method == 'GET'):
        # Load index file as default
        # Check info, prevent connect to info.html when don't enter username-password
        if(((filename=='info.html'or filename=='files.html')and checkPwd==False) or filename==''):
            filename = 'index.html'
            MovePage(filename, connector)
            continue
        if (filename == 'index.html'):
            checkPwd = False
        if (filename == 'files.html'):
            pathF = 'files'
            listfile = os.listdir(pathF)
            for i in listfile:
                dirF = pathF + "/"
                dirF = dirF + i
                day_m = os.path.getmtime(dirF)
                files_html += '<tr><form action="' + dirF + '" method="POST"><td></i><i class="fa fa-file-o"><input class ="btn-link" type="submit" value="' + i + '" /></form>'
                day_m2 = time.localtime(day_m)
                size = os.path.getsize(dirF)
                files_html += '<td>' + str(day_m2.tm_year) + '-' + str(day_m2.tm_mon) + '-' + str(
                    day_m2.tm_mday) + ' ' + str(day_m2.tm_hour) + ':' + str(day_m2.tm_min) + '</td>'
                files_html += '<td>' + str(round(size / 1024, 1)) + 'M</td></tr>'
            MovePage(filename, connector)
            continue
    elif (method == 'POST'):
        if (filename == 'info.html'):
            pass_and_user = string_list[-1].split('username=')[1]
            username = pass_and_user.split('&password=')[0]
            password = pass_and_user.split('&password=')[1]
            print('Username: ', username)
            print('Password: ', password)
            if (username == 'admin' and password == 'admin'):
                checkPwd = True
                MovePage(filename, connector)
                continue
            else:
                filename = '404.html'
                checkPwd = False
        else:
            MovePage(filename, connector)
            continue
    else:
        connector.close()
        continue
    try:
        file = open(filename, 'rb')  # open file , r => read , b => byte format
        content = file.read()
        file.close()
        if (filename == '404.html'):
            MovePage(filename, connector)
            continue
        else:
            header = 'HTTP/1.1 200 OK\n'
        # -- library not support pptx ...
        if (filename.endswith(".jpg") or filename.endswith('.jpeg')):
            mimetype = 'image/jpg'
        elif (filename.endswith(".png")):
            mimetype = 'image/png'
        elif (filename.endswith(".css")):
            mimetype = 'text/css'
        elif (filename.endswith('.html') or filename.endswith('.htm')):
            mimetype = 'text/html'
        elif (filename.endswith(".pdf")):
            mimetype = 'application/pdf'
        elif (filename.endswith(".ppt")):
            mimetype = 'application/vnd.ms-powerpoint'
        elif (filename.endswith(".pptx")):
            mimetype = 'application/vnd.openxmlformats-officedocument.presentationml.presentation'
        elif (filename.endswith(".rar")):
            mimetype = 'application/vnd.rar'
        elif (filename.endswith(".xls")):
            mimetype = 'application/vnd.ms-excel'
        elif (filename.endswith(".xlsx")):
            mimetype = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        elif (filename.endswith(".doc")):
            mimetype = 'application/msword'
        elif (filename.endswith(".docx")):
            mimetype = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        elif (filename.endswith(".zip")):
            mimetype = 'application/zip'
        elif (filename.endswith(".csv")):
            mimetype = 'text/csv'
        elif (filename.endswith(".php")):
            mimetype = 'application/x-httpd-php'
        elif (filename.endswith(".mp3")):
            mimetype = 'audio/mpeg'
        # mimetype = mimetypes.MimeTypes().guess_type(myfile)[0] -- library not support pptx...
        header += 'Content-Type: ' + str(mimetype) + '\n\n'

    except Exception as e:
        header = 'HTTP/1.1 404 Not Found\n\n'
        file2 = open('404.html', 'r')
        content = file2.read()
        file2.close()
        content = content.encode('utf-8')
    print('Server response: ', header)
    response = header.encode('utf-8')
    response += content
    connector.send(response)
    connector.close()

# PORT = 80
# HOST = 'localhost'
# server=(HOST,PORT)
# webServer=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# webServer.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
# webServer.bind(server)
# webServer.listen(5)
# print("Web server application is running on: \nHost:\t",HOST,"\nPort:\t",PORT)
#
#
# checkPwd=False
# while True:
#     connectClient=(connector,Client)=webServer.accept()
#     print('New connection:\nClient:\t',Client[0],'\nPort:\t',Client[1])
#     request=connector.recv(1024).decode('utf-8')
#     spiltReqList=request.split(' ')
#     method=spiltReqList[0]
#     reqFile=spiltReqList[1]
#     fileName=reqFile.spilt('?')[0]
#     fileName=fileName.lstrip('/')
#     if(method=='GET'):
#         if(((fileName=='info.html'or fileName=='files.html')and checkPwd==False) or fileName==''):
#             fileName='index.html'
#             header = "HTTP/1.1 301 Moved Permanently\n"+"Location: /" + fileName
#             print('Server response:',header)
#             response=header.encode('utf-8')
#             connector.send(response)
#             connector.close()
#             continue
#         if(fileName=='index.html'):
#             checkPwd=False
#         if(fileName=='files.html'):
#             filesHTML=open('files.html','r')
#             content=filesHTML.read()
#             path='files'
#             filesList=os.listdir(path)
#             for i in filesList:
#                 dirF = path + "/"
#                 dirF = dirF + i
#                 filesHTML+= '<tr><form action="' + dirF + '" method="GET"><td></i><i class="fa fa-file-o"><input class ="link" type="submit" value="' + i + '" /></form>'
#                 modDay= os.path.getmtime(dirF)
#                 modDay = time.localtime(modDay)
#                 size = round(os.path.getsize(dirF)/1024,1)
#                 content += '<td>' + str(modDay.tm_year) + '-' + str(modDay.tm_mon) + '-' + str(modDay.tm_mday) +' ' + str(modDay.tm_hour) +':' + str(modDay.tm_min) +'</td>'
#                 content += '<td>' + str(size) + 'KB</td></tr>'
#             header = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n'
#             print('Server response: ',header)
#             response=header+content
#             response=response.encode('utf-8')
#             connector.send()
#             connector.close()
#             continue
#
#             # for i in listfile:
#             #     dirF = pathF + "/"
#             #     dirF = dirF + i
#             #     day_m = os.path.getmtime(dirF);
#             #     code_files += '<tr><form action="' + dirF + '" method="POST"><td></i><i class="fa fa-file-o"><input class ="btn-link" type="submit" value="' + i + '" /></form>'
#             #     day_m2 = time.localtime(day_m)
#             #     size = os.path.getsize(dirF)
#             #     code_files += '<td>' + str(day_m2.tm_year) + '-' + str(day_m2.tm_mon) + '-' + str(
#             #         day_m2.tm_mday) + ' ' + str(day_m2.tm_hour) + ':' + str(day_m2.tm_min) + '</td>'
#             #     code_files += '<td>' + str(round(size / 1024, 1)) + 'M</td></tr>'
#
#
#
#
# >>>>>>> 705857f60e2c53e51347b24dfa5a0a35d377af13
