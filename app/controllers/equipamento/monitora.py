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
        self.listaStatusComputadores = []
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
        '''Retorna o status dos computadores'''
        computador = {
            'conectado': 0,
            'desconectado': 0,
            'atencao': 0,
            'data': '',
            'hora': ''
        }
        for comp in self.listaComputadores:
            if comp['status']:
                computador['conectado'] += 1
                dataataualizacao = datetime
                dataataualizacao = comp['data']
                computador['data'] = dataataualizacao.strftime('%d/%m/%Y')
                computador['hora'] = dataataualizacao.strftime('%H:%M:%S')
            else:
                '''Ainda falta fazer o calcula da Data para saber o tempo que está inativo'''
                computador['desconectado'] += 1
                dataataualizacao = datetime
                dataataualizacao = comp['data']
                computador['data'] = dataataualizacao.strftime('%d/%m/%Y')
                computador['hora'] = dataataualizacao.strftime('%H:%M:%S')

        return computador

    def consultaAtualizaStatusComputadores(self, listaComputador):
        '''Realiza Ping em uma lista de computadores para saber se estão conectado corretamente na rede'''
        status = {
            'idComputador': 0,
            'idStatus': 0,
            'statusComputador': 0
        }
        if subprocess.Popen(["ping", "-n", "2", listaComputador['hostname']]).wait():
            status['idComputador'] = listaComputador['id']
            status['idStatus'] = listaComputador['idStatus']
            status['statusComputador'] = False
            self.listaStatusComputadores.append(status)
        else:
            status['idComputador'] = listaComputador['id']
            status['idStatus'] = listaComputador['idStatus']
            status['statusComputador'] = True
            self.listaStatusComputadores.append(status)

    def threadAtualizarStatusComputador(self) -> None:
        result = self.executarThread(
            self.consultaAtualizaStatusComputadores, self.listaComputadores)
        self.atualizarStatusComputador(self.listaStatusComputadores)

    def executarThread(self, func, lista):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(func, lista)

    def atualizarStatusComputador(self, listaDeComputadores):
        try:
            for computador in listaDeComputadores:
                status = db.session.query(Status).join(Computador, Status.id == Computador.idStatus).filter(
                    Computador.id == computador['idComputador'] and Status.id == computador['idStatus']).first_or_404()
                if computador['statusComputador']:
                    status.ativo = computador['statusComputador']
                    status.dataHora = self.horaAtual()
                elif(status.ativo):
                    status.ativo = computador['statusComputador']
                    status.dataHora = self.horaAtual()
                db.session.commit()
        except Exception as e:
            db.session.flush()
            db.session.rollback()
            print(f'Error: {e}')

    def horaAtual(self):
        data_e_hora_atuais = datetime.now()
        fuso_horario = timezone('America/Sao_Paulo')
        data_e_hora_sao_paulo = data_e_hora_atuais.astimezone(fuso_horario)

        return data_e_hora_sao_paulo
