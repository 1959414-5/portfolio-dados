(function(){
  var btn=document.querySelector('.menu-btn'),list=document.querySelector('nav ul');
  if(btn&&list){btn.addEventListener('click',function(){var o=list.classList.toggle('open');btn.setAttribute('aria-expanded',o)})}
  var filters=document.querySelectorAll('.filters button'),cards=document.querySelectorAll('[data-tipo]');
  filters.forEach(function(b){b.addEventListener('click',function(){
    filters.forEach(function(x){x.setAttribute('aria-pressed',x===b)});
    cards.forEach(function(c){c.hidden=!(b.dataset.filtro==='todos'||c.dataset.tipo===b.dataset.filtro)})})});
})();
