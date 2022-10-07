-- SELECT * from Computador

-- SELECT * FROM LocalFisico

-- SELECT Computador.serial, Computador.hostname, status.ativo, status.dataHora, LocalPa.descricaoPa FROM Computador JOIN LocalPa on Computador.idLocalPa = LocalPa.id JOIN status on status.id = Computador.idStatus

-- SELECT Computador.id, Computador.hostname,Computador.serial, status.id, status.dataHora, status.ativo FROM Computador JOIN status on Computador.idStatus=status.id

-- SELECT * FROM Computador JOIN status on Computador.idStatus = status.id WHERE Computador.id=2 AND status.id =2