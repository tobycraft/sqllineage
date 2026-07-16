"""
CodSpeed benchmark: end-to-end ``print_column_lineage()`` over the 99
TPC-DS queries (see ``benchmarks/tpcds/README.md``), combined into a single
script and analyzed by one ``LineageRunner`` so lineage is built statement
upon statement inside one merged graph, like a real multi-statement ETL job.
"""

import contextlib
import io
import os
import re

from sqllineage.config import SQLLineageConfig
from sqllineage.runner import LineageRunner

TPCDS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tpcds")


def _load_combined_sql() -> str:
    files = sorted(
        (f for f in os.listdir(TPCDS_DIR) if f.endswith(".sql")),
        key=lambda f: int(re.sub(r"\D", "", f)),
    )
    parts: list[str] = []
    for filename in files:
        name = filename[:-4]
        with open(os.path.join(TPCDS_DIR, filename)) as f:
            sql = f.read()
        # some query files hold several statements (e.g. query14); wrap each
        # as CREATE TABLE ... AS so column lineage has a write target
        stmts = [s.strip() for s in sql.split(";") if s.strip()]
        parts.extend(
            f"CREATE TABLE lineage_{name}_{i} AS\n{stmt}"
            for i, stmt in enumerate(stmts)
        )
    return ";\n".join(parts)


COMBINED_SQL = _load_combined_sql()


def test_tpcds_print_column_lineage(benchmark):
    def run():
        with contextlib.redirect_stdout(io.StringIO()):
            LineageRunner(COMBINED_SQL, dialect="ansi").print_column_lineage()

    benchmark(run)


def test_tpcds_print_column_lineage_rustworkx(benchmark):
    def run():
        with SQLLineageConfig(
            GRAPH_OPERATOR_CLASS="sqllineage.core.graph.rustworkx.RustworkXGraphOperator"
        ):
            with contextlib.redirect_stdout(io.StringIO()):
                LineageRunner(COMBINED_SQL, dialect="ansi").print_column_lineage()

    benchmark(run)
