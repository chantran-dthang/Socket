import socket
import os
import os.path
import time

PORT = 80
HOST = 'localhost'
server=(HOST,PORT)
webServer=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
webServer.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
webServer.bind(server)
webServer.listen(5)
print("Web server application is running on: \nHost:\t",HOST,"\nPort:\t",PORT)


checkPwd=False
while True:
    connectClient=(connector,Client)=webServer.accept()
    print('New connection:\nClient:\t',Client[0],'\nPort:\t',Client[1])
    request=connector.recv(1024).decode('utf-8')
    spiltReqList=request.split(' ')
    method=spiltReqList[0]
    reqFile=spiltReqList[1]
    fileName=reqFile.spilt('?')[0]
    fileName=fileName.lstrip('/')
    if(method=='GET'):
        if(((fileName=='info.html'or fileName=='files.html')and checkPwd==False) or fileName==''):
            fileName='index.html'
            header = "HTTP/1.1 301 Moved Permanently\n"+"Location: /" + fileName
            print('Server response:',header)
            response=header.encode('utf-8')
            connector.send(response)
            connector.close()
            continue
        if(fileName=='index.html'):
            checkPwd=False
        if(fileName=='files.html'):
            filesHTML=open('files.html','r')
            content=filesHTML.read()
            path='files'
            filesList=os.listdir(path)
            for i in filesList: 
                dirF = path + "/"
                dirF = dirF + i
                filesHTML+= '<tr><form action="' + dirF + '" method="GET"><td></i><i class="fa fa-file-o"><input class ="link" type="submit" value="' + i + '" /></form>'
                modDay= os.path.getmtime(dirF)
                modDay = time.localtime(modDay)
                size = round(os.path.getsize(dirF)/1024,1)
                content += '<td>' + str(modDay.tm_year) + '-' + str(modDay.tm_mon) + '-' + str(modDay.tm_mday) +' ' + str(modDay.tm_hour) +':' + str(modDay.tm_min) +'</td>'
                content += '<td>' + str(size) + 'KB</td></tr>'
            header = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n'
            print('Server response: ',header)
            response=header+content
            response=response.encode('utf-8')
            connector.send()
            connector.close()
            continue




