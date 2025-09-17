
import streamlit as st
import pandas as pd
import numpy as np
from io import StringIO
import os

st.set_page_config(page_title="Voyage Performance (t/1000nm)", layout="wide")

st.title("Voyage Performance Analysis — Pre-DD vs Post-DD")
st.caption("Filter voyages, choose any t/1000nm metric, and quantify Post-DD vs Pre-DD deltas for B.c and L.c.")

# -----------------------------
# Data loading
# -----------------------------
uploaded = st.sidebar.file_uploader("Upload data (CSV/TSV with the same columns)", type=["csv","tsv"])

# Embedded fallback TSV (so the app works even without files)
EMBED_TSV = """Voy no\tPre-DD / Post-DD\tB/L\tCombined\tAvg Draft\tCargo Qty\tEOSP Date\tDur (COSP-EOSP) (Hrs)\tNM\tME FO\tME GO\tAE FO\tAE GO\tME+AE\tBlr\tt/1000nm(ME-FO)\tt/1000nm(ME-GO)\tt/1000nm(AE-FO)\tt/1000nm(AE-GO)\tt/1000nm(Total ME)\tt/1000nm(Total AE)\tt/1000nm(Total ME+AE)\tt/1000nm(Blr)\tFrom\tTo
2324944-B\tPre-DD\t\tB.c\t7.985\t0\t45291.5\t642\t6794.105\t393.55\t31.45\t58.8\t4.9\t488.7\t26.2\t57.92521605\t4.629012946\t8.654561565\t0.721213464\t62.554229\t9.375775028\t71.93000403\t3.856284235\tFangcheng\tNeptune Terminal
2324944-L\tPre-DD\t\tL.c\t14.53\t93023\t45328.96667\t644.5\t6214.461\t410.6\t14.7\t60.3\t3.7\t489.3\t25.7\t66.07169954\t2.365450519\t9.703174579\t0.595385505\t68.43715006\t10.29856008\t78.73571014\t4.135515534\tNeptune Terminal\tFangcheng
2400665-B\tPre-DD\t\tB.c\t8.305\t0\t45365.58333\t657.5\t7184.815\t445.8\t28.8\t57.3\t4.9\t536.8\t30.7\t62.04752662\t4.008453941\t7.975153153\t0.6819939\t66.05598056\t8.657147052\t74.71312762\t4.272900555\tFangcheng\tNeptune Terminal
240065-L\tPre-DD\t\tL.c\t14.94\t96118\t45403.91667\t699\t6345.12\t490.85\t4.2\t60.35\t0.5\t555.9\t13.8\t77.35866304\t0.661926016\t9.511246438\t0.078800716\t78.02058905\t9.590047154\t87.61063621\t2.174899765\tNeptune Terminal\tFangcheng
2401786-B\tPre-DD\t\tB.c\t6.6\t0\t45429.54167\t542.2\t6449.242\t342.6\t30.7\t46.5\t5.1\t424.9\t11.4\t53.122522\t4.760249344\t7.210149658\t0.790790608\t57.88277134\t8.000940266\t65.88371161\t1.767649594\tFangcheng\tNeptune Terminal
2401786-L\tPre-DD\t\tL.c\t15.01\t96798\t45462.39583\t619\t6330.79\t448.7\t0\t57.2\t0\t505.9\t19.9\t70.87583066\t0\t9.035207296\t0\t70.87583066\t9.035207296\t79.91103796\t3.143367573\tNeptune Terminal\tFangcheng
2402093-B\tPre-DD\t\tB.c\t6.6\t0\t45477.34167\t129.1\t1558.044\t77.28\t5.07\t13.75\t1.64\t97.74\t1.27\t49.60065313\t3.254080116\t8.825167967\t1.052601852\t52.85473324\t9.877769819\t62.73250306\t0.815124605\tFangcheng\tChengxi
2403543-B\tPost-DD\t\tB.c\t7.06\t0\t45530.0375\t456\t5271.93\t270.8\t17.3\t49.57\t2.86\t340.53\t10.94\t51.36638764\t3.281530673\t9.402628639\t0.542495822\t54.64791831\t9.945124461\t64.59304278\t2.075141362\tChengxi\tNeptune Terminal
2403543-L\tPost-DD\t\tL.c\t14.81\t95447\t45568.54167\t634\t6355.62\t424.53\t3.35\t59.53\t0.52\t487.93\t25.49\t66.79600102\t0.527092557\t9.366513416\t0.081817352\t67.32309358\t9.448330769\t76.77142435\t4.010623669\tNeptune Terminal\tFangcheng
2404792-B\tPost-DD\t\tB.c\t7.346666667\t0\t45599.29167\t534.6\t6022.316\t310.11\t32.48\t56.26\t4.67\t403.52\t24.02\t51.49347859\t5.39327395\t9.341920949\t0.775449179\t56.88675254\t10.11737013\t67.00412267\t3.988498777\tFangcheng\tRoberts Bank
2404792-L\tPost-DD\t\tL.c\t14.92\t95820\t45641.925\t626.2\t6454.886\t408.37\t3.07\t59.64\t0.34\t471.42\t9.28\t63.26525364\t0.475608709\t9.239512518\t0.052673277\t63.74086235\t9.292185795\t73.03304814\t1.437670627\tRoberts Bank\tFangcheng
2406105-B\tPost-DD\t\tB.c\t7.225\t0\t45674.75\t633\t6426.47\t351.19\t35.66\t54.85\t3.62\t445.32\t0.18\t54.64741919\t5.548924993\t8.535012223\t0.563295246\t60.19634418\t9.098307469\t69.29465165\t0.028009156\tFangcheng\tNeptune Terminal
2406105-L\tPost-DD\t\tL.c\t14.75\t95074\t45722.41667\t803.2\t7145.944\t460.45\t63.47\t63.59\t9.67\t597.18\t0\t64.4351537\t8.881961571\t8.898754314\t1.353215195\t73.31711528\t10.25196951\t83.56908478\t0\tNeptune Terminal\tFangcheng
2501172-B\tPost-DD\t\tB.c\t7.515\t0\t45752.97917\t540.8\t6080.357\t325.93\t24.68\t50.2\t3.65\t404.46\t0.04\t53.60376044\t4.058972195\t8.256094173\t0.6002937\t57.66273263\t8.856387873\t66.51912051\t0.006578561\tFangcheng\tNeptune Terminal
2501173-L\tPost-DD\t\tL.c\t14.78\t95713\t45782.90833\t612.8\t6354.386\t515.15\t1.87\t52.6\t0.33\t569.95\t0\t81.06998851\t0.294284924\t8.277747055\t0.051932634\t81.36427343\t8.329679689\t89.69395312\t0\tNeptune Terminal\tFangcheng
2502862-B\tPost-DD\t\tB.c\t7.455\t0\t45809.5375\t546.5\t6064.862\t271.365\t26.81\t48.961\t3.65\t350.786\t0.06\t44.74380456\t4.42054576\t8.07289597\t0.601827379\t49.16435032\t8.674723349\t57.83907367\t0.009893053\tFangcheng\tAt Sea
2502862-L\tPost-DD\t\tL.c\t14.95\t96800\t45841.08333\t637.2\t6307.968\t422.21\t5.44\t56.52\t0.74\t484.91\t0.01\t66.93280625\t0.862401331\t8.960096183\t0.117311946\t67.79520759\t9.077408129\t76.87261571\t0.001585297\tAt Sea\tFangcheng
2504325-B\tPost-DD\t\tB.c\t7.405\t0\t45871.37917\t450.9\t5319.115\t256.47\t19.82\t42.71\t3.26\t322.26\t0\t48.21666762\t3.726183773\t8.029531228\t0.61288391\t51.9428514\t8.642415139\t60.58526653\t0\tFangcheng\tAt Sea
2504325-L\tPost-DD\t\tL.c\t14.99\t96800\t45904.33333\t609\t6245.6\t408.4\t3.29\t57.42\t0.41\t469.52\t0\t65.39003458\t0.526770847\t9.193672345\t0.065646215\t65.91680543\t9.25931856\t75.17612399\t0\tNeptune Terminal\tFangcheng
2505346-B\tPost-DD\t\tB.c\t6.6\t0\t45910.9375\t35.5\t403.045\t0\t21.9\t0\t2.98\t24.88\t0.01\t0\t54.33636443\t0\t7.393715342\t54.33636443\t7.393715342\t61.73007977\t0.024811125\tFangcheng\tHong Kong
"""

def load_data():
    # 1) uploaded file if any
    if uploaded is not None:
        raw = uploaded.read()
        try:
            return pd.read_csv(StringIO(raw.decode("utf-8")))
        except Exception:
            return pd.read_csv(StringIO(raw.decode("utf-8")), sep="\\t")
    # 2) local data file in repo
    local_csv = os.path.join("data", "voyage_data.csv")
    if os.path.exists(local_csv):
        return pd.read_csv(local_csv)
    # 3) fallback to embedded data
    return pd.read_csv(StringIO(EMBED_TSV), sep="\\t")

df = load_data()

# Ensure numeric columns
for c in df.columns:
    if c not in ["Voy no", "Pre-DD / Post-DD", "B/L", "Combined", "From", "To"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")

metric_cols = [c for c in df.columns if c.startswith("t/1000nm")]
default_metric = "t/1000nm(Total ME+AE)" if "t/1000nm(Total ME+AE)" in metric_cols else (metric_cols[0] if metric_cols else None)

# -----------------------------
# Controls
# -----------------------------
phase = st.sidebar.selectbox("Phase", ["All", "Pre-DD", "Post-DD"], index=0)
mode = st.sidebar.selectbox("Combined (B.c or L.c)", ["All"] + sorted(df["Combined"].dropna().unique().tolist()), index=0)
metric = st.sidebar.selectbox("Metric (t/1000nm)", metric_cols, index=metric_cols.index(default_metric) if default_metric else 0)

filtered = df.copy()
if phase != "All":
    filtered = filtered[filtered["Pre-DD / Post-DD"] == phase]
if mode != "All":
    filtered = filtered[filtered["Combined"] == mode]

voyages = sorted(filtered["Voy no"].astype(str).unique().tolist())
pick_voys = st.sidebar.multiselect("Voyages to compare", voyages, default=voyages)

view = filtered[filtered["Voy no"].astype(str).isin(pick_voys)] if pick_voys else filtered

# -----------------------------
# Main layout
# -----------------------------
left, right = st.columns([2,1])

with left:
    st.subheader("Selected Voyages — Values")
    show_cols = ["Voy no", "Pre-DD / Post-DD", "Combined", metric]
    st.dataframe(view[show_cols].sort_values(["Combined","Pre-DD / Post-DD","Voy no"]).reset_index(drop=True), use_container_width=True)

    st.subheader("Comparison Chart")
    chart_df = view[["Voy no", metric]].copy()
    chart_df = chart_df.set_index("Voy no")
    st.bar_chart(chart_df)

with right:
    st.subheader("Phase Averages (by Combined)")
    phase_tbl = (df[df["Voy no"].astype(str).isin(pick_voys) if pick_voys else [True]]
                 .groupby(["Combined","Pre-DD / Post-DD"]))[metric].mean().unstack()
    st.dataframe(phase_tbl, use_container_width=True)

    st.subheader("Improvement — Post vs Pre (lower is better)")
    rows = []
    for comb, chunk in df.groupby("Combined"):
        pre = chunk.loc[chunk["Pre-DD / Post-DD"]=="Pre-DD", metric].mean()
        post = chunk.loc[chunk["Pre-DD / Post-DD"]=="Post-DD", metric].mean()
        delta = (post - pre) if (pd.notna(pre) and pd.notna(post)) else np.nan
        pct = ((post - pre)/pre*100) if (pd.notna(pre) and pd.notna(post) and pre!=0) else np.nan
        rows.append({"Combined": comb, "Pre": pre, "Post": post, "Δ (Post-Pre)": delta, "% change": pct})
    imp_df = pd.DataFrame(rows)
    st.dataframe(imp_df, use_container_width=True)

# -----------------------------
# Downloads
# -----------------------------
st.sidebar.markdown("---")
st.sidebar.download_button("Download current data (CSV)", data=df.to_csv(index=False), file_name="voyage_data_current.csv", mime="text/csv")
st.sidebar.download_button("Download filtered view (CSV)", data=view.to_csv(index=False), file_name="voyage_data_filtered.csv", mime="text/csv")

st.sidebar.info("Tip: Upload your updated CSV/TSV with the same column names to refresh the analysis.")
