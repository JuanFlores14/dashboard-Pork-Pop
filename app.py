import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go
import numpy as np
import pandas as pd

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Pork&Pop · Simulador de Rentabilidad",
    page_icon="🐷",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
#  DETECTOR DE TEMA (inyecta data-theme en <html>)
# ─────────────────────────────────────────────
components.html("""
<script>
(function() {
  function applyTheme() {
    var app = window.parent.document.querySelector('.stApp');
    if (!app) return;
    var bg  = window.parent.getComputedStyle(app).backgroundColor;
    var rgb = bg.match(/\\d+/g);
    if (!rgb) return;
    var brightness = +rgb[0] + +rgb[1] + +rgb[2];
    var theme = brightness < 382 ? 'dark' : 'light';
    window.parent.document.documentElement.setAttribute('data-theme', theme);
  }
  applyTheme();
  setInterval(applyTheme, 400);
  var app = window.parent.document.querySelector('.stApp');
  if (app) {
    new MutationObserver(applyTheme).observe(app, {
      attributes: true, attributeFilter: ['style','class'], subtree: false
    });
  }
})();
</script>
""", height=0)

# ─────────────────────────────────────────────
#  PALETA PORK&POP + MODO CLARO / OSCURO
# ─────────────────────────────────────────────
st.markdown("""
<style>

/* ══ 1. CUSTOM PROPERTIES ══════════════════════════════════════ */

:root,
[data-theme="light"] {
  --p1 : #C24483;
  --p2 : #C7669D;
  --p3 : #D187B4;
  --p4 : #DDA6C8;
  --p5 : #E8C1D9;
  --wh : #FFFFFF;

  --bg-app   : #FBF3F8;
  --bg-card  : #FFFFFF;
  --bg-card2 : #FEF0F8;
  --bg-input : #FEF8FC;

  --tx-hi    : #1A0A14;
  --tx-md    : #5A2A48;
  --tx-lo    : #8A5A76;

  --bd       : #E8C1D9;
  --bd-str   : #DDA6C8;

  --ok       : #1A7A50;
  --warn     : #B86800;
  --bad      : #C0392B;

  --shadow   : rgba(194,68,131,0.10);
  --shadow-h : rgba(194,68,131,0.22);

  --ch-text  : #8A5A76;
  --ch-grid  : rgba(194,68,131,0.10);
  --ch-zero  : rgba(194,68,131,0.25);
}

[data-theme="dark"] {
  --bg-app   : #0F0710;
  --bg-card  : #1C0C1A;
  --bg-card2 : #261420;
  --bg-input : #1C0C1A;

  --tx-hi    : #E8C1D9;
  --tx-md    : #DDA6C8;
  --tx-lo    : #9A6484;

  --bd       : #3A1630;
  --bd-str   : #C24483;

  --ok       : #2ACA7A;
  --warn     : #F5A623;
  --bad      : #F06060;

  --shadow   : rgba(0,0,0,0.45);
  --shadow-h : rgba(0,0,0,0.65);

  --ch-text  : #DDA6C8;
  --ch-grid  : rgba(194,68,131,0.18);
  --ch-zero  : rgba(194,68,131,0.35);
}

@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --bg-app   : #0F0710;
    --bg-card  : #1C0C1A;
    --bg-card2 : #261420;
    --bg-input : #1C0C1A;
    --tx-hi    : #E8C1D9;
    --tx-md    : #DDA6C8;
    --tx-lo    : #9A6484;
    --bd       : #3A1630;
    --bd-str   : #C24483;
    --ok       : #2ACA7A;
    --warn     : #F5A623;
    --bad      : #F06060;
    --shadow   : rgba(0,0,0,0.45);
    --shadow-h : rgba(0,0,0,0.65);
    --ch-text  : #DDA6C8;
    --ch-grid  : rgba(194,68,131,0.18);
    --ch-zero  : rgba(194,68,131,0.35);
  }
}

/* ══ 2. BASE ═══════════════════════════════════════════════════ */

html, body, [class*="css"] {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}
.stApp {
  background-color: var(--bg-app) !important;
}

/* ══ 3. HERO ════════════════════════════════════════════════════ */

.hero {
  background: linear-gradient(135deg, #C24483 0%, #C7669D 55%, #D187B4 100%);
  padding: 26px 32px 20px;
  border-radius: 16px;
  margin-bottom: 6px;
  box-shadow: 0 4px 28px rgba(194,68,131,0.30);
}
.hero h1 {
  color: #FFFFFF;
  font-size: 1.9rem;
  font-weight: 900;
  margin: 0;
  letter-spacing: -0.5px;
}
.hero p {
  color: rgba(255,255,255,0.82);
  margin: 6px 0 0;
  font-size: 0.88rem;
}

/* ══ 4. SLIDER BOX ═════════════════════════════════════════════ */

.slider-box {
  background   : var(--bg-card2);
  border       : 1.5px solid var(--bd);
  border-radius: 14px;
  padding      : 18px 20px 14px;
  transition   : border-color .2s, box-shadow .2s;
  height       : 100%;
}
.slider-box:focus-within {
  border-color: var(--bd-str);
  box-shadow  : 0 0 0 3px rgba(194,68,131,0.12);
}
.slider-box.growth-active {
  border-color: var(--p1);
  box-shadow  : 0 0 0 3px rgba(194,68,131,0.15);
}
.slider-title {
  font-size  : 0.82rem;
  font-weight: 700;
  color      : var(--p1);
  margin     : 0 0 6px;
  letter-spacing: 0.3px;
}
.slider-hint {
  font-size: 0.71rem;
  color    : var(--tx-lo);
  margin   : 3px 0 0;
}

/* ══ 5. KPI CARDS ══════════════════════════════════════════════ */

.kpi-card {
  background   : var(--bg-card);
  border-radius: 14px;
  padding      : 18px 20px;
  box-shadow   : 0 2px 18px var(--shadow);
  border-top   : 4px solid var(--p1);
  text-align   : center;
  transition   : border-color .25s, box-shadow .25s;
}
.kpi-card:hover {
  box-shadow: 0 4px 28px var(--shadow-h);
}
.kpi-card.ok   { border-top-color: var(--ok);   }
.kpi-card.warn { border-top-color: var(--warn);  }
.kpi-card.bad  { border-top-color: var(--bad);   }

.kpi-lbl {
  font-size     : 0.68rem;
  color         : var(--tx-lo);
  font-weight   : 700;
  letter-spacing: 0.9px;
  text-transform: uppercase;
  margin        : 0;
}
.kpi-val {
  font-size  : 1.85rem;
  font-weight: 900;
  color      : var(--tx-hi);
  margin     : 6px 0 2px;
  line-height: 1;
}
.kpi-sub {
  font-size: 0.71rem;
  color    : var(--tx-md);
  margin   : 0;
}

/* ══ 6. SECTION LABEL ══════════════════════════════════════════ */

.sec-lbl {
  font-size     : 0.67rem;
  font-weight   : 800;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  color         : var(--p1);
  margin        : 0 0 10px;
}

/* ══ 7. BADGES ═════════════════════════════════════════════════ */

.badge {
  display    : inline-flex;
  align-items: center;
  gap        : 5px;
  padding    : 4px 12px;
  border-radius: 20px;
  font-size  : 0.73rem;
  font-weight: 700;
}
.b-ok   { background: rgba(26,122,80 ,0.13); color: var(--ok);   }
.b-warn { background: rgba(184,104,0 ,0.13); color: var(--warn); }
.b-bad  { background: rgba(192,57,43 ,0.13); color: var(--bad);  }
.b-growth {
  background: rgba(194,68,131,0.13);
  color: var(--p1);
}

/* ══ 8. DIVIDER ════════════════════════════════════════════════ */

.div { border: none; border-top: 1px solid var(--bd); margin: 22px 0; }

/* ══ 9. PLOTLY SVG — REACTIVE COLOR OVERRIDES ════════════════ */

.js-plotly-plot .bg,
.js-plotly-plot rect.bg           { fill: transparent !important; }

.js-plotly-plot .xtick text,
.js-plotly-plot .ytick text,
.js-plotly-plot .g-xtitle text,
.js-plotly-plot .g-ytitle text,
.js-plotly-plot .gtitle,
.js-plotly-plot .annotation-text  { fill: var(--ch-text) !important; }

.js-plotly-plot .legend text       { fill: var(--tx-md)   !important; }

.js-plotly-plot .colorbar-title text,
.js-plotly-plot .colorbar text     { fill: var(--ch-text) !important; }

.js-plotly-plot .xgrid,
.js-plotly-plot .ygrid             { stroke: var(--ch-grid) !important; }
.js-plotly-plot .xaxis line,
.js-plotly-plot .yaxis line,
.js-plotly-plot .xaxis path,
.js-plotly-plot .yaxis path        { stroke: var(--bd) !important; }

/* ══ 10. STREAMLIT WIDGETS ════════════════════════════════════ */

[data-testid="stSlider"] [role="progressbar"] {
  background-color: var(--p1) !important;
}
[data-testid="stSlider"] [role="slider"] {
  background-color: var(--p1) !important;
  border-color    : var(--p1) !important;
  box-shadow      : 0 0 0 3px rgba(194,68,131,0.20) !important;
}

p, li, span                    { color: var(--tx-hi) !important; }
.stMarkdown p                  { color: var(--tx-hi) !important; }
label[data-testid]             { color: var(--tx-md) !important; }

[data-testid="stDataFrame"]       { border-radius: 12px; overflow: hidden; }
[data-testid="stDataFrame"] thead th {
  background: var(--bg-card2) !important;
  color     : var(--tx-hi)    !important;
  font-weight: 600;
}
[data-testid="stDataFrame"] tbody td {
  background: var(--bg-card) !important;
  color     : var(--tx-md)   !important;
}
[data-testid="stDataFrame"] tbody tr:hover td {
  background: var(--bg-card2) !important;
}

</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  CONSTANTES DEL PROYECTO
# ─────────────────────────────────────────────
FIXED_COSTS  = 3_321_554.40 - 55_200 - 736_000  # ≈ $2,530,354

BAGS_M_PILOT = 900    # 3 bolsas × 10 sucursales × 30 días
BAGS_M_EXP   = 4_500  # 3 bolsas × 50 sucursales × 30 días

TRANSP     = "rgba(0,0,0,0)"
FONT_FAM   = "Inter, -apple-system, sans-serif"
AXIS_COLOR = "#9A6484"

# ─────────────────────────────────────────────
#  HERO
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <h1>🐷 Pork&amp;Pop — Simulador de Rentabilidad</h1>
  <p>Canal OXXO &nbsp;·&nbsp; Etapa I: Piloto 10 sucursales &nbsp;|&nbsp; Etapa II: Expansión 50 sucursales</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SLIDERS
# ─────────────────────────────────────────────
cs, cp, cg = st.columns(3, gap="large")

with cs:
    st.markdown('<div class="slider-box"><p class="slider-title">📦 Costo de producción por bolsa</p>',
                unsafe_allow_html=True)
    costo = st.slider("costo", 12.0, 20.0, 16.0, 0.25,
                      "$%.2f MXN", label_visibility="collapsed")
    st.markdown('<p class="slider-hint">Rango estimado: $12.00 – $20.00 MXN</p></div>',
                unsafe_allow_html=True)

with cp:
    st.markdown('<div class="slider-box"><p class="slider-title">💰 Precio de venta a OXXO</p>',
                unsafe_allow_html=True)
    precio = st.slider("precio", 27.50, 30.00, 27.50, 0.25,
                       "$%.2f MXN", label_visibility="collapsed")
    st.markdown('<p class="slider-hint">Precio B2B de referencia: $27.50 MXN</p></div>',
                unsafe_allow_html=True)

with cg:
    growth_cls = "growth-active" if True else ""
    st.markdown(f'<div class="slider-box {growth_cls}"><p class="slider-title">📈 Crecimiento mensual de ventas</p>',
                unsafe_allow_html=True)
    growth = st.slider("growth", 0.0, 15.0, 0.0, 0.5,
                       "%.1f%%", label_visibility="collapsed")
    st.markdown('<p class="slider-hint">0% = ventas constantes (modelo base)</p></div>',
                unsafe_allow_html=True)

st.markdown('<div class="div"></div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  MODELO DE VOLUMEN CON CRECIMIENTO COMPUESTO
#
#  Cada mes: bolsas = base_mensual × (1 + g)^(mes−1)
#  donde base es BAGS_M_PILOT para meses 1-3
#  y BAGS_M_EXP para meses 4-24.
#  Al mes 4 hay un salto natural por la expansión de tiendas
#  (×5) más el crecimiento acumulado de los 3 meses previos.
# ─────────────────────────────────────────────
g = growth / 100

def vol(month, rate):
    base = BAGS_M_PILOT if month <= 3 else BAGS_M_EXP
    return base * (1 + rate) ** (month - 1)

monthly_bags = [vol(m, g) for m in range(1, 25)]

pilot_vol = sum(monthly_bags[:3])
exp_vol   = sum(monthly_bags[3:11])
total_vol = pilot_vol + exp_vol

# ─────────────────────────────────────────────
#  CÁLCULOS EN TIEMPO REAL
# ─────────────────────────────────────────────
margen_u   = precio - costo
margen_pct = (margen_u / precio) * 100

utilidad  = total_vol * margen_u
inversion = FIXED_COSTS + total_vol * costo
roi       = (utilidad / inversion) * 100

# Flujo mensual acumulado (con crecimiento)
cf_mes = [monthly_bags[m - 1] * margen_u for m in range(1, 25)]
cf_acc = []
acc = -FIXED_COSTS
for cf in cf_mes:
    acc += cf
    cf_acc.append(acc)

payback = next((i + 1 for i, v in enumerate(cf_acc) if v >= 0), None)
pb_str  = f"{payback} mes{'es' if payback != 1 else ''}" if payback else "> 24 meses"

# Flujo baseline (sin crecimiento) — solo para comparar en el chart
cf_acc_base = []
acc_b = -FIXED_COSTS
for m in range(1, 25):
    acc_b += vol(m, 0) * margen_u
    cf_acc_base.append(acc_b)

payback_base = next((i + 1 for i, v in enumerate(cf_acc_base) if v >= 0), None)

# Badge escenario
if margen_pct >= 40:
    badge = '<span class="badge b-ok">▲ Escenario Óptimo</span>'
elif margen_pct >= 30:
    badge = '<span class="badge b-warn">◆ Escenario Neutral</span>'
else:
    badge = '<span class="badge b-bad">▼ Escenario Pesimista</span>'

growth_badge = (f'&nbsp;<span class="badge b-growth">📈 +{growth:.1f}% crecimiento mensual</span>'
                if growth > 0 else "")

# ─────────────────────────────────────────────
#  KPI CARDS
# ─────────────────────────────────────────────
st.markdown(f'<div style="margin-bottom:14px">{badge}{growth_badge}</div>',
            unsafe_allow_html=True)

def cls(v, g_thresh, b_thresh):
    return "ok" if v >= g_thresh else ("bad" if v <= b_thresh else "warn")

k1, k2, k3, k4 = st.columns(4, gap="medium")
kpis = [
    (k1, "Margen por Bolsa",  f"${margen_u:.2f}",  "MXN por unidad",          cls(margen_u, 12, 6)),
    (k2, "Margen Bruto",      f"{margen_pct:.1f}%", "sobre precio de venta",   cls(margen_pct, 38, 25)),
    (k3, "ROI del Proyecto",  f"{roi:.1f}%",        "retorno sobre inversión", cls(roi, 15, 0)),
    (k4, "Payback Period",    pb_str,               "para recuperar inversión",cls((24 - (payback or 999)), 10, 0)),
]
for col, lbl, val, sub, c in kpis:
    with col:
        st.markdown(f"""
        <div class="kpi-card {c}">
          <p class="kpi-lbl">{lbl}</p>
          <p class="kpi-val">{val}</p>
          <p class="kpi-sub">{sub}</p>
        </div>""", unsafe_allow_html=True)

st.markdown('<div class="div"></div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  GRÁFICAS
# ─────────────────────────────────────────────
gc1, gc2 = st.columns([1.15, 0.85], gap="large")

# ── HEATMAP ROI (siempre a g=0 como mapa de referencia) ───────
with gc1:
    TOTAL_BAGS_BASE = BAGS_M_PILOT * 3 + BAGS_M_EXP * 8
    costos_r  = np.arange(12.00, 20.25, 0.25)
    precios_r = np.arange(27.50, 30.25, 0.25)
    roi_mat   = [
        [((p - c) * TOTAL_BAGS_BASE) / (FIXED_COSTS + TOTAL_BAGS_BASE * c) * 100
         for p in precios_r]
        for c in costos_r
    ]

    fig_h = go.Figure(go.Heatmap(
        z=roi_mat,
        x=[f"${p:.2f}" for p in precios_r],
        y=[f"${c:.2f}" for c in costos_r],
        colorscale=[
            [0.00, "#C0392B"],
            [0.20, "#E8C1D9"],
            [0.45, "#D187B4"],
            [0.70, "#C7669D"],
            [1.00, "#C24483"],
        ],
        zmin=-10, zmax=40,
        colorbar=dict(
            title=dict(text="ROI %", font=dict(size=11, color=AXIS_COLOR)),
            tickfont=dict(size=10, color=AXIS_COLOR),
            thickness=14,
        ),
        text=[[f"{v:.0f}%" for v in row] for row in roi_mat],
        texttemplate="%{text}",
        textfont=dict(size=7.5),
        hovertemplate="Precio: %{x}<br>Costo: %{y}<br>ROI: %{z:.1f}%<extra></extra>",
    ))
    roi_base = ((precio - costo) * TOTAL_BAGS_BASE) / (FIXED_COSTS + TOTAL_BAGS_BASE * costo) * 100
    fig_h.add_trace(go.Scatter(
        x=[f"${precio:.2f}"], y=[f"${costo:.2f}"],
        mode="markers",
        marker=dict(symbol="star", size=18, color="#FFFFFF",
                    line=dict(color="#1A0A14", width=1.5)),
        name="Escenario actual",
        hovertemplate=f"Escenario actual — ROI base: {roi_base:.1f}%<extra></extra>",
    ))
    fig_h.update_layout(
        title=dict(text="Mapa de ROI — Precio vs Costo (ventas base)",
                   font=dict(size=13, color=AXIS_COLOR, family=FONT_FAM)),
        xaxis=dict(title="Precio venta OXXO (MXN)", tickfont=dict(size=9, color=AXIS_COLOR),
                   linecolor=AXIS_COLOR, gridcolor="rgba(194,68,131,0.10)"),
        yaxis=dict(title="Costo de producción (MXN)", tickfont=dict(size=9, color=AXIS_COLOR),
                   linecolor=AXIS_COLOR, gridcolor="rgba(194,68,131,0.10)"),
        paper_bgcolor=TRANSP, plot_bgcolor=TRANSP,
        font=dict(family=FONT_FAM, color=AXIS_COLOR),
        height=430, margin=dict(t=46, b=50, l=60, r=16),
    )
    st.plotly_chart(fig_h, use_container_width=True)

# ── BARRAS AGRUPADAS (volúmenes ajustados por crecimiento) ─────
with gc2:
    stage_labels = [
        f"Piloto<br>({pilot_vol:,.0f} bolsas)",
        f"Expansión<br>({exp_vol:,.0f} bolsas)",
    ]
    bags_per_stage = [pilot_vol, exp_vol]

    def bar(name, vals, color):
        return go.Bar(
            name=name, x=stage_labels, y=vals,
            marker_color=color,
            text=[f"${v:,.0f}" for v in vals],
            textposition="outside",
            textfont=dict(size=10, color=AXIS_COLOR),
        )

    fig_b = go.Figure([
        bar("Ingresos",       [b * precio   for b in bags_per_stage], "#27AE60"),
        bar("COGS",           [b * costo    for b in bags_per_stage], "#C24483"),
        bar("Utilidad Bruta", [b * margen_u for b in bags_per_stage], "#D187B4"),
    ])
    fig_b.update_layout(
        title=dict(text="Ingresos · COGS · Utilidad por Etapa",
                   font=dict(size=13, color=AXIS_COLOR, family=FONT_FAM)),
        barmode="group",
        paper_bgcolor=TRANSP, plot_bgcolor=TRANSP,
        font=dict(family=FONT_FAM, color=AXIS_COLOR),
        yaxis=dict(title="MXN ($)", tickformat="$,.0f",
                   gridcolor="rgba(194,68,131,0.10)", linecolor=AXIS_COLOR),
        xaxis=dict(linecolor=AXIS_COLOR),
        height=430, margin=dict(t=46, b=50, l=70, r=16),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0,
                    font=dict(color=AXIS_COLOR, size=11)),
    )
    st.plotly_chart(fig_b, use_container_width=True)

# ── FLUJO DE CAJA ────────────────────────────
title_cf = (f"📈 Flujo de Caja Acumulado — 24 meses"
            + (f" &nbsp;<span style='color:var(--p1);font-size:0.65rem;font-weight:700'>"
               f"(línea punteada = sin crecimiento)</span>" if growth > 0 else ""))
st.markdown(f'<p class="sec-lbl">{title_cf}</p>', unsafe_allow_html=True)

meses  = list(range(0, 25))
cf_plt = [-FIXED_COSTS] + cf_acc
pts_col = ["#27AE60" if v >= 0 else "#C24483" for v in cf_plt]

fig_cf = go.Figure()

# Área rellena bajo la curva principal
fig_cf.add_trace(go.Scatter(
    x=meses, y=cf_plt, fill="tozeroy", mode="none",
    fillcolor="rgba(194,68,131,0.09)", showlegend=False, hoverinfo="skip",
))

# Línea baseline (sin crecimiento) — solo cuando growth > 0
if growth > 0:
    cf_plt_base = [-FIXED_COSTS] + cf_acc_base
    fig_cf.add_trace(go.Scatter(
        x=meses, y=cf_plt_base,
        mode="lines",
        line=dict(color="#DDA6C8", width=2, dash="dot"),
        name="Sin crecimiento",
        hovertemplate="Mes %{x} — $%{y:,.0f} MXN (base)<extra></extra>",
    ))
    # Payback baseline
    if payback_base and payback_base <= 24:
        fig_cf.add_vline(
            x=payback_base,
            line_dash="dot", line_color="#DDA6C8", line_width=1.5,
            annotation_text=f"  Payback base: mes {payback_base}",
            annotation_font=dict(color="#DDA6C8", size=10),
        )

# Curva principal (con crecimiento)
fig_cf.add_trace(go.Scatter(
    x=meses, y=cf_plt, mode="lines+markers",
    line=dict(color="#C24483", width=3),
    marker=dict(size=7, color=pts_col, line=dict(color=TRANSP, width=0)),
    name="Flujo acumulado",
    hovertemplate="Mes %{x} — $%{y:,.0f} MXN<extra></extra>",
))

fig_cf.add_hline(y=0, line_dash="dot", line_color=AXIS_COLOR, opacity=0.45)
fig_cf.add_vrect(x0=0,  x1=3,  fillcolor="#F5A623", opacity=0.07,
                 annotation_text="Piloto", annotation_position="top left",
                 annotation_font=dict(color=AXIS_COLOR, size=11))
fig_cf.add_vrect(x0=3,  x1=11, fillcolor="#C7669D", opacity=0.07,
                 annotation_text="Expansión", annotation_position="top left",
                 annotation_font=dict(color=AXIS_COLOR, size=11))

if payback and payback <= 24:
    fig_cf.add_vline(x=payback, line_dash="dash", line_color="#27AE60", line_width=2,
                     annotation_text=f"  Payback: mes {payback}",
                     annotation_font=dict(color="#27AE60", size=11))

fig_cf.update_layout(
    paper_bgcolor=TRANSP, plot_bgcolor=TRANSP,
    font=dict(family=FONT_FAM, color=AXIS_COLOR),
    xaxis=dict(title="Mes del proyecto", dtick=2,
               gridcolor="rgba(194,68,131,0.10)", linecolor=AXIS_COLOR),
    yaxis=dict(title="MXN ($)", tickformat="$,.0f",
               gridcolor="rgba(194,68,131,0.10)", linecolor=AXIS_COLOR),
    height=330, margin=dict(t=16, b=50, l=80, r=20),
    showlegend=growth > 0,
    legend=dict(orientation="h", yanchor="bottom", y=1.01, x=0,
                font=dict(color=AXIS_COLOR, size=11)),
)
st.plotly_chart(fig_cf, use_container_width=True)

# ─────────────────────────────────────────────
#  TABLA RESUMEN
# ─────────────────────────────────────────────
st.markdown('<div class="div"></div>', unsafe_allow_html=True)
st.markdown('<p class="sec-lbl">📋 Resumen del Escenario Actual</p>', unsafe_allow_html=True)

tc1, tc2 = st.columns(2, gap="large")
with tc1:
    st.dataframe(pd.DataFrame({
        "Concepto": ["Costo producción", "Precio venta OXXO",
                     "Margen por bolsa", "Margen bruto %",
                     "Crecimiento mensual"],
        "Valor":    [f"${costo:.2f} MXN", f"${precio:.2f} MXN",
                     f"${margen_u:.2f} MXN", f"{margen_pct:.1f}%",
                     f"{growth:.1f}% / mes"],
    }), hide_index=True, use_container_width=True)

with tc2:
    st.dataframe(pd.DataFrame({
        "Concepto": ["Bolsas totales proyectadas", "Ingresos brutos totales",
                     "Utilidad bruta total",
                     "Inversión total (fija + COGS)", "ROI estimado", "Payback period"],
        "Valor":    [f"{total_vol:,.0f} bolsas",
                     f"${total_vol * precio:,.0f} MXN",
                     f"${utilidad:,.0f} MXN",
                     f"${inversion:,.0f} MXN",
                     f"{roi:.1f}%",
                     pb_str],
    }), hide_index=True, use_container_width=True)

# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding:20px 0 8px; color:var(--tx-lo); font-size:0.70rem;">
  Pork&amp;Pop · Dashboard de Rentabilidad &nbsp;·&nbsp;
  Entregable 2 – Equipo #8 · Tec de Monterrey 2026
</div>
""", unsafe_allow_html=True)
