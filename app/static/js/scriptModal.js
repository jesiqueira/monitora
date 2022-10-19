function excluirSite(id_site){
  document.querySelector('#id_site').value = id_site;
}

function excluirLocal(id_local){
  document.querySelector('#id_local').value = id_local;
}

function editarUser(id_user){
  document.querySelector('#id_user').value = id_user;
}


function updateURLUser(){
  
  var id_user = document.querySelector('#id_user').value;
  // var url = window.location.hostname;
  var url ='/usuario/' + id_user + '/update';
  // console.log('Id user: ', id_user, url);
  // console.log("URL nova: "+ url);
  return url;
}

function trocarSenhaURLUser(){
  
  var id_user = document.querySelector('#id_user').value;
  // var url = window.location.hostname;
  // var port = window.location.port;
  // var url ='/usuario/' + id_user + '/updatePassword';
  // var url =url + ':' + port + '/usuario/' + id_user + '/updatePassword';
  var url ='/atualizarSenha';
  // console.log('Id user: ', id_user, url);
  // console.log("URL nova: "+ url);

  var form = document.createElement('form');
  form.action=url;
  form.method='POST';

  var input = document.createElement('input');
  input.type = 'hidden';
  input.name = 'id_users';
  input.value = id_user;
  form.appendChild(input);
  document.body.appendChild(form);
  form.submit();
}

// =========== Funções para página inventário================

function editarInventario(id_inventario){
  document.querySelector('#id_inventario').value = id_inventario;
}

function ediatarDadosEquipamentoInventario(){
  
  var id_inventario = document.querySelector('#id_inventario').value;
  // var url = window.location.hostname;
  // var port = window.location.port;
  // var url ='/usuario/' + id_user + '/updatePassword';
  // var url =url + ':' + port + '/usuario/' + id_user + '/updatePassword';
  var url ='/atualizarInventario';
  // console.log('Id user: ', id_user, url);
  // console.log("URL nova: "+ url);

  var form = document.createElement('form');
  form.action=url;
  form.method='POST';

  var input = document.createElement('input');
  input.type = 'hidden';
  input.name = 'id_inventario';
  input.value = id_inventario;
  form.appendChild(input);
  document.body.appendChild(form);
  form.submit();
}


// =============Funções para Estoque=======================

function updateEstoque(idEstoque, idSite){
  document.querySelector('#idEstoque').value = idEstoque;
  document.querySelector('#idSite').value = idSite;
}

function ediatarDadosEquipamentoEstoque(){
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

  document.body.appendChild(form)
  form.submit();
}
