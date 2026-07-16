# TPC-DS queries (realistic benchmark corpus)

The 99 standard TPC-DS queries, taken verbatim from the Apache Doris
project (Apache License 2.0):

- repository: https://github.com/apache/doris
- commit: `4090f6c40d2238b7aff73185bcada48f96fbd6be` (branch-3.0)
- path: `tools/tpcds-tools/queries/sf100/query{1..99}.sql`

Local deviation from the Doris copy: `query57.sql` had `v1. cc_name` /
`v1_lag. cc_name` / `v1_lead. cc_name` (whitespace after the qualifier
dot), which sqlfluff dialects cannot parse; the space was removed so all
99 queries parse under `--dialect ansi`.