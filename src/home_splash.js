(function(){
  var root=document.documentElement;
  if(!root.classList.contains('splash')) return;
  var NS='http://www.w3.org/2000/svg';
  var sp=document.getElementById('splash'), svg=document.getElementById('spSvg'), g=document.getElementById('spG'),
      defs=document.getElementById('spDefs'), lay=document.getElementById('spLines'), h1=document.querySelector('.hero h1'), done=false, t;
  var EASE='cubic-bezier(.45,0,.2,1)';
  var SWEEP=[{start:.25,dur:1.9},{start:1.15,dur:2.5}];   // seconds: RAMY, then ELGAZAR (they overlap, so it flows)
  var GO=3900;                                           // ms until the name flies to the headline
  function finish(){
    if(done) return; done=true; clearTimeout(t);
    root.classList.remove('splash');
    try{sessionStorage.setItem('rg-splash','1')}catch(e){}
    if(sp&&sp.parentNode) sp.parentNode.removeChild(sp);
  }
  if(!sp||!svg||!g||!defs||!lay||!h1){ finish(); return; }
  sp.addEventListener('click',finish);
  document.addEventListener('keydown',function(e){ if(e.key==='Escape'||e.key==='Enter'||e.key===' ') finish(); });
  function el(n,a){ var e=document.createElementNS(NS,n); for(var k in a) e.setAttribute(k,a[k]); return e; }
  function measure(){
    var rg=document.createRange(); rg.selectNodeContents(h1);
    var rs=[].filter.call(rg.getClientRects(),function(r){return r.width>1&&r.height>1;});
    if(rs.length<2) return null;
    function baselineAt(before){
      var pr=document.createElement('span'); pr.style.cssText='display:inline-block;width:0;height:0;vertical-align:baseline';
      if(before) h1.insertBefore(pr,before); else h1.appendChild(pr);
      var y=pr.getBoundingClientRect().bottom; h1.removeChild(pr); return y;
    }
    return {x1:rs[0].left, y1:baselineAt(h1.querySelector('br')), x2:rs[rs.length-1].left, y2:baselineAt(null)};
  }
  function run(){
    if(done) return;
    h1.style.animation='none'; h1.style.opacity='1'; h1.style.transform='none';
    var cs=getComputedStyle(h1), fs=parseFloat(cs.fontSize), vw=innerWidth, vh=innerHeight;
    var m0=measure(); if(!m0){ finish(); return; }
    var words=['RAMY','ELGAZAR'], xs=[m0.x1,m0.x2], ys=[m0.y1,m0.y2], boxes=[], i;
    for(i=0;i<2;i++){
      var tx=el('text',{x:xs[i],y:ys[i],fill:'#f4f4f4','font-family':'Anton, Impact, sans-serif'});
      tx.style.fontSize=fs+'px'; tx.style.fontWeight=cs.fontWeight; tx.style.fontStyle=cs.fontStyle; tx.style.letterSpacing='-.01em';
      tx.textContent=words[i];
      var grp=el('g',{mask:'url(#spm'+i+')'}); grp.appendChild(tx); lay.appendChild(grp);
      var bb=tx.getBBox(); boxes.push(bb);
      // the reveal: a slanted edge sweeping left to right across the word
      var pad=fs*.1, slant=Math.tan(10*Math.PI/180), top=ys[i]-fs*1.4, hgt=fs*2, wdt=bb.width+pad*2+hgt*slant, x0=bb.x-pad;
      var sk='translate(0 '+ys[i]+') skewX(-10) translate(0 '+(-ys[i])+')';
      var mk=el('mask',{id:'spm'+i,maskUnits:'userSpaceOnUse',x:-3000,y:-3000,width:9000,height:9000});
      var mg=el('g',{transform:sk}), rect=el('rect',{x:x0,y:top,width:wdt,height:hgt,fill:'#fff'});
      mg.appendChild(rect); mk.appendChild(mg); defs.appendChild(mk);
      // a thin orange edge rides the front of the sweep
      var lg=el('g',{transform:sk}), edge=el('rect',{x:x0+wdt-fs*.045,y:ys[i]-fs*.98,width:fs*.045,height:fs*1.12,fill:'#FF4D00'});
      lg.appendChild(edge); g.appendChild(lg);
      var o={duration:SWEEP[i].dur*1000,delay:SWEEP[i].start*1000,fill:'both',easing:EASE}, from='translateX('+(-wdt)+'px)', to='translateX(0px)';
      rect.style.transform=from; edge.style.transform=from;
      rect.animate([{transform:from},{transform:to}],o);
      edge.animate([{transform:from},{transform:to}],o);
      var total=o.duration+300;
      edge.animate([{opacity:0,offset:0},{opacity:1,offset:.04},{opacity:1,offset:(o.duration-60)/total},{opacity:0,offset:1}],{duration:total,delay:o.delay,fill:'both',easing:'linear'});
    }
    var bbAll={x:Math.min(boxes[0].x,boxes[1].x), y:boxes[0].y, width:Math.max(boxes[0].width,boxes[1].width), height:boxes[1].y+boxes[1].height-boxes[0].y};
    var S=Math.min(3,(vw*.88)/bbAll.width,(vh*.6)/bbAll.height), cx=bbAll.x+bbAll.width/2, cy=bbAll.y+bbAll.height/2;
    g.style.transform='translate('+(vw/2-S*cx)+'px,'+(vh/2-S*cy)+'px) scale('+S+')';
    sp.classList.add('play');
    t=setTimeout(function(){
      var m1=measure()||m0;   // the headline may have moved slightly since (late fonts): aim at where it is now
      sp.classList.add('go','out');
      g.style.transform='translate('+(m1.x1-m0.x1)+'px,'+(m1.y1-m0.y1)+'px) scale(1)';
      t=setTimeout(finish,1150);
    },GO);
  }
  var fonts=(document.fonts&&document.fonts.ready)?Promise.race([document.fonts.ready,new Promise(function(r){setTimeout(r,1200)})]):Promise.resolve();
  fonts.then(run);
})();
