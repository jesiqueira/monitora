var local = document.querySelector('#local')

local.addEventListener('click', function () {
  if (local.value === 'Inventario'){
    var localPa = document.querySelector('.localPa');
    var button = document.querySelector('.button');
    localPa.classList.remove('hide')
    button.classList.remove('hide')
  }
 else if(local.value === 'Descarte'){
    var localPa = document.querySelector('.localPa');
    localPa.classList.add('hide');
  }
});