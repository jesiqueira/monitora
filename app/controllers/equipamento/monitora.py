from app.models.bdMonitora import Computador, LocalPa, Status
from app import db
import subprocess
import threading
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
        return computador

    def consultaAtaualizaStatusComputadores(self, listaComputador):
        '''Realiza Ping em uma lista de computadores para saber se estão conectado corretamente na rede'''
        for listaComputador in listaComputador:
            if subprocess.Popen(["ping", "-n", "2", listaComputador['hostname']]).wait():
                self.atualizarStatusComputador(
                    idComputador=listaComputador['id'], idStatus=listaComputador['idStatus'], statusComputador=False)
            else:
                self.atualizarStatusComputador(
                    idComputador=listaComputador['id'], idStatus=listaComputador['idStatus'], statusComputador=True)

    def threadAtualizarStatusComputador(self) -> None:
        t = threading.Thread(
            target=self.consultaAtaualizaStatusComputadores(self.listaComputadores))
        t.start()
        print('Finalizou')

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

    def horaAtual(self):
        data_e_hora_atuais = datetime.now()
        fuso_horario = timezone('America/Sao_Paulo')
        data_e_hora_sao_paulo = data_e_hora_atuais.astimezone(fuso_horario)

        return data_e_hora_sao_paulo
