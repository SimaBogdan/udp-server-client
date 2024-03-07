import socket
import random
import queue

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("127.0.0.1", 12345))

clients = {} #clientii sunt salvati intr-un dictionar pentru usurinta sufletului meu
client_queue = queue.Queue()

ok = 1  #acest ok e doar pentru a printa startul serverului

#aceasta functie compara statusurile clientiilor/jucatoriilor, le atribuie punctele si declara castigatorul
def compare_stats(client1, stats1, client2, stats2):

    points1 = 0
    points2 = 0

    for stat in stats1:
        if stats1[stat] > stats2[stat]:
            points1 += 1
        elif stats2[stat] > stats1[stat]:
            points2 += 1

    if points1 > points2:
        return f'{client1} wins!'
    elif points2 > points1:
        return f'{client2} wins!'
    else:
        return "It's a tie :("

#partea principala a serverului
while True:

    if ok == 1:
        print("IT'S TIME TO DU-DU-DUEL!")#is this a yu-gi-oh reference ? :O
        ok = 0

    data, client_address = server.recvfrom(1024)#se iau informatiile din client
    message = data.decode('utf-8')#decodeaza datele primite

    print(f"Client connected from {client_address}")#cand se conecteaza clientul

    if message.startswith('CONNECT'):
        _, client_name = message.split()#ne intereseaza doar numele oferit de client

        stats = {
            'Strength': random.randint(1, 10),
            'Speed': random.randint(1, 10),
            'Durability': random.randint(1, 10),
            'IQ': random.randint(1, 10)
        }

        clients[client_name] = (stats, client_address)
        client_queue.put(client_name)

        client_stats = ', '.join(f'{stat}: {value}' for stat, value in stats.items())#trimitem la client statusurile pe care le are ca sa stie de ce a pierdut si sa nu fie salty
        server.sendto(client_stats.encode('utf-8'), client_address)

        if len(clients) >= 2:
            client1 = client_queue.get()
            client2 = client_queue.get()

            client1_stats, client1_address = clients[client1]
            client2_stats, client2_address = clients[client2]

            winner = compare_stats(client1, client1_stats, client2, client2_stats)#aflam castigatorul

            server.sendto(f'{winner}'.encode('utf-8'), client1_address)#trimitem jucatoriilor rezultatul
            server.sendto(f'{winner}'.encode('utf-8'), client2_address)#la fel si pentru el