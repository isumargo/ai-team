#!/usr/bin/env python3
'''Sync truth-map across 3 layers.

Layers:
  1. truth-map.md          CANONICAL  - diedit manusia (teks/mermaid/tabel)
  2. truth-map.html        GENERATED  - viewer + editor live (mermaid dirender)
  3. truth-map.excalidraw  GENERATED  - visual, diedit di excalidraw.com

Round-trip:
  sync_map.py html                 md -> html
  sync_map.py excalidraw           md -> excalidraw (call gen_truth_map.py)
  sync_map.py read-excalidraw F    excalidraw -> markdown ringkasan (YANG DIBACA AI)

Catatan: sync_map tidak pernah mengubah truth-map.md otomatis (md = canonical, manusia punya kendali penuh).
'''
import json
import re
import sys
from pathlib import Path

DOCS = Path("/root/ai-team/docs")
MD = DOCS / "truth-map.md"
HTML = DOCS / "truth-map.html"
EXCAL = DOCS / "truth-map.excalidraw"
MERMAID_JS = DOCS / "mermaid" / "mermaid.min.js"


# ---------------------------------------------------------------- md parsing
def parse_md(text):
    """Split markdown into ordered blocks: heading / text / mermaid / table."""
    lines = text.split("\n")
    blocks, i, buf = [], 0, []

    def flush_text():
        if buf:
            t = "\n".join(buf).strip()
            if t:
                blocks.append({"type": "text", "content": t})
            buf.clear()

    while i < len(lines):
        ln = lines[i]
        if ln.strip() == "```mermaid" :
            flush_text()
            i += 1
            mbuf = []
            while i < len(lines) and lines[i].strip() != "```":
                mbuf.append(lines[i])
                i += 1
            blocks.append({"type": "mermaid", "content": "\n".join(mbuf)})
            i += 1
            continue
        if ln.strip() == "```":
            flush_text()
            i += 1
            cbuf = []
            while i < len(lines) and lines[i].strip() != "```":
                cbuf.append(lines[i])
                i += 1
            blocks.append({"type": "code", "lang": "", "content": "\n".join(cbuf)})
            i += 1
            continue
        if ln.startswith("|"):
            flush_text()
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append(lines[i])
                i += 1
            blocks.append({"type": "table", "content": "\n".join(rows)})
            continue
        if ln.startswith("#"):
            flush_text()
            blocks.append({"type": "heading", "content": ln})
            buf.append(ln)
            i += 1
            continue
        buf.append(ln)
        i += 1
    flush_text()
    # re-attach headings to following text so html renders properly
    return blocks


def md_to_html(text):
    blocks = parse_md(text)
    parts = []
    di = 0
    for b in blocks:
        if b["type"] == "mermaid":
            di += 1
            parts.append({
                "kind": "mermaid",
                "id": f"dia{di}",
                "title": "Diagram",
                "src": b["content"],
            })
        elif b["type"] == "heading":
            parts.append({"kind": "heading", "src": b["content"]})
        elif b["type"] == "table":
            parts.append({"kind": "table", "src": b["content"]})
        elif b["type"] == "code":
            parts.append({"kind": "code", "src": b["content"]})
        else:
            parts.append({"kind": "text", "src": b["content"]})
    return parts


# ---------------------------------------------------------------- html build
HTML_TMPL = r"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__</title>
<style>
:root{--bg:#0b1015;--card:#141b22;--line:#243040;--fg:#e6edf3;--dim:#8b98a5;
--acc:#74c0fc;--ok:#51cf66;--warn:#ffd43b;--bad:#ff6b6b;--edit:#ffa94d}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);
font:14px/1.55 ui-monospace,"JetBrains Mono",Menlo,Consolas,monospace}
header{padding:18px 22px;border-bottom:1px solid var(--line);display:flex;
align-items:center;gap:14px;flex-wrap:wrap;position:sticky;top:0;background:#0b1015ee;
backdrop-filter:blur(6px);z-index:9}
h1{font-size:17px;margin:0;font-weight:600}
.badge{font-size:11px;padding:2px 8px;border-radius:20px;border:1px solid var(--line);
color:var(--dim)}
.badge.edit{border-color:var(--edit);color:var(--edit)}
.badge.ok{border-color:var(--ok);color:var(--ok)}
.spacer{flex:1}
button{font:inherit;font-size:12px;background:#1c2530;color:var(--fg);
border:1px solid var(--line);border-radius:6px;padding:6px 12px;cursor:pointer}
button:hover{border-color:var(--acc);color:var(--acc)}
button.pri{background:var(--acc);color:#06121f;border-color:var(--acc);font-weight:600}
main{padding:22px;max-width:1500px;margin:0 auto}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;
margin-bottom:20px;overflow:hidden}
.card>h2{margin:0;padding:11px 15px;font-size:13px;font-weight:600;
border-bottom:1px solid var(--line);background:#182029;display:flex;
align-items:center;gap:10px}
.card>h2 .tag{font-size:10px;color:var(--dim);text-transform:uppercase;
letter-spacing:.8px}
.body{padding:15px}
.body h1,.body h2,.body h3{font-size:15px;margin:18px 0 8px;color:var(--acc)}
.body h1:first-child{margin-top:0}
.body p{margin:9px 0;color:var(--dim)}
.body ul{margin:9px 0;padding-left:20px;color:var(--dim)}
.body li{margin:4px 0}
.body code{background:#0e141a;padding:1px 5px;border-radius:4px;color:var(--warn);
font-size:12.5px}
.body strong{color:var(--fg)}
table{border-collapse:collapse;width:100%;margin:10px 0;font-size:12.5px}
th,td{border:1px solid var(--line);padding:6px 9px;text-align:left;vertical-align:top}
th{background:#182029;color:var(--acc);font-weight:600}
tr:nth-child(even) td{background:#10161d}
pre{background:#0e141a;border:1px solid var(--line);border-radius:8px;padding:12px;
overflow:auto;max-height:340px;font-size:12.5px;color:#c9d5e0}
.editwrap{grid-template-columns:1fr 1fr;gap:14px;display:grid;align-items:start}
@media(max-width:1000px){.editwrap{grid-template-columns:1fr}}
textarea{width:100%;min-height:340px;background:#0e141a;color:#c9d5e0;
border:1px solid var(--line);border-radius:8px;padding:12px;font:12.5px/1.5 inherit;
resize:vertical;tab-size:2}
textarea:focus{outline:none;border-color:var(--acc)}
.rend{background:#0e141a;border:1px solid var(--line);border-radius:8px;padding:12px;
min-height:340px;overflow:auto}
.rend svg{max-width:100%;height:auto}
.rend .err{color:var(--bad);font-size:12.5px;white-space:pre-wrap}
.bar{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-top:10px}
.hint{font-size:11.5px;color:var(--dim);margin-top:8px}
.hint code{color:var(--warn)}
#toast{position:fixed;right:18px;bottom:18px;background:#16202b;border:1px solid var(--acc);
color:var(--acc);padding:10px 16px;border-radius:8px;font-size:12.5px;opacity:0;
transition:opacity .25s;pointer-events:none;z-index:50}
#toast.on{opacity:1}
.legend i{font-style:normal;padding:2px 7px;border-radius:5px;margin-right:6px;
display:inline-block;font-size:11px}
.li{background:#16202b;border:1px solid var(--line)}
</style>
</head>
<body>
<header>
  <h1>__TITLE__</h1>
  <span class="badge">canonical: <code>truth-map.md</code></span>
  <span class="badge edit" id="dirty">tersimpan lokal</span>
  <span class="spacer"></span>
  <button id="btn-render">Render ulang</button>
  <button id="btn-md">Unduh .md</button>
  <button class="pri" id="btn-patch">Unduh patch JSON</button>
</header>
<main>
  <div class="card">
    <div class="body">
      <p><b>Cara pakai:</b></p>
      <ul>
        <li>Diagram Mermaid: ubah teks di panel kiri, klik <b>Render ulang</b> atau tekan <code>Ctrl+S</code>.</li>
        <li>Semua perubahan tersimpan otomatis di browser (localStorage).</li>
        <li><b>Unduh .md</b> = file canonical baru untuk dikirim ke AI (tempel ke <code>/root/ai-team/docs/truth-map.md</code>).</li>
        <li><b>Unduh patch JSON</b> = daftar edit + hash, dibaca AI lewat <code>sync_map.py read-patch</code>.</li>
        <li>Versi visual Excalidraw: <code>truth-map.excalidraw</code> — impor ke excalidraw.com, edit di UI, lalu kirim balik file-nya ke AI.</li>
      </ul>
      <div class="legend">
        <span class="badge ok">runtime = sumber kebenaran</span>
        <span class="badge">dokumentasi = manual, bisa basi</span>
        <span class="badge edit">kuning = UP</span>
        <span class="badge">merah = DOWN</span>
      </div>
    </div>
  </div>
__SECTIONS__
</main>
<div id="toast"></div>
<script>__MERMAID_JS__</script>
<script>
const KEY='truthmap.v1';
const state={blocks:__BLOCKS__};
let dirty=false;

function save(){localStorage.setItem(KEY,JSON.stringify(state.blocks));}
function load(){try{const v=localStorage.getItem(KEY);if(v)state.blocks=JSON.parse(v);}catch(e){}}

function toast(m){const t=document.getElementById('toast');t.textContent=m;
t.classList.add('on');setTimeout(()=>t.classList.remove('on'),1900);}

async function renderAll(){
  mermaid.initialize({startOnLoad:false,theme:'dark',securityLevel:'loose',
    themeVariables:{fontFamily:'ui-monospace,Menlo,monospace',fontSize:'13px',
      primaryColor:'#16202b',primaryTextColor:'#e6edf3',primaryBorderColor:'#74c0fc',
      lineColor:'#5a6b7d',secondaryColor:'#1c2530',tertiaryColor:'#141b22'}});
  for(const b of state.blocks){
    if(b.kind!=='mermaid')continue;
    const ta=document.getElementById('ta-'+b.id), host=document.getElementById('rv-'+b.id);
    if(!ta||!host)continue;
    const src=ta.value;
    try{
      const {svg}=await mermaid.render('g_'+b.id+'_'+Date.now(),src);
      host.innerHTML=svg;
    }catch(e){
      host.innerHTML='<div class="err">Render gagal:\\n'+(e&&e.message?e.message:String(e))+'</div>';
    }
  }
}

function markDirty(){dirty=true;document.getElementById('dirty').textContent='ada edit belum disimpan';}
function markClean(){dirty=false;document.getElementById('dirty').textContent='tersimpan lokal';}

function mdFromBlocks(){
  const out=[];
  for(const b of state.blocks){
    if(b.kind==='mermaid'){out.push('```mermaid\n'+b.src+'\n```');}
    else if(b.kind==='heading'){out.push(b.src);}
    else if(b.kind==='table'){out.push(b.src);}
    else if(b.kind==='code'){out.push('```\n'+b.src+'\n```');}
    else{out.push(b.src);}
  }
  return out.join('\n\n')+'\n';
}

function download(name,text,mime){
  const b=new Blob([text],{type:mime||'text/plain'});
  const a=document.createElement('a');a.href=URL.createObjectURL(b);a.download=name;
  document.body.appendChild(a);a.click();a.remove();
  setTimeout(()=>URL.revokeObjectURL(a.href),4000);
}

function patchObj(){
  const p={file:'truth-map.md',generated_at:new Date().toISOString(),
    tool:'truth-map.html',diagrams:{}};
  state.blocks.forEach(b=>{if(b.kind==='mermaid')p.diagrams[b.id]=b.src;});
  p.full_md=mdFromBlocks();
  return p;
}

document.getElementById('btn-render').onclick=()=>{renderAll();toast('dirender ulang');};
document.getElementById('btn-md').onclick=()=>{
  save();download('truth-map.md',mdFromBlocks(),'text/markdown');
  markClean();toast('truth-map.md terunduh');
};
document.getElementById('btn-patch').onclick=()=>{
  save();download('truth-map.edits.json',JSON.stringify(patchObj(),null,2),'application/json');
  toast('patch JSON terunduh');
};
document.addEventListener('keydown',e=>{
  if((e.ctrlKey||e.metaKey)&&e.key==='s'){e.preventDefault();renderAll();save();markClean();toast('tersimpan + dirender');}
});
document.querySelectorAll('textarea').forEach(t=>{
  t.addEventListener('input',()=>{markDirty();save();});
});
load();
state.blocks.forEach(b=>{if(b.kind==='mermaid'){
  const ta=document.getElementById('ta-'+b.id);if(ta)ta.value=b.src;}});
renderAll();
</script>
</body>
</html>
"""


def build_html():
    text = MD.read_text()
    parts = md_to_html(text)
    secs, dia = [], 0
    body_html = []
    for p in parts:
        if p["kind"] == "mermaid":
            dia += 1
            did = f"dia{dia}"
            secs.append(f"""
  <div class="card" data-dia="{did}">
    <h2>Diagram {dia} <span class="tag">mermaid — bisa diedit</span></h2>
    <div class="body editwrap">
      <div>
        <textarea id="ta-{did}" spellcheck="false">{p["src"]}</textarea>
        <div class="hint">Source Mermaid. Ubah di sini &rarr; <b>Render ulang</b>. <code>Ctrl+S</code> = simpan + render.</div>
      </div>
      <div><div class="rend" id="rv-{did}"></div></div>
    </div>
  </div>""")
            body_html.append(("mermaid", did))
        elif p["kind"] == "heading":
            lvl = len(p["src"]) - len(p["src"].lstrip("#"))
            body_html.append(("html", f"<h{lvl}>{p['src'].lstrip('#').strip()}</h{lvl}>"))
        elif p["kind"] == "table":
            body_html.append(("html", _table_html(p["src"])))
        elif p["kind"] == "code":
            body_html.append(("html", f"<pre>{_esc(p['src'])}</pre>"))
        else:
            body_html.append(("html", _md_inline(p["src"])))

    # tables + prose are rendered in one "docs" card after diagrams
    prose = "\n".join(h for k, h in body_html if k == "html")
    html = HTML_TMPL.replace("__TITLE__", "Truth Map — AI Team Ical")
    html = html.replace("__SECTIONS__", "\n".join(secs) + f"""
  <div class="card">
    <h2>Dokumen <span class="tag">isi truth-map.md</span></h2>
    <div class="body" id="prose">{prose}</div>
  </div>""")
    js = MERMAID_JS.read_text() if MERMAID_JS.exists() else ""
    html = html.replace("__MERMAID_JS__", js)
    blocks_json = []
    n = 0
    for p in parts:
        if p["kind"] == "mermaid":
            n += 1
            blocks_json.append({"kind": "mermaid", "id": f"dia{n}", "src": p["src"]})
        elif p["kind"] == "heading":
            blocks_json.append({"kind": "heading", "src": p["src"]})
        elif p["kind"] == "table":
            blocks_json.append({"kind": "table", "src": p["src"]})
        elif p["kind"] == "code":
            blocks_json.append({"kind": "code", "src": p["src"]})
        else:
            blocks_json.append({"kind": "text", "src": p["src"]})
    html = html.replace("__BLOCKS__", json.dumps(blocks_json, ensure_ascii=False))
    HTML.write_text(html)
    return len(html), len(blocks_json)


def _esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def _table_html(rows):
    lines = [r for r in rows.split("\n") if r.strip()]
    if len(lines) < 2:
        return "<pre>" + _esc(rows) + "</pre>"
    def cells(r):
        return [c.strip() for c in r.strip().strip("|").split("|")]
    head = cells(lines[0])
    body = [cells(r) for r in lines[2:]] if len(lines) > 2 else []
    out = ["<table><thead><tr>"]
    out += [f"<th>{_esc(h)}</th>" for h in head]
    out.append("</tr></thead><tbody>")
    for r in body:
        out.append("<tr>" + "".join(f"<td>{_md_inline(c)}</td>" for c in r) + "</tr>")
    out.append("</tbody></table>")
    return "".join(out)


def _md_inline(s):
    s = _esc(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<i>\1</i>", s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"^&gt; (.+)$", r"<span style='color:#8b98a5'>\1</span>", s, flags=re.M)
    s = s.replace("\n", "<br>")
    return s


# ------------------------------------------------- read user's excalidraw
def read_excalidraw(path):
    """Extract boxes, labels, edges from an .excalidraw file -> markdown."""
    d = json.loads(Path(path).read_text())
    els = d.get("elements", [])
    by_id = {e["id"]: e for e in els}
    boxes, edges, loose = [], [], []
    for e in els:
        if e.get("isDeleted"):
            continue
        if e["type"] == "text":
            cont = e.get("containerId")
            if cont and cont in by_id:
                continue
            loose.append(e.get("text", ""))
        elif e["type"] == "rectangle":
            lab = ""
            for t in els:
                if t["type"] == "text" and t.get("containerId") == e["id"]:
                    lab = t.get("text", "")
                    break
            boxes.append({
                "x": round(e["x"]), "y": round(e["y"]),
                "w": round(e["width"]), "h": round(e["height"]),
                "stroke": e.get("strokeColor"), "bg": e.get("backgroundColor"),
                "text": lab,
            })
        elif e["type"] == "arrow":
            p = e.get("points") or [[0, 0]]
            lab = ""
            for t in els:
                if t["type"] == "text" and t.get("containerId") == e["id"]:
                    lab = t.get("text", "")
                    break
            edges.append({
                "from": (round(e["x"] + p[0][0]), round(e["y"] + p[0][1])),
                "to": (round(e["x"] + p[-1][0]), round(e["y"] + p[-1][1])),
                "label": lab, "stroke": e.get("strokeColor"),
                "dashed": e.get("strokeStyle") == "dashed",
            })

    out = [f"# Hasil edit Excalidraw — {Path(path).name}", "",
           f"_Diekspor {len(boxes)} box, {len(edges)} garis, {len(loose)} label bebas._", "",
           "## Boxes (urutan kiri-atas)", "",
           "| # | x | y | w | h | teks |", "|---|---|---|---|---|---|"]
    for i, b in enumerate(sorted(boxes, key=lambda z: (z["y"], z["x"])), 1):
        t = b["text"].replace("\n", " / ") or "(kosong)"
        out.append(f"| {i} | {b['x']} | {b['y']} | {b['w']} | {b['h']} | {t} |")
    out += ["", "## Lines / edges", "", "| # | dari | ke | label | style |", "|---|---|---|---|---|"]
    for i, a in enumerate(sorted(edges, key=lambda z: (z["from"][1], z["from"][0])), 1):
        l = a["label"].replace("\n", " / ") or "-"
        st = ("dashed" if a["dashed"] else "solid") + f" `{a['stroke']}`"
        out.append(f"| {i} | {a['from']} | {a['to']} | {l} | {st} |")
    if loose:
        out += ["", "## Label bebas (tidak dalam box)", ""]
        out += [f"- {t.replace(chr(10), ' / ')}" for t in loose if t.strip()]
    out += ["", "## Diff vs truth-map.md (judul yang berubah)", "",
            "_Bandingkan isi kolom 'teks' di tabel Boxes dengan truth-map.md — "
            "bagian yang tidak ada di md = tambahan baru._", ""]
    return "\n".join(out)


def read_patch(path):
    p = json.loads(Path(path).read_text())
    out = [f"# Patch dari editor — {Path(path).name}", "",
           f"_generated_at: {p.get('generated_at')}_", ""]
    for k, v in (p.get("diagrams") or {}).items():
        out += [f"## {k}", "", "```mermaid", v, "```", ""]
    if p.get("full_md"):
        out += ["## Full markdown (siap pakai)", "", "```markdown", p["full_md"], "```"]
    return "\n".join(out)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "html"
    if cmd == "html":
        size, nblocks = build_html()
        print(f"OK html {size/1024:.0f}KB, {nblocks} blocks → {HTML}")
    elif cmd == "read-excalidraw":
        src = sys.argv[2] if len(sys.argv) > 2 else EXCAL
        dst = DOCS / "edits-from-excalidraw.md"
        dst.write_text(read_excalidraw(src))
        print(f"OK → {dst}")
    elif cmd == "read-patch":
        src = sys.argv[2]
        dst = DOCS / "edits-from-patch.md"
        dst.write_text(read_patch(src))
        print(f"OK → {dst}")
    else:
        print(__doc__)
        sys.exit(1)
