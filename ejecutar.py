"""Ejecutar desde la raíz: python ejecutar.py"""
import json
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from src.analisis import preparar, calidad, resumenes_paralelos, correlacion

BASE=Path(__file__).resolve().parent
raw=pd.read_excel(BASE/'data/dataset_set_B_madernova.xlsx')
df=preparar(raw)
df.to_csv(BASE/'data/datos_procesados.csv',index=False,encoding='utf-8-sig')
produccion=df[['fecha_registro','planta','tipo_tablero','volumen_producido_m3','merma_m3','consumo_energia_kwh','tiempo_produccion_hr','tasa_merma_pct','energia_kwh_m3','productividad_m3_hr']]
comercial=df[['fecha_registro','tipo_tablero','ventas_unidades','canal_distribucion','tiempo_despacho_dias']]
produccion.to_csv(BASE/'resultados/produccion.csv',index=False,encoding='utf-8-sig')
comercial.to_csv(BASE/'resultados/comercial_distribucion.csv',index=False,encoding='utf-8-sig')
plantas=resumenes_paralelos(df)
plantas.to_csv(BASE/'resultados/resumen_plantas.csv',index=False,encoding='utf-8-sig')
res={'calidad':calidad(df),'correlacion':correlacion(df),'inicio':str(df.fecha_registro.min().date()),'fin':str(df.fecha_registro.max().date()),'volumen_total':float(df.volumen_producido_m3.sum()),'merma_total':float(df.merma_m3.sum()),'merma_pct_ponderada':float(100*df.merma_m3.sum()/df.volumen_producido_m3.sum()),'despacho_promedio':float(df.tiempo_despacho_dias.mean()),'energia_total':float(df.consumo_energia_kwh.sum()),'ventas_total':int(df.ventas_unidades.sum()),'planta':plantas.to_dict(orient='records'),'por_canal':df.groupby('canal_distribucion').agg(ventas=('ventas_unidades','sum'),despacho_dias=('tiempo_despacho_dias','mean')).reset_index().to_dict(orient='records')}
(BASE/'resultados/metricas.json').write_text(json.dumps(res,indent=2,ensure_ascii=False),encoding='utf-8')
plt.rcParams.update({'font.size':10,'figure.facecolor':'white','axes.spines.top':False,'axes.spines.right':False})
fig,axs=plt.subplots(2,2,figsize=(13,8))
pl=plantas.sort_values('volumen_m3',ascending=False)
axs[0,0].bar(pl.planta,pl.volumen_m3,color='#1d7874');axs[0,0].set_title('Volumen producido por planta');axs[0,0].set_ylabel('m³')
axs[0,1].bar(pl.planta,pl.merma_pct_ponderada,color='#de8446');axs[0,1].set_title('Tasa de merma por planta');axs[0,1].set_ylabel('% sobre volumen producido')
canal=df.groupby('canal_distribucion').ventas_unidades.sum().sort_values(ascending=False)
axs[1,0].bar(canal.index,canal.values,color='#5276a5');axs[1,0].set_title('Ventas por canal');axs[1,0].set_ylabel('Unidades')
tipo=df.groupby('tipo_tablero').tiempo_despacho_dias.mean().sort_values(ascending=False)
axs[1,1].bar(tipo.index,tipo.values,color='#9474b6');axs[1,1].set_title('Tiempo medio de despacho por tablero');axs[1,1].set_ylabel('Días')
for a in axs.flat:a.tick_params(axis='x',labelrotation=12);a.grid(axis='y',alpha=.18)
fig.suptitle('MaderNova | Dashboard exploratorio',fontsize=18,fontweight='bold');fig.tight_layout()
fig.savefig(BASE/'dashboards/dashboard_exploratorio.png',dpi=180,bbox_inches='tight');plt.close(fig)
fig,ax=plt.subplots(figsize=(9,5));ax.scatter(df.volumen_producido_m3,df.consumo_energia_kwh,alpha=.55,color='#1d7874');ax.set(xlabel='Volumen producido (m³)',ylabel='Consumo (kWh)',title='Volumen y consumo energético');ax.grid(alpha=.2);fig.tight_layout();fig.savefig(BASE/'dashboards/volumen_energia.png',dpi=180);plt.close(fig)
try:
 import plotly.express as px
 import plotly.graph_objects as go
 from plotly.subplots import make_subplots
 fig=make_subplots(rows=2,cols=2,subplot_titles=('Producción por planta','Merma por planta','Ventas por canal','Despacho por tablero'))
 fig.add_trace(go.Bar(x=pl.planta,y=pl.volumen_m3,name='m³'),1,1)
 fig.add_trace(go.Bar(x=pl.planta,y=pl.merma_pct_ponderada,name='Merma %'),1,2)
 fig.add_trace(go.Bar(x=canal.index,y=canal.values,name='Ventas'),2,1)
 fig.add_trace(go.Bar(x=tipo.index,y=tipo.values,name='Días'),2,2)
 fig.update_layout(title='MaderNova — Dashboard interactivo',height=800,showlegend=False)
 fig.write_html(BASE/'dashboards/dashboard_interactivo.html',include_plotlyjs=True)
except ImportError: print('Plotly no instalado: dashboard HTML opcional omitido')
print(json.dumps(res,ensure_ascii=False,indent=2))
