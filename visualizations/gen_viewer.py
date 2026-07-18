# -*- coding: utf-8 -*-
import csv, json, os

CSV = r"C:\Users\photc\Developer\Jamming\CALiPPSO.jl\packing_d3_N512.csv"
OUT = r"C:\Users\photc\AppData\Local\Temp\claude\C--Users-photc-Developer-Jamming\7b1340e8-f48f-4bbf-ae6a-549e6fdda82e\scratchpad\packing_viewer.html"

# --- read metadata + rows ---
meta = {}
rows = []
with open(CSV, "r") as f:
    header = f.readline().strip().lstrip("#").strip()
    for tok in header.split():
        k, v = tok.split("=")
        meta[k] = v
    f.readline()  # column header line
    for line in f:
        line = line.strip()
        if not line:
            continue
        x, y, z, c = line.split(",")
        rows.append((round(float(x), 4), round(float(y), 4), round(float(z), 4), int(c)))

N = len(rows)
R = float(meta["R"])
L = float(meta["L"])
phi = float(meta["phi"])

# flat data array: x,y,z,coord repeated
flat = []
for (x, y, z, c) in rows:
    flat.extend([x, y, z, c])

coords = [r[3] for r in rows]
rattlers = sum(1 for c in coords if c == 0)
nonr = N - rattlers
nz = [c for c in coords if c > 0]
meanz = sum(nz) / len(nz)
contacts = round(sum(coords) / 2)   # sum of z / 2

data_js = json.dumps(flat, separators=(",", ":"))

meta_js = json.dumps({
    "N": N, "R": round(R, 6), "L": L, "phi": round(phi, 5),
    "rattlers": rattlers, "nonr": nonr, "meanz": round(meanz, 3),
    "contacts": contacts, "zmin": min(nz), "zmax": max(nz),
})

HTML = r"""<title>Jammed Sphere Packing — N=512, phi=0.6305</title>
<style>
  :root{
    --bg:#0b0e14; --bg2:#0f141d; --panel:#141b26; --panel2:#1b2431;
    --line:#26303f; --ink:#dfe6ef; --muted:#8a97a8; --faint:#5c6675;
    --accent:#e0a458; --accent-dim:#a87a3f;
    --box:#3b4757; --grid:#1a2330;
    --shadow:0 1px 0 rgba(255,255,255,.03), 0 8px 30px rgba(0,0,0,.45);
    --mono:ui-monospace,"SFMono-Regular","Cascadia Code",Menlo,Consolas,"Liberation Mono",monospace;
    --sans:ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  }
  @media (prefers-color-scheme: light){
    :root{
      --bg:#eef1f5; --bg2:#e6eaf0; --panel:#ffffff; --panel2:#f3f6fa;
      --line:#d5dce5; --ink:#1a2230; --muted:#5a6675; --faint:#8a95a4;
      --accent:#b9762a; --accent-dim:#caa06a; --box:#9aa7b8; --grid:#dde3ec;
      --shadow:0 1px 0 rgba(255,255,255,.6), 0 10px 30px rgba(30,45,70,.10);
    }
  }
  :root[data-theme="dark"]{
    --bg:#0b0e14; --bg2:#0f141d; --panel:#141b26; --panel2:#1b2431;
    --line:#26303f; --ink:#dfe6ef; --muted:#8a97a8; --faint:#5c6675;
    --accent:#e0a458; --accent-dim:#a87a3f; --box:#3b4757; --grid:#1a2330;
    --shadow:0 1px 0 rgba(255,255,255,.03), 0 8px 30px rgba(0,0,0,.45);
  }
  :root[data-theme="light"]{
    --bg:#eef1f5; --bg2:#e6eaf0; --panel:#ffffff; --panel2:#f3f6fa;
    --line:#d5dce5; --ink:#1a2230; --muted:#5a6675; --faint:#8a95a4;
    --accent:#b9762a; --accent-dim:#caa06a; --box:#9aa7b8; --grid:#dde3ec;
    --shadow:0 1px 0 rgba(255,255,255,.6), 0 10px 30px rgba(30,45,70,.10);
  }

  *{box-sizing:border-box}
  body{margin:0;background:radial-gradient(120% 120% at 70% 10%,var(--bg2),var(--bg));
    color:var(--ink);font-family:var(--sans);min-height:100vh}
  .wrap{max-width:1180px;margin:0 auto;padding:22px 20px 40px;display:flex;flex-direction:column;gap:16px}

  header{display:flex;flex-wrap:wrap;align-items:flex-end;justify-content:space-between;gap:14px}
  .eyebrow{font-family:var(--mono);font-size:11.5px;letter-spacing:.18em;text-transform:uppercase;
    color:var(--accent);margin:0 0 6px}
  h1{font-size:clamp(20px,3.4vw,29px);line-height:1.08;margin:0;font-weight:650;letter-spacing:-.01em;text-wrap:balance}
  h1 .var{font-family:var(--mono);color:var(--muted);font-weight:500}
  .sub{color:var(--muted);font-size:13.5px;margin:8px 0 0;max-width:60ch;line-height:1.5}

  .metricbar{display:flex;flex-wrap:wrap;gap:1px;background:var(--line);border:1px solid var(--line);
    border-radius:12px;overflow:hidden;box-shadow:var(--shadow)}
  .metric{background:var(--panel);padding:10px 15px;flex:1 1 auto;min-width:96px}
  .metric .k{font-family:var(--mono);font-size:10.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--faint)}
  .metric .v{font-family:var(--mono);font-size:18px;font-variant-numeric:tabular-nums;margin-top:3px;font-weight:600}
  .metric .v.good{color:var(--accent)}
  .metric .v small{font-size:11px;color:var(--muted);font-weight:400}

  .stage{display:grid;grid-template-columns:1fr 250px;gap:14px}
  @media (max-width:760px){.stage{grid-template-columns:1fr}}

  .canvaswrap{position:relative;background:
      linear-gradient(180deg,var(--panel2),var(--panel));
    border:1px solid var(--line);border-radius:14px;overflow:hidden;box-shadow:var(--shadow);
    aspect-ratio:1/1;min-height:340px;touch-action:none;cursor:grab}
  .canvaswrap.drag{cursor:grabbing}
  canvas{display:block;width:100%;height:100%}
  .hint{position:absolute;left:12px;bottom:10px;font-family:var(--mono);font-size:10.5px;color:var(--faint);
    letter-spacing:.03em;pointer-events:none;user-select:none}
  .fps{position:absolute;right:12px;top:10px;font-family:var(--mono);font-size:10px;color:var(--faint)}

  .panel{background:var(--panel);border:1px solid var(--line);border-radius:14px;box-shadow:var(--shadow);
    padding:14px;display:flex;flex-direction:column;gap:16px;align-self:start}
  .grouplabel{font-family:var(--mono);font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;
    color:var(--faint);margin:0 0 8px}

  .seg{display:flex;flex-direction:column;gap:6px}
  .segbtns{display:flex;background:var(--panel2);border:1px solid var(--line);border-radius:9px;padding:3px;gap:3px}
  .segbtns button{flex:1;font-family:var(--mono);font-size:11px;letter-spacing:.02em;color:var(--muted);
    background:transparent;border:0;border-radius:6px;padding:7px 4px;cursor:pointer;transition:.15s}
  .segbtns button:hover{color:var(--ink)}
  .segbtns button[aria-pressed="true"]{background:var(--accent);color:#1a1204;font-weight:600}
  :root[data-theme="light"] .segbtns button[aria-pressed="true"]{color:#fff}
  @media (prefers-color-scheme:light){.segbtns button[aria-pressed="true"]{color:#fff}}

  .toggle{display:flex;align-items:center;justify-content:space-between;gap:10px;cursor:pointer;
    font-size:13px;color:var(--ink);user-select:none}
  .toggle .sw{width:36px;height:20px;border-radius:20px;background:var(--panel2);border:1px solid var(--line);
    position:relative;flex:none;transition:.18s}
  .toggle .sw::after{content:"";position:absolute;top:2px;left:2px;width:14px;height:14px;border-radius:50%;
    background:var(--faint);transition:.18s}
  .toggle input{position:absolute;opacity:0;width:0;height:0}
  .toggle input:checked + .sw{background:var(--accent);border-color:var(--accent)}
  .toggle input:checked + .sw::after{left:18px;background:#1a1204}
  .toggle input:focus-visible + .sw{outline:2px solid var(--accent);outline-offset:2px}

  .resetbtn{font-family:var(--mono);font-size:11.5px;color:var(--muted);background:var(--panel2);
    border:1px solid var(--line);border-radius:9px;padding:9px;cursor:pointer;transition:.15s;letter-spacing:.03em}
  .resetbtn:hover{color:var(--ink);border-color:var(--accent-dim)}

  .legend{display:flex;flex-direction:column;gap:8px}
  .legend .bar{height:12px;border-radius:6px;border:1px solid var(--line)}
  .legend .ends{display:flex;justify-content:space-between;font-family:var(--mono);font-size:10.5px;color:var(--muted)}
  .legend .note{font-size:11.5px;color:var(--muted);line-height:1.45}
  .legend .rat{display:flex;align-items:center;gap:7px;font-size:11.5px;color:var(--muted)}
  .legend .rat .dot{width:11px;height:11px;border-radius:50%;background:rgba(140,150,165,.5);
    border:1px solid var(--faint);flex:none}

  footer{color:var(--faint);font-size:11.5px;font-family:var(--mono);line-height:1.6;
    border-top:1px solid var(--line);padding-top:14px}
  footer b{color:var(--muted);font-weight:600}
  @media (prefers-reduced-motion:reduce){*{transition:none!important}}
</style>

<div class="wrap">
  <header>
    <div>
      <p class="eyebrow">CALiPPSO &middot; Linear-programming jamming</p>
      <h1>Jammed hard-sphere packing <span class="var">d=3, N=512</span></h1>
      <p class="sub">A monodisperse packing driven from a random gas (&phi;=0.30) to the jamming point by
        iterated linear programming. Each sphere is shaded and depth-sorted; drag to rotate the periodic unit cell.</p>
    </div>
  </header>

  <div class="metricbar" id="metricbar"></div>

  <div class="stage">
    <div class="canvaswrap" id="stage">
      <canvas id="cv"></canvas>
      <div class="fps" id="fps"></div>
      <div class="hint">drag &middot; rotate  &nbsp;|&nbsp;  scroll &middot; zoom</div>
    </div>

    <aside class="panel">
      <div class="seg">
        <p class="grouplabel">Colour by</p>
        <div class="segbtns" id="colormode" role="group" aria-label="Colour mode">
          <button data-v="coord" aria-pressed="true">contacts&nbsp;z</button>
          <button data-v="depth" aria-pressed="false">depth</button>
          <button data-v="mono" aria-pressed="false">plain</button>
        </div>
      </div>

      <div style="display:flex;flex-direction:column;gap:11px">
        <label class="toggle"><span>Auto-rotate</span>
          <input type="checkbox" id="spin" checked><span class="sw"></span></label>
        <label class="toggle"><span>Unit cell</span>
          <input type="checkbox" id="box" checked><span class="sw"></span></label>
        <label class="toggle"><span>Fade rattlers</span>
          <input type="checkbox" id="fade" checked><span class="sw"></span></label>
      </div>

      <button class="resetbtn" id="reset">&#8635; reset view</button>

      <div class="legend" id="legend">
        <p class="grouplabel" style="margin:0">Contacts per sphere</p>
        <div class="bar" id="legbar"></div>
        <div class="ends"><span id="legmin">z=4</span><span>z=2d=6</span><span id="legmax">z=10</span></div>
        <div class="rat"><span class="dot"></span> rattlers (z=0), unconstrained</div>
        <div class="note">Isostaticity means each non-rattler carries just enough contacts to be rigid — mean z&nbsp;&rarr;&nbsp;2d.</div>
      </div>
    </aside>
  </div>

  <footer id="foot"></footer>
</div>

<script>
const DATA = __DATA__;
const META = __META__;
const $ = s => document.querySelector(s);

/* ---------- metric bar ---------- */
$("#metricbar").innerHTML = [
  ["particles N", META.N, ""],
  ["packing &phi;", META.phi, ""],
  ["radius R", META.R, ""],
  ["contacts", META.contacts, ""],
  ["mean z", META.meanz, "&nbsp;&asymp; 2d"],
  ["rattlers", META.rattlers, "&nbsp;/ "+META.N],
  ["isostatic", "yes", "GOOD"],
].map(([k,v,extra])=>{
  const good = extra==="GOOD";
  return `<div class="metric"><div class="k">${k}</div>
    <div class="v${good?' good':''}">${good?'&#10003; '+v:v}${!good&&extra?`<small>${extra}</small>`:''}</div></div>`;
}).join("");

$("#foot").innerHTML =
  `<b>method</b> CALiPPSO (iterative LP), HiGHS interior-point solver &nbsp;&middot;&nbsp; `+
  `<b>system</b> ${META.N} monodisperse spheres, periodic cube L=${META.L} &nbsp;&middot;&nbsp; `+
  `<b>result</b> isostatic packing, ${META.contacts} contacts among ${META.nonr} non-rattlers, `+
  `mean z=${META.meanz}, ${META.rattlers} rattlers (${(100*META.rattlers/META.N).toFixed(2)}%).`;

/* ---------- viridis colour scale ---------- */
const STOPS = [[68,1,84],[59,82,139],[33,145,140],[94,201,98],[253,231,37]];
function viridis(t){
  t=Math.max(0,Math.min(1,t)); const x=t*(STOPS.length-1); const i=Math.floor(x); const f=x-i;
  const a=STOPS[i], b=STOPS[Math.min(i+1,STOPS.length-1)];
  return [a[0]+(b[0]-a[0])*f, a[1]+(b[1]-a[1])*f, a[2]+(b[2]-a[2])*f];
}
// paint legend bar
(()=>{ const stops=[]; for(let i=0;i<=6;i++){const c=viridis(i/6);stops.push(`rgb(${c.map(Math.round).join(",")}) ${i/6*100}%`);}
  $("#legbar").style.background=`linear-gradient(90deg,${stops.join(",")})`;
  $("#legmin").textContent="z="+META.zmin; $("#legmax").textContent="z="+META.zmax; })();

/* ---------- geometry ---------- */
const N=META.N, L=META.L, R=META.R;
// centre positions about origin
const P=new Float32Array(N*3), COORD=new Int8Array(N);
let cx=0,cy=0,cz=0;
for(let i=0;i<N;i++){ P[i*3]=DATA[i*4]-L/2; P[i*3+1]=DATA[i*4+1]-L/2; P[i*3+2]=DATA[i*4+2]-L/2; COORD[i]=DATA[i*4+3]; }
const zmin=META.zmin, zspan=Math.max(1,META.zmax-META.zmin);

// unit-cube edges (as index pairs of the 8 corners)
const H=L/2, CORN=[], EDG=[];
for(let s=0;s<8;s++) CORN.push([ (s&1?H:-H),(s&2?H:-H),(s&4?H:-H) ]);
for(let a=0;a<8;a++) for(let b=a+1;b<8;b++){ let d=0; for(let k=0;k<3;k++) if(CORN[a][k]!==CORN[b][k]) d++; if(d===1) EDG.push([a,b]); }

/* ---------- view state ---------- */
let yaw=0.6, pitch=-0.45, zoom=1, spin=true, showBox=true, fadeRat=true, colorMode="coord";
const cv=$("#cv"), ctx=cv.getContext("2d"); let W=0,Hh=0,DPR=1;
function syncSize(){ const r=cv.getBoundingClientRect(); DPR=Math.min(2,window.devicePixelRatio||1);
  const w=Math.round(r.width), h=Math.round(r.height); if(w<=0||h<=0) return;
  W=w; Hh=h; const bw=w*DPR, bh=h*DPR;
  if(cv.width!==bw||cv.height!==bh){ cv.width=bw; cv.height=bh; }
  ctx.setTransform(DPR,0,0,DPR,0,0); }
syncSize();

const FOCAL=3.0;               // camera distance (in box units)
const LIGHT=[-0.5,0.7,0.6];    // light direction (screen space)
(()=>{const n=Math.hypot(...LIGHT);LIGHT[0]/=n;LIGHT[1]/=n;LIGHT[2]/=n;})();

function rot(x,y,z){
  const cyaw=Math.cos(yaw),syaw=Math.sin(yaw);
  let X=cyaw*x+syaw*z, Z=-syaw*x+cyaw*z;
  const cp=Math.cos(pitch),sp=Math.sin(pitch);
  let Y=cp*y-sp*Z; Z=sp*y+cp*Z;
  return [X,Y,Z];
}

const prim=[];
function frame(){
  syncSize();
  ctx.clearRect(0,0,W,Hh);
  const base=Math.min(W,Hh)*0.46*zoom;
  const ox=W/2, oy=Hh/2;
  prim.length=0;

  for(let i=0;i<N;i++){
    const [X,Y,Z]=rot(P[i*3],P[i*3+1],P[i*3+2]);
    const persp=FOCAL/(FOCAL-Z);
    if(persp<=0) continue;
    const sx=ox+X*base*persp, sy=oy-Y*base*persp, sr=R*base*persp;
    prim.push({t:0,z:Z,sx,sy,sr,i});
  }
  if(showBox){
    for(const [a,b] of EDG){
      const ra=rot(...CORN[a]), rb=rot(...CORN[b]);
      const pa=FOCAL/(FOCAL-ra[2]), pb=FOCAL/(FOCAL-rb[2]);
      prim.push({t:1,z:(ra[2]+rb[2])/2,
        x1:ox+ra[0]*base*pa, y1:oy-ra[1]*base*pa,
        x2:ox+rb[0]*base*pb, y2:oy-rb[1]*base*pb});
    }
  }
  prim.sort((p,q)=>p.z-q.z);

  for(const p of prim){
    if(p.t===1){
      ctx.strokeStyle=getComputedStyle(document.documentElement).getPropertyValue('--box').trim()||"#3b4757";
      ctx.globalAlpha=0.55; ctx.lineWidth=1.1;
      ctx.beginPath(); ctx.moveTo(p.x1,p.y1); ctx.lineTo(p.x2,p.y2); ctx.stroke();
      ctx.globalAlpha=1;
      continue;
    }
    const i=p.i, z=COORD[i], isRat=(z===0);
    let col;
    if(colorMode==="mono") col=[150,163,181];
    else if(colorMode==="depth"){ const t=(p.z+H)/(2*H); col=viridis(t); }
    else col= isRat ? [140,150,165] : viridis((z-zmin)/zspan);

    let alpha=1;
    if(isRat && fadeRat) alpha=0.28;
    drawSphere(p.sx,p.sy,p.sr,col,alpha,isRat);
  }
}

function drawSphere(sx,sy,r,col,alpha,isRat){
  if(r<0.4) return;
  const [cr,cg,cb]=col;
  // light offset for highlight
  const hx=sx - LIGHT[0]*r*0.55, hy=sy - LIGHT[1]*r*0.55;
  const g=ctx.createRadialGradient(hx,hy,r*0.08, sx,sy,r*1.02);
  const hi=(v)=>Math.min(255, v+90), lo=(v)=>v*0.32;
  g.addColorStop(0,`rgba(${hi(cr)},${hi(cg)},${hi(cb)},${alpha})`);
  g.addColorStop(0.45,`rgba(${cr},${cg},${cb},${alpha})`);
  g.addColorStop(1,`rgba(${lo(cr)|0},${lo(cg)|0},${lo(cb)|0},${alpha})`);
  ctx.beginPath(); ctx.arc(sx,sy,r,0,6.2832); ctx.fillStyle=g; ctx.fill();
  // subtle rim
  ctx.globalAlpha=alpha*0.5; ctx.lineWidth=Math.max(0.5,r*0.05);
  ctx.strokeStyle=`rgba(${lo(cr)|0},${lo(cg)|0},${lo(cb)|0},1)`; ctx.stroke();
  ctx.globalAlpha=1;
}

/* ---------- animation loop w/ fps ---------- */
let last=performance.now(), fpsAcc=0, fpsN=0;
function loop(now){
  const dt=Math.min(0.05,(now-last)/1000); last=now;
  if(spin) yaw += dt*0.35;
  frame();
  fpsAcc+=1/Math.max(1e-3,dt); fpsN++;
  if(fpsN>=20){ $("#fps").textContent=Math.round(fpsAcc/fpsN)+" fps"; fpsAcc=0;fpsN=0; }
  requestAnimationFrame(loop);
}
requestAnimationFrame(loop);

/* ---------- interaction ---------- */
const stage=$("#stage"); let dragging=false, lx=0, ly=0;
stage.addEventListener("pointerdown",e=>{dragging=true;lx=e.clientX;ly=e.clientY;stage.classList.add("drag");
  stage.setPointerCapture(e.pointerId); spin=false; $("#spin").checked=false;});
stage.addEventListener("pointermove",e=>{ if(!dragging)return;
  yaw += (e.clientX-lx)*0.008; pitch += (e.clientY-ly)*0.008;
  pitch=Math.max(-1.5,Math.min(1.5,pitch)); lx=e.clientX; ly=e.clientY; });
addEventListener("pointerup",()=>{dragging=false;stage.classList.remove("drag");});
stage.addEventListener("wheel",e=>{e.preventDefault(); zoom*=Math.exp(-e.deltaY*0.0012);
  zoom=Math.max(0.45,Math.min(3.5,zoom));},{passive:false});

$("#spin").addEventListener("change",e=>spin=e.target.checked);
$("#box").addEventListener("change",e=>showBox=e.target.checked);
$("#fade").addEventListener("change",e=>fadeRat=e.target.checked);
$("#colormode").addEventListener("click",e=>{const b=e.target.closest("button"); if(!b)return;
  colorMode=b.dataset.v; [...e.currentTarget.children].forEach(x=>x.setAttribute("aria-pressed", x===b));
  const leg=$("#legend"); leg.style.opacity = colorMode==="coord"?1:0.4;});
$("#reset").addEventListener("click",()=>{yaw=0.6;pitch=-0.45;zoom=1;spin=true;$("#spin").checked=true;});
</script>
"""

HTML = HTML.replace("__DATA__", data_js).replace("__META__", meta_js)
with open(OUT, "w", encoding="utf-8") as f:
    f.write(HTML)
print("WROTE", OUT, os.path.getsize(OUT), "bytes")
