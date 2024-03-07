import socket

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

client_name = input("Enter your player name: ")
client.sendto(f'CONNECT {client_name}'.encode('utf-8'), ("127.0.0.1", 12345))

stats_data, _ = client.recvfrom(1024) #colectam statusurile din server
client_stats = stats_data.decode('utf-8')
print(f'Your stats: {client_stats}') #acum jucatorul stie de ce e capabil

result, _ = client.recvfrom(1024) #luam rezultatele dupa meci
result.decode('utf-8')
print(result)

client.close()
