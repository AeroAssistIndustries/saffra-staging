#!/usr/bin/env python3
"""Build real pages from the single-file site.  usage: build_pages.py BASE_URL OUT_DIR [public]"""
import sys,re,os,json,shutil,html
SRC=os.environ.get('SAFFRA_SRC','/home/claude/saffra')
BASE=sys.argv[1].rstrip('/')+'/'; OUT=sys.argv[2]; PUBLIC='public' in sys.argv[3:]; API='api/submit.php' if 'api' in sys.argv[3:] else ''
s=open(SRC+'/index.html').read()
views=json.loads(re.search(r"var views=(\[[^\]]*\])",s).group(1).replace("'",'"'))
P={ # view: (title, description)
'home':("Saffra | Daily Intimacy Gummies for Her and for Him","Saffra makes daily intimacy gummies for her and for him. Seven ingredients, every dose on the label, and 10% of every sale helps survivors."),
'her':("Saffra for Her | Daily Intimacy Gummies for Women","Saffra for Her: saffron 30 mg, fenugreek 600 mg, L-theanine, B6, folate, B12 and D3 in two vegan gummies a day. Every dose shown."),
'him':("Saffra for Him | Daily Intimacy Gummies for Men","Saffra for Him: saffron 30 mg, fenugreek 600 mg, zinc, selenium, vitamin E, B12 and D3 in two vegan gummies a day. Every dose shown."),
'science':("The Science Behind Saffra | Ingredients, Doses and Studies","Every Saffra ingredient, the daily amount, and the human study behind it. Saffron, fenugreek, L-theanine, zinc, selenium and daily vitamins."),
'about':("Our Story | Saffra, Founded by a Couple","Saffra was founded by a couple who wanted an honest daily ritual for desire. Read why we started and what we believe."),
'quiz':("Find Your Formula | Saffra Quiz","Answer five quick questions to find the Saffra formula for you, your partner, or the two of you. Your answers stay on your device."),
'journal':("The Saffra Journal | Honest Reads on Desire and Rituals","Short, honest articles on desire, long relationships, daily rituals and how to read a supplement label."),
'play':("Games for Two | Free Couples Question Deck and Date Night Spinner","Free games for couples: a question deck in three levels, a date night spinner, Know me, This or that and a 30-day ritual tracker."),
'ask':("Questions, Answered | Ask the Saffra Team","Plain answers about Saffra gummies, safety, subscriptions and making time for each other. Ask us anything."),
'creators':("Creators | Work With Saffra","Partner with Saffra as a creator. Honest briefs, clear disclosure and products made to be shared by couples."),
'brand':("Saffra Brand Kit | Logo, Colors and Type","The Saffra brand kit: logo, color palette, typography, packaging and voice."),
'giving':("Giving Back | 10% of Every Saffra Sale Helps Survivors","Ten percent of every Saffra sale, not profit, goes to help survivors of sexual abuse and sex trafficking rebuild their lives."),
'rewards':("Saffra Circle Rewards | Earn Points, Give $10, Get $10","Earn a point for every dollar, get $5 back for every 100 points, and give $10, get $10 when you refer a couple."),
'app':("Saffra Together | A Private Daily Ritual App for Couples","A free, private app for two: daily check-ins, history, couples trivia, truth or dare and intimacy ideas for tonight."),
'members':("Members Only | The Saffra Inner Circle","What Saffra members get: the After Dark deck, monthly date nights, guided evenings, ask the doctors and member pricing."),
'download':("Get the Saffra Together App | iPhone and Android","Install the free Saffra Together couples app on iPhone or Android in under a minute."),
'privacy':("Privacy Policy | Saffra","How Saffra collects, uses and protects your information, and the choices you have."),
'terms':("Terms of Use | Saffra","The terms that apply when you use the Saffra website, app, rewards and subscriptions."),
'shipping':("Shipping, Returns and Subscriptions | Saffra","Free US shipping in a plain box, a 30-day money-back guarantee, and subscriptions you can skip or cancel anytime."),
'accessibility':("Accessibility | Saffra","Saffra's commitment to an accessible website and how to reach us if something does not work for you."),
}
# articles: title and description from the page itself
for v in views:
    if v.startswith('read-'):
        i=s.index('<main id="v-%s">'%v); seg=s[i:s.index('</main>',i)]
        h=html.unescape(re.sub('<[^>]+>','',re.search(r'<h1[^>]*>(.*?)</h1>',seg,re.S).group(1))).strip()
        t=html.unescape(re.sub('<[^>]+>','',re.search(r'<div class="tldr"><b>[^<]*</b>(.*?)</div>',seg,re.S).group(1))).strip()
        P[v]=(h+" | Saffra Journal", t if len(t)<=160 else t[:157].rsplit(' ',1)[0]+'...')
missing=[v for v in views if v not in P]; assert not missing,missing
esc=lambda t:html.escape(t,quote=True)
T={v:P[v][0] for v in P}
s=re.sub(r'var T=\{"home"[^}]*\};document\.title=[^;]*;','var T='+json.dumps(T)+';document.title=T[v]||T.home;',s,count=1); assert '"home": "Saffra | Daily' in s
if PUBLIC: s=s.replace('<meta name="robots" content="noindex, nofollow">\n','').replace('<meta name="robots" content="noindex, nofollow">','')
s=s.replace('https://aeroassistindustries.github.io/saffra-staging/',BASE)
viewset=set(views)
def links(doc,prefix):
    return re.sub(r'href="#([a-z0-9-]+)"',lambda m:'href="%s%s/"'%(prefix,m.group(1)) if m.group(1) in viewset else m.group(0),doc)
def product(v):
    who='Her' if v=='her' else 'Him'
    return {"@context":"https://schema.org","@type":"Product","name":"Saffra for "+who,"description":P[v][1],"brand":{"@type":"Brand","name":"Saffra"},"image":BASE+"img/bottle-%s.webp"%v,"url":BASE+v+"/","offers":{"@type":"Offer","price":"36.00","priceCurrency":"USD","availability":"https://schema.org/PreOrder","url":BASE+v+"/"}}
def page(v):
    d=s; url=BASE+('' if v=='home' else v+'/'); t,desc=P[v]
    d=re.sub(r'<title>[^<]*</title>','<title>%s</title>'%esc(t),d,count=1)
    d=re.sub(r'<meta name="description" content="[^"]*">','<meta name="description" content="%s">\n<link rel="canonical" href="%s">'%(esc(desc),url),d,count=1)
    d=re.sub(r'<meta property="og:title" content="[^"]*">','<meta property="og:title" content="%s">'%esc(t),d)
    d=re.sub(r'<meta property="og:description" content="[^"]*">','<meta property="og:description" content="%s">'%esc(desc),d)
    d=re.sub(r'<meta property="og:url" content="[^"]*">','<meta property="og:url" content="%s">'%url,d)
    extra=[]
    if v in('her','him'): extra.append(product(v))
    if v.startswith('read-'): extra.append({"@context":"https://schema.org","@type":"Article","headline":t.replace(' | Saffra Journal',''),"description":desc,"author":{"@type":"Organization","name":"Saffra"},"publisher":{"@type":"Organization","name":"Saffra"},"mainEntityOfPage":url})
    if v!='home': extra.append({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Saffra","item":BASE},{"@type":"ListItem","position":2,"name":t.split(' | ')[0],"item":url}]})
    if extra: d=d.replace('</head>','<script type="application/ld+json">'+json.dumps(extra)+'</script>\n</head>',1)
    d=re.sub(r'<html([^>]*)>',lambda m:'<html%s data-pages%s>'%(m.group(1),' data-api="%s"'%API if API else ''),d,count=1)
    if v=='home': return links(d,'')
    d=links(d,'../')
    mid='brand' if v=='brand' else 'v-'+v
    i=d.index('<main id="%s"'%mid); j=d.index('</main>',i)+len('</main>'); blk=d[i:j]; d=d[:i]+d[j:]
    k=d.index('<main id="site"'); d=d[:k]+blk+'\n'+d[k:]
    d=re.sub(r'<html([^>]*)>',lambda m:'<html%s data-page="%s">'%(m.group(1),v),d,count=1)
    d=re.sub(r'<body([^>]*)>',lambda m:'<body%s data-view="%s">'%(re.sub(r'\s*data-view="[^"]*"','',m.group(1)),v),d,count=1)
    d=re.sub(r'''(["'(])(img|fonts)/''',r'\1../\2/',d)
    d=d.replace('href="manifest.webmanifest"','href="../manifest.webmanifest"').replace("register('sw.js')","register('../sw.js')")
    d=d.replace('<a class="logo" href="#top"','<a class="logo" href="../"')
    return d
os.makedirs(OUT,exist_ok=True)
open(OUT+'/index.html','w').write(page('home'))
for v in views:
    os.makedirs(OUT+'/'+v,exist_ok=True); open(OUT+'/'+v+'/index.html','w').write(page(v))
for f in ('404.html','manifest.webmanifest','sw.js'): shutil.copy(SRC+'/'+f,OUT+'/'+f)
for dname in ('img','fonts'):
    os.makedirs(OUT+'/'+dname,exist_ok=True)
    for f in os.listdir(SRC+'/'+dname): shutil.copy(SRC+'/'+dname+'/'+f,OUT+'/'+dname+'/'+f)
urls=[BASE]+[BASE+v+'/' for v in views if v not in('brand',)]
open(OUT+'/sitemap.xml','w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join('  <url><loc>%s</loc></url>\n'%u for u in urls)+'</urlset>\n')
open(OUT+'/robots.txt','w').write('User-agent: *\nAllow: /\n\nSitemap: %ssitemap.xml\n'%BASE)
if API:
    os.makedirs(OUT+'/api',exist_ok=True)
    php=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'submit.php')).read() if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)),'submit.php')) else open('/home/claude/build/live-api/submit.php').read()
    dom=re.sub(r'^https?://(www\.)?','',BASE).strip('/').split('/')[0]
    open(OUT+'/api/submit.php','w').write(php.replace('__DOMAIN__',dom).replace('__NOTIFY_EMAIL__',os.environ.get('SAFFRA_NOTIFY','__NOTIFY_EMAIL__')))
print('built',1+len(views),'pages ->',OUT,'public' if PUBLIC else 'hidden (noindex)')
