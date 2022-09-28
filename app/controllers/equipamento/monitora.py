from app.models.bdMonitora import Computador, LocalPa, Status
from app import db
import subprocess
import threading
from datetime import datetime
from pytz import timezone


class Monitora:

    def __init__(self) -> None:
        self.listaComputadores = []
        self.consultaComputador()

    def consultaComputador(self):

        computadores = db.session.query(Computador.id, Computador.hostname, Computador.serial, Computador.patrimonio, Status.id.label('idStatus'), Status.ativo,
                                        Status.dataHora, LocalPa.descricaoPa).join(Computador, LocalPa.id == Computador.idLocalPa).join(Status, Status.id == Computador.idStatus).all()
        for computador in computadores:
            desktop = {
                'id': computador.id,
                'hostname': computador.hostname,
                'serial': computador.serial,
                'patrimonio': computador.patrimonio,
                'idStatus': computador.idStatus,
                'status': computador.ativo,
                'descricaoPa': computador.descricaoPa,
                'data': computador.dataHora
            }
            self.listaComputadores.append(desktop)

    def computadoresView(self):
        return self.listaComputadores

    # ips = ['10.204.2.38', '10.204.2.40', 'NBR001150-01485']

    def consultaStatusComputadores(self, listaComputadores):
        for computador in listaComputadores:
            # print(computador['hostname'])
            # result = subprocess.Popen(["ping", "-n", "2", computador['hostname']]).wait()
            if subprocess.Popen(["ping", "-n", "2", computador['hostname']]).wait():
                print(f"Hostname: {computador['hostname']}, está inativo")
            else:
                print(f"Hostname: {computador['hostname']}, está ativo")

    def atualizarStatusComputador(self) -> None:
        t = threading.Thread(target=self.consultaStatusComputadores(self.listaComputadores))
        t.start()

    def calculaHora(self):
      data_e_hora_atuais = datetime.now()
      fuso_horario = timezone('America/Sao_Paulo')
      data_e_hora_sao_paulo = data_e_hora_atuais.astimezone(fuso_horario)
      data1 = datetime.strptime(data_e_hora_sao_paulo.strftime('%d/%m/%Y %H:%M'), '%d/%m/%Y %H:%M')
      data_e_hora_em_texto = "27/09/2022 12:30"
      data2 = datetime.strptime(data_e_hora_em_texto, '%d/%m/%Y %H:%M')
      print(data1 - data2)

      time_1 = datetime.strptime(data_e_hora_sao_paulo.strftime("%H:%M:%S"), "%H:%M:%S")
      for computador in self.listaComputadores:
        time_2 = datetime.strptime(computador['data'].strftime("%H:%M:%S"),"%H:%M:%S") 
        # hora = computador['data']
        # atual = data_e_hora_sao_paulo - hora
        # print(f"Diferença horas: {atual}")
      print(time_1 - time_2)