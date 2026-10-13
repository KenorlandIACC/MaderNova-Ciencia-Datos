"""Funciones reutilizables para el análisis de MaderNova."""
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import spearmanr, zscore
from joblib import Parallel, delayed

CAMPOS = ['fecha_registro','planta','tipo_tablero','volumen_producido_m3','merma_m3','consumo_energia_kwh','tiempo_produccion_hr','ventas_unidades','canal_distribucion','tiempo_despacho_dias']

def preparar(df):
    """Normaliza fechas y calcula indicadores sin modificar la fuente."""
    df = df.copy()
    if pd.api.types.is_numeric_dtype(df['fecha_registro']):
        df['fecha_registro'] = pd.to_datetime(df['fecha_registro'], unit='D', origin='1899-12-30')
    else:
        df['fecha_registro'] = pd.to_datetime(df['fecha_registro'], errors='coerce')
    for c in CAMPOS[3:8] + ['tiempo_despacho_dias']:
        df[c] = pd.to_numeric(df[c], errors='coerce')
    df['tasa_merma_pct'] = np.where(df['volumen_producido_m3']>0,100*df['merma_m3']/df['volumen_producido_m3'],np.nan)
    df['energia_kwh_m3'] = np.where(df['volumen_producido_m3']>0,df['consumo_energia_kwh']/df['volumen_producido_m3'],np.nan)
    df['productividad_m3_hr'] = np.where(df['tiempo_produccion_hr']>0,df['volumen_producido_m3']/df['tiempo_produccion_hr'],np.nan)
    return df

def calidad(df):
    """Auditoría de integridad, rangos y valores extremos IQR."""
    numericas = ['volumen_producido_m3','merma_m3','consumo_energia_kwh','tiempo_produccion_hr','ventas_unidades','tiempo_despacho_dias']
    res={'filas':len(df),'faltantes':int(df[CAMPOS].isna().sum().sum()),'duplicados':int(df[CAMPOS].duplicated().sum()),'fechas_invalidas':int(df.fecha_registro.isna().sum()),'negativos':int((df[numericas]<0).sum().sum()),'merma_supera_volumen':int((df.merma_m3>df.volumen_producido_m3).sum()),'tiempo_produccion_no_positivo':int((df.tiempo_produccion_hr<=0).sum()),'volumen_no_positivo':int((df.volumen_producido_m3<=0).sum())}
    res['atipicos_iqr']={}
    for c in numericas:
        q1,q3=np.percentile(df[c].dropna(),[25,75]);iqr=q3-q1
        res['atipicos_iqr'][c]=int(((df[c]<q1-1.5*iqr)|(df[c]>q3+1.5*iqr)).sum())
    return res

def resumen_planta(grupo):
    """Cálculos ponderados por volumen para una planta."""
    nombre, g=grupo
    v=g.volumen_producido_m3.sum()
    return {'planta':nombre,'registros':len(g),'volumen_m3':v,'merma_m3':g.merma_m3.sum(),'merma_pct_ponderada':100*g.merma_m3.sum()/v,'energia_kwh_m3_ponderada':g.consumo_energia_kwh.sum()/v,'despacho_promedio_dias':g.tiempo_despacho_dias.mean()}

def resumenes_paralelos(df):
    """Joblib permite procesar plantas independientemente; n_jobs=2."""
    return pd.DataFrame(Parallel(n_jobs=2)(delayed(resumen_planta)(grupo) for grupo in df.groupby('planta')))

def correlacion(df):
    """Correlación de Spearman entre volumen y consumo; no implica causalidad."""
    r,p=spearmanr(df.volumen_producido_m3,df.consumo_energia_kwh,nan_policy='omit')
    return {'rho':float(r),'p_valor':float(p)}
