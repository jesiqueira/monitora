from app.models.bdMonitora import Computador, LocalPa, Status
from app import db
import subprocess
import threading
import concurrent.futures
from datetime import datetime, timedelta
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
        computador = {
            'conectado': 0,
            'desconectado': 0,
            'atencao': 0,
            'data': '',
            'hora': ''
        }
        for comp in self.listaComputadores:
            if comp['status']:
                # print(f"idStatus: {comp['idStatus']}, Status: {comp['status']}")
                computador['conectado'] += 1
                dataataualizacao = datetime
                dataataualizacao = comp['data']
                computador['data'] = dataataualizacao.strftime('%d/%m/%Y')
                computador['hora'] = dataataualizacao.strftime('%H:%M:%S')
                # print(computador['hora'])
            else:
                computador['desconectado'] += 1
        return computador

    def consultaAtaualizaStatusComputadores(self, listaComputador):
        # print(listaComputadores['id'])
        # for listaComputador in listaComputador:
        #     if subprocess.Popen(["ping", "-n", "2", listaComputador['hostname']]).wait():
        #         self.atualizarStatusComputador(
        #             idComputador=listaComputador['id'], idStatus=listaComputador['idStatus'], statusComputador=False)
        #     else:
        #         self.atualizarStatusComputador(idComputador=listaComputador['id'], idStatus=listaComputador['idStatus'], statusComputador=True)
        #    result = subprocess.Popen(["ping", "-n", "2", listaComputador['hostname']]).wait()
        listaStatus = []
        status ={
            'idComputador' : 0,
            'idStatus' : 0,
            'statusComputador' : 0
        }
        if subprocess.Popen(["ping", "-n", "2", listaComputador['hostname']]).wait():
            status['idComputador'] = listaComputador['id']
            status['idStatus'] = listaComputador['idStatus']
            status['statusComputador'] = False
            listaStatus.append(status)

            # self.executarProcess(self.atualizarStatusComputador, listaStatus)
            self.testeConsultaSQL(lista=listaStatus)
            # self.atualizarStatusComputador(
            #     idComputador=listaComputador['id'], idStatus=listaComputador['idStatus'], statusComputador=False)
            # print(f"Hostname: {listaComputador['hostname']}, está inativo")
        else:
            status['idComputador'] = listaComputador['id']
            status['idStatus'] = listaComputador['idStatus']
            status['statusComputador'] = True
            listaStatus.append(status)

            # self.executarProcess(self.atualizarStatusComputador, listaStatus)
            self.testeConsultaSQL(lista=listaStatus)
            self.atualizarStatusComputador(
                idComputador=listaComputador['id'], idStatus=listaComputador['idStatus'], statusComputador=True)
            # print(f"Hostname: {computador['hostname']}, está ativo")
    
    def agoraVai(self, listaComputador):
        t = threading.Thread(target=self.consultaAtaualizaStatusComputadores(self.listaComputadores))
        t.start()

    def threadAtualizarStatusComputador(self) -> None:
        # self.executarThread(self.consultaAtaualizaStatusComputadores, self.listaComputadores)
        self.agoraVai(self.listaComputadores)
        # pass
    
    def executarThread(self, func, lista):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(func, lista)

    def executarProcess(self, func, lista):
        with concurrent.futures.ProcessPoolExecutor() as executor:
            executor.map(func, lista)

    def atualizarStatusComputador(self, idComputador=0, idStatus=0, statusComputador=False):
        try:
            status = db.session.query(Status).join(Computador, Status.id == Computador.idStatus).filter(
                Computador.id == idComputador and Status.id == idStatus).first_or_404()
            if statusComputador:
                status.ativo = statusComputador
                status.dataHora = self.horaAtual()
            elif(status.ativo):
                status.ativo = statusComputador
                status.dataHora = self.horaAtual()
            db.session.commit()
        except Exception as e:
            db.session.flush()
            db.session.rollback()
            print(f'Error: {e}')
    
    def testeConsultaSQL(self):

        print('aqui')
        status = Status.query.get_or_404(1)
        print(status)

    def horaAtual(self):
        data_e_hora_atuais = datetime.now()
        fuso_horario = timezone('America/Sao_Paulo')
        data_e_hora_sao_paulo = data_e_hora_atuais.astimezone(fuso_horario)

        return data_e_hora_sao_paulo

    def calculaHora(self):
        data_e_hora_atuais = datetime.now()
        fuso_horario = timezone('America/Sao_Paulo')
        data_e_hora_sao_paulo = data_e_hora_atuais.astimezone(fuso_horario)
        data1 = datetime.strptime(data_e_hora_sao_paulo.strftime(
            '%d/%m/%Y %H:%M'), '%d/%m/%Y %H:%M')
        data_e_hora_em_texto = "27/09/2022 12:30"
        data2 = datetime.strptime(data_e_hora_em_texto, '%d/%m/%Y %H:%M')
        print(data1 - data2)

        time_1 = datetime.strptime(data_e_hora_sao_paulo.strftime(
            "%d/%m/%Y %H:%M"), "%d/%m/%Y %H:%M")
        for computador in self.listaComputadores:
            texto_simples = computador['data']
            novo_texto_simples = datetime.strftime(
                computador['data'], '%d/%m/%Y %H:%M')
            # print(f'Novo texto: {novo_texto_simples}')
            time_2 = datetime.strptime(computador['data'].strftime(
                '%d/%m/%Y %H:%M'), '%d/%m/%Y %H:%M')
            # hora = computador['data']
            # atual = data_e_hora_sao_paulo - hora
            # print(f"Diferença horas: {atual}")
        difereca_time = time_1 - time_2
    #   print(str(difereca_time))
    #   print(dir(difereca_time))
        print(f'Data hora atual: {data_e_hora_sao_paulo}')
        print(f'Dirença: {difereca_time.days}')
