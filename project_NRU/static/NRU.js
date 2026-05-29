const out = document.getElementById('out');
const inp = document.getElementById('inp');
const memBoxes = document.getElementById('mem-boxes');
const statsEl = document.getElementById('stats');
const pasoBadge = document.getElementById('paso-badge');

let state = { mode: 'menu', step: 0, data: {} };
let totalMarcos = 0;

function print(html) {
  const d = document.createElement('div');
  d.innerHTML = html;
  out.appendChild(d);
  out.scrollTop = out.scrollHeight;
}
function line(txt) { print(`<span class="line">${txt}</span>`); }
function empty() { line(''); }

function renderMem(memoria, highlight = -1, evict = -1) {
  memBoxes.innerHTML = '';
  for (let i = 0; i < totalMarcos; i++) {
    const box = document.createElement('div');
    if (i >= memoria.length) {
      box.className = 'page-box empty';
      box.innerHTML = `<span class="pnum" style="color:var(--dim)">_</span><span class="pbits">—</span>`;
    } else {
      const pg = memoria[i];
      const c = pg.R * 2 + pg.M;
      const anim = i === highlight ? ' new' : i === evict ? ' evict' : '';
      box.className = `page-box c${c}${anim}`;
      box.innerHTML = `<span class="pnum">${pg.pag}</span><span class="pbits">R=${pg.R} M=${pg.M}</span>`;
    }
    memBoxes.appendChild(box);
  }
}

function showMenu() {
  state = { mode: 'menu', step: 0, data: {} };
  empty();
  line(`<span class="b">╔═════════════════════════════════════════════╗</span>`);
  line(`<span class="b"></span>  <span class="g">ALGORITMO NRU — GRUPO #4</span>               <span class="b"></span>`);
  line(`<span class="b"></span>  <span class="d">No Recently Used — Reemplazo de Páginas</span><span class="b"></span>`);
  line(`<span class="b"></span><span class="b"></span>`);
  line(`<span class="b">╚════════════════════════════════════════════╝</span>`);
  empty();
  line(`  <span class="g">[1]</span>  Ejecutar NRU`);
  line(`  <span class="g">[2]</span>  Ejemplo automático`);
  line(`  <span class="d">[clear]</span>  Limpiar pantalla`);
  empty();
}

async function ejecutarNRU(marcos, referencias, reset_cada) {
  totalMarcos = marcos;
  renderMem([], -1, -1);
  empty();
  line(`<span class="p">═══ SIMULACIÓN NRU — Python corriendo atrás ═══</span>`);
  line(`<span class="d">Marcos: ${marcos} | Referencias: [${referencias}] | Reset cada: ${reset_cada}</span>`);
  line(`<span class="y">Enviando datos a Flask...</span>`);

  const response = await fetch('/ejecutar', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ marcos, referencias, reset_cada })
  });

  const resultado = await response.json();
  empty();
  line(`<span class="d">Paso  Tipo              Página   Clase      Resultado</span>`);
  line(`<span class="d">${'─'.repeat(60)}</span>`);

  let paso = 1;
  let delay = 0;

  resultado.pasos.forEach((p, i) => {
    setTimeout(() => {
      if (p.tipo === 'reset') {
        print(`<span class="line"><span class="d">      ↻ Reset bit R en todas las páginas</span></span>`);
        return;
      }

      if (p.tipo === 'acierto') {
        renderMem(p.memoria);
        const c = p.clase;
        print(`<span class="line">  <span class="d">${String(paso).padEnd(4)}</span> <span class="b">Acierto</span>         <span class="b">${String(p.pagina).padEnd(8)}</span><span class="b-c${c}"> Clase ${c} </span>  <span class="b-ok"> ✓ Acierto </span></span>`);
      }

      if (p.tipo === 'fallo_espacio') {
        renderMem(p.memoria, p.memoria.length - 1, -1);
        print(`<span class="line">  <span class="d">${String(paso).padEnd(4)}</span> <span class="y">Fallo+espacio</span>   <span class="y">${String(p.pagina).padEnd(8)}</span><span class="d">—         </span>  <span class="b-err"> ❌ Fallo  </span></span>`);
      }

      if (p.tipo === 'fallo_reemplazo') {
        renderMem(p.memoria, -1, -1);
        const cls = p.clase_victima;
        print(`<span class="line">  <span class="d">${String(paso).padEnd(4)}</span> <span class="r">Fallo+reemplazo</span> <span class="y">${String(p.pagina).padEnd(8)}</span><span class="b-c${cls}"> Clase ${cls} </span>  <span class="b-err"> ❌ Fallo  </span></span>`);
        line(`<span class="d">       └ P${p.victima} fue reemplazada</span>`);
      }

      pasoBadge.textContent = `Paso ${paso}/${resultado.pasos.filter(x => x.tipo !== 'reset').length}`;
      paso++;

      if (i === resultado.pasos.length - 1) {
        setTimeout(() => {
          empty();
          line(`<span class="d">${'─'.repeat(50)}</span>`);
          line(`<span class="g">✅ Simulación completada — resultado de Python</span>`);
          line(`  Fallos   : <span class="r">${resultado.fallos}</span> de ${resultado.pasos.filter(x => x.tipo !== 'reset').length}`);
          line(`  Aciertos : <span class="g">${resultado.aciertos}</span>`);
          line(`  Tasa     : <span class="y">${resultado.tasa}%</span>`);
          empty();
          line(`  Estado final:`);
          resultado.memoria_final.forEach(pg => {
            const c = pg.R * 2 + pg.M;
            line(`  <span class="b-c${c}"> Clase ${c} </span>  Página <span class="b">${pg.pag}</span>  R=${pg.R} M=${pg.M}`);
          });
          statsEl.innerHTML = `<div style="margin-top:8px;font-size:11px"><div style="color:var(--red);margin-bottom:4px">Fallos: ${resultado.fallos}</div><div style="color:var(--green);margin-bottom:4px">Aciertos: ${resultado.aciertos}</div><div style="color:var(--dim)">Tasa: ${resultado.tasa}%</div></div>`;
          empty();
          line(`<span class="d">Presioná Enter para volver al menú...</span>`);
          state = { mode: 'back' };
        }, 400);
      }
    }, delay);
    delay += 500;
  });
}

function handle(val) {
  val = val.trim();
  if (!val) { if (state.mode === 'back') showMenu(); return; }
  print(`<span class="line d">nru@grupo4:~$ ${val}</span>`);
  if (val === 'clear') { out.innerHTML = ''; showMenu(); return; }
  if (state.mode === 'back') { showMenu(); return; }

  if (state.mode === 'menu') {
    if (val === '1') {
      state = { mode: 'nru', step: 0, data: {} };
      empty();
      line(`<span class="p">─── CONFIGURAR SIMULACIÓN ───</span>`);
      line(`<span class="g">¿Cuántos marcos de memoria? (ej: 3):</span>`);
      return;
    }
    if (val === '2') {
      empty();
      line(`<span class="y">Cargando ejemplo automático...</span>`);
      setTimeout(() => ejecutarNRU(3, '2 3 2 1 5 2 4 5 3 2', 4), 300);
      return;
    }
    line(`<span class="r">Opción no válida.</span>`);
    return;
  }

  if (state.mode === 'nru') {
    const d = state.data;
    if (state.step === 0) {
      d.marcos = parseInt(val);
      totalMarcos = d.marcos;
      renderMem([], -1, -1);
      state.step = 1;
      line(`<span class="g">Cadena de referencias (ej: 2 3 2 1 5 2 4 5):</span>`);
      return;
    }
    if (state.step === 1) {
      d.referencias = val;
      state.step = 2;
      line(`<span class="g">¿Cada cuántos pasos resetear bit R? (ej: 4):</span>`);
      return;
    }
    if (state.step === 2) {
      ejecutarNRU(d.marcos, d.referencias, parseInt(val));
      return;
    }
  }
}

inp.addEventListener('keydown', e => {
  if (e.key === 'Enter') { const v = inp.value; inp.value = ''; handle(v); }
});

setTimeout(() => {
  line(`<span class="g">Iniciando NRU Terminal con Flask...</span>`);
  setTimeout(() => {
    line(`<span class="d">Python 3.11 | Flask | Ubuntu 24.04 WSL2</span>`);
    setTimeout(showMenu, 400);
  }, 300);
}, 200);