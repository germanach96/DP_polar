"""Métodos de forecast. Todos con la misma firma:

    f(ctx, m) -> np.ndarray (n_ean x 8) con el forecast de los meses m+1..m+8

donde m es el índice de columna del "mes en curso" (versión): solo se usan columnas < m.
ctx: dict con H (n x T histórico, NaN antes de lanzamiento), C (cortes), E (EPOS), attr, months.
"""
import numpy as np
import pandas as pd
import warnings

H_LAGS = 8


def _ly(H, m):
    """Base año anterior para los meses m+1..m+8 (columna t-12)."""
    T = H.shape[1]
    out = np.full((H.shape[0], H_LAGS), np.nan)
    for k in range(1, H_LAGS + 1):
        j = m + k - 12
        if 0 <= j < min(m, T):
            out[:, k - 1] = H[:, j]
    return out


def _window(H, m, w):
    if m - w - 12 < 0:
        nan = np.full((H.shape[0], w), np.nan)
        return nan, nan.copy()
    rec = H[:, m - w:m]
    ly = H[:, m - w - 12:m - 12]
    return rec, ly


def _apply(base, g, cap=None):
    g = np.where(np.isfinite(g), g, 0.0)
    if cap is not None:
        g = np.clip(g, cap[0], cap[1])
    return np.clip(base * (1 + g)[:, None], 0, None)


# ---------------- trends sobre el EAN ----------------
def g_flat(H, m, w):
    rec, ly = _window(H, m, w)
    with np.errstate(invalid="ignore", divide="ignore"):
        s_ly = np.nansum(ly, 1)
        g = np.nansum(rec, 1) / s_ly - 1
    g[(s_ly <= 0) | np.isnan(ly).any(1)] = np.nan
    return g


def _ratios(H, m, w):
    rec, ly = _window(H, m, w)
    with np.errstate(invalid="ignore", divide="ignore"):
        r = rec / ly
    r[~np.isfinite(r) | (ly <= 0)] = np.nan
    return r


def g_median(H, m, w=6):
    r = _ratios(H, m, w)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return np.nanmedian(r, 1) - 1


def g_trimmed(H, m, w=6):
    r = _ratios(H, m, w)
    out = np.full(r.shape[0], np.nan)
    for i, row in enumerate(r):
        x = np.sort(row[np.isfinite(row)])
        if len(x) >= 3:
            out[i] = x[1:-1].mean() - 1
        elif len(x) > 0:
            out[i] = x.mean() - 1
    return out


def make_trend_method(gfun, cap=None, **kw):
    def f(ctx, m):
        H = ctx["H"]
        return _apply(_ly(H, m), gfun(H, m, **kw), cap)
    return f


def naive(ctx, m):
    return np.clip(_ly(ctx["H"], m), 0, None)


# ---------------- trend agregado (familia -> SKU) ----------------
def make_group_trend(level, w=6, cap=None):
    def f(ctx, m):
        H = ctx["H"]
        if m - w - 12 < 0:
            return np.full((H.shape[0], H_LAGS), np.nan)
        keys = ctx["attr"][level].values
        H0 = np.nan_to_num(H)
        df = pd.DataFrame(H0[:, m - w - 12:m])
        df["k"] = keys
        G = df.groupby("k").sum()
        rec = G.iloc[:, 12:12 + w].sum(1)
        ly = G.iloc[:, :w].sum(1)
        g = (rec / ly.where(ly > 0) - 1).reindex(keys).values
        return _apply(_ly(H, m), g, cap)
    return f


def make_blend_trend(level, w=6, alpha=0.5, cap=None):
    """Mezcla trend EAN y trend familia: alpha*EAN + (1-alpha)*familia (EAN sin trend -> familia)."""
    fam = make_group_trend(level, w)

    def f(ctx, m):
        H = ctx["H"]
        if m - w - 12 < 0:
            return np.full((H.shape[0], H_LAGS), np.nan)
        keys = ctx["attr"][level].values
        H0 = np.nan_to_num(H)
        df = pd.DataFrame(H0[:, m - w - 12:m]); df["k"] = keys
        G = df.groupby("k").sum()
        gf = (G.iloc[:, 12:12 + w].sum(1) / G.iloc[:, :w].sum(1).where(lambda s: s > 0) - 1).reindex(keys).values
        ge = g_flat(H, m, w)
        g = np.where(np.isfinite(ge), alpha * ge + (1 - alpha) * np.nan_to_num(gf), gf)
        return _apply(_ly(H, m), g, cap)
    return f


# ---------------- histórico limpio ----------------
def clean_history(H, m, x=0.4, win=5, seasonal=False, ctx=None):
    """Sustituye outliers (|A - mediana móvil| > x * mediana móvil) por la mediana móvil.
    Solo usa columnas < m. seasonal=True: aplica la regla sobre la serie desestacionalizada con el índice
    estacional de la house (para no marcar los picos navideños como outlier)."""
    Hm = H[:, :m].copy()
    if seasonal:
        S = ctx["season_idx"][:, :m]
        Hm = Hm / S
    df = pd.DataFrame(Hm.T)
    med = df.rolling(win, center=True, min_periods=3).median().values.T
    with np.errstate(invalid="ignore"):
        out = np.abs(Hm - med) > x * med
    out &= np.isfinite(Hm) & (med > 0)
    Hc = np.where(out, med, Hm)
    if seasonal:
        Hc = Hc * S
    return Hc, out


def make_clean_trend(x=0.4, w=6, win=5, seasonal=False, clean_base=True):
    def f(ctx, m):
        H = ctx["H"]
        Hc, _ = clean_history(H, m, x, win, seasonal, ctx)
        g = g_flat(Hc, m, w)
        base = _ly(Hc if clean_base else H, m)
        return _apply(base, g)
    return f


# ---------------- ajuste por cortes ----------------
def make_cut_adjusted(div=4, w=6, base_adj=True):
    def f(ctx, m):
        Ha = ctx["H"] + ctx["C"] / div
        g = g_flat(Ha, m, w)
        return _apply(_ly(Ha if base_adj else ctx["H"], m), g)
    return f


# ---------------- EPOS ----------------
def make_epos_trend(w=6, blend=None):
    """Trend de sell-out (EPOS) YoY aplicado al envío LY. blend=a -> a*EPOS + (1-a)*trend envíos."""
    def f(ctx, m):
        E = ctx["E"]
        ge = g_flat(E, m, w)
        if blend is not None:
            gs = g_flat(ctx["H"], m, w)
            ge = np.where(np.isfinite(ge), blend * ge + (1 - blend) * np.nan_to_num(gs), gs)
        return _apply(_ly(ctx["H"], m), ge)
    return f


# ---------------- nivel x estacionalidad ----------------
def make_level_season(w=3, level="house"):
    """Nivel reciente desestacionalizado (media de los últimos w meses / índice) x índice estacional del grupo.
    No necesita histórico de un año del EAN (sirve para lanzamientos)."""
    def f(ctx, m):
        H = ctx["H"]
        S = seasonal_index(H, m, ctx["attr"][level].values, ctx["months"])
        des = H[:, m - w:m] / S[:, m - w:m]
        lvl = np.nanmean(des, 1)
        idx = S[:, m + 1:m + 1 + H_LAGS] if S.shape[1] >= m + 1 + H_LAGS else None
        out = lvl[:, None] * idx
        return np.clip(out, 0, None)
    return f


def seasonal_index(H, m, keys, months, horizon=12):
    """Índice estacional por grupo con datos < m (media del peso de cada mes calendario en su año móvil).
    Devuelve matriz n x (T + horizon) alineada con months extendidos."""
    T = H.shape[1]
    allm = pd.date_range(months[0], periods=T + horizon, freq="MS")
    H0 = pd.DataFrame(np.nan_to_num(H[:, :m]), columns=months[:m]); H0["k"] = keys
    G = H0.groupby("k").sum()
    # índice por mes calendario: share del mes / (1/12), usando solo años completos de 12 meses previos a m
    Gm = G.T
    Gm.index = pd.to_datetime(Gm.index)
    roll = Gm.rolling(12, center=True, min_periods=12).mean()
    ratio = (Gm / roll).replace([np.inf, -np.inf], np.nan)
    idx = ratio.groupby(ratio.index.month).mean()
    # fallback global para meses sin dato
    glob = (Gm.sum(1) / Gm.sum(1).rolling(12, center=True, min_periods=12).mean())
    gidx = glob.groupby(glob.index.month).mean()
    idx = idx.apply(lambda c: c.fillna(gidx)).fillna(1.0)
    idx = idx.clip(lower=0.05)
    idx = idx / idx.mean()  # normaliza a media 1
    mat = idx.loc[allm.month].T.values  # grupos x meses
    gpos = {k: i for i, k in enumerate(idx.columns)}
    return mat[[gpos[k] for k in keys]]


# ---------------- ETS amortiguado ----------------
def ets_damped(ctx, m):
    from statsmodels.tsa.holtwinters import ExponentialSmoothing
    H = ctx["H"]
    out = np.full((H.shape[0], H_LAGS), np.nan)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for i in range(H.shape[0]):
            y = H[i, :m]
            y = y[np.isfinite(y)]
            if len(y) < 24 or y.sum() <= 0:
                continue
            try:
                mod = ExponentialSmoothing(y + 1.0, trend="add", damped_trend=True, seasonal="mul",
                                           seasonal_periods=12, initialization_method="estimated").fit()
                fc = mod.forecast(H_LAGS + 1)[1:] - 1.0  # m es el mes en curso -> saltar 1
                out[i] = np.clip(fc, 0, None)
            except Exception:
                pass
    return out


def ets_damped_house_share(ctx, m):
    """ETS damped a nivel house (serie más estable) y reparto a EAN por su peso LY en el mismo mes."""
    from statsmodels.tsa.holtwinters import ExponentialSmoothing
    H = ctx["H"]; keys = ctx["attr"]["house"].values
    if m < 24:
        return np.full((H.shape[0], H_LAGS), np.nan)
    H0 = pd.DataFrame(np.nan_to_num(H[:, :m])); H0["k"] = keys
    G = H0.groupby("k").sum()
    ly = _ly(H, m); ly0 = np.nan_to_num(ly)
    out = np.full((H.shape[0], H_LAGS), np.nan)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for k, row in G.iterrows():
            y = row.values
            mod = ExponentialSmoothing(y + 1.0, trend="add", damped_trend=True, seasonal="mul",
                                       seasonal_periods=12, initialization_method="estimated").fit()
            fc = mod.forecast(H_LAGS + 1)[1:] - 1.0
            sel = keys == k
            tot_ly = ly0[sel].sum(0)
            with np.errstate(invalid="ignore", divide="ignore"):
                out[sel] = ly0[sel] / tot_ly * fc
    return np.where(np.isnan(ly), np.nan, np.clip(out, 0, None))


# ---------------- variantes v2 ----------------
def make_group_trend_clean(level, w=12, x=0.4, damp=1.0):
    """Trend de grupo calculado sobre histórico limpio (regla estacional), aplicado a la base LY limpia del EAN.
    damp<1 aplica solo una fracción del trend."""
    def f(ctx, m):
        H = ctx["H"]
        if m - w - 12 < 0:
            return np.full((H.shape[0], H_LAGS), np.nan)
        Hc, _ = clean_history(H, m, x, 5, True, ctx)
        keys = ctx["attr"][level].values
        df = pd.DataFrame(np.nan_to_num(Hc[:, m - w - 12:m])); df["k"] = keys
        G = df.groupby("k").sum()
        g = (G.iloc[:, 12:12 + w].sum(1) / G.iloc[:, :w].sum(1).where(lambda s: s > 0) - 1).reindex(keys).values
        return _apply(_ly(Hc, m), damp * g)
    return f


def make_damped_group(level, w=12, damp=0.5):
    base = make_group_trend(level, w)

    def f(ctx, m):
        H = ctx["H"]
        F = base(ctx, m)
        ly = np.clip(_ly(H, m), 0, None)
        return ly + damp * (F - ly)
    return f


def make_combo(*fs):
    """Media simple de varios métodos (ignora NaN)."""
    def f(ctx, m):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            return np.nanmean(np.stack([g(ctx, m) for g in fs]), 0)
    return f


def make_ytd_house(min_months=3):
    """Trend acumulado del año fiscal en curso a nivel house (si < min_months, usa últimos 12M)."""
    def f(ctx, m):
        months = ctx["months"]
        cur = pd.Timestamp(months[0]) + pd.DateOffset(months=m)
        n = (cur.month - 7) % 12  # meses cerrados del FY en curso
        w = n if n >= min_months else 12
        return make_group_trend("house", w)(ctx, m)
    return f


# ---------------- variantes v3 ----------------
def _group_g(M, m, w, keys, mask=None):
    if m - w - 12 < 0:
        return np.full(M.shape[0], np.nan)
    X = np.nan_to_num(M[:, m - w - 12:m]).copy()
    if mask is not None:
        X[~mask] = 0
    df = pd.DataFrame(X); df["k"] = keys
    G = df.groupby("k").sum()
    g = G.iloc[:, 12:12 + w].sum(1) / G.iloc[:, :w].sum(1).where(lambda s: s > 0) - 1
    return g.reindex(keys).values


def make_group_lfl(level, w=12, clean=False):
    """Trend de grupo like-for-like: solo EANs con venta en toda la ventana LY (excluye lanzamientos que inflan el trend)."""
    def f(ctx, m):
        H = ctx["H"]
        if m - w - 12 < 0:
            return np.full((H.shape[0], H_LAGS), np.nan)
        Hs = clean_history(H, m, 0.4, 5, True, ctx)[0] if clean else H
        mask = np.isfinite(H[:, m - w - 12])  # vivo al inicio de la ventana LY
        g = _group_g(Hs, m, w, ctx["attr"][level].values, mask)
        return _apply(_ly(Hs, m), g)
    return f


def make_epos_group(level, w=6, lfl=True):
    """Trend de EPOS agregado al grupo aplicado al envío LY del EAN."""
    def f(ctx, m):
        E = ctx["E"]
        mask = np.isfinite(E[:, m - w - 12]) if (lfl and m - w - 12 >= 0) else None
        g = _group_g(E, m, w, ctx["attr"][level].values, mask)
        return _apply(_ly(ctx["H"], m), g)
    return f


def make_clean_rescaled(level="house", w=12, x=0.4, total_level="house", lfl_total=False):
    """Base limpia (reparto por EAN sin picos) pero total del grupo = LY real x trend del grupo (sin perder volumen).
    Es decir: el % del grupo decide el total; la limpieza solo decide cómo se reparte entre EANs/meses."""
    def f(ctx, m):
        H = ctx["H"]
        if m - w - 12 < 0:
            return np.full((H.shape[0], H_LAGS), np.nan)
        Hc, _ = clean_history(H, m, x, 5, True, ctx)
        keys = ctx["attr"][total_level].values
        g = _group_g(Hc, m, w, keys)
        Fc = _apply(_ly(Hc, m), g)  # limpia
        lyr = np.nan_to_num(_ly(H, m)); lyc = np.nan_to_num(_ly(Hc, m))
        out = Fc.copy()
        for k in np.unique(keys):
            sel = keys == k
            for j in range(H_LAGS):
                sc = lyr[sel, j].sum() / max(lyc[sel, j].sum(), 1e-9)
                out[sel, j] = Fc[sel, j] * sc
        return out
    return f
