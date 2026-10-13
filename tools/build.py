"""Assemble the site from src/ into static pages. Run from the repo root: python3 tools/build.py"""
import re,os,html
R=lambda p:open(p).read()
SEC=lambda k:R(f'src/sections/{k}.html')
head_t=R('src/head.html'); jsonld=R('src/jsonld.html'); body_top=R('src/body_top.html'); footer=R('src/footer.html')
css=R('src/style.css'); app=R('src/app.js'); extra_css=R('src/pages.css'); extra_js=R('src/pages.js'); boot=R('src/home_splash_boot.js'); hsplash=R('src/home_splash.js')
press=SEC('press')
# the ticker block: from '<div class="press-ticker">' to its end (before the coverage heading)
a=press.index('<div class="press-ticker">'); b=press.index('<h3 class="pcov-title">')
ticker_html=press[a:b].rstrip()+'\n'
PAGES={
 'home':dict(url='/',path='index.html',title='Ramy Elgazar | Four Time US Sumo Open Champion',
   desc='Egyptian sumo wrestler Ramy Elgazar: first Arab to win the US Sumo Open heavyweight title. Referee, performer, chef. 1,900 live shows, 1.5B views.',
   secs=['hero','stats','streak','record','abudhabi','HOME_EXPLORE','HOME_PRESS','faq','CONTACT_TEASER']),
 'about':dict(url='/about/',path='about/index.html',title='About Ramy Elgazar | Story, Career and Audience',
   desc='The story of Ramy Elgazar: born in El Mahalla El Kubra, four time US Sumo Open champion, ISF referee, chef and creator with 1.4 million followers.',
   h1='The story',eyebrow='About',lead='From a wrestling club in El Mahalla El Kubra to the largest sumo stages in the world, and a kitchen in Los Angeles.',
   splash='ABOUT',dir='right',secs=['who','standing','road','quote_about','kitchen','audience','arabic','PAGE_CTA']),
 'shows':dict(url='/shows/',path='shows/index.html',title='Shows, Film and Collaborations | Ramy Elgazar',
   desc='Live shows, film and television, and creator collaborations with Ramy Elgazar: Sumo and Sushi, MrBeast, Nick DiGiovanni, Hail Mary and more.',
   h1='Shows & screen',eyebrow='Stage and screen',lead='1,900 live shows, feature films, television and 32 creator collaborations.',
   splash='SHOWS',dir='up',secs=['shows','screen','film','partners','PAGE_CTA']),
 'contact':dict(url='/contact/',path='contact/index.html',title='Contact Ramy Elgazar | Collaborations, Bookings and Media',
   desc='Contact Ramy Elgazar\'s team for brand partnerships, live shows, film and television, appearances and press. WhatsApp for the USA, Egypt, GCC and Saudi Arabia.',
   h1='Contact',eyebrow='Work with Ramy',lead='Brand partnerships, appearances, hosting and media enquiries. Message his team on WhatsApp and choose your region: USA, Egypt, GCC or Saudi Arabia.',
   splash='CONTACT',dir='down',secs=['contact']),
 'press':dict(url='/press/',path='press/index.html',title='Press Coverage of Ramy Elgazar | 22 Stories and Links',
   desc='Press coverage of Ramy Elgazar from Los Angeles Times, Ahram Online, CairoScene, Calgary Herald, CityNews and more, with links to every story.',
   h1='Press & coverage',eyebrow='Coverage',lead='Every story, newest first, with links to the original. Filter by year or by where it was published.',
   splash='PRESS',dir='left',secs=['press','links','PAGE_CTA']),
}
ID2PAGE={}
SECIDS={'hero':'intro','stats':None,'streak':None,'record':'record','abudhabi':'abudhabi','faq':'faq','contact':'contact','who':'who','standing':'standing','road':'road','kitchen':'kitchen','audience':'audience','arabic':'arabic','shows':'shows','screen':'screen','partners':'partners','press':'press','links':'links'}
for pg,c in PAGES.items():
    for s in c['secs']:
        i=SECIDS.get(s)
        if i: ID2PAGE[i]=pg
ID2PAGE['film']=None
def rewrite(h,cur):
    def hf(m):
        i=m.group(1)
        pg=ID2PAGE.get(i)
        if pg is None or pg==cur: return m.group(0)
        return 'href="'+PAGES[pg]['url']+('' if i in ('press','shows','contact') else '#'+i)+'"'
    h=re.sub(r'href="#([A-Za-z0-9_-]+)"',hf,h)
    h=re.sub(r'(src|srcset|poster|data-src)="(?!https?:|/|#|mailto:|tel:|data:)([^"]+)"',lambda m:f'{m.group(1)}="/{m.group(2)}"',h)
    h=re.sub(r"url\((?!['\"]?(?:https?:|/|#|data:))(['\"]?)([^)'\"]+)",lambda m:f"url({m.group(1)}/{m.group(2)}",h)
    return h
from PIL import Image as _Im
_dim={}
def add_dims(h):
    def f(m):
        tag=m.group(0)
        if 'width=' in tag: return tag
        src=re.search(r'src="/([^"?#]+)"',tag)
        if not src: return tag
        fp=src.group(1)
        if fp not in _dim:
            try:
                with _Im.open(fp) as im: _dim[fp]=im.size
            except Exception: _dim[fp]=None
        d=_dim[fp]
        if not d: return tag
        return tag.replace('<img ',f'<img width="{d[0]}" height="{d[1]}" ',1)
    return re.sub(r'<img\b[^>]*>',f,h)
def nav(cur):
    items=[('home','/','Home'),('about','/about/','About'),('shows','/shows/','Shows &amp; Screen'),('press','/press/','Press')]
    a=''.join(f'<a href="{u}"'+(' class="on" aria-current="page"' if k==cur else '')+f'>{t}</a>' for k,u,t in items)
    a+='<a href="/contact/"'+(' class="on" aria-current="page"' if cur=='contact' else '')+'>Contact</a>'
    return f'<nav id="tabs" aria-label="Main">\n  <div class="tabs-scroll">\n    {a}\n  </div>\n</nav>'
def explore():
    cards=[('about','/about/','About','The story, the career and the audience','who-portrait.webp','Ramy Elgazar portrait'),
     ('shows','/shows/','Shows & screen','Live shows, film, television and collaborations','img/ramy-elgazar-arena-staging-sumo-and-sushi.jpg','Ramy Elgazar in the ring at a Sumo and Sushi arena show'),
     ('press','/press/','Press & coverage','22 stories, with links to the original','img/ramy-elgazar-film-premiere-screening.jpg','Ramy Elgazar at a film premiere screening')]
    c=''.join(f'<a class="xcard" href="{u}"><span class="xph"><img src="/{img}" alt="{html.escape(alt)}" loading="lazy"></span><span class="xt">{html.escape(t).replace("&amp;","&amp;")}</span><span class="xs">{s}</span><span class="xgo">Open <i aria-hidden="true">&#8594;</i></span></a>' for k,u,t,s,img,alt in cards)
    return f'<section id="explore"><div class="wrap"><div class="eyebrow">Explore</div><h2 class="sec">More about<br><span class="o">Ramy</span></h2><div class="xgrid">{c}</div></div></section>\n'
def home_press():
    return f'<section id="press-teaser"><div class="wrap"><div class="eyebrow">Coverage</div><h2 class="sec">In the press</h2>\n{ticker_html}<p class="foot-link"><a class="btn btn-primary" href="/press/">All press coverage <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6" stroke-linecap="round" stroke-linejoin="round"/></svg></a></p></div></section>\n'
def page_cta():
    return '<section class="pcta"><div class="wrap"><div class="eyebrow">Work with Ramy</div><h2 class="sec">Let\'s make<br><span class="o">something big</span></h2><p class="lead">Brand campaigns, live shows, film and television, appearances.</p><p><a class="btn btn-primary" href="/contact/">Collaborate with Ramy <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6" stroke-linecap="round" stroke-linejoin="round"/></svg></a></p></div></section>\n'
def quote_about():
    q=SEC('quote'); return q.replace('Next: Abu Dhabi, 2026','Next: Shows &amp; screen').replace('href="#abudhabi"','href="/shows/"')
def contact_teaser():
    return '<section id="contact-teaser" class="pcta"><div class="wrap"><div class="eyebrow">Work with Ramy</div><h2 class="sec">To collaborate<br><span class="o">with Ramy</span></h2><p class="lead">Brand partnerships, appearances, hosting and media enquiries. His team answers on WhatsApp for the USA, Egypt, GCC and Saudi Arabia.</p><p><a class="btn btn-primary" href="/contact/">Contact Ramy\'s team <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6" stroke-linecap="round" stroke-linejoin="round"/></svg></a></p></div></section>\n'
def crumbs(c):
    return f'<nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">/</span><span aria-current="page">{c["h1"].replace("&","&amp;") if "&amp;" not in c["h1"] else c["h1"]}</span></nav>'
def phero(c):
    return f'<header class="phero"><div class="wrap">{crumbs(c)}<div class="eyebrow">{c["eyebrow"]}</div><h1 class="display">{c["h1"]}</h1><p class="lead">{c["lead"]}</p></div></header>\n'
def head(pg,c):
    h=head_t
    t=c['title'];d=c['desc'];u='https://ramyelgazar.com'+c['url']
    h=re.sub(r'<title>.*?</title>',f'<title>{html.escape(t)}</title>',h,flags=re.S)
    h=re.sub(r'(<meta name="description" content=")[^"]*',r'\g<1>'+d.replace('\\','\\\\'),h)
    h=re.sub(r'(<link rel="canonical" href=")[^"]*',r'\g<1>'+u,h)
    h=re.sub(r'(<meta property="og:url" content=")[^"]*',r'\g<1>'+u,h)
    h=re.sub(r'(<meta property="og:title" content=")[^"]*',r'\g<1>'+html.escape(t),h)
    h=re.sub(r'(<meta property="og:description" content=")[^"]*',r'\g<1>'+d,h)
    h=re.sub(r'(<meta name="twitter:title" content=")[^"]*',r'\g<1>'+html.escape(t),h)
    h=re.sub(r'(<meta name="twitter:description" content=")[^"]*',r'\g<1>'+d,h)
    h=h.replace('<meta name="theme-color"','<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">\n<meta property="og:locale" content="en_US">\n<meta name="theme-color"',1)
    if pg=='home': h+='\n<link rel="preload" as="image" href="/img/ramy-elgazar-sumo-ring-entrance.webp" type="image/webp" fetchpriority="high">'
    h+='\n<link rel="stylesheet" href="/site.css">\n'
    return h
import json
SITE='https://ramyelgazar.com'
def ld_sub(pg,c):
    url=SITE+c['url']
    crumbs=[{"@type":"ListItem","position":1,"name":"Home","item":SITE+"/"},{"@type":"ListItem","position":2,"name":c['h1'].replace('&amp;','&'),"item":url}]
    kind={'about':'AboutPage','shows':'CollectionPage','press':'CollectionPage','contact':'ContactPage'}[pg]
    node={"@type":kind,"@id":url+"#page","url":url,"name":c['title'],"description":c['desc'],"inLanguage":"en","isPartOf":{"@id":SITE+"/#website"},"about":{"@id":SITE+"/#ramy"},"breadcrumb":{"@id":url+"#crumbs"}}
    g=[node,{"@type":"BreadcrumbList","@id":url+"#crumbs","itemListElement":crumbs}]
    if pg=='press':
        h=SEC('press'); items=[]
        starts=[m.start() for m in re.finditer(r'<(?:a|div) class="pcov[ "]',h)]+[len(h)]
        for x,y in zip(starts,starts[1:]):
            blk=h[x:y]
            hu=re.search(r'href="(https?://[^"]+)"',blk).group(1)
            name=html.unescape(re.sub(r'<[^>]+>','',re.search(r'<strong class="pcov-h">(.*?)</strong>',blk,re.S).group(1)))
            items.append({"@type":"ListItem","position":len(items)+1,"url":hu,"name":name})
        node["mainEntity"]={"@type":"ItemList","name":"Press coverage of Ramy Elgazar","numberOfItems":len(items),"itemListElement":items}
    if pg=='contact':
        node["mainEntity"]={"@type":"Organization","name":"Ramy Elgazar, management and media","email":"Media@ramyelgazar.com","contactPoint":[
          {"@type":"ContactPoint","contactType":"bookings and collaborations","telephone":"+14245990027","areaServed":"US","availableLanguage":["English","Arabic"]},
          {"@type":"ContactPoint","contactType":"bookings and collaborations","telephone":"+971502561030","areaServed":["EG","AE","SA","QA","KW","BH","OM"],"availableLanguage":["English","Arabic"]}]}
    return '<script type="application/ld+json">\n'+json.dumps({"@context":"https://schema.org","@graph":g},ensure_ascii=False,indent=1)+'\n</script>\n'
def build():
    for pg,c in PAGES.items():
        h=head(pg,c)
        if pg=='home':
            h+=jsonld+'\n<script>\n(function(){try{var m={who:"/about/",standing:"/about/",road:"/about/",kitchen:"/about/",audience:"/about/",arabic:"/about/",shows:"/shows/",screen:"/shows/",partners:"/shows/",press:"/press/",links:"/press/"},k=location.hash.slice(1);if(m[k]){location.replace(m[k]+"#"+k)}}catch(e){}})();\n</script>\n<script>\n'+boot+'</script>\n'
        else:
            h+=ld_sub(pg,c)
            h+=f'<script>(function(){{try{{var k="sp:"+location.pathname;if(!(window.matchMedia&&matchMedia("(prefers-reduced-motion: reduce), (max-width: 768px)").matches)){{document.documentElement.classList.add("psp");setTimeout(function(){{document.documentElement.classList.remove("psp")}},2600)}}}}catch(e){{}}}})();</script>\n'
        h+='</head>\n<body>\n'
        bt=body_top
        bt=re.sub(r'<nav id="tabs".*?</nav>',lambda m:nav(pg),bt,flags=re.S)
        if pg!='home':
            bt=re.sub(r'<div id="splash".*?</div>\n',f'<div id="psplash" data-dir="{c["dir"]}" aria-hidden="true"><b>{c["splash"]}</b><i></i></div>\n',bt,flags=re.S)
        body=bt
        if pg!='home': body+=phero(c)
        for s in c['secs']:
            if s=='HOME_EXPLORE': body+=explore()
            elif s=='HOME_PRESS': body+=home_press()
            elif s=='PAGE_CTA': body+=page_cta()
            elif s=='CONTACT_TEASER': body+=contact_teaser()
            elif s=='quote_about': body+=quote_about()
            elif s=='contact' and pg=='contact':
                t=SEC('contact'); t=re.sub(r'    <div class="eyebrow">Work with Ramy</div>\n    <h2 class="sec">.*?</h2>\n    <p class="lead">.*?</p>\n','',t,flags=re.S); body+=t+'\n'
            else: body+=SEC(s)+'\n'
        body+='\n</main>\n'+footer.replace('<footer>','<footer>\n  <div class="wrap"><nav class="foot-nav" aria-label="Footer"><a href="/">Home</a><a href="/about/">About</a><a href="/shows/">Shows &amp; screen</a><a href="/press/">Press</a><a href="/contact/">Contact</a></nav></div>',1)
        js=app+'\n'+extra_js
        if pg=='home': js+='\n'+hsplash
        bodyr=rewrite(body,pg)
        if pg=='contact': bodyr=bodyr.replace('<h3','<h2').replace('</h3>','</h2>')
        out=h+add_dims(bodyr)+'\n<script src="/site.js" defer></script>\n</body>\n</html>\n'
        os.makedirs(os.path.dirname(c['path']) or '.',exist_ok=True)
        open(c['path'],'w').write(out)
        print(pg,len(out))
    open('site.css','w').write(rewrite(css,'x')+'\n'+extra_css)
    open('site.js','w').write(js_all())
def js_all():
    # one shared script; the home splash only runs where #spSvg exists (it bails out otherwise)
    return app+'\n'+extra_js+'\n'+hsplash

def sitemap():
    import subprocess
    old=subprocess.run(['git','show','HEAD:sitemap.xml'],capture_output=True,text=True).stdout if not os.path.exists('src/image_titles.txt') else ''
    if old:
        t=dict(re.findall(r'<image:loc>https://ramyelgazar.com/([^<]+)</image:loc><image:title>([^<]*)</image:title>',old))
        open('src/image_titles.txt','w').write('\n'.join(f'{k}\t{v}' for k,v in t.items()))
    t=dict(l.split('\t',1) for l in open('src/image_titles.txt').read().split('\n') if l)
    out=['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']
    for pg,c in PAGES.items():
        h=open(c['path']).read()
        imgs=[]
        if pg=='home': imgs.append('og.jpg')
        for m in re.findall(r'(?:src|srcset)="/(img/[^"]+?\.jpg|[a-z-]+\.jpg)"',h):
            if m in t and m not in imgs: imgs.append(m)
        out+=['  <url>',f'    <loc>https://ramyelgazar.com{c["url"]}</loc>','    <lastmod>2026-10-11</lastmod>','    <changefreq>monthly</changefreq>',f'    <priority>{1.0 if pg=="home" else 0.8}</priority>']
        for i in imgs:
            out.append(f'    <image:image><image:loc>https://ramyelgazar.com/{i}</image:loc><image:title>{t.get(i,"Ramy Elgazar")}</image:title></image:image>')
        out.append('  </url>')
    out.append('</urlset>');open('sitemap.xml','w').write('\n'.join(out)+'\n')
build()
sitemap()
def notfound():
    c=dict(title='Page not found | Ramy Elgazar',desc='This page does not exist. Go back to the Ramy Elgazar homepage.',url='/404.html')
    h=head_t
    h=re.sub(r'<title>.*?</title>','<title>Page not found | Ramy Elgazar</title>',h,flags=re.S)
    h=re.sub(r'(<meta name="description" content=")[^"]*',r'\g<1>This page does not exist.',h)
    h=re.sub(r'<link rel="canonical"[^>]*>\n','',h); h=re.sub(r'<meta property="og:url"[^>]*>\n','',h)
    h=h.replace('<meta name="theme-color"','<meta name="robots" content="noindex">\n<meta name="theme-color"',1)
    h+='\n<link rel="stylesheet" href="/site.css">\n</head>\n<body>\n'
    b=re.sub(r'<div id="splash".*?</div>\n','',body_top,flags=re.S); b=re.sub(r'<nav id="tabs".*?</nav>',lambda m:nav('none'),b,flags=re.S)
    b+='<header class="phero"><div class="wrap"><div class="eyebrow">404</div><h1 class="display">Page not found</h1><p class="lead">That page does not exist. Try the homepage or one of the pages above.</p><p><a class="btn btn-primary" href="/">Back to home</a></p></div></header>\n</main>\n'
    open('404.html','w').write(h+b+'<script src="/site.js" defer></script>\n</body>\n</html>\n')
notfound()
import json as _j
open('vercel.json','w').write(_j.dumps({"trailingSlash":True,"headers":[
 {"source":"/(.*)","headers":[{"key":"X-Content-Type-Options","value":"nosniff"},{"key":"Referrer-Policy","value":"strict-origin-when-cross-origin"},{"key":"X-Frame-Options","value":"SAMEORIGIN"},{"key":"Permissions-Policy","value":"camera=(), microphone=(), geolocation=()"}]},
 {"source":"/img/(.*)","headers":[{"key":"Cache-Control","value":"public, max-age=604800, stale-while-revalidate=86400"}]},
 {"source":"/(site\\.css|site\\.js)","headers":[{"key":"Cache-Control","value":"public, max-age=3600, must-revalidate"}]}]},indent=1)+'\n')
