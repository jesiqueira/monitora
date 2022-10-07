from typing import List
from app.models.bdMonitora import Computadores, PontoAtendimentos, Status
from app import db
import subprocess
import concurrent.futures
from datetime import datetime
from pytz import timezone


class Monitora:

    def __init__(self) -> None:
        self.listaComputadores = []
        self.listaStatusComputadores = []
        self.consultaComputador()

    def consultaComputador(self):
        '''Realiza a consulta de todos os computadores cadastrado no BD que estão instalados em um site e salva o resultado em uma lista para uso posterior.'''
        computadores = db.session.query(Computadores.id, Computadores.hostname, Computadores.serial, Computadores.patrimonio, Status.id.label('idStatus'), Status.ativo,
                                        Status.dataHora, PontoAtendimentos.descricao).join(Computadores, PontoAtendimentos.id == Computadores.idPontoAtendimentos).join(Status, Status.id == Computadores.idStatus).all()
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
            self.listaComputadores.append(desktop.copy())

    def computadoresView(self):
        '''Retorna o Status: Conectado/Desconectado/Atenção, Data e Hora dos computadores que estão alocado no site'''
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
                dataAtualizacao = datetime
                dataAtualizacao = comp['data']
                computador['data'] = dataAtualizacao.strftime('%d/%m/%Y')
                computador['hora'] = dataAtualizacao.strftime('%H:%M:%S')
            elif not comp['status'] and self.calculaDiasComputadorOffiline(comp['data']) > 2:
                computador['desconectado'] += 1
                dataAtualizacao = datetime
                dataAtualizacao = comp['data']
                # computador['data'] = dataAtualizacao.strftime('%d/%m/%Y')
                # computador['hora'] = dataAtualizacao.strftime('%H:%M:%S')
            else:
                computador['atencao'] += 1
                dataAtualizacao = datetime
                dataAtualizacao = comp['data']
                # computador['data'] = dataAtualizacao.strftime('%d/%m/%Y')
                # computador['hora'] = dataAtualizacao.strftime('%H:%M:%S')

        return computador

    def consultaAtualizaStatusComputadores(self, listaComputador):
        '''Realiza Ping em uma lista de computadores para saber se estão conectado corretamente na rede e salva as informações em uma nova lista para uso posterior.'''
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
        '''Está função faz as chamadas dos metodos parar realizar a consulta via Thread do Status dos computadores na rede e atualizar o BD com os Status recebidos'''
        result = self.executarThread(
            self.consultaAtualizaStatusComputadores, self.listaComputadores)
        self.atualizarStatusComputador(self.listaStatusComputadores)

    def executarThread(self, func, lista):
        '''Criar e executa Thread'''
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(func, lista)

    def atualizarStatusComputador(self, listaDeComputadores):
        '''Atualiza o status dos computadores no BD ao receber uma lista com Status da consulta realizada por PIP nos computadores da rede'''
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

    def horaAtual(self) -> datetime:
        '''Retorna o dia e hora atual em São Paulo'''
        data_e_hora_atuais = datetime.now()
        fuso_horario = timezone('America/Sao_Paulo')
        data_e_hora_sao_paulo = data_e_hora_atuais.astimezone(fuso_horario)
        return data_e_hora_sao_paulo

    def calculaDiasComputadorOffiline(self, data) -> int:
        '''Calcula e retorna a quantidade de dias que o computador está sem responder na rede'''
        data1 = datetime.strptime(self.horaAtual().strftime(
            "%d/%m/%Y %H:%M"), "%d/%m/%Y %H:%M")
        data2 = datetime.strptime(data.strftime(
            '%d/%m/%Y %H:%M'), '%d/%m/%Y %H:%M')
        diferenca = data1 - data2
        return diferenca.days

    def statusAtencao(self) -> List:
        '''Retorna os computadores que estão com Status marcado com Atenção'''
        atencao = {
            'serial': '',
            'patrimonio': '',
            'hostname': '',
            'descricaoPa': ''
        }
        computadores = []
        for computador in self.listaComputadores:
            atencao.clear()
            if not computador['status'] and self.calculaDiasComputadorOffiline(computador['data']) <= 2:
                atencao['serial'] = computador['serial']
                atencao['patrimonio'] = computador['patrimonio']
                atencao['hostname'] = computador['hostname']
                atencao['descricaoPa'] = computador['descricaoPa']
                computadores.append(atencao.copy())

        return computadores

    def statusDesconectado(self) -> List:
        '''Retorna os computadores que estão com Status marcado com Atenção'''
        computadores = []
        desconectado = {
            'serial': '',
            'patrimonio': '',
            'hostname': '',
            'descricaoPa': '',
        }
        for computador in self.listaComputadores:
            desconectado.clear()
            if not computador['status'] and self.calculaDiasComputadorOffiline(computador['data']) >=3:
                desconectado['serial'] = computador['serial']
                desconectado['patrimonio'] = computador['patrimonio']
                desconectado['hostname'] = computador['hostname']
                desconectado['descricaoPa'] = computador['descricaoPa']
                computadores.append(desconectado.copy())
        return computadores
