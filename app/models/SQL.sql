-- SELECT * from Computador

-- SELECT Computador.serial, Computador.hostname, status.ativo, status.dataHora, LocalPa.descricaoPa FROM Computador JOIN LocalPa on Computador.idLocalPa = LocalPa.id JOIN status on status.id = Computador.idStatus

-- SELECT Computador.hostname,Computador.serial, status.dataHora FROM Computador JOIN status on Computador.idStatus=status.id