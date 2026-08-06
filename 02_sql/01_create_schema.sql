-- =====================================================================
-- 01_create_schema.sql
-- Mubadala Portfolio Strategy Analyst - analytical warehouse
-- Dialect: SQLite (portable; syntax is ANSI-compatible for Postgres/T-SQL
--          with only the AUTOINCREMENT / data-type keywords changed)
--
-- Design: Kimball-style STAR SCHEMA.
--   * dim_*  tables describe "who / what / where"  (few rows, many columns)
--   * fact_* tables record measurable events        (many rows, few columns)
-- Why a star schema? Power BI's VertiPaq engine and DAX relationships are
-- optimised for one-to-many joins radiating from dimensions into facts.
-- A single flat table would duplicate text, bloat the model and make
-- slicers ambiguous.
-- =====================================================================

DROP TABLE IF EXISTS fact_whoop_metrics;
DROP TABLE IF EXISTS fact_omv_financials;
DROP TABLE IF EXISTS fact_gfs_segment;
DROP TABLE IF EXISTS fact_gfs_financials;
DROP TABLE IF EXISTS fact_market_data;
DROP TABLE IF EXISTS fact_transaction;
DROP TABLE IF EXISTS fact_holding;
DROP TABLE IF EXISTS fact_credit_rating;
DROP TABLE IF EXISTS fact_asset_allocation;
DROP TABLE IF EXISTS fact_capital_flow;
DROP TABLE IF EXISTS fact_performance;
DROP TABLE IF EXISTS dim_asset_class;
DROP TABLE IF EXISTS dim_geography;
DROP TABLE IF EXISTS dim_sector;
DROP TABLE IF EXISTS dim_platform;
DROP TABLE IF EXISTS dim_source;

-- ---------------------------------------------------------------- DIMENSIONS
CREATE TABLE dim_source (
    source_id    TEXT PRIMARY KEY,
    source_name  TEXT NOT NULL,
    source_url   TEXT,
    as_of_date   DATE,
    source_class TEXT CHECK (source_class IN
                 ('Official','Market data','Press reporting','Analyst estimate'))
);

CREATE TABLE dim_platform (
    platform_id   INTEGER PRIMARY KEY,
    platform_name TEXT NOT NULL UNIQUE,
    platform_ceo  TEXT,
    mandate       TEXT,
    reach         TEXT,
    source_id     TEXT REFERENCES dim_source(source_id)
);

CREATE TABLE dim_sector (
    sector_id       INTEGER PRIMARY KEY,
    sector_name     TEXT NOT NULL UNIQUE,
    strategic_theme TEXT,
    ai_exposure     TEXT CHECK (ai_exposure IN ('High','Medium','Low','n/a'))
);

CREATE TABLE dim_geography (
    geo_id       INTEGER PRIMARY KEY,
    country      TEXT NOT NULL UNIQUE,
    region       TEXT NOT NULL,
    currency     TEXT,
    market_class TEXT
);

CREATE TABLE dim_asset_class (
    asset_class_id  INTEGER PRIMARY KEY,
    asset_class     TEXT NOT NULL UNIQUE,
    weight_2025_pct REAL CHECK (weight_2025_pct BETWEEN 0 AND 100),
    description     TEXT,
    source_id       TEXT REFERENCES dim_source(source_id)
);

-- -------------------------------------------------------------------- FACTS
CREATE TABLE fact_performance (
    year      INTEGER NOT NULL,
    metric    TEXT    NOT NULL,
    value     REAL,
    basis     TEXT,
    source_id TEXT REFERENCES dim_source(source_id),
    PRIMARY KEY (year, metric)
);

CREATE TABLE fact_capital_flow (
    year                     INTEGER PRIMARY KEY,
    deployments_usd_bn       REAL,
    proceeds_usd_bn          REAL,
    net_deployment_usd_bn    REAL,
    basis                    TEXT,
    source_id                TEXT REFERENCES dim_source(source_id)
);

CREATE TABLE fact_asset_allocation (
    year           INTEGER NOT NULL,
    asset_class_id INTEGER NOT NULL REFERENCES dim_asset_class(asset_class_id),
    asset_class    TEXT,
    weight_pct     REAL,
    implied_usd_bn REAL,
    source_id      TEXT REFERENCES dim_source(source_id),
    PRIMARY KEY (year, asset_class_id)
);

CREATE TABLE fact_credit_rating (
    agency    TEXT NOT NULL,
    tenor     TEXT NOT NULL,
    rating    TEXT,
    outlook   TEXT,
    source_id TEXT REFERENCES dim_source(source_id),
    PRIMARY KEY (agency, tenor)
);

CREATE TABLE fact_holding (
    holding_id        INTEGER PRIMARY KEY,
    holding_name      TEXT NOT NULL,
    sector_id         INTEGER REFERENCES dim_sector(sector_id),
    geo_id            INTEGER REFERENCES dim_geography(geo_id),
    platform_id       INTEGER REFERENCES dim_platform(platform_id),
    ownership         TEXT,
    listing_status    TEXT CHECK (listing_status IN ('Listed','Private')),
    ticker            TEXT,
    investment_thesis TEXT,
    evidence_grade    TEXT,
    source_id         TEXT REFERENCES dim_source(source_id)
);

CREATE TABLE fact_transaction (
    deal_id         INTEGER PRIMARY KEY,
    announce_date   DATE NOT NULL,
    target          TEXT NOT NULL,
    deal_type       TEXT,
    sector_id       INTEGER REFERENCES dim_sector(sector_id),
    geo_id          INTEGER REFERENCES dim_geography(geo_id),
    platform_id     INTEGER REFERENCES dim_platform(platform_id),
    value_usd_m     REAL,
    disclosure_note TEXT,
    evidence_grade  TEXT,
    source_id       TEXT REFERENCES dim_source(source_id)
);

CREATE TABLE fact_market_data (
    ticker            TEXT PRIMARY KEY,
    company           TEXT,
    sector_id         INTEGER REFERENCES dim_sector(sector_id),
    currency          TEXT,
    price             REAL,
    mkt_cap_bn        REAL,
    ev_bn             REAL,
    revenue_ttm_bn    REAL,
    ebitda_ttm_bn     REAL,
    net_income_ttm_bn REAL,
    pe_ttm            REAL,
    ev_ebitda         REAL,
    ev_sales          REAL,
    fcf_ttm_bn        REAL,
    net_debt_bn       REAL,
    beta_5y           REAL,
    as_of             DATE,
    source_id         TEXT REFERENCES dim_source(source_id)
);

CREATE TABLE fact_gfs_financials (
    year                     INTEGER PRIMARY KEY,
    revenue_usd_m            REAL,
    gross_profit_usd_m       REAL,
    operating_income_usd_m   REAL,
    net_income_usd_m         REAL,
    operating_cash_flow_usd_m REAL,
    capex_usd_m              REAL,
    free_cash_flow_usd_m     REAL,
    source_id                TEXT REFERENCES dim_source(source_id)
);

CREATE TABLE fact_gfs_segment (
    year          INTEGER NOT NULL,
    end_market    TEXT NOT NULL,
    revenue_usd_m REAL,
    source_id     TEXT REFERENCES dim_source(source_id),
    PRIMARY KEY (year, end_market)
);

CREATE TABLE fact_omv_financials (
    year                    INTEGER PRIMARY KEY,
    revenue_eur_m           REAL,
    ebit_eur_m              REAL,
    ebitda_eur_m            REAL,
    net_income_common_eur_m REAL,
    free_cash_flow_eur_m    REAL,
    dps_eur                 REAL,
    source_id               TEXT REFERENCES dim_source(source_id)
);

CREATE TABLE fact_whoop_metrics (
    metric         TEXT PRIMARY KEY,
    value          REAL,
    evidence_grade TEXT,
    source_id      TEXT REFERENCES dim_source(source_id)
);

-- Indexes on the foreign keys most used in slicing
CREATE INDEX idx_holding_sector  ON fact_holding(sector_id);
CREATE INDEX idx_holding_geo     ON fact_holding(geo_id);
CREATE INDEX idx_txn_sector      ON fact_transaction(sector_id);
CREATE INDEX idx_txn_date        ON fact_transaction(announce_date);
CREATE INDEX idx_mkt_sector      ON fact_market_data(sector_id);
