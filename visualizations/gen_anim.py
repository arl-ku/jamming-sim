# -*- coding: utf-8 -*-
import json, os

SRC = r"C:\Users\photc\Developer\Jamming\CALiPPSO.jl\packing_trajectory.json"
OUT = r"C:\Users\photc\AppData\Local\Temp\claude\C--Users-photc-Developer-Jamming\7b1340e8-f48f-4bbf-ae6a-549e6fdda82e\scratchpad\packing_animation.html"

with open(SRC, "r", encoding="utf-8") as f:
    traj = json.load(f)

# compact re-serialize (already rounded in Julia)
traj_js = json.dumps(traj, separators=(",", ":"))
print("frames kept:", len(traj["frames"]), "N:", traj["N"],
      "phi:", traj["phi0"], "->", round(traj["phiFinal"], 4))

HTML = r"""<title>Watching a hard-sphere packing jam — CALiPPSO</title>
<style>
  :root{
    --bg:#0b0e14; --bg2:#0f141d; --panel:#141b26; --panel2:#1b2431;
    --line:#26303f; --ink:#dfe6ef; --muted:#8a97a8; --faint:#5c6675;
    --accent:#e0a458; --accent-dim:#a87a3f; --box:#3b4757;
    --shadow:0 1px 0 rgba(255,255,255,.03), 0 8px 30px rgba(0,0,0,.45);
    --mono:ui-monospace,"SFMono-Regular","Cascadia Code",Menlo,Consolas,"Liberation Mono",monospace;
    --sans:ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  }
  @media (prefers-color-scheme: light){
    :root{ --bg:#eef1f5; --bg2:#e6eaf0; --panel:#fff; --panel2:#f3f6fa; --line:#d5dce5;
      --ink:#1a2230; --muted:#5a6675; --faint:#8a95a4; --accent:#b9762a; --accent-dim:#caa06a; --box:#9aa7b8;
      --shadow:0 1px 0 rgba(255,255,255,.6), 0 10px 30px rgba(30,45,70,.10);}
  }
  :root[data-theme="dark"]{ --bg:#0b0e14; --bg2:#0f141d; --panel:#141b26; --panel2:#1b2431; --line:#26303f;
    --ink:#dfe6ef; --muted:#8a97a8; --faint:#5c6675; --accent:#e0a458; --accent-dim:#a87a3f; --box:#3b4757;
    --shadow:0 1px 0 rgba(255,255,255,.03), 0 8px 30px rgba(0,0,0,.45);}
  :root[data-theme="light"]{ --bg:#eef1f5; --bg2:#e6eaf0; --panel:#fff; --panel2:#f3f6fa; --line:#d5dce5;
    --ink:#1a2230; --muted:#5a6675; --faint:#8a95a4; --accent:#b9762a; --accent-dim:#caa06a; --box:#9aa7b8;
    --shadow:0 1px 0 rgba(255,255,255,.6), 0 10px 30px rgba(30,45,70,.10);}

  *{box-sizing:border-box}
  body{margin:0;background:radial-gradient(120% 120% at 70% 8%,var(--bg2),var(--bg));color:var(--ink);
    font-family:var(--sans);min-height:100vh}
  .wrap{max-width:1120px;margin:0 auto;padding:22px 20px 40px;display:flex;flex-direction:column;gap:16px}
  .eyebrow{font-family:var(--mono);font-size:11.5px;letter-spacing:.18em;text-transform:uppercase;color:var(--accent);margin:0 0 6px}
  h1{font-size:clamp(20px,3.4vw,29px);line-height:1.08;margin:0;font-weight:650;letter-spacing:-.01em;text-wrap:balance}
  h1 .var{font-family:var(--mono);color:var(--muted);font-weight:500}
  .sub{color:var(--muted);font-size:13.5px;margin:8px 0 0;max-width:64ch;line-height:1.5}

  .stage{display:grid;grid-template-columns:1fr 232px;gap:14px}
  @media (max-width:760px){.stage{grid-template-columns:1fr}}
  .canvaswrap{position:relative;background:linear-gradient(180deg,var(--panel2),var(--panel));
    border:1px solid var(--line);border-radius:14px;overflow:hidden;box-shadow:var(--shadow);
    aspect-ratio:1/1;min-height:330px;touch-action:none;cursor:grab}
  .canvaswrap.drag{cursor:grabbing}
  canvas{display:block;width:100%;height:100%}
  .badge{position:absolute;left:12px;top:11px;font-family:var(--mono);font-size:11px;letter-spacing:.03em;
    color:var(--ink);background:rgba(10,14,20,.55);border:1px solid var(--line);border-radius:8px;
    padding:5px 9px;pointer-events:none;backdrop-filter:blur(4px)}
  :root[data-theme="light"] .badge{background:rgba(255,255,255,.7)}
  @media(prefers-color-scheme:light){.badge{background:rgba(255,255,255,.7)}}
  .phase{position:absolute;right:12px;top:11px;font-family:var(--mono);font-size:10.5px;letter-spacing:.06em;
    text-transform:uppercase;color:var(--accent);background:rgba(10,14,20,.5);border-radius:8px;padding:5px 9px;pointer-events:none}
  .hint{position:absolute;left:12px;bottom:10px;font-family:var(--mono);font-size:10.5px;color:var(--faint);pointer-events:none;user-select:none}

  .panel{background:var(--panel);border:1px solid var(--line);border-radius:14px;box-shadow:var(--shadow);
    padding:14px;display:flex;flex-direction:column;gap:15px;align-self:start}
  .grouplabel{font-family:var(--mono);font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--faint);margin:0 0 8px}

  .phi{display:flex;flex-direction:column;gap:7px}
  .phi .row{display:flex;justify-content:space-between;align-items:baseline}
  .phi .big{font-family:var(--mono);font-size:26px;font-weight:650;font-variant-numeric:tabular-nums;color:var(--accent)}
  .phi .cap{font-family:var(--mono);font-size:10.5px;color:var(--faint);letter-spacing:.06em}
  .meter{height:8px;border-radius:6px;background:var(--panel2);border:1px solid var(--line);overflow:hidden;position:relative}
  .meter .fill{height:100%;background:linear-gradient(90deg,var(--accent-dim),var(--accent));width:0%}
  .meter .tick{position:absolute;top:-3px;bottom:-3px;width:1px;background:var(--faint);opacity:.6}
  .scale{display:flex;justify-content:space-between;font-family:var(--mono);font-size:10px;color:var(--faint)}

  .segbtns{display:flex;background:var(--panel2);border:1px solid var(--line);border-radius:9px;padding:3px;gap:3px}
  .segbtns button{flex:1;font-family:var(--mono);font-size:11px;color:var(--muted);background:transparent;border:0;border-radius:6px;padding:7px 4px;cursor:pointer;transition:.15s}
  .segbtns button:hover{color:var(--ink)}
  .segbtns button[aria-pressed="true"]{background:var(--accent);color:#1a1204;font-weight:600}
  :root[data-theme="light"] .segbtns button[aria-pressed="true"]{color:#fff}
  @media(prefers-color-scheme:light){.segbtns button[aria-pressed="true"]{color:#fff}}

  .toggle{display:flex;align-items:center;justify-content:space-between;gap:10px;cursor:pointer;font-size:13px;color:var(--ink);user-select:none}
  .toggle .sw{width:36px;height:20px;border-radius:20px;background:var(--panel2);border:1px solid var(--line);position:relative;flex:none;transition:.18s}
  .toggle .sw::after{content:"";position:absolute;top:2px;left:2px;width:14px;height:14px;border-radius:50%;background:var(--faint);transition:.18s}
  .toggle input{position:absolute;opacity:0;width:0;height:0}
  .toggle input:checked + .sw{background:var(--accent);border-color:var(--accent)}
  .toggle input:checked + .sw::after{left:18px;background:#1a1204}
  .toggle input:focus-visible + .sw{outline:2px solid var(--accent);outline-offset:2px}

  /* transport */
  .transport{display:flex;align-items:center;gap:13px;background:var(--panel);border:1px solid var(--line);
    border-radius:12px;padding:11px 14px;box-shadow:var(--shadow)}
  .play{flex:none;width:42px;height:42px;border-radius:50%;border:1px solid var(--accent-dim);background:var(--accent);
    color:#1a1204;cursor:pointer;display:grid;place-items:center;transition:.15s}
  :root[data-theme="light"] .play{color:#fff}
  @media(prefers-color-scheme:light){.play{color:#fff}}
  .play:hover{filter:brightness(1.08)}
  .play svg{width:16px;height:16px;display:block}
  .scrub{flex:1;display:flex;flex-direction:column;gap:5px}
  .scrub input[type=range]{width:100%;accent-color:var(--accent);cursor:pointer}
  .scrub .lab{display:flex;justify-content:space-between;font-family:var(--mono);font-size:10.5px;color:var(--muted)}
  .speed{display:flex;gap:4px;align-items:center;font-family:var(--mono);font-size:11px;color:var(--muted)}
  .speed button{font-family:var(--mono);font-size:11px;color:var(--muted);background:var(--panel2);border:1px solid var(--line);border-radius:7px;padding:5px 8px;cursor:pointer}
  .speed button[aria-pressed="true"]{background:var(--accent);color:#1a1204;font-weight:600;border-color:var(--accent)}
  :root[data-theme="light"] .speed button[aria-pressed="true"]{color:#fff}
  @media(prefers-color-scheme:light){.speed button[aria-pressed="true"]{color:#fff}}

  footer{color:var(--faint);font-size:11.5px;font-family:var(--mono);line-height:1.6;border-top:1px solid var(--line);padding-top:14px}
  footer b{color:var(--muted);font-weight:600}
  @media (prefers-reduced-motion:reduce){*{transition:none!important}}
</style>

<div class="wrap">
  <header>
    <p class="eyebrow">CALiPPSO &middot; the jamming process, iteration by iteration</p>
    <h1>Watching a hard-sphere packing jam <span class="var">d=3, N=512</span></h1>
    <p class="sub">Start from a loose random gas at &phi;=0.30. Each step solves a linear program that
      inflates every sphere and nudges it as far as it can go without overlaps. Repeat until nothing can move &mdash;
      the jammed, isostatic state at &phi;&asymp;0.63. Drag to rotate while it plays.</p>
  </header>

  <div class="stage">
    <div class="canvaswrap" id="stage">
      <canvas id="cv"></canvas>
      <div class="badge" id="badge"></div>
      <div class="phase" id="phase"></div>
      <div class="hint">drag &middot; rotate</div>
    </div>

    <aside class="panel">
      <div class="phi">
        <div class="row"><span class="cap">packing fraction &phi;</span></div>
        <div class="big" id="phival">0.300</div>
        <div class="meter"><div class="fill" id="phifill"></div><div class="tick" id="phitick"></div></div>
        <div class="scale"><span>0.30</span><span id="phiend">0.63</span></div>
      </div>

      <div>
        <p class="grouplabel">Colour spheres by</p>
        <div class="segbtns" id="colormode" role="group">
          <button data-v="depth" aria-pressed="true">depth</button>
          <button data-v="coord" aria-pressed="false">final z</button>
        </div>
      </div>

      <div style="display:flex;flex-direction:column;gap:11px">
        <label class="toggle"><span>Auto-rotate</span><input type="checkbox" id="spin"><span class="sw"></span></label>
        <label class="toggle"><span>Unit cell</span><input type="checkbox" id="box" checked><span class="sw"></span></label>
        <label class="toggle"><span>Loop</span><input type="checkbox" id="loop" checked><span class="sw"></span></label>
      </div>
    </aside>
  </div>

  <div class="transport">
    <button class="play" id="play" aria-label="Play/pause">
      <svg id="playicon" viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>
    </button>
    <div class="scrub">
      <input type="range" id="seek" min="0" max="1000" value="0" step="1">
      <div class="lab"><span id="iterlab">iteration 0</span><span id="pctlab">0%</span></div>
    </div>
    <div class="speed" id="speed">
      <button data-s="0.5">0.5&times;</button>
      <button data-s="1" aria-pressed="true">1&times;</button>
      <button data-s="2">2&times;</button>
    </div>
  </div>

  <footer id="foot"></footer>
</div>

<script>
const T = __TRAJ__;
const $ = s => document.querySelector(s);
const d=T.d, N=T.N, L=T.L, H=L/2;
const FR=T.frames, NF=FR.length;
const COORD=T.coord, zmin=Math.min(...COORD.filter(z=>z>0)), zmax=Math.max(...COORD);

// pre-parse frames -> {R, pos:Float32Array(N*d) in [0,L)} and iteration index
const FRAMES=FR.map(f=>({R:f.R, i:f.i, p:Float32Array.from(f.p)}));
const iterMax = FRAMES[NF-1].i;

// phi from R:  phi = N * (4/3)π R^3 / L^3   (d=3)
const sphereVol = R => (4/3)*Math.PI*R*R*R;
const phiOf = R => N*sphereVol(R)/(L*L*L);
$("#phiend").textContent = T.phiFinal.toFixed(2);
$("#foot").innerHTML =
  `<b>method</b> CALiPPSO (iterative LP) &middot; HiGHS solver &nbsp;|&nbsp; `+
  `<b>trajectory</b> ${iterMax} iterations, ${NF} frames shown &nbsp;|&nbsp; `+
  `<b>&phi;</b> ${T.phi0.toFixed(2)} &rarr; ${T.phiFinal.toFixed(4)} &nbsp;|&nbsp; interpolation uses minimal-image so periodic wraps don't streak.`;
// phi tick at final (meter spans phi0..a bit above final)
const phiLo=T.phi0, phiHi=T.phiFinal*1.02;
$("#phitick").style.left = (100*(T.phiFinal-phiLo)/(phiHi-phiLo))+"%";

/* viridis */
const STOPS=[[68,1,84],[59,82,139],[33,145,140],[94,201,98],[253,231,37]];
function viridis(t){t=Math.max(0,Math.min(1,t));const x=t*(STOPS.length-1),i=Math.floor(x),f=x-i;
  const a=STOPS[i],b=STOPS[Math.min(i+1,STOPS.length-1)];return [a[0]+(b[0]-a[0])*f,a[1]+(b[1]-a[1])*f,a[2]+(b[2]-a[2])*f];}

/* cube edges */
const CORN=[],EDG=[];
for(let s=0;s<8;s++)CORN.push([(s&1?H:-H),(s&2?H:-H),(s&4?H:-H)]);
for(let a=0;a<8;a++)for(let b=a+1;b<8;b++){let dd=0;for(let k=0;k<3;k++)if(CORN[a][k]!==CORN[b][k])dd++;if(dd===1)EDG.push([a,b]);}

/* view + playback state */
let yaw=0.6,pitch=-0.42,zoom=1,spin=false,showBox=true,doLoop=true,colorMode="depth";
let playing=true, t=0, speed=1;               // t in [0, NF-1] continuous
const FPP=7;                                   // frames(display) per trajectory-step-second baseline
const cv=$("#cv"),ctx=cv.getContext("2d");let W=0,Hh=0,DPR=1;
function syncSize(){const r=cv.getBoundingClientRect();DPR=Math.min(2,window.devicePixelRatio||1);
  const w=Math.round(r.width),h=Math.round(r.height);if(w<=0||h<=0)return;W=w;Hh=h;
  const bw=w*DPR,bh=h*DPR;if(cv.width!==bw||cv.height!==bh){cv.width=bw;cv.height=bh;}ctx.setTransform(DPR,0,0,DPR,0,0);}
syncSize();

const FOCAL=3.0, LIGHT=[-0.5,0.7,0.6];
(()=>{const n=Math.hypot(...LIGHT);LIGHT[0]/=n;LIGHT[1]/=n;LIGHT[2]/=n;})();
function rot(x,y,z){const cy=Math.cos(yaw),sy=Math.sin(yaw);let X=cy*x+sy*z,Z=-sy*x+cy*z;
  const cp=Math.cos(pitch),sp=Math.sin(pitch);let Y=cp*y-sp*Z;Z=sp*y+cp*Z;return [X,Y,Z];}

// interpolate positions/R at continuous t, minimal-image aware, centered about origin
const curPos=new Float32Array(N*3); let curR=FRAMES[0].R, curPhi=phiOf(curR), curIter=0;
function sampleAt(tt){
  tt=Math.max(0,Math.min(NF-1,tt));
  const i0=Math.floor(tt), i1=Math.min(NF-1,i0+1), fr=tt-i0;
  const A=FRAMES[i0], B=FRAMES[i1];
  curR = A.R+(B.R-A.R)*fr;
  curIter = Math.round(A.i+(B.i-A.i)*fr);
  curPhi = phiOf(curR);
  for(let i=0;i<N;i++){
    for(let c=0;c<3;c++){
      let a=A.p[i*3+c], b=B.p[i*3+c], delta=b-a;
      if(delta>H)delta-=L; else if(delta<-H)delta+=L;
      let v=a+delta*fr; v-=Math.floor(v/L)*L;      // wrap into [0,L)
      curPos[i*3+c]=v-H;                            // center
    }
  }
}

const prim=[];
function frame(){
  syncSize(); ctx.clearRect(0,0,W,Hh);
  const base=Math.min(W,Hh)*0.46*zoom, ox=W/2, oy=Hh/2; prim.length=0;
  for(let i=0;i<N;i++){
    const [X,Y,Z]=rot(curPos[i*3],curPos[i*3+1],curPos[i*3+2]);
    const persp=FOCAL/(FOCAL-Z); if(persp<=0)continue;
    prim.push({t:0,z:Z,sx:ox+X*base*persp,sy:oy-Y*base*persp,sr:curR*base*persp,i});
  }
  if(showBox)for(const[a,b]of EDG){const ra=rot(...CORN[a]),rb=rot(...CORN[b]);
    const pa=FOCAL/(FOCAL-ra[2]),pb=FOCAL/(FOCAL-rb[2]);
    prim.push({t:1,z:(ra[2]+rb[2])/2,x1:ox+ra[0]*base*pa,y1:oy-ra[1]*base*pa,x2:ox+rb[0]*base*pb,y2:oy-rb[1]*base*pb});}
  prim.sort((p,q)=>p.z-q.z);
  const boxCol=getComputedStyle(document.documentElement).getPropertyValue('--box').trim()||"#3b4757";
  for(const p of prim){
    if(p.t===1){ctx.strokeStyle=boxCol;ctx.globalAlpha=.55;ctx.lineWidth=1.1;
      ctx.beginPath();ctx.moveTo(p.x1,p.y1);ctx.lineTo(p.x2,p.y2);ctx.stroke();ctx.globalAlpha=1;continue;}
    let col;
    if(colorMode==="coord"){const z=COORD[p.i];col= z===0?[140,150,165]:viridis((z-zmin)/Math.max(1,zmax-zmin));}
    else col=viridis((p.z+H)/(2*H));
    drawSphere(p.sx,p.sy,p.sr,col);
  }
}
function drawSphere(sx,sy,r,col){
  if(r<0.4)return;const[cr,cg,cb]=col;
  const hx=sx-LIGHT[0]*r*0.55,hy=sy-LIGHT[1]*r*0.55;
  const g=ctx.createRadialGradient(hx,hy,r*0.08,sx,sy,r*1.02);
  const hi=v=>Math.min(255,v+90),lo=v=>v*0.32;
  g.addColorStop(0,`rgb(${hi(cr)},${hi(cg)},${hi(cb)})`);
  g.addColorStop(0.45,`rgb(${cr|0},${cg|0},${cb|0})`);
  g.addColorStop(1,`rgb(${lo(cr)|0},${lo(cg)|0},${lo(cb)|0})`);
  ctx.beginPath();ctx.arc(sx,sy,r,0,6.2832);ctx.fillStyle=g;ctx.fill();
  ctx.globalAlpha=.5;ctx.lineWidth=Math.max(0.5,r*0.05);
  ctx.strokeStyle=`rgb(${lo(cr)|0},${lo(cg)|0},${lo(cb)|0})`;ctx.stroke();ctx.globalAlpha=1;
}

/* HUD */
const seek=$("#seek");
function updateHUD(){
  $("#phival").textContent=curPhi.toFixed(3);
  $("#phifill").style.width=(100*Math.max(0,Math.min(1,(curPhi-phiLo)/(phiHi-phiLo))))+"%";
  $("#badge").innerHTML=`iter ${curIter} &nbsp;&middot;&nbsp; R=${curR.toFixed(4)} &nbsp;&middot;&nbsp; &phi;=${curPhi.toFixed(3)}`;
  const done = t>=NF-1-1e-6;
  const ph = done?"jammed &middot; isostatic" : (curPhi<0.5?"inflating":(curPhi<0.60?"rearranging":"closing gaps"));
  $("#phase").innerHTML=ph;
  $("#iterlab").textContent="iteration "+curIter;
  const pct=100*t/(NF-1);
  $("#pctlab").textContent=Math.round(pct)+"%";
  seek.value=Math.round(pct*10);
}

/* animation loop */
let last=performance.now();
function loop(now){
  const dt=Math.min(0.05,(now-last)/1000);last=now;
  if(playing){ t+=dt*FPP*speed;
    if(t>=NF-1){ if(doLoop){ t=0; } else { t=NF-1; playing=false; setIcon(); } } }
  if(spin) yaw+=dt*0.3;
  sampleAt(t); frame(); updateHUD();
  requestAnimationFrame(loop);
}
sampleAt(0); requestAnimationFrame(loop);

/* icons */
const PLAY='<path d="M8 5v14l11-7z"/>', PAUSE='<path d="M6 5h4v14H6zM14 5h4v14h-4z"/>';
function setIcon(){$("#playicon").innerHTML=playing?PAUSE:PLAY;}
setIcon();

/* controls */
$("#play").addEventListener("click",()=>{ if(!playing && t>=NF-1-1e-6) t=0; playing=!playing; setIcon(); });
seek.addEventListener("input",e=>{ playing=false; setIcon(); t=(e.target.value/1000)*(NF-1); sampleAt(t); });
$("#speed").addEventListener("click",e=>{const b=e.target.closest("button");if(!b)return;speed=parseFloat(b.dataset.s);
  [...e.currentTarget.querySelectorAll("button")].forEach(x=>x.setAttribute("aria-pressed",x===b));});
$("#colormode").addEventListener("click",e=>{const b=e.target.closest("button");if(!b)return;colorMode=b.dataset.v;
  [...e.currentTarget.children].forEach(x=>x.setAttribute("aria-pressed",x===b));});
$("#spin").addEventListener("change",e=>spin=e.target.checked);
$("#box").addEventListener("change",e=>showBox=e.target.checked);
$("#loop").addEventListener("change",e=>doLoop=e.target.checked);

/* rotate by drag */
const stage=$("#stage");let dragging=false,lx=0,ly=0;
stage.addEventListener("pointerdown",e=>{dragging=true;lx=e.clientX;ly=e.clientY;stage.classList.add("drag");stage.setPointerCapture(e.pointerId);});
stage.addEventListener("pointermove",e=>{if(!dragging)return;yaw+=(e.clientX-lx)*0.008;pitch+=(e.clientY-ly)*0.008;
  pitch=Math.max(-1.5,Math.min(1.5,pitch));lx=e.clientX;ly=e.clientY;});
addEventListener("pointerup",()=>{dragging=false;stage.classList.remove("drag");});
stage.addEventListener("wheel",e=>{e.preventDefault();zoom*=Math.exp(-e.deltaY*0.0012);zoom=Math.max(0.45,Math.min(3.5,zoom));},{passive:false});
addEventListener("keydown",e=>{if(e.code==="Space"){e.preventDefault();$("#play").click();}});
</script>
"""

HTML = HTML.replace("__TRAJ__", traj_js)
with open(OUT, "w", encoding="utf-8") as f:
    f.write(HTML)
print("WROTE", OUT, os.path.getsize(OUT), "bytes")
