-- =====================================================================
-- 03_analysis_queries.sql
-- Twelve analytical queries answering the research questions of this
-- project. Each is written to be readable and to demonstrate a distinct
-- SQL technique (CTEs, window functions, self-joins, CASE logic,
-- aggregate filtering, ranking, percent-of-total, concentration maths).
-- =====================================================================

-- Q1 --------------------------------------------------------------------
-- Headline scorecard: everything Mubadala officially disclosed for 2025.
SELECT p.year, p.metric, p.value, s.source_class, s.source_url
FROM   fact_performance p
JOIN   dim_source s ON s.source_id = p.source_id
WHERE  p.year = 2025
ORDER  BY p.metric;

-- Q2 --------------------------------------------------------------------
-- Asset-class mix with a running cumulative weight (window function).
-- Shows how much of the book the top N asset classes represent.
SELECT  asset_class,
        weight_pct,
        implied_usd_bn,
        SUM(weight_pct) OVER (ORDER BY weight_pct DESC
                              ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
            AS cumulative_weight_pct,
        RANK() OVER (ORDER BY weight_pct DESC) AS weight_rank
FROM    fact_asset_allocation
WHERE   year = 2025
ORDER   BY weight_pct DESC;

-- Q3 --------------------------------------------------------------------
-- Capital recycling: is Mubadala a net buyer or net seller, and is the
-- balance sheet self-funding? A recycling ratio above 1.0 means the
-- portfolio returned more cash than it consumed.
SELECT  year,
        deployments_usd_bn,
        proceeds_usd_bn,
        net_deployment_usd_bn,
        ROUND(proceeds_usd_bn / deployments_usd_bn, 3) AS recycling_ratio,
        ROUND(100.0 * (deployments_usd_bn - LAG(deployments_usd_bn)
              OVER (ORDER BY year)) / LAG(deployments_usd_bn)
              OVER (ORDER BY year), 1) AS deployment_growth_pct
FROM    fact_capital_flow
ORDER   BY year;

-- Q4 --------------------------------------------------------------------
-- Portfolio composition by sector: holdings count and share of book.
SELECT  se.sector_name,
        se.strategic_theme,
        se.ai_exposure,
        COUNT(h.holding_id)                                   AS n_holdings,
        ROUND(100.0 * COUNT(h.holding_id) /
              (SELECT COUNT(*) FROM fact_holding), 1)          AS pct_of_holdings
FROM    fact_holding h
JOIN    dim_sector  se ON se.sector_id = h.sector_id
GROUP   BY se.sector_name, se.strategic_theme, se.ai_exposure
ORDER   BY n_holdings DESC, se.sector_name;

-- Q5 --------------------------------------------------------------------
-- Geographic footprint, rolled up to region, with home-bias flag.
SELECT  g.region,
        COUNT(*)                                    AS n_holdings,
        ROUND(100.0*COUNT(*)/(SELECT COUNT(*) FROM fact_holding),1) AS pct,
        CASE WHEN g.region = 'Middle East' THEN 'Domestic / mandate-driven'
             ELSE 'International / return-driven' END          AS capital_role
FROM    fact_holding h
JOIN    dim_geography g ON g.geo_id = h.geo_id
GROUP   BY g.region
ORDER   BY n_holdings DESC;

-- Q6 --------------------------------------------------------------------
-- Platform x sector cross-tab (conditional aggregation instead of PIVOT,
-- which SQLite does not support).
SELECT  pl.platform_name,
        SUM(CASE WHEN se.sector_name='Technology'                THEN 1 ELSE 0 END) AS technology,
        SUM(CASE WHEN se.sector_name='Healthcare & Life Sciences' THEN 1 ELSE 0 END) AS healthcare,
        SUM(CASE WHEN se.sector_name='Energy & Sustainability'    THEN 1 ELSE 0 END) AS energy,
        SUM(CASE WHEN se.sector_name='Financial Services'         THEN 1 ELSE 0 END) AS financial_services,
        COUNT(*)                                                                     AS total
FROM    fact_holding h
JOIN    dim_platform pl ON pl.platform_id = h.platform_id
JOIN    dim_sector   se ON se.sector_id   = h.sector_id
GROUP   BY pl.platform_name
ORDER   BY total DESC;

-- Q7 --------------------------------------------------------------------
-- Deal flow by year and sector, using only transactions with a disclosed
-- value so the totals are honest.
WITH dated AS (
    SELECT CAST(strftime('%Y', announce_date) AS INTEGER) AS deal_year, *
    FROM   fact_transaction
)
SELECT  d.deal_year,
        se.sector_name,
        COUNT(*)                                    AS n_deals,
        SUM(CASE WHEN d.value_usd_m IS NOT NULL THEN 1 ELSE 0 END) AS n_with_value,
        ROUND(SUM(COALESCE(d.value_usd_m,0))/1000.0, 2)            AS disclosed_usd_bn
FROM    dated d
JOIN    dim_sector se ON se.sector_id = d.sector_id
GROUP   BY d.deal_year, se.sector_name
ORDER   BY d.deal_year DESC, disclosed_usd_bn DESC;

-- Q8 --------------------------------------------------------------------
-- Concentration: Herfindahl-Hirschman Index of the asset-class mix.
-- HHI = sum of squared percentage weights. Below 1500 = unconcentrated,
-- 1500-2500 = moderately concentrated, above 2500 = concentrated.
SELECT  ROUND(SUM(weight_pct * weight_pct), 0)              AS hhi,
        CASE WHEN SUM(weight_pct*weight_pct) < 1500 THEN 'Unconcentrated'
             WHEN SUM(weight_pct*weight_pct) < 2500 THEN 'Moderately concentrated'
             ELSE 'Concentrated' END                        AS interpretation,
        ROUND(1.0/ (SUM(weight_pct*weight_pct)/10000.0), 2) AS effective_n_buckets
FROM    fact_asset_allocation
WHERE   year = 2025;

-- Q9 --------------------------------------------------------------------
-- Trading-multiple comparables table by sector, with the sector median
-- computed as a window so every peer row can see its own premium/discount.
WITH peers AS (
    SELECT m.*, se.sector_name
    FROM   fact_market_data m
    JOIN   dim_sector se ON se.sector_id = m.sector_id
    WHERE  m.pe_ttm IS NOT NULL
)
SELECT  sector_name,
        ticker,
        company,
        ROUND(mkt_cap_bn,1)  AS mkt_cap_bn,
        ROUND(pe_ttm,1)      AS pe_ttm,
        ROUND(AVG(pe_ttm) OVER (PARTITION BY sector_name),1) AS sector_mean_pe,
        ROUND(pe_ttm - AVG(pe_ttm) OVER (PARTITION BY sector_name),1) AS vs_sector_mean,
        NTILE(4) OVER (PARTITION BY sector_name ORDER BY pe_ttm) AS pe_quartile
FROM    peers
ORDER   BY sector_name, pe_ttm;

-- Q10 -------------------------------------------------------------------
-- GlobalFoundries: revenue mix shift, 2023 -> 2025. Shows the pivot from
-- smart mobile toward automotive and datacenter (the AI-adjacent markets).
WITH mix AS (
    SELECT year, end_market, revenue_usd_m,
           ROUND(100.0*revenue_usd_m /
                 SUM(revenue_usd_m) OVER (PARTITION BY year), 1) AS pct_of_revenue
    FROM   fact_gfs_segment
)
SELECT  a.end_market,
        a.revenue_usd_m  AS rev_2023, a.pct_of_revenue AS pct_2023,
        c.revenue_usd_m  AS rev_2025, c.pct_of_revenue AS pct_2025,
        ROUND(c.pct_of_revenue - a.pct_of_revenue, 1) AS mix_shift_pp,
        ROUND(100.0*(c.revenue_usd_m - a.revenue_usd_m)/a.revenue_usd_m,1) AS growth_pct
FROM    mix a
JOIN    mix c ON c.end_market = a.end_market AND c.year = 2025
WHERE   a.year = 2023
ORDER   BY mix_shift_pp DESC;

-- Q11 -------------------------------------------------------------------
-- OMV: cash generation and dividend cover through the commodity cycle.
SELECT  year,
        revenue_eur_m,
        ebitda_eur_m,
        ROUND(100.0*ebitda_eur_m/revenue_eur_m,1)                AS ebitda_margin_pct,
        free_cash_flow_eur_m,
        dps_eur,
        ROUND(free_cash_flow_eur_m / (dps_eur*326.0), 2)         AS fcf_dividend_cover_x,
        CASE WHEN free_cash_flow_eur_m < dps_eur*326.0
             THEN 'Dividend NOT covered by FCF' ELSE 'Covered' END AS cover_flag
FROM    fact_omv_financials
ORDER   BY year;

-- Q12 -------------------------------------------------------------------
-- Evidence-quality audit: what proportion of the dataset is officially
-- sourced versus estimated? Any serious analyst should be able to answer
-- this about their own model.
SELECT 'fact_holding' AS table_name, evidence_grade, COUNT(*) AS n
FROM   fact_holding      GROUP BY evidence_grade
UNION ALL
SELECT 'fact_transaction', evidence_grade, COUNT(*)
FROM   fact_transaction  GROUP BY evidence_grade
ORDER  BY table_name, n DESC;
