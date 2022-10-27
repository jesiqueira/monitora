-- SQLite
-- SELECT * FROM Acoes
-- SELECT * FROM DispositivosEquipamentos
-- SELECT * FROM Status
-- SELECT * FROM Computadores
-- SELECT * FROM PontoAtendimentos
-- SELECT * FROM TipoEquipamentos
-- SELECT DispositivosEquipamentos.serial, Areas.nome, Areas.id FROM DispositivosEquipamentos JOIN Areas ON DispositivosEquipamentos.idArea=Areas.id WHERE Areas.nome = 'Estoque'
-- UPDATE DispositivosEquipamentos SET idArea = 1 WHERE DispositivosEquipamentos.idArea = 2
SELECT TipoEquipamentos.nome FROM tipoEquipamentoSites JOIN TipoEquipamentos on tipoEquipamentoSites.idTipos=TipoEquipamentos.id where tipoEquipamentoSites.idSites=2