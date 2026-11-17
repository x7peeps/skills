#!/usr/bin/env python3
"""skills.x7peeps.com — 只展示真实可获取的产出。未上线的一律不渲染。"""
import json, html, pathlib

ROOT = pathlib.Path(__file__).parent
D = json.loads((ROOT / "data.json").read_text(encoding="utf-8"))
SK = D["skills"]
LIVE = [s for s in SK if s.get("status") == "live"]
CATS = [c for c in D["cats"] if c["id"] != "all"]

TOTAL = D["meta"]["totalSkills"]
BUILT = D["meta"]["built"]

def esc(s):
    return html.escape(s or "", quote=True)

# ---------- 已公开项目卡 ----------
def live_card(s, i):
    tag = "".join(f'<span class="chip chip--tag">{esc(t)}</span>' for t in s.get("tags", []))
    site = (f'<a class="chip chip--site" href="{esc(s["site"])}" target="_blank" rel="noopener">'
            f'<span class="dot"></span>主站</a>') if s.get("site") else ""
    return f'''<article class="card">
  <div class="card-top"><span class="card-idx">{str(i+1).zfill(2)}</span><span class="card-cat">OPEN SOURCE</span></div>
  <h3>{esc(s["name"])}</h3>
  <p class="card-en">{esc(s["en"])}</p>
  <p class="card-desc">{esc(s["desc"])}</p>
  <div class="chips">
    <a class="chip chip--gh" href="{esc(s["gh"])}" target="_blank" rel="noopener"><span class="dot"></span>GitHub 源码</a>
    {site}{tag}
  </div>
</article>'''

cards_html = "\n".join(live_card(s, i) for i, s in enumerate(LIVE))

# ---------- 能力域 ----------
dom_rows = "\n".join(
    f'''<li class="dom">
  <span class="dom-no">{c["no"]}</span>
  <span class="dom-name">{esc(c["name"])}</span>
  <span class="dom-note">{esc(c["note"])}</span>
</li>''' for c in CATS)

HTML = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light">
<title>技能库 · x7peeps</title>
<meta name="description" content="x7peeps 的技能与产出：已经开放源码的作品，以及九个能力域各自解决什么问题。未上线的技能不在这里列出。">
<meta name="theme-color" content="#F2EFE6">
<meta property="og:type" content="website">
<meta property="og:title" content="技能库 · x7peeps">
<meta property="og:description" content="已经能拿到的 {len(LIVE)} 个开源产出，和九个能力域。未上线的技能不列出。">
<meta property="og:url" content="https://x7peeps.com/skills/">
<meta property="og:image" content="https://x7peeps.com/skills/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://x7peeps.com/skills/og.png">
<link rel="canonical" href="https://x7peeps.com/skills/">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' fill='%2315150F'/%3E%3Ctext x='16' y='23' font-family='monospace' font-size='16' font-weight='700' fill='%23F2EFE6' text-anchor='middle'%3Ex7%3C/text%3E%3C/svg%3E">
<style>
:root{{
  color-scheme:light;
  --paper:#F2EFE6; --paper-2:#EBE7DA; --ink:#15150F; --ink-2:#3B3B32; --ink-3:#6B6A5C;
  --rule:#D3CDBC; --signal:#B93A1E; --wb:#1F5F8B;
  --fs-micro:10.5px; --fs-meta:11.5px; --fs-body:13.5px; --fs-lede:16px;
  --fs-card:19px; --fs-sec:22px;
  --mono:"SF Mono","JetBrains Mono","IBM Plex Mono",ui-monospace,Menlo,Consolas,monospace;
  --sans:"PingFang SC","Hiragino Sans GB","Source Han Sans SC","Noto Sans CJK SC","Microsoft YaHei",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
  --pad:clamp(20px,4vw,40px);
}}
*{{box-sizing:border-box}}
html{{scroll-behavior:smooth;scroll-padding-top:72px}}
body{{margin:0;background:var(--paper);color:var(--ink);font-family:var(--sans);
  font-size:var(--fs-body);line-height:1.6;-webkit-font-smoothing:antialiased;font-weight:400}}
a{{color:inherit;text-decoration:none}}
button{{font:inherit;color:inherit;background:none;border:0;cursor:pointer}}
:focus-visible{{outline:2px solid var(--signal);outline-offset:2px}}
.wrap{{max-width:1360px;margin:0 auto;padding:0 var(--pad)}}

.mast{{position:sticky;top:0;z-index:30;background:rgba(242,239,230,.74);
  backdrop-filter:blur(14px) saturate(1.05);border-bottom:1px solid var(--rule)}}
.mast-in{{max-width:1360px;margin:0 auto;padding:0 var(--pad);height:56px;display:flex;align-items:center;gap:24px}}
.brand{{display:flex;align-items:center;gap:7px;font-family:var(--mono);font-size:13.5px;
  letter-spacing:.02em;flex:1;min-height:44px}}
.brand b{{font-weight:600}}
.brand .sl{{color:var(--signal);font-weight:600}}
.brand .sub{{color:var(--ink-3);font-size:var(--fs-micro);letter-spacing:.14em;text-transform:uppercase}}
.mast-nav{{display:flex;gap:22px;font-family:var(--mono);font-size:var(--fs-meta);letter-spacing:.08em;text-transform:uppercase}}
.mast-nav a{{color:var(--ink-2);padding:12px 0;border-bottom:1px solid transparent}}
.mast-nav a:hover{{color:var(--ink);border-bottom-color:var(--ink)}}
.mast-dl{{display:inline-flex;align-items:center;gap:7px;min-height:44px;padding:0 2px;
  font-family:var(--mono);font-size:var(--fs-meta);letter-spacing:.1em;text-transform:uppercase;
  color:var(--ink-2);line-height:1}}
.mast-dl:hover{{color:var(--signal)}}

.hero{{padding:clamp(36px,5vw,52px) 0 0;display:grid;
  grid-template-columns:minmax(0,1fr) minmax(300px,344px);gap:clamp(24px,3.4vw,48px);
  align-items:start;border-bottom:1px solid var(--ink)}}
.hero-body{{padding-bottom:clamp(18px,2.4vw,24px)}}
.eyebrow{{font-family:var(--mono);font-size:var(--fs-meta);letter-spacing:.16em;text-transform:uppercase;
  color:var(--ink-3);margin:0 0 14px;display:flex;align-items:center;gap:10px;flex-wrap:wrap}}
.eyebrow .sq{{display:inline-block;width:7px;height:7px;background:var(--signal);flex:0 0 auto}}
h1{{margin:0;font-size:clamp(62px,9vw,118px);font-weight:900;letter-spacing:-.045em;line-height:.86}}
.h1-en{{display:block;font-family:var(--mono);font-size:var(--fs-micro);font-weight:400;letter-spacing:.4em;
  color:var(--ink-3);margin-top:9px;text-transform:uppercase}}
.lede{{margin:20px 0 0;font-size:var(--fs-lede);line-height:1.7;color:var(--ink-2);max-width:42em;text-wrap:pretty}}
.lede b{{color:var(--ink);font-weight:600;white-space:nowrap}}
.facts{{list-style:none;margin:18px 0 0;padding:0;display:grid;gap:4px;max-width:42em}}
.facts li{{display:flex;gap:10px;font-size:var(--fs-body);color:var(--ink-2);line-height:1.45}}
.facts li::before{{content:"";flex:0 0 14px;height:1px;background:var(--signal);margin-top:.6em}}
.facts b{{font-weight:600;color:var(--ink)}}
.cta-row{{display:flex;gap:10px;flex-wrap:wrap;margin-top:24px}}
.btn{{display:inline-flex;align-items:center;gap:10px;padding:14px 20px;font-family:var(--mono);
  font-size:var(--fs-meta);letter-spacing:.1em;text-transform:uppercase;border:1px solid var(--ink);
  transition:background .15s,color .15s,border-color .15s;min-height:48px}}
.btn--p{{background:var(--ink);color:var(--paper)}}
.btn--p:hover{{background:var(--signal);border-color:var(--signal)}}
.btn--s:hover{{background:var(--ink);color:var(--paper)}}
.btn .ar{{font-size:var(--fs-lede);line-height:1}}
.cta-note{{margin:14px 0 0;font-size:var(--fs-body);line-height:1.6;color:var(--ink-3);max-width:34em}}
.cta-note b{{color:var(--ink-2);font-weight:600}}
.cta-note .nb{{white-space:nowrap}}
.hero::after{{content:"";display:block;grid-column:1/-1;height:7px;margin-top:0;
  background:repeating-linear-gradient(90deg,var(--ink) 0 1px,transparent 1px 13px);opacity:.55}}

.countcard{{border:1px solid var(--ink);background:var(--paper);align-self:start;margin-bottom:24px}}
.countcard-h{{display:flex;justify-content:space-between;align-items:baseline;padding:11px 14px;
  border-bottom:1px solid var(--ink);font-family:var(--mono);font-size:var(--fs-micro);
  letter-spacing:.16em;text-transform:uppercase}}
.countcard-h b{{color:var(--signal);font-weight:600}}
.count-row{{display:flex;align-items:baseline;justify-content:space-between;gap:10px;
  padding:12px 14px;border-bottom:1px solid var(--rule)}}
.count-row:last-child{{border-bottom:0}}
.count-k{{font-size:var(--fs-body);color:var(--ink-2)}}
.count-v{{font-family:var(--mono);font-size:26px;font-weight:600;letter-spacing:-.02em;
  font-variant-numeric:tabular-nums;line-height:1}}
.count-v small{{font-size:var(--fs-meta);font-weight:400;color:var(--ink-3);margin-left:4px;letter-spacing:0}}

.sec-h{{display:flex;align-items:baseline;gap:14px;padding:clamp(34px,4.4vw,52px) 0 16px;flex-wrap:wrap}}
.sec-no{{font-family:var(--mono);font-size:var(--fs-meta);color:var(--signal);letter-spacing:.1em}}
.sec-t{{margin:0;font-size:var(--fs-sec);font-weight:800;letter-spacing:-.02em}}
.sec-note{{font-family:var(--mono);font-size:var(--fs-micro);color:var(--ink-3);letter-spacing:.1em;
  text-transform:uppercase;margin-left:auto}}

.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(276px,1fr));
  border-top:1px solid var(--rule);border-left:1px solid var(--rule)}}
.card{{background:var(--paper);padding:20px 18px 16px;display:flex;flex-direction:column;min-height:230px;
  border-right:1px solid var(--rule);border-bottom:1px solid var(--rule);
  transition:background .15s,color .15s}}
.card:hover{{background:var(--ink);color:var(--paper)}}
.card-top{{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:9px}}
.card-idx{{font-family:var(--mono);font-size:var(--fs-micro);color:var(--signal);letter-spacing:.08em}}
.card-cat{{font-family:var(--mono);font-size:var(--fs-micro);letter-spacing:.12em;color:var(--ink-3);text-transform:uppercase}}
.card:hover .card-cat{{color:#8A8878}}
.card h3{{margin:0;font-size:var(--fs-card);font-weight:600;letter-spacing:-.015em;line-height:1.3}}
.card-en{{margin:3px 0 0;font-family:var(--mono);font-size:var(--fs-micro);letter-spacing:.04em;
  color:var(--ink-3);text-transform:uppercase;word-break:break-word}}
.card:hover .card-en{{color:#8A8878}}
.card-desc{{margin:10px 0 14px;font-size:var(--fs-body);line-height:1.6;color:var(--ink-2);flex:1}}
.card:hover .card-desc{{color:#C9C5B5}}
.chips{{display:flex;flex-wrap:wrap;gap:5px;margin-top:auto}}
.chip{{display:inline-flex;align-items:center;gap:5px;font-family:var(--mono);font-size:var(--fs-meta);
  letter-spacing:.04em;padding:4px 7px;border:1px solid var(--rule);color:var(--ink-3);
  text-transform:uppercase;line-height:1.2;min-height:26px;
  transition:border-color .15s,color .15s,background .15s}}
.chip .dot{{width:4px;height:4px;background:currentColor;flex:0 0 auto}}
a.chip:hover{{border-color:var(--ink);color:var(--ink);background:var(--paper-2)}}
.card:hover .chip{{border-color:#4A4A3E;color:#B5B1A0}}
.card:hover a.chip:hover{{border-color:var(--paper);color:var(--paper);background:#2A2A22}}

.doms{{list-style:none;margin:0;padding:0;border-top:1px solid var(--rule)}}
.dom{{display:grid;grid-template-columns:38px 132px minmax(0,1fr);gap:14px;align-items:baseline;
  padding:14px 2px;border-bottom:1px solid var(--rule)}}
.dom-no{{font-family:var(--mono);font-size:var(--fs-micro);color:var(--signal);letter-spacing:.08em}}
.dom-name{{font-size:var(--fs-lede);font-weight:600;letter-spacing:-.01em}}
.dom-note{{font-size:var(--fs-body);line-height:1.6;color:var(--ink-2)}}

.how{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:clamp(16px,3vw,34px)}}
.step{{border-top:2px solid var(--ink);padding-top:14px}}
.step-no{{font-family:var(--mono);font-size:var(--fs-meta);color:var(--signal);letter-spacing:.1em}}
.step h4{{margin:8px 0 6px;font-size:var(--fs-lede);font-weight:600}}
.step p{{margin:0;font-size:var(--fs-body);line-height:1.66;color:var(--ink-2)}}
.step p b{{font-weight:600;color:var(--ink)}}
.note{{margin:26px 0 0;padding:16px 18px;border:1px solid var(--rule);background:var(--paper-2);
  font-size:var(--fs-body);line-height:1.7;color:var(--ink-2);max-width:64em}}
.note b{{color:var(--ink);font-weight:600}}

footer{{margin-top:clamp(48px,6vw,80px);border-top:1px solid var(--ink);padding:26px 0 44px}}
.foot-in{{display:flex;gap:24px;flex-wrap:wrap;align-items:flex-start}}
.foot-brand{{font-family:var(--mono);font-size:13.5px;letter-spacing:.02em;flex:1;min-width:220px}}
.foot-brand b{{font-weight:600}}
.foot-brand p{{margin:8px 0 0;font-size:var(--fs-micro);line-height:1.7;color:var(--ink-3);
  font-family:var(--sans);letter-spacing:0;max-width:34em}}
.foot-links{{display:flex;gap:18px;flex-wrap:wrap;font-family:var(--mono);font-size:var(--fs-micro);
  letter-spacing:.08em;text-transform:uppercase}}
.foot-links a{{border-bottom:1px solid var(--rule);padding:13px 0;min-height:44px;display:inline-flex;align-items:center}}
.foot-links a:hover{{border-bottom-color:var(--signal);color:var(--signal)}}
.legal{{margin-top:20px;padding-top:14px;border-top:1px solid var(--rule);font-family:var(--mono);
  font-size:var(--fs-micro);color:var(--ink-3);line-height:1.7;letter-spacing:.02em}}

@media (max-width:1080px){{
  .hero{{grid-template-columns:minmax(0,1fr)}}
  .countcard{{margin-top:4px}}
  .how{{grid-template-columns:minmax(0,1fr);gap:20px}}
  .dom{{grid-template-columns:32px minmax(0,1fr);gap:10px}}
  .dom-note{{grid-column:2}}
}}
@media (max-width:820px){{
  .mast-nav{{display:none}}
  .grid{{grid-template-columns:repeat(auto-fill,minmax(240px,1fr))}}
  .card{{min-height:0}}
}}
@media (max-width:560px){{
  .hero{{padding-top:26px}}
  .hero-body{{padding-bottom:12px}}
  .grid{{grid-template-columns:minmax(0,1fr)}}
  .card{{padding:16px}}
  h1{{font-size:clamp(54px,15.5vw,80px)}}
  .cta-note{{margin-top:10px}}
  .facts{{gap:3px}}
  .h1-en{{display:none}}
  .eyebrow{{margin-bottom:10px}}
  .chip{{padding:7px 9px;min-height:34px}}
  .brand .sub{{display:none}}
  .mast-in{{gap:12px}}
  .dom{{padding:12px 0}}
}}
@media (prefers-reduced-motion:reduce){{
  *{{transition:none!important;scroll-behavior:auto!important}}
}}
</style>
</head>
<body>

<header class="mast">
  <div class="mast-in">
    <a class="brand" href="/"><b>x7peeps</b><span class="sl">/</span><span class="sub">skills</span></a>
    <nav class="mast-nav" aria-label="主导航">
      <a href="#live">已公开</a>
      <a href="#domains">能力域</a>
      <a href="#how">怎么拿</a>
    </nav>
    <a class="mast-dl" href="https://x7peeps.com/" target="_blank" rel="noopener">回主站 ↗</a>
  </div>
</header>

<main class="wrap">

  <section class="hero">
    <div class="hero-body">
      <p class="eyebrow"><span class="sq"></span>X7PEEPS<span>/</span>一人公司技能栈<span>/</span>2026</p>
      <h1>技能库</h1>
      <span class="h1-en">Skill Library</span>
      <p class="lede">这套技能做出过能跑的东西。<b>这里只列已经能拿到的</b>——源码在哪、能干什么、跑起来要什么。没上线的，一个都不放。</p>
      <ul class="facts">
        <li><span>{len(LIVE)} 项已开放源码，<b>clone 下来就能跑</b></span></li>
        <li><span>九个能力域，每个都对应真实交付，不是设想</span></li>
        <li><span>页面<b>无登录、无弹窗</b>，不收集任何输入</span></li>
      </ul>
      <div class="cta-row">
        <a class="btn btn--p" href="#live">看已公开的 {len(LIVE)} 个 <span class="ar">↓</span></a>
        <a class="btn btn--s" href="#domains">能力域 <span class="ar">↓</span></a>
      </div>
      <p class="cta-note">WorkBuddy 版还在平台审核里：<span class="nb">通过一个，这里才多一个</span>。</p>
    </div>

    <aside class="countcard" aria-label="数量">
      <div class="countcard-h"><span>Status</span><b>11-17</b></div>
      <div class="count-row"><span class="count-k">已公开可获取</span><span class="count-v">{len(LIVE)}<small>个</small></span></div>
      <div class="count-row"><span class="count-k">能力域</span><span class="count-v">09<small>个</small></span></div>
      <div class="count-row"><span class="count-k">库内技能</span><span class="count-v">{TOTAL}<small>个</small></span></div>
    </aside>
  </section>

  <section id="live">
    <div class="sec-h">
      <span class="sec-no">§ 01</span>
      <h2 class="sec-t">已经能拿到的</h2>
      <span class="sec-note">源码公开</span>
    </div>
    <div class="grid">
      {cards_html}
    </div>
  </section>

  <section id="domains">
    <div class="sec-h">
      <span class="sec-no">§ 02</span>
      <h2 class="sec-t">这套技能覆盖什么</h2>
      <span class="sec-note">九个方向</span>
    </div>
    <ul class="doms">
      {dom_rows}
    </ul>
    <p class="note"><b>为什么只写方向、不列技能名：</b>库里还有上千个技能，但大部分还只在我自己的机器上跑得通，没做成别人能装的东西。把名字列出来、又给不了安装方式，等于让你白点一次。<b>要哪个方向的具体能力，直接说，我做出来再放上来。</b></p>
  </section>

  <section id="how">
    <div class="sec-h">
      <span class="sec-no">§ 03</span>
      <h2 class="sec-t">怎么拿</h2>
      <span class="sec-note">三条路</span>
    </div>
    <div class="how">
      <div class="step">
        <div class="step-no">01</div>
        <h4>要源码</h4>
        <p>上面 {len(LIVE)} 个项目直接 clone。每个仓库都有 README，写清依赖和最小可跑命令，不含需要我私下配合的步骤。</p>
      </div>
      <div class="step">
        <div class="step-no">02</div>
        <h4>要 WorkBuddy 版</h4>
        <p>技能正在按官方 SKILL.md 规范走平台审核。<b>目前市场上还搜不到</b>，通过了会在这里出现，也只在通过之后才出现。</p>
      </div>
      <div class="step">
        <div class="step-no">03</div>
        <h4>要别的东西</h4>
        <p>九个方向里的任何一件，说清楚你要什么输入、什么输出。我做出来、验一遍，再挂上来。不做「先上架再补功能」。</p>
      </div>
    </div>
    <p class="note"><b>这个页面为什么这么短：</b>因为按「只放拿得到的」这个标准，现在就只有这么多。我不拿库里的技能名充数——那些是手艺，还不是商品。<b>短是真的短，但上面每个链接都点得通。</b></p>
  </section>

</main>

<footer>
  <div class="wrap">
    <div class="foot-in">
      <div class="foot-brand">
        <b>x7peeps</b> / 一人公司技能栈
        <p>一个人，一套技能，从选题到上线全自己走。技能是手艺的容器，不是提示词合集。</p>
      </div>
      <nav class="foot-links" aria-label="站外链接">
        <a href="https://x7peeps.com/" target="_blank" rel="noopener">主站</a>
        <a href="https://github.com/x7peeps" target="_blank" rel="noopener">GitHub</a>
        <a href="https://www.workbuddy.cn/" target="_blank" rel="noopener">WorkBuddy</a>
        <a href="https://x7peeps.com/关于/" target="_blank" rel="noopener">关于</a>
      </nav>
    </div>
    <p class="legal">
      安全与逆向类项目仅用于授权范围内的安全测试、应急响应与防御建设。<br>
      build {BUILT[5:]} · {len(LIVE)} 个公开 · 未上架不展示
    </p>
  </div>
</footer>

</body>
</html>'''

out = ROOT / "index.html"
out.write_text(HTML, encoding="utf-8")
print(f"written {out}  {len(HTML)} bytes  live={len(LIVE)}")
