#!/usr/bin/env python3
"""生成 skills.x7peeps.com 静态页：单文件 HTML，内联 CSS/JS，无外部依赖。"""
import json, html, pathlib

ROOT = pathlib.Path(__file__).parent
D = json.loads((ROOT / "data.json").read_text(encoding="utf-8"))
SK = D["skills"]
CATS = D["cats"]
CATMAP = {c["id"]: c for c in CATS}

def esc(s):
    return html.escape(s or "", quote=True)

def count(cid):
    return len(SK) if cid == "all" else sum(1 for s in SK if s["cat"] == cid)

# ---------- 卡片 ----------
def card(s):
    c = CATMAP[s["cat"]]
    n = [x for x in SK if x["cat"] == s["cat"]].index(s) + 1
    idx = f'{c["no"]}-{str(n).zfill(2)}'
    chips = []
    if s.get("wb"):
        chips.append(f'<button class="chip chip--wb" data-copy="{esc(s["wb"])}" data-kind="wb" type="button" '
                     f'title="复制技能名，在 WorkBuddy 技能市场搜索安装"><span class="dot"></span>WorkBuddy</button>')
    if s.get("gh"):
        chips.append(f'<a class="chip chip--gh" href="{esc(s["gh"])}" target="_blank" rel="noopener">'
                     f'<span class="dot"></span>GitHub</a>')
    if s.get("site"):
        chips.append(f'<a class="chip chip--site" href="{esc(s["site"])}" target="_blank" rel="noopener">'
                     f'<span class="dot"></span>主站</a>')
    for t in s.get("tags", []):
        chips.append(f'<span class="chip chip--tag">{esc(t)}</span>')
    chips.append(f'<button class="chip chip--copy" data-copy="{esc(s["name"])}" data-kind="name" type="button" '
                 f'aria-label="复制「{esc(s["name"])}」的技能名">复制名</button>')
    return f'''<article class="card" data-cat="{s["cat"]}" data-wb="{1 if s.get("wb") else 0}" data-name="{esc(s["name"] + " " + s["en"] + " " + s["desc"])}">
  <div class="card-top"><span class="card-idx">{idx}</span><span class="card-cat">{c["en"]}</span></div>
  <h3>{esc(s["name"])}</h3>
  <p class="card-en">{esc(s["en"])}</p>
  <p class="card-desc">{esc(s["desc"])}</p>
  <div class="chips">{"".join(chips)}</div>
</article>'''

cards_html = "\n".join(card(s) for s in SK)

nav_items = "\n".join(
    f'<li><button class="nav-item{" is-on" if c["id"]=="all" else ""}" data-filter="{c["id"]}" type="button">'
    f'<span class="nav-no">{c["no"]}</span><span class="nav-name">{esc(c["name"])}</span>'
    f'<span class="nav-count">{count(c["id"])}</span></button></li>' for c in CATS)

index_rows = "\n".join(
    f'<li><button class="idx-row" data-filter="{c["id"]}" type="button">'
    f'<span class="idx-no">{c["no"]}</span><span class="idx-name">{esc(c["name"])}</span>'
    f'<span class="idx-dots"></span><span class="idx-count">{count(c["id"])}</span></button></li>'
    for c in CATS if c["id"] != "all")

CHANNELS = [
    ("WORKBUDDY", "WorkBuddy", "https://www.workbuddy.cn/",
     "技能市场搜名字即装。已按官方 SKILL.md 规范提交两个（口播提取、文案整理），审核通过后可直接搜到。", "去下载 →"),
    ("GITHUB", "GitHub", "https://github.com/x7peeps",
     "能开源的那几个直接给源码：内存马审计、行为分析器、狗生大梦、联机赛车，都能 clone 下来跑。",
     "看仓库 →"),
    ("X7PEEPS.COM", "主站", "https://x7peeps.com/",
     "技术文章都在主站。技能背后为什么这么做、踩过哪些坑、失败长什么样，都写在里面。",
     "读文章 →"),
]
chan_html = "\n".join(
    f'''<a class="chan" href="{url}" target="_blank" rel="noopener">
  <span class="chan-tag">{tag}</span>
  <span class="chan-name">{name}</span>
  <span class="chan-desc">{desc}</span>
  <span class="chan-go">{go}</span>
</a>''' for tag, name, url, desc, go in CHANNELS)

PROOF = [
    ("狗生大梦", "Three.js 可玩世界，Tripo 生成资产，真机部署。给一只狗做的。",
     "https://github.com/x7peeps/dog-dream", "开源 · 可玩"),
    ("内存马审计器", "JVM attach 检测五类内存马，JMG 真实载荷 7/7 检出。",
     "https://github.com/x7peeps/memshell-auditor", "开源 · 安全"),
    ("行为分析器", "样本静态、动态、取证、流量，一条命令，纯离线出报告。",
     "https://github.com/x7peeps/behaviorscope", "开源 · 安全"),
    ("联机漂移赛车", "5 人实时漂移，道具、圈速、实拍车模，单文件零构建。",
     "https://github.com/x7peeps/drift-race", "开源 · 游戏"),
]
proof_html = "\n".join(
    f'''<a class="proof" href="{u}" target="_blank" rel="noopener">
  <span class="proof-tag">{t}</span>
  <h4>{esc(n)}</h4>
  <p>{esc(d)}</p>
  <span class="proof-go">打开 ↗</span>
</a>''' for n, d, u, t in PROOF)

TOTAL = D["meta"]["totalSkills"]
BUILT = D["meta"]["built"]

HTML = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>技能库 · x7peeps — {len(SK)} 个可安装的 AI Agent 技能</title>
<meta name="description" content="x7peeps 技能库：{TOTAL} 个 AI Agent 技能，覆盖内容生产、影视、安全、量化、设计、游戏、音乐。SKILL.md 标准格式，WorkBuddy / Claude Code / Codex / Hermes 通用。">
<meta name="theme-color" content="#F2EFE6">
<meta property="og:type" content="website">
<meta property="og:title" content="技能库 · x7peeps">
<meta property="og:description" content="{TOTAL} 个给 AI Agent 用的技能，每一个都在本机跑通过。">
<meta property="og:url" content="https://skills.x7peeps.com/">
<link rel="canonical" href="https://skills.x7peeps.com/">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' fill='%2315150F'/%3E%3Ctext x='16' y='23' font-family='monospace' font-size='16' font-weight='700' fill='%23F2EFE6' text-anchor='middle'%3Ex7%3C/text%3E%3C/svg%3E">
<style>
:root{{
  --paper:#F2EFE6; --paper-2:#EBE7DA; --ink:#15150F; --ink-2:#3B3B32; --ink-3:#6B6A5C;
  --rule:#D3CDBC; --signal:#B93A1E; --wb:#1F5F8B;
  --fs-micro:10.5px; --fs-meta:11.5px; --fs-body:13.5px; --fs-lede:16px;
  --fs-card:19px; --fs-sec:22px;
  --mono:"SF Mono","JetBrains Mono","IBM Plex Mono",ui-monospace,Menlo,Consolas,monospace;
  --sans:"PingFang SC","Hiragino Sans GB","Source Han Sans SC","Noto Sans CJK SC","Microsoft YaHei",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
  --pad:clamp(20px,4vw,40px);
}}
*{{box-sizing:border-box}}
html{{scroll-behavior:smooth}}
body{{margin:0;background:var(--paper);color:var(--ink);font-family:var(--sans);
  font-size:var(--fs-body);line-height:1.6;-webkit-font-smoothing:antialiased;font-weight:400}}
a{{color:inherit;text-decoration:none}}
button{{font:inherit;color:inherit;background:none;border:0;cursor:pointer}}
:focus-visible{{outline:2px solid var(--signal);outline-offset:2px}}
.wrap{{max-width:1360px;margin:0 auto;padding:0 var(--pad)}}

/* masthead */
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
  border-bottom:1px solid var(--ink);line-height:1}}
.mast-dl:hover{{color:var(--signal);border-bottom-color:var(--signal)}}

/* hero */
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
.lede{{margin:20px 0 0;font-size:var(--fs-lede);line-height:1.7;color:var(--ink-2);max-width:42em}}
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
.hero::after{{content:"";display:block;grid-column:1/-1;height:7px;margin-top:0;
  background:repeating-linear-gradient(90deg,var(--ink) 0 1px,transparent 1px 13px);opacity:.55}}

/* index card */
.indexcard{{border:1px solid var(--ink);background:var(--paper);align-self:start;margin-bottom:24px}}
.indexcard-h{{display:flex;justify-content:space-between;align-items:baseline;padding:11px 14px;
  border-bottom:1px solid var(--ink);font-family:var(--mono);font-size:var(--fs-micro);
  letter-spacing:.16em;text-transform:uppercase}}
.indexcard-h b{{color:var(--signal);font-weight:600}}
.idx-list{{list-style:none;margin:0;padding:0}}
.idx-row{{display:flex;align-items:baseline;gap:9px;width:100%;padding:8px 14px;text-align:left;
  border-bottom:1px solid var(--rule);transition:background .12s,padding-left .12s;min-height:36px}}
.idx-list li:last-child .idx-row{{border-bottom:0}}
.idx-row:hover{{background:var(--paper-2);padding-left:18px}}
.idx-no{{font-family:var(--mono);font-size:var(--fs-micro);color:var(--ink-3);flex:0 0 auto}}
.idx-name{{font-size:var(--fs-body);font-weight:600;white-space:nowrap}}
.idx-dots{{flex:1;border-bottom:1px dotted var(--rule);transform:translateY(-3px)}}
.idx-count{{font-family:var(--mono);font-size:var(--fs-meta);font-variant-numeric:tabular-nums;color:var(--ink-2)}}

/* channels */
.chans{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1px;background:var(--rule);
  border:1px solid var(--rule)}}
.chan{{background:var(--paper);padding:18px 20px 16px;display:flex;flex-direction:column;gap:6px;
  min-height:140px;transition:background .15s,color .15s}}
.chan:hover{{background:var(--ink);color:var(--paper)}}
.chan-tag{{font-family:var(--mono);font-size:var(--fs-micro);letter-spacing:.16em;color:var(--signal)}}
.chan:hover .chan-tag{{color:#E8A08F}}
.chan-name{{font-size:var(--fs-lede);font-weight:600;letter-spacing:-.01em}}
.chan-desc{{font-size:var(--fs-body);line-height:1.6;color:var(--ink-2);flex:1}}
.chan:hover .chan-desc{{color:#C9C5B5}}
.chan-desc em{{font-style:normal;color:var(--wb);font-weight:600}}
.chan:hover .chan-desc em{{color:#8FC0E0}}
.chan-go{{font-family:var(--mono);font-size:var(--fs-micro);letter-spacing:.12em;text-transform:uppercase}}

/* section head */
.sec-h{{display:flex;align-items:baseline;gap:14px;padding:clamp(34px,4.4vw,52px) 0 16px;flex-wrap:wrap}}
.sec-no{{font-family:var(--mono);font-size:var(--fs-meta);color:var(--signal);letter-spacing:.1em}}
.sec-t{{margin:0;font-size:var(--fs-sec);font-weight:800;letter-spacing:-.02em}}
.sec-note{{font-family:var(--mono);font-size:var(--fs-micro);color:var(--ink-3);letter-spacing:.1em;
  text-transform:uppercase;margin-left:auto}}

/* catalog */
.layout{{display:grid;grid-template-columns:206px minmax(0,1fr);gap:clamp(18px,3vw,34px);align-items:start}}
.side{{position:sticky;top:74px}}
.side-h{{font-family:var(--mono);font-size:var(--fs-micro);letter-spacing:.16em;text-transform:uppercase;
  color:var(--ink-3);padding-bottom:8px;border-bottom:1px solid var(--ink);margin-bottom:2px}}
.nav-list{{list-style:none;margin:0;padding:0}}
.nav-item{{display:flex;align-items:baseline;gap:8px;width:100%;padding:9px 8px 9px 0;text-align:left;
  border-bottom:1px solid var(--rule);transition:color .12s,padding-left .12s;min-height:38px}}
.nav-item:hover{{padding-left:5px}}
.nav-no{{font-family:var(--mono);font-size:var(--fs-micro);color:var(--ink-3);flex:0 0 18px}}
.nav-name{{font-size:var(--fs-body);font-weight:600;flex:1;white-space:nowrap}}
.nav-count{{font-family:var(--mono);font-size:var(--fs-micro);color:var(--ink-3);font-variant-numeric:tabular-nums}}
.nav-item.is-on{{color:var(--signal);padding-left:5px}}
.nav-item.is-on .nav-no,.nav-item.is-on .nav-count{{color:var(--signal)}}
.nav-item.is-on .nav-name::before{{content:"";display:inline-block;width:3px;height:11px;background:var(--signal);
  margin-right:8px;transform:translateY(-1px)}}
.side-foot{{margin-top:16px;font-size:var(--fs-micro);line-height:1.6;color:var(--ink-3);font-family:var(--mono)}}

.toolbar{{display:flex;align-items:center;gap:12px;margin-bottom:12px;flex-wrap:wrap}}
.search{{flex:1;min-width:200px;display:flex;align-items:center;gap:9px;border-bottom:1px solid var(--ink);padding:8px 2px}}
.search svg{{flex:0 0 14px;opacity:.5}}
.search input{{flex:1;border:0;background:none;font:inherit;font-size:var(--fs-lede);color:var(--ink);
  padding:2px 0;min-width:0}}
.search input::placeholder{{color:var(--ink-3);font-size:var(--fs-body)}}
.search input:focus{{outline:none}}
.search kbd{{font-family:var(--mono);font-size:var(--fs-micro);border:1px solid var(--rule);padding:2px 5px;color:var(--ink-3)}}
.tcount{{font-family:var(--mono);font-size:var(--fs-meta);color:var(--ink-3);font-variant-numeric:tabular-nums;white-space:nowrap}}
.tcount b{{color:var(--ink);font-weight:600}}
.wbtoggle{{display:inline-flex;align-items:center;gap:6px;border:1px solid var(--rule);padding:7px 10px;
  font-family:var(--mono);font-size:var(--fs-micro);letter-spacing:.08em;text-transform:uppercase;
  color:var(--ink-3);min-height:34px;transition:border-color .15s,color .15s,background .15s;white-space:nowrap}}
.wbtoggle .dot{{width:5px;height:5px;background:var(--wb);flex:0 0 auto}}
.wbtoggle:hover{{border-color:var(--wb);color:var(--wb)}}
.wbtoggle[aria-pressed="true"]{{border-color:var(--wb);color:var(--wb);background:#EAF0F4}}
.wbtoggle[aria-pressed="true"] .dot{{background:var(--wb)}}

.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(286px,1fr));gap:1px;background:var(--rule);
  border:1px solid var(--rule)}}
.card{{background:var(--paper);padding:18px 18px 15px;display:flex;flex-direction:column;min-height:186px;
  transition:background .15s,color .15s}}
.card:hover{{background:var(--ink);color:var(--paper)}}
.card-top{{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:9px}}
.card-idx{{font-family:var(--mono);font-size:var(--fs-micro);color:var(--signal);letter-spacing:.08em}}
.card-cat{{font-family:var(--mono);font-size:var(--fs-micro);letter-spacing:.12em;color:var(--ink-3);text-transform:uppercase}}
.card:hover .card-cat{{color:#8A8878}}
.card h3{{margin:0;font-size:var(--fs-card);font-weight:600;letter-spacing:-.015em;line-height:1.3}}
.card-en{{margin:3px 0 0;font-family:var(--mono);font-size:var(--fs-micro);letter-spacing:.04em;color:var(--ink-3);
  text-transform:uppercase;word-break:break-word}}
.card:hover .card-en{{color:#8A8878}}
.card-desc{{margin:10px 0 14px;font-size:var(--fs-body);line-height:1.6;color:var(--ink-2);flex:1}}
.card:hover .card-desc{{color:#C9C5B5}}
.chips{{display:flex;flex-wrap:wrap;gap:5px;margin-top:auto}}
.chip{{display:inline-flex;align-items:center;gap:5px;font-family:var(--mono);font-size:var(--fs-micro);
  letter-spacing:.05em;padding:4px 7px;border:1px solid var(--rule);color:var(--ink-3);
  text-transform:uppercase;line-height:1.2;transition:border-color .15s,color .15s,background .15s}}
.chip .dot{{width:4px;height:4px;background:currentColor;flex:0 0 auto}}
.chip--wb{{color:var(--wb);border-color:#B9CDDC}}
a.chip,button.chip{{min-height:26px}}
a.chip:hover,button.chip:hover{{border-color:var(--ink);color:var(--ink);background:var(--paper-2)}}
.card:hover .chip{{border-color:#4A4A3E;color:#B5B1A0}}
.card:hover .chip:hover{{border-color:var(--paper);color:var(--paper);background:#2A2A22}}
.chip--copy{{margin-left:auto;cursor:pointer}}
.empty{{display:none;padding:56px 20px;text-align:center;border:1px solid var(--rule);border-top:0}}
.empty.is-on{{display:block}}
.empty p{{margin:0 0 6px;font-size:var(--fs-lede);font-weight:600}}
.empty span{{font-size:var(--fs-body);color:var(--ink-3)}}

/* proof */
.proofs{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:1px;background:var(--rule);border:1px solid var(--rule)}}
.proof{{background:var(--paper);padding:18px;display:flex;flex-direction:column;gap:7px;min-height:176px;
  transition:background .15s,color .15s}}
.proof:hover{{background:var(--ink);color:var(--paper)}}
.proof-tag{{font-family:var(--mono);font-size:var(--fs-micro);letter-spacing:.12em;color:var(--signal)}}
.proof:hover .proof-tag{{color:#E8A08F}}
.proof h4{{margin:0;font-size:var(--fs-card);font-weight:600;letter-spacing:-.01em}}
.proof p{{margin:0;font-size:var(--fs-body);line-height:1.6;color:var(--ink-2);flex:1}}
.proof:hover p{{color:#C9C5B5}}
.proof-go{{font-family:var(--mono);font-size:var(--fs-micro);letter-spacing:.1em;text-transform:uppercase}}

/* how */
.how{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:clamp(16px,3vw,34px)}}
.step{{border-top:2px solid var(--ink);padding-top:14px}}
.step-no{{font-family:var(--mono);font-size:var(--fs-meta);color:var(--signal);letter-spacing:.1em}}
.step h4{{margin:8px 0 6px;font-size:var(--fs-lede);font-weight:600}}
.step p{{margin:0;font-size:var(--fs-body);line-height:1.66;color:var(--ink-2)}}
.step p b{{font-weight:600;color:var(--ink)}}
.note{{margin:26px 0 0;padding:16px 18px;border:1px solid var(--rule);background:var(--paper-2);
  font-size:var(--fs-body);line-height:1.7;color:var(--ink-2);max-width:64em}}
.note b{{color:var(--ink);font-weight:600}}

/* footer */
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

/* toast */
.toast{{position:fixed;left:50%;bottom:24px;transform:translate(-50%,16px);z-index:80;
  background:var(--ink);color:var(--paper);padding:10px 14px;display:flex;align-items:center;gap:10px;
  font-family:var(--mono);font-size:var(--fs-meta);letter-spacing:.04em;opacity:0;pointer-events:none;
  transition:opacity .18s,transform .18s;max-width:calc(100vw - 28px)}}
.toast.is-on{{opacity:1;transform:translate(-50%,0);pointer-events:auto}}
.toast a{{color:#9FD0F0;border-bottom:1px solid #9FD0F0;padding:12px 0;min-height:44px;display:inline-flex;align-items:center}}
.toast .x{{color:#8A8878;min-width:44px;min-height:44px;display:inline-flex;align-items:center;
  justify-content:center;cursor:pointer;margin-right:-8px}}

@media (max-width:1080px){{
  .hero{{grid-template-columns:minmax(0,1fr)}}
  .indexcard{{display:none}}
  .layout{{grid-template-columns:minmax(0,1fr)}}
  .side{{position:static;top:auto;border-bottom:1px solid var(--ink);padding-bottom:10px;margin-bottom:14px}}
  .side-h{{display:none}}
  .nav-list{{display:flex;gap:6px;overflow-x:auto;padding-bottom:4px;scrollbar-width:none}}
  .nav-list::-webkit-scrollbar{{display:none}}
  .nav-item{{width:auto;border:1px solid var(--rule);padding:8px 10px;gap:6px;white-space:nowrap;flex:0 0 auto;min-height:44px}}
  .nav-item:hover,.nav-item.is-on{{padding-left:10px}}
  .nav-item.is-on{{border-color:var(--signal)}}
  .nav-item.is-on .nav-name::before{{display:none}}
  .side-foot{{display:none}}
  .chans{{grid-template-columns:minmax(0,1fr)}}
  .proofs{{grid-template-columns:repeat(2,minmax(0,1fr))}}
  .how{{grid-template-columns:minmax(0,1fr);gap:20px}}
}}
@media (max-width:820px){{
  .mast-nav{{display:none}}
  .grid{{grid-template-columns:repeat(auto-fill,minmax(240px,1fr))}}
  .card{{min-height:0}}
}}
@media (max-width:560px){{
  .grid{{grid-template-columns:minmax(0,1fr)}}
  .proofs{{grid-template-columns:minmax(0,1fr)}}
  .card{{padding:16px}}
  h1{{font-size:clamp(56px,16.5vw,84px)}}
  .chip{{padding:7px 9px}}
  a.chip,button.chip{{min-height:34px}}
  .brand .sub{{display:none}}
  .mast-in{{gap:12px}}
  .search kbd{{display:none}}
  .wbtoggle{{min-height:44px}}
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
      <a href="#catalog">全部技能</a>
      <a href="#channels">渠道</a>
      <a href="#proof">产出</a>
      <a href="#how">怎么用</a>
    </nav>
    <a class="mast-dl" href="https://www.workbuddy.cn/" target="_blank" rel="noopener">下载客户端 ↗</a>
  </div>
</header>

<main class="wrap">

  <section class="hero">
    <div class="hero-body">
      <p class="eyebrow"><span class="sq"></span>X7PEEPS<span>/</span>一人公司技能栈<span>/</span>2026</p>
      <h1>技能库</h1>
      <span class="h1-en">Skill Library</span>
      <p class="lede">{TOTAL} 个给 AI Agent 用的技能。内容、影视、安全、量化、设计、游戏、音乐——<b>每一个都在本机跑通过</b>，不是提示词收藏夹。</p>
      <ul class="facts">
        <li><span><b>SKILL.md 标准格式</b>，WorkBuddy、Claude Code、Codex、Hermes 都能装</span></li>
        <li><span>每条都对得上一次<b>真实交付</b>：一篇发出去了的文章、一条上了线的片、一个跑着的系统</span></li>
        <li><span>页面<b>无登录、无弹窗</b>，不收集任何输入</span></li>
      </ul>
      <div class="cta-row">
        <a class="btn btn--p" href="https://www.workbuddy.cn/" target="_blank" rel="noopener">装 WorkBuddy，搜名字就能用 <span class="ar">↗</span></a>
        <a class="btn btn--s" href="#catalog">看全部技能 <span class="ar">↓</span></a>
      </div>
    </div>

    <aside class="indexcard" aria-label="能力域索引">
      <div class="indexcard-h"><span>Index</span><b>09 Domains</b></div>
      <ul class="idx-list">
        {index_rows}
      </ul>
    </aside>
  </section>

  <section id="catalog">
    <div class="sec-h">
      <span class="sec-no">§ 01</span>
      <h2 class="sec-t">目录</h2>
      <span class="sec-note">selected / total</span>
    </div>
    <div class="layout">
      <aside class="side">
        <div class="side-h">Filter</div>
        <ul class="nav-list">
          {nav_items}
        </ul>
        <p class="side-foot">按「/」跳到搜索。<br>点卡片上的「复制名」，去 WorkBuddy 技能市场粘贴。</p>
      </aside>

      <div>
        <div class="toolbar">
          <label class="search">
            <svg viewBox="0 0 16 16" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><circle cx="6.6" cy="6.6" r="4.6"/><path d="M10.2 10.2L14 14"/></svg>
            <input id="q" type="search" placeholder="搜技能、场景或关键词：口播、内存马、回测、MV…" autocomplete="off" aria-label="搜索技能">
            <kbd>/</kbd>
          </label>
          <button class="wbtoggle" id="wbtoggle" type="button" aria-pressed="false">
            <span class="dot"></span>WorkBuddy 版
          </button>
          <span class="tcount"><b id="n">0</b> / {len(SK)}</span>
        </div>
        <div class="grid" id="grid">
          {cards_html}
        </div>
        <div class="empty" id="empty">
          <p>没有匹配的技能。</p>
          <span>换个词试试，或者在 x7peeps 公众号留言说你缺什么——按需求量排上架顺序。</span>
        </div>
      </div>
    </div>
  </section>

  <section id="channels">
    <div class="sec-h">
      <span class="sec-no">§ 02</span>
      <h2 class="sec-t">在哪拿到</h2>
      <span class="sec-note">three routes</span>
    </div>
    <div class="chans">
      {chan_html}
    </div>
  </section>

  <section id="proof">
    <div class="sec-h">
      <span class="sec-no">§ 03</span>
      <h2 class="sec-t">这些技能真出过东西</h2>
      <span class="sec-note">shipped, not slides</span>
    </div>
    <div class="proofs">
      {proof_html}
    </div>
  </section>

  <section id="how">
    <div class="sec-h">
      <span class="sec-no">§ 04</span>
      <h2 class="sec-t">三步用上</h2>
      <span class="sec-note">3 steps</span>
    </div>
    <div class="how">
      <div class="step">
        <div class="step-no">01</div>
        <h4>装一个宿主</h4>
        <p>WorkBuddy 最省事，Windows 和 macOS 都有客户端。已经在用 Claude Code、Codex 或 Hermes 的，跳过这步。</p>
      </div>
      <div class="step">
        <div class="step-no">02</div>
        <h4>把技能放进去</h4>
        <p>带 <b>WorkBuddy</b> 标记的，到技能市场搜名字直接装。其余的按 SKILL.md 目录放进宿主的 skills 目录，或用市场右上角「创建技能」导入。</p>
      </div>
      <div class="step">
        <div class="step-no">03</div>
        <h4>用一句话叫它</h4>
        <p>不用记命令。说「把这条抖音的口播稿提出来」或者「帮我看看这个 jar 有没有内存马」，技能自己会接上。</p>
      </div>
    </div>
    <p class="note"><b>关于上架进度：</b>已经按官方规范提交到 WorkBuddy 技能市场的是内容生产那一批——口播提取、文案整理。剩下六十多个能离线跑，但还没走完平台审核。想要哪个，公众号说一声，我按要的人多少排顺序。<b>不承诺搜得到，也不让你点空链接。</b></p>
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
      安全与逆向类技能仅用于授权范围内的安全测试、应急响应与防御建设，不提供针对未授权目标的攻击能力。<br>
      build {BUILT[5:]} · {len(SK)} skills listed · SKILL.md format
    </p>
  </div>
</footer>

<div class="toast" id="toast" role="status" aria-live="polite">
  <span id="toast-t">已复制</span>
  <a href="https://www.workbuddy.cn/" target="_blank" rel="noopener">去 WorkBuddy 市场粘贴 ↗</a>
  <span class="x" id="toast-x" role="button" tabindex="0" aria-label="关闭">✕</span>
</div>

<script>
(function(){{
  var grid=document.getElementById('grid'), cards=[].slice.call(grid.querySelectorAll('.card:not(.card--ghost)')),
      q=document.getElementById('q'), nEl=document.getElementById('n'), empty=document.getElementById('empty'),
      navs=[].slice.call(document.querySelectorAll('[data-filter]')), cur='all',
      wbBtn=document.getElementById('wbtoggle'), onlyWb=false;

  function apply(){{
    var term=(q.value||'').trim().toLowerCase(), shown=0;
    cards.forEach(function(c){{
      var on = (cur==='all' || c.dataset.cat===cur)
            && (!onlyWb || c.dataset.wb==='1')
            && (!term || c.dataset.name.toLowerCase().indexOf(term)>-1);
      c.style.display = on ? '' : 'none';
      if(on) shown++;
    }});
    nEl.textContent = shown;
    empty.classList.toggle('is-on', shown===0);
    grid.style.display = shown===0 ? 'none' : '';
    ghosts();
  }}
  function ghosts(){{
    [].slice.call(grid.querySelectorAll('.card--ghost')).forEach(function(g){{ g.remove(); }});
    var vis = cards.filter(function(c){{ return c.style.display!=='none'; }});
    if(!vis.length) return;
    var cw = vis[0].getBoundingClientRect().width;
    var cols = Math.max(1, Math.round((grid.clientWidth+1)/(cw+1)));
    var rem = vis.length % cols;
    for(var i=0; i<(rem ? cols-rem : 0); i++){{
      var g=document.createElement('div'); g.className='card card--ghost';
      g.setAttribute('aria-hidden','true'); grid.appendChild(g);
    }}
  }}
  function setCat(id){{
    cur=id;
    navs.forEach(function(b){{ b.classList.toggle('is-on', b.dataset.filter===id); }});
    apply();
  }}
  navs.forEach(function(b){{ b.addEventListener('click', function(){{ setCat(b.dataset.filter); }}); }});
  wbBtn.addEventListener('click', function(){{
    onlyWb = !onlyWb;
    wbBtn.setAttribute('aria-pressed', onlyWb ? 'true' : 'false');
    apply();
  }});
  q.addEventListener('input', apply);
  var rt; window.addEventListener('resize', function(){{ clearTimeout(rt); rt=setTimeout(ghosts,120); }});
  apply();

  var toast=document.getElementById('toast'), toastT=document.getElementById('toast-t'), tt;
  function show(msg){{ toastT.textContent=msg; toast.classList.add('is-on'); clearTimeout(tt);
    tt=setTimeout(function(){{toast.classList.remove('is-on');}},4200); }}
  function fallback(text){{
    var ta=document.createElement('textarea'); ta.value=text; ta.setAttribute('readonly','');
    ta.style.cssText='position:fixed;top:-1000px;opacity:0';
    document.body.appendChild(ta); ta.select();
    try{{ document.execCommand('copy'); }}catch(e){{}}
    document.body.removeChild(ta);
  }}
  function copy(text, kind){{
    var done=function(){{ show(kind==='wb' ? '已复制「'+text+'」· 到 WorkBuddy 技能市场搜索粘贴' : '已复制「'+text+'」'); }};
    if(navigator.clipboard && window.isSecureContext){{
      navigator.clipboard.writeText(text).then(done).catch(function(){{ fallback(text); done(); }});
    }} else {{ fallback(text); done(); }}
  }}
  document.addEventListener('click', function(e){{
    var b=e.target.closest('[data-copy]');
    if(b){{ e.preventDefault(); copy(b.dataset.copy, b.dataset.kind); }}
  }});
  document.getElementById('toast-x').addEventListener('click', function(){{ toast.classList.remove('is-on'); }});

  document.addEventListener('keydown', function(e){{
    if(e.key==='/' && document.activeElement!==q && !/input|textarea/i.test(document.activeElement.tagName)){{
      e.preventDefault(); q.focus();
    }}
    if(e.key==='Escape' && document.activeElement===q){{ q.value=''; apply(); q.blur(); }}
  }});
}})();
</script>
</body>
</html>'''

out = ROOT / "index.html"
out.write_text(HTML, encoding="utf-8")
print(f"written {out}  {len(HTML)} bytes  skills={len(SK)}")
