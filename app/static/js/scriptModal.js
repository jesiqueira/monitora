// =========== Funções para página Usuarios================

function excluirSite(id_site) {
  document.querySelector('#id_site').value = id_site;
}

function excluirLocal(id_local) {
  document.querySelector('#id_local').value = id_local;
}

function editarUser(id_user, idSite) {
  document.querySelector('#id_user').value = id_user;
  document.querySelector('#id_site').value = idSite;
}

function updateURLUser() {
  var idUser = document.querySelector('#id_user').value;
  var idSite = document.querySelector('#id_site').value;

  var url = '/usuarioUpdate';

  var form = document.createElement('form');
  form.action = url;
  form.method = 'POST';

  var input = document.createElement('input');
  input.type = 'hidden';
  input.name = 'idUser';
  input.value = idUser;
  form.appendChild(input);
  document.body.appendChild(form);

  var input1 = document.createElement('input');
  input1.type = 'hidden';
  input1.name = 'idSite';
  input1.value = idSite;
  form.appendChild(input1);
  document.body.appendChild(form);

  form.submit();
}

function trocarSenhaURLUser() {
  var id_user = document.querySelector('#id_user').value;
  var idSite = document.querySelector('#id_site').value;
  var url = '/atualizarSenha';

  var form = document.createElement('form');
  form.action = url;
  form.method = 'POST';

  var input = document.createElement('input');
  input.type = 'hidden';
  input.name = 'id_users';
  input.value = id_user;
  form.appendChild(input);
  document.body.appendChild(form);

  var input1 = document.createElement('input');
  input1.type = 'hidden';
  input1.name = 'idSite';
  input1.value = idSite;
  form.appendChild(input1);
  document.body.appendChild(form);

  form.submit();
}

// =========== Funções para página inventário================

function editarInventario(idDispositivo, idSite) {
  document.querySelector('#idDispositivo').value = idDispositivo;
  document.querySelector('#idSite').value = idSite;
  console.log(`Id Dispositivo: ${idDispositivo}`)
}

function editarDadosEquipamentoInventario() {
  var idDispositivo = document.querySelector('#idDispositivo').value;
  var idSite = document.querySelector('#idSite').value;
  // var url = window.location.hostname;
  // var port = window.location.port;
  // var url ='/usuario/' + id_user + '/updatePassword';
  // var url =url + ':' + port + '/usuario/' + id_user + '/updatePassword';
  var url = '/atualizarInventario';
  // console.log('Id user: ', id_user, url);
  // console.log("URL nova: "+ url);

  var form = document.createElement('form');
  form.action = url;
  form.method = 'POST';

  var input = document.createElement('input');
  input.type = 'hidden';
  input.name = 'idDispositivo';
  input.value = idDispositivo;
  form.appendChild(input);
  document.body.appendChild(form);

  var input1 = document.createElement('input');
  input1.type = 'hidden';
  input1.name = 'idSite';
  input1.value = idSite;
  form.appendChild(input1);
  document.body.appendChild(form);

  form.submit();
}

function moverEstoque(){
  var idDispositivo = document.querySelector('#idDispositivo').value;
  var idSite = document.querySelector('#idSite').value;

  var url = '/moverEstoque';

  var form = document.createElement('form');
  form.action = url;
  form.method = 'POST';

  var input = document.createElement('input');
  input.type = 'hidden';
  input.name = 'idDispositivo';
  input.value = idDispositivo;
  form.appendChild(input);
  document.body.appendChild(form);

  var input1 = document.createElement('input');
  input1.type = 'hidden';
  input1.name = 'idSite';
  input1.value = idSite;
  form.appendChild(input1);
  document.body.appendChild(form);

  form.submit();
}

function moverDescarte(){
  var idDispositivo = document.querySelector('#idDispositivo').value;
  var idSite = document.querySelector('#idSite').value;

  var url = '/inventarioMoverDescarte';

  var form = document.createElement('form');
  form.action = url;
  form.method = 'POST';

  var input = document.createElement('input');
  input.type = 'hidden';
  input.name = 'idDispositivo';
  input.value = idDispositivo;
  form.appendChild(input);
  document.body.appendChild(form);

  var input1 = document.createElement('input');
  input1.type = 'hidden';
  input1.name = 'idSite';
  input1.value = idSite;
  form.appendChild(input1);
  document.body.appendChild(form);

  form.submit();
}

function mudarLayout() {
  var idDispositivo = document.querySelector('#idDispositivo').value;
  var idSite = document.querySelector('#idSite').value;


  var url = '/mudancaDeLayout';

  var form = document.createElement('form');
  form.action = url;
  form.method = 'POST';

  var input = document.createElement('input');
  input.type = 'hidden';
  input.name = 'idDispositivo';
  input.value = idDispositivo;
  form.appendChild(input);
  document.body.appendChild(form);

  var input1 = document.createElement('input');
  input1.type = 'hidden';
  input1.name = 'idSite';
  input1.value = idSite;
  form.appendChild(input1);
  document.body.appendChild(form);

  form.submit();
}

// =============Funções para Estoque=======================

function updateEstoque(idEstoque, idSite) {
  document.querySelector('#idEstoque').value = idEstoque;
  document.querySelector('#idSite').value = idSite;
}

function editarDadosEquipamentoEstoque() {
  var idEstoque = document.querySelector('#idEstoque').value;
  var idSite = document.querySelector('#idSite').value;
  let url = '/updateEstoque';

  var form = document.createElement('form');
  form.action = url;
  form.method = 'POST';

  var input = document.createElement('input');
  input.type = 'hidden';
  input.name = 'idEstoque';
  input.value = idEstoque;
  form.appendChild(input);
  document.body.appendChild(form);

  var input1 = document.createElement('input');
  input1.type = 'hidden';
  input1.name = 'idSite';
  input1.value = idSite;
  form.appendChild(input1);
  document.body.appendChild(form);

  form.submit();
}

function deleteEquipamentoEstoque() {
  var idEstoque = document.querySelector('#idEstoque').value;
  var idSite = document.querySelector('#idSite').value;
  let url = '/deleteEstoque';

  var form = document.createElement('form');
  form.action = url;
  form.method = 'POST';

  var input = document.createElement('input');
  input.type = 'hidden';
  input.name = 'idEstoque';
  input.value = idEstoque;
  form.appendChild(input);
  document.body.appendChild(form);

  var input1 = document.createElement('input');
  input1.type = 'hidden';
  input1.name = 'idSite';
  input1.value = idSite;
  form.appendChild(input1);

  document.body.appendChild(form);
  form.submit();
}

function estoqueMudarLocal() {
  var idEstoque = document.querySelector('#idEstoque').value;
  var idSite = document.querySelector('#idSite').value;
  let url = '/mudarLocal';

  var form = document.createElement('form');
  form.action = url;
  form.method = 'POST';

  var input = document.createElement('input');
  input.type = 'hidden';
  input.name = 'idEstoque';
  input.value = idEstoque;
  form.appendChild(input);
  document.body.appendChild(form);

  var input1 = document.createElement('input');
  input1.type = 'hidden';
  input1.name = 'idSite';
  input1.value = idSite;
  form.appendChild(input1);

  document.body.appendChild(form);
  form.submit();
}
