import subprocess
import threading
# ips = ['10.204.2.38', '10.204.2.40', 'NBR001150-01485']
# # ip = "10.204.2.38"

# # os.system(f'ping -n 2 {ip}')


# for i in ips:
#     # print(i)
#     result = subprocess.Popen(["ping", "-n", "2", i]).wait()
#     print(f'result: {result}')
#     if result:
#         print(f"IP: {i}, está inativo")
#     else:
#         print(f"IP: {i}, está ativo")

class ConsultaIP():

    ips = ['10.204.2.38', '10.204.2.40', 'NBR001150-01485']

    def ping(self, listaIP):
        for ip in listaIP:
            result = subprocess.Popen(["ping", "-n", "2", ip]).wait()
            if result:
                print(f"IP: {ip}, está inativo")
            else:
                print(f"IP: {ip}, está ativo")
    
    def __init__(self) -> None:
        t = threading.Thread(target=self.ping(self.ips))
        t.start()

ConsultaIP()
