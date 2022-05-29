import socket

def start_my_server():
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('127.0.0.1', 2000))
        #Можно так
        #server = socket.create_server(('127.0.0.1', 2000))

        # Указание серверу слушать указанный порт
        server.listen(4)
        while True:
            print('Working...')
            #С помощью метода accept сервер принимает отправленные ему запросы и
            # разделяет их на клиента и адрес, с которого прилетел запрос.
            #Особенностью этого метода является то, что на этом моменте программа
            # фиксируется и не идет дальше до тех пор пока кто- то не подключится
            # к этому серверу
            client_socket, address = server.accept()
            #Из оъекта клиента получаем содержимое запроса
            data = client_socket.recv(1024).decode('utf-8')
        #    print(data)
            #На отправку клиенту
            content = load_page_from_get_request(data)
            #Энкодируем заголовки и добавляем наш контент
            client_socket.send(content)
            #Закрытие соединения с конкретным клиентом после того, как ему был отправлен ответ
            client_socket.shutdown(socket.SHUT_WR)
    except KeyboardInterrupt:
        server.close()
        print('shutdown this shut...')

#Функция обработчик
def load_page_from_get_request(request_data):
    # Указание браузеру Chrome напрямую, что передается именно html информация.
    # Это делается с помощью заголовков, в котором указывается тип ответа, статус,
    # код статуса и кодировка
    HDRS = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'
    #Заголовок если страница не найдена 404
    HDRS_404 = 'HTTP/1.1 404 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'
    #Парсинг запроса клиента
    path = request_data.split(' ')[1]
    response = ''
    try:
        with open('views'+path, 'rb') as file:
            response = file.read()
        return HDRS.encode('utf-8') + response
    except FileNotFoundError:
        return (HDRS_404 + 'Sorry, bro! No page...').encode('utf-8')

if __name__ == '__main__':
    start_my_server()