"""
tools.py — Database tools that can be passed to an LLM as callable functions.

Each tool is returned from a factory that accepts the db session,
keeping the function stateless and reusable across requests.
"""

from sqlalchemy.orm import Session
from sqlalchemy import text

DISALLOWED_KEYWORDS = {"INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "TRUNCATE", "GRANT"}


def _is_safe(sql: str) -> bool:
    upper = sql.upper()
    return not any(keyword in upper for keyword in DISALLOWED_KEYWORDS)


def build_execute_sql_tool(db: Session):
    """
    Factory that returns an execute_sql function bound to the given db session.
    Pass the returned function directly to your LLM's tool list.
    """

    def execute_sql(query: str) -> str:
        """
        Execute a SQL SELECT query against the campus PostgreSQL database
        and return the results as a plain-text string.
        Only SELECT queries are permitted.

        Args:
            query: A valid PostgreSQL SELECT statement.

        Returns:
            A string representation of the query results, or an error message.
        """
        if not _is_safe(query):
            return "Error: Only SELECT queries are permitted. Write operations are blocked."
        try:
            rows = db.execute(text(query)).fetchall()
            results = [dict(row._mapping) for row in rows]
            if not results:
                return "Query returned no results."
            return str(results)
        except Exception as e:
            return f"Query failed: {e}"

    return execute_sql
