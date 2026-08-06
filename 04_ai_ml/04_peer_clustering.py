"""
04_peer_clustering.py
Unsupervised clustering of the listed peer universe.

QUESTION: analysts assign comparables by industry label. But the market does
not price industries - it prices business characteristics. Which companies
does the market ACTUALLY treat as similar to GlobalFoundries and OMV?

METHOD: standardise size and valuation features, reduce with PCA for
visualisation, then k-means. Cluster count chosen by silhouette score rather
than by eye.
"""
import json, os
import numpy as np, pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

HERE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(HERE, "outputs"); os.makedirs(OUT, exist_ok=True)
WH   = os.path.join(os.path.dirname(HERE), "01_data", "warehouse")

df = pd.read_csv(os.path.join(WH, "fact_market_data.csv"))
df = df.dropna(subset=["pe_ttm","mkt_cap_bn","revenue_ttm_bn"]).copy()
df["ps_ratio"]      = df["mkt_cap_bn"] / df["revenue_ttm_bn"]
df["log_mkt_cap"]   = np.log(df["mkt_cap_bn"])
df["log_revenue"]   = np.log(df["revenue_ttm_bn"])
df["log_pe"]        = np.log(df["pe_ttm"])
FEATS = ["log_mkt_cap","log_revenue","log_pe","ps_ratio"]

X = StandardScaler().fit_transform(df[FEATS].values)
pca = PCA(n_components=2, random_state=0); XY = pca.fit_transform(X)

scores = {}
for k in range(2, 6):
    km = KMeans(n_clusters=k, n_init=25, random_state=0).fit(X)
    scores[k] = float(silhouette_score(X, km.labels_))
best_k = max(scores, key=scores.get)
km = KMeans(n_clusters=best_k, n_init=50, random_state=0).fit(X)
df["cluster"] = km.labels_
df["pc1"], df["pc2"] = XY[:,0], XY[:,1]

def neighbours(ticker, n=3):
    row = df[df.ticker==ticker]
    if row.empty: return []
    i = row.index[0]
    d = np.linalg.norm(X - X[df.index.get_loc(i)], axis=1)
    order = np.argsort(d)[1:n+1]
    return [{"ticker":df.iloc[j]["ticker"], "company":df.iloc[j]["company"],
             "distance":round(float(d[j]),3),
             "same_industry_label": bool(df.iloc[j]["sector_id"]==row.iloc[0]["sector_id"])}
            for j in order]

profiles = []
for c in sorted(df.cluster.unique()):
    sub = df[df.cluster==c]
    profiles.append({"cluster":int(c), "n":int(len(sub)),
        "members":sub["ticker"].tolist(),
        "median_mkt_cap_bn":round(float(sub.mkt_cap_bn.median()),1),
        "median_pe":round(float(sub.pe_ttm.median()),1),
        "median_ps":round(float(sub.ps_ratio.median()),2)})

result = {
 "question":"Which listed companies does the market actually price like GlobalFoundries and OMV?",
 "features_used":FEATS,
 "n_companies":int(len(df)),
 "silhouette_by_k":scores, "chosen_k":best_k,
 "pca_explained_variance":[round(float(v),3) for v in pca.explained_variance_ratio_],
 "cluster_profiles":profiles,
 "assignments":[{"ticker":r.ticker,"company":r.company,"cluster":int(r.cluster),
                 "pe":round(float(r.pe_ttm),1),"ps":round(float(r.ps_ratio),2),
                 "mkt_cap_bn":float(r.mkt_cap_bn),"pc1":round(float(r.pc1),3),
                 "pc2":round(float(r.pc2),3)} for r in df.itertuples()],
 "nearest_neighbours":{"GFS":neighbours("GFS"), "OMV":neighbours("OMV")},
 "reading":("Clustering on size and valuation characteristics rather than industry labels "
            "is a check on comparables selection. Where a company's nearest neighbours come "
            "from a different industry, the analyst should ask whether the chosen peer set "
            "reflects how the market really prices the business."),
}
with open(os.path.join(OUT,"peer_clustering.json"),"w") as f: json.dump(result,f,indent=2)
df.to_csv(os.path.join(OUT,"peer_clusters.csv"), index=False)

print(f"{len(df)} companies | silhouette by k: " + ", ".join(f"k={k}:{v:.3f}" for k,v in scores.items()))
print(f"Chosen k = {best_k}; PCA explains {sum(pca.explained_variance_ratio_)*100:.0f}% of variance\n")
for p in profiles:
    print(f"  Cluster {p['cluster']} (n={p['n']:2d})  median cap ${p['median_mkt_cap_bn']:7.1f}bn  P/E {p['median_pe']:6.1f}x  P/S {p['median_ps']:5.2f}x")
    print(f"              {', '.join(p['members'])}")
print("\nNearest neighbours of GFS:", [f"{n['ticker']} ({n['distance']})" for n in result['nearest_neighbours']['GFS']])
print("Nearest neighbours of OMV:", [f"{n['ticker']} ({n['distance']})" for n in result['nearest_neighbours']['OMV']])
