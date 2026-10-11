"""One-off: split the single-page index.html into src/ partials (run once, from the repo root)."""
import re,os
L=open('index.html').read().split('\n')
def seg(a,b): return '\n'.join(L[a-1:b])+'\n'   # 1-indexed inclusive
W=lambda p,t: open(p,'w').write(t)
S={'hero':(884,922),'stats':(924,936),'who':(938,952),'streak':(954,965),'standing':(967,991),'record':(993,1006),
'road':(1008,1126),'quote':(1128,1137),'abudhabi':(1139,1152),'shows':(1154,1188),'screen':(1190,1199),'film':(1201,1311),
'partners':(1313,1338),'kitchen':(1340,1371),'audience':(1373,1387),'arabic':(1389,1409),'press':(1411,1665),'links':(1667,1760),
'faq':(1762,1785),'contact':(1786,1836)}
for k,(a,b) in S.items(): W(f'src/sections/{k}.html',seg(a,b))
W('src/jsonld.html',seg(26,369))
W('src/style.css','\n'.join(L[376:856])+'\n')           # lines 377..856 (inside <style>)
W('src/footer.html',seg(1839,1856))
W('src/body_top.html',seg(860,883))
W('src/home_splash_boot.js','\n'.join(L[370:374])+'\n')  # lines 371..374 inner of boot script
# scripts
first='\n'.join(L[1858:1979])+'\n'   # inner of first script (1859..1979)
first=re.sub(r"\(function\(\)\{\n  var ids=\[.*?\n\}\)\(\);\n","",first,flags=re.S)  # drop old scroll-spy tabs
W('src/app.js',first+'\n'+'\n'.join(L[2054:2151])+'\n')  # lightbox..filters (2055..2151)
W('src/home_splash.js','\n'.join(L[1981:2053])+'\n')       # 1982..2053
print('ok')
