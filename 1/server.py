import socket
import threading

# تعريف حسابات البنك مع أرصدتها
accounts = {
    'mayas': ('1111', 1000.0),
    'mohsen': ('1111', 1500.0)
}

# تابع للتعامل مع كل عميل متصل
def handle_client(client_socket):
    try:
        # استقبال بيانات الحساب ورمز PIN من العميل
        client_socket.send(b'Enter account number and PIN (format: account_number:PIN): ')
        credentials = client_socket.recv(1024).decode().strip()
        account_number, pin = credentials.split(':')

        # التحقق من صحة بيانات الحساب
        if account_number in accounts and accounts[account_number][0] == pin:
            client_socket.send(b'Authenticated\n')
            while True:
                # إرسال الخيارات المتاحة للعميل
                client_socket.send(b'Choose operation (format: operation:amount): check, deposit, withdraw, exit\n')
                operation = client_socket.recv(1024).decode().strip().split(':')

                if operation[0] == 'check':
                    # تحقق من الرصيد
                    balance = accounts[account_number][1]
                    client_socket.send(f'Your balance is {balance}\n'.encode())

                elif operation[0] == 'deposit':
                    # إيداع المال
                    amount = float(operation[1])
                    accounts[account_number] = (pin, accounts[account_number][1] + amount)
                    client_socket.send(b'Deposit successful\n')

                elif operation[0] == 'withdraw':
                    # سحب المال
                    amount = float(operation[1])
                    if accounts[account_number][1] >= amount:
                        accounts[account_number] = (pin, accounts[account_number][1] - amount)
                        client_socket.send(b'Withdrawal successful\n')
                    else:
                        client_socket.send(b'Insufficient balance\n')

                elif operation[0] == 'exit':
                    # إنهاء الجلسة
                    balance = accounts[account_number][1]
                    client_socket.send(f'Your final balance is {balance}\n'.encode())
                    break
                else:
                    client_socket.send(b'Invalid operation\n')

        else:
            client_socket.send(b'Authentication failed\n')
    finally:
        client_socket.close()

# تابع بدء الخادم
def start_server():
    ssock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssock.bind(('0.0.0.0', 5555))
    ssock.listen(5)
    print("Server started and listening on port 5555")

    while True:
        client_socket, addr = ssock.accept()
        print(f'Accepted connection from {addr}')
        th = threading.Thread(target=handle_client, args=(client_socket,))
        th.start()

if __name__ == "__main__":
    start_server()
