-- SQLite
-- SELECT * FROM Acoes
-- SELECT * FROM DispositivosEquipamentos
-- SELECT * FROM Status
-- SELECT * FROM PontoAtendimentos
-- SELECT * FROM TipoEquipamentos
-- SELECT * FROM Computadores
-- SELECT DispositivosEquipamentos.serial, Areas.nome, Areas.id FROM DispositivosEquipamentos JOIN Areas ON DispositivosEquipamentos.idArea=Areas.id WHERE Areas.nome = 'Estoque'
-- UPDATE DispositivosEquipamentos SET idArea = 1 WHERE DispositivosEquipamentos.idArea = 2
-- SELECT TipoEquipamentos.nome FROM tipoEquipamentoSites JOIN TipoEquipamentos on tipoEquipamentoSites.idTipos=TipoEquipamentos.id where tipoEquipamentoSites.idSites=2
-- SELECT DispositivosEquipamentos.id, DispositivosEquipamentos.serial, TipoEquipamentos.nome, Areas.nome, Computadores.id, Computadores.idDispositosEquipamento, PontoAtendimentos.descricao FROM DispositivosEquipamentos join TipoEquipamentos on DispositivosEquipamentos.idTipo=TipoEquipamentos.id JOIN Areas on Areas.id=DispositivosEquipamentos.idArea JOIN Computadores on Computadores.idDispositosEquipamento=DispositivosEquipamentos.id JOIN PontoAtendimentos ON PontoAtendimentos.id=Computadores.idPontoAtendimento WHERE DispositivosEquipamentos.idSite=1 AND Areas.nome='Inventario' AND DispositivosEquipamentos.id=14
-- SELECT * FROM Areas join areaSites on areaSites.idAreas=Areas.id WHERE areaSites.idSites=1 AND Areas.nome='Descarte'
SELECT * FROM Computadores WHERE Computadores.id=2