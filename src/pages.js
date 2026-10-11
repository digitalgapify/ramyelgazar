
/* sub-page splash: remove when finished, or on click/Escape */
(function(){
  var el=document.getElementById('psplash'); if(!el) return;
  var root=document.documentElement;
  function done(){ root.classList.remove('psp'); if(el.parentNode) el.parentNode.removeChild(el); }
  if(!root.classList.contains('psp')){ done(); return; }
  el.addEventListener('animationend',function(e){ if(e.target===el) done(); });
  document.addEventListener('keydown',function(e){ if(e.key==='Escape') done(); });
  setTimeout(done,2600);
})();
