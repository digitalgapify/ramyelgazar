
(function(){
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var bar = document.getElementById('prog');
  function prog(){
    var h = document.documentElement.scrollHeight - window.innerHeight;
    bar.style.width = (h>0 ? (window.scrollY/h)*100 : 0) + '%';
  }
  window.addEventListener('scroll', prog, {passive:true}); prog();

  var strip = document.getElementById('strip');
  if(strip){
    var down=false, sx=0, sl=0;
    strip.addEventListener('mousedown', function(e){ down=true; strip.classList.add('drag'); sx=e.pageX; sl=strip.scrollLeft; });
    window.addEventListener('mouseup', function(){ down=false; strip.classList.remove('drag'); });
    strip.addEventListener('mousemove', function(e){ if(!down) return; e.preventDefault(); strip.scrollLeft = sl - (e.pageX - sx)*1.3; });
  }

  var himg = document.querySelector('.himg');
  if(himg) requestAnimationFrame(function(){ himg.classList.add('go'); });

  if(reduce) return;

  var sel = '.stats, .stat, .panel, .card, .tile, .tbl, h2.sec, p.lead, .eyebrow, .rstop, .rtimeline, .split > div';
  var items = [].slice.call(document.querySelectorAll(sel));
  items.forEach(function(el){ if(!el.classList.contains('stat') && !el.classList.contains('panel') && !el.classList.contains('rstop') && !el.classList.contains('rtimeline')) el.classList.add('rv'); });

  function animateNum(el){
    var raw = el.textContent.trim();
    var m = raw.match(/^([0-9][0-9.,]*)(.*)$/);
    if(!m) return;
    var target = parseFloat(m[1].replace(/,/g,''));
    var suffix = m[2];
    var dec = (m[1].indexOf('.') > -1) ? 1 : 0;
    var grouped = m[1].indexOf(',') > -1;
    var t0 = null, dur = 1100;
    function fmt(v){
      var out = dec ? v.toFixed(1) : Math.round(v).toString();
      if(grouped) out = Math.round(v).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
      return out + suffix;
    }
    function step(ts){
      if(!t0) t0 = ts;
      var p = Math.min((ts-t0)/dur, 1);
      var e = 1 - Math.pow(1-p, 3);
      el.textContent = fmt(target*e);
      if(p<1) requestAnimationFrame(step);
    }
    el.textContent = fmt(0);
    requestAnimationFrame(step);
  }

  var io = new IntersectionObserver(function(entries){
    entries.forEach(function(en){
      if(!en.isIntersecting) return;
      var el = en.target;
      el.classList.add('in');
      if(el.classList.contains('rtimeline')) el.classList.add('go');
      var n = el.querySelector(':scope > .n');
      if(n && !n.dataset.done){ n.dataset.done = '1'; animateNum(n); }
      io.unobserve(el);
    });
  }, {threshold:0.15, rootMargin:'0px 0px -8% 0px'});

  items.forEach(function(el, i){
    if(el.classList.contains('rv')) el.style.transitionDelay = (Math.min(i%6,5)*45)+'ms';
    io.observe(el);
  });
})();


(function(){
  var cta = document.getElementById("stickyCta");
  var contactEl = document.getElementById("contact");
  if(!cta) return;
  var menu = document.getElementById("ctaMenu");
  function closeMenu(){
    if(!menu || menu.hidden) return;
    menu.hidden = true; cta.setAttribute("aria-expanded","false");
  }
  if(menu){
    cta.addEventListener("click", function(e){
      e.preventDefault();
      var open = menu.hidden;
      menu.hidden = !open; cta.setAttribute("aria-expanded", open ? "true" : "false");
      if(open){ var f = menu.querySelector("a"); if(f) f.focus(); }
    });
    document.addEventListener("click", function(e){
      if(!menu.hidden && !menu.contains(e.target) && !cta.contains(e.target)) closeMenu();
    });
    document.addEventListener("keydown", function(e){
      if(e.key === "Escape" && !menu.hidden){ closeMenu(); cta.focus(); }
    });
    menu.addEventListener("click", function(){ closeMenu(); });
  }
  function upd(){
    var pastHero = window.scrollY > window.innerHeight*0.7;
    var nearContact = false;
    if(contactEl){
      var r = contactEl.getBoundingClientRect();
      nearContact = r.top < window.innerHeight*0.85;
    }
    var on = pastHero && !nearContact;
    cta.classList.toggle("show", on);
    if(!on) closeMenu();
  }
  window.addEventListener("scroll", upd, {passive:true});
  window.addEventListener("resize", upd);
  upd();
})();

(function(){
  var lb=document.createElement('div'); lb.className='lb'; lb.setAttribute('role','dialog'); lb.setAttribute('aria-modal','true'); lb.setAttribute('aria-label','Image preview');
  lb.innerHTML='<button type="button" aria-label="Close image">&times;</button><img alt="">';
  document.body.appendChild(lb);
  var im=lb.querySelector('img'), x=lb.querySelector('button'), last=null;
  function close(){ lb.classList.remove('open'); if(last) last.focus(); }
  document.addEventListener('click',function(e){
    var t=e.target.closest('.rimg img,.tile img,.panel .ph img');
    if(t){ last=t; im.src=t.currentSrc||t.src; im.alt=t.alt; lb.classList.add('open'); x.focus(); return; }
    if(lb.classList.contains('open')) close();
  });
  document.addEventListener('keydown',function(e){ if(e.key==='Escape'&&lb.classList.contains('open')) close(); });

  var f=document.getElementById('cform'); if(!f) return;
  var note=document.getElementById('cfNote');
  var NUM={'USA':'14245990027'}, DEF='971502561030';
  function msg(){
    var d=new FormData(f), r=d.get('region');
    return {region:r, text:'Hi Ramy\'s team, I\'d like to collaborate with Ramy.\nName: '+d.get('name')+(d.get('org')?'\nCompany: '+d.get('org'):'')+'\nRegion: '+r+'\nType: '+d.get('type')+'\n\n'+d.get('msg')};
  }
  function ok(){
    var good=true;
    [].forEach.call(f.querySelectorAll('[required]'),function(el){ var bad=!el.value.trim(); el.classList.toggle('invalid',bad); if(bad) good=false; });
    note.textContent=good?'':'Please add your name and a short message.';
    return good;
  }
  f.addEventListener('submit',function(e){
    e.preventDefault(); if(!ok()) return;
    var m=msg(); window.open('https://wa.me/'+(NUM[m.region]||DEF)+'?text='+encodeURIComponent(m.text),'_blank','noopener');
    note.textContent='Opening WhatsApp with your message ready to send.';
  });
  document.getElementById('cfMail').addEventListener('click',function(){
    if(!ok()) return; var m=msg();
    location.href='mailto:Media@ramyelgazar.com?subject='+encodeURIComponent('Collaboration enquiry: '+m.region)+'&body='+encodeURIComponent(m.text);
  });
})();

(function(){
  var CH='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m6 9 6 6 6-6" stroke-linecap="round" stroke-linejoin="round"/></svg>';
  var open=null;
  function closeAll(except){
    [].forEach.call(document.querySelectorAll('.csel-btn[aria-expanded="true"],.pop-btn[aria-expanded="true"]'),function(b){
      if(b===except) return; b.setAttribute('aria-expanded','false'); b.nextElementSibling.hidden=true; });
  }
  function items(list){ return [].slice.call(list.querySelectorAll('li,a')); }
  function toggle(btn,list,force){
    var o=force===undefined?list.hidden:force; closeAll(o?btn:null);
    list.hidden=!o; btn.setAttribute('aria-expanded',o?'true':'false');
    if(o){ var it=items(list); var cur=list.querySelector('[aria-selected="true"]')||it[0]; if(cur) cur.focus(); }
  }
  function keys(btn,list){
    btn.addEventListener('keydown',function(e){ if(e.key==='ArrowDown'||e.key==='ArrowUp'){ e.preventDefault(); toggle(btn,list,true); } });
    list.addEventListener('keydown',function(e){
      var it=items(list), i=it.indexOf(document.activeElement);
      if(e.key==='ArrowDown'){ e.preventDefault(); it[(i+1)%it.length].focus(); }
      else if(e.key==='ArrowUp'){ e.preventDefault(); it[(i-1+it.length)%it.length].focus(); }
      else if(e.key==='Home'){ e.preventDefault(); it[0].focus(); }
      else if(e.key==='End'){ e.preventDefault(); it[it.length-1].focus(); }
      else if(e.key==='Escape'){ e.preventDefault(); toggle(btn,list,false); btn.focus(); }
      else if(e.key==='Tab'){ toggle(btn,list,false); }
      else if((e.key==='Enter'||e.key===' ')&&list.classList.contains('csel-list')){ e.preventDefault(); document.activeElement.click(); }
    });
  }
  [].forEach.call(document.querySelectorAll('.cform select'),function(sel){
    var wrap=document.createElement('div'); wrap.className='csel';
    var btn=document.createElement('button'); btn.type='button'; btn.className='csel-btn'; btn.setAttribute('aria-haspopup','listbox'); btn.setAttribute('aria-expanded','false');
    var lab=document.createElement('span'); btn.appendChild(lab); btn.insertAdjacentHTML('beforeend',CH);
    var ul=document.createElement('ul'); ul.className='csel-list'; ul.setAttribute('role','listbox'); ul.hidden=true;
    [].forEach.call(sel.options,function(o){
      var li=document.createElement('li'); li.setAttribute('role','option'); li.tabIndex=-1; li.textContent=o.text; li.dataset.v=o.value;
      li.setAttribute('aria-selected',o.selected?'true':'false');
      li.addEventListener('click',function(){
        sel.value=li.dataset.v; lab.textContent=li.textContent;
        [].forEach.call(ul.children,function(c){ c.setAttribute('aria-selected',c===li?'true':'false'); });
        toggle(btn,ul,false); btn.focus();
      });
      ul.appendChild(li);
    });
    lab.textContent=sel.options[sel.selectedIndex].text;
    btn.addEventListener('click',function(){ toggle(btn,ul); });
    keys(btn,ul);
    wrap.appendChild(btn); wrap.appendChild(ul); sel.parentNode.insertBefore(wrap,sel);
  });
  [].forEach.call(document.querySelectorAll('.pop-btn'),function(btn){
    var list=btn.nextElementSibling; btn.addEventListener('click',function(){ toggle(btn,list); }); keys(btn,list);
    list.addEventListener('click',function(){ toggle(btn,list,false); });
  });
  document.addEventListener('click',function(e){ if(!e.target.closest('.csel,.pop-wrap')) closeAll(null); });
})();

(function(){var g=document.getElementById('pcovGrid');if(!g)return;var tg=document.getElementById('pcovToggle'),cnt=document.getElementById('pcovCount'),emp=document.getElementById('pcovEmpty'),sel={year:'',place:''};
var cards=[].slice.call(g.querySelectorAll('.pcov'));
function apply(){var any=sel.year||sel.place,n=0;g.classList.toggle('filtered',!!any);
cards.forEach(function(c){var ok=(!sel.year||c.dataset.year===sel.year)&&(!sel.place||c.dataset.place===sel.place);c.classList.toggle('hide',!ok);if(ok)n++;});
cnt.textContent=(any?n:cards.length)+(n===1&&any?' story':' stories');emp.hidden=!(any&&n===0);tg.parentNode.hidden=!!any;}
document.querySelectorAll('.pf').forEach(function(b){b.addEventListener('click',function(){var f=b.dataset.f;sel[f]=b.dataset.v;document.querySelectorAll('.pf[data-f="'+f+'"]').forEach(function(x){x.classList.toggle('on',x===b)});apply();});});
tg.addEventListener('click',function(){var o=g.classList.toggle('open');tg.setAttribute('aria-expanded',o);tg.textContent=o?'Show fewer':'Show all 22 stories';});})();
