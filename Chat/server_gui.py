import tkinter as tk
import socket
import threading
window = tk.Tk()
window.title("Server")
topFrame = tk.Frame(window)
btnStart = tk.Button(topFrame, text="Connect", command=lambda: start_server())
btnStart.pack(side=tk.LEFT)
btnStop = tk.Button(topFrame, text="Stop", command=lambda: stop_server(), state=tk.DISABLED)
btnStop.pack(side=tk.LEFT)
topFrame.pack(side=tk.TOP, pady=(5, 0))
middleFrame = tk.Frame(window)
lblHost = tk.Label(middleFrame, text="Host: X.X.X.X")
lblHost.pack(side=tk.LEFT)
lblPort = tk.Label(middleFrame, text="Port:XXXX")
lblPort.pack(side=tk.LEFT)
middleFrame.pack(side=tk.TOP, pady=(5, 0))
clientFrame = tk.Frame(window)
lblLine = tk.Label(clientFrame, text="**********Client List**********").pack()
scrollBar = tk.Scrollbar(clientFrame)
scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
tkDisplay = tk.Listbox(clientFrame, height=15, width=30, selectmode=tk.SINGLE)
tkDisplay.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
scrollBar.config(command=tkDisplay.yview)
tkDisplay.config(yscrollcommand=scrollBar.set, background="#F4F6F7")
removeBtn = tk.Button(clientFrame, text="Remove Selected", command=lambda: remove_client())
removeBtn.pack(side=tk.BOTTOM, pady=(5, 10))
clientFrame.pack(side=tk.BOTTOM, pady=(5, 10))
server = None
HOST_ADDR = "localhost"
HOST_PORT = 8000
client_name = " "
clients = []
clients_names = []
def start_server():
    global server, HOST_ADDR, HOST_PORT
    btnStart.config(state=tk.DISABLED)
    btnStop.config(state=tk.NORMAL)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(socket.AF_INET)
    print(socket.SOCK_STREAM)
    server.bind((HOST_ADDR, HOST_PORT))
    server.listen(5)
    threading._start_new_thread(accept_clients, (server, " "))
    lblHost["text"] = "Host: " + HOST_ADDR
    lblPort["text"] = "Port: " + str(HOST_PORT)
def stop_server():
    global server
    btnStart.config(state=tk.NORMAL)
    btnStop.config(state=tk.DISABLED)
def accept_clients(the_server, y):
    while True:
        client, addr = the_server.accept()
        clients.append((client, addr))  # Store both client connection and address
        threading._start_new_thread(send_receive_client_message, (client, addr))
def send_receive_client_message(client_connection, client_ip_addr):
    global server, client_name, clients, clients_addr
    client_msg = " "
    client_name = client_connection.recv(4096).decode()
    welcome_msg = "Welcome " + client_name + ". Use 'exit' to quit"
    client_connection.send(welcome_msg.encode())
    clients_names.append(client_name)
    update_client_names_display(clients_names)
    while True:
        data = client_connection.recv(4096).decode()
        if not data:
            break
        if data == "exit":
            break
        client_msg = data
        idx = get_client_index(clients, client_connection)
        sending_client_name = clients_names[idx]
        for c, addr in clients:
            if c != client_connection:
                server_msg = str(sending_client_name + "->" + client_msg)
                c.send(server_msg.encode())
    idx = get_client_index(clients, client_connection)
    del clients_names[idx]
    del clients[idx]
    server_msg = "BYE!"
    client_connection.send(server_msg.encode())
    client_connection.close()
    update_client_names_display(clients_names)
def get_client_index(client_list, curr_client):
    idx = 0
    for conn, addr in client_list:
        if conn == curr_client:
            break
        idx += 1
    return idx
def update_client_names_display(name_list):
    tkDisplay.delete(0, tk.END)
    for c in name_list:
        tkDisplay.insert(tk.END, c)
def remove_client():
    selected_index = tkDisplay.curselection()
    if selected_index:
        selected_index = selected_index[0]
        if 0 <= selected_index < len(clients):
            client, addr = clients[selected_index]
            client_name = clients_names[selected_index]
            server_msg = "SERVER: " + client_name + " has been removed."
            client.send(server_msg.encode())
            client.close()
            del clients_names[selected_index]
            del clients[selected_index]
            update_client_names_display(clients_names)
window.mainloop()
