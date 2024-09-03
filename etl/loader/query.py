from sqlalchemy import text
from etl.loader.table import Table


def upsert_query_func(table: Table, table_name: str, unique_key: str):
    """
    Upsert SQL Query Func

    Args:
        table: data
        table_name: schema table name
        unique_key: upsert unique key
    """

    update_clause = ", ".join(
        f"{col} = VALUES({col})" for col in table.columns if col != unique_key
    )

    query = f"""
    INSERT INTO {table_name} ({table.comma_seperated_columns})
    VALUES {table.comma_seperated_itertuples}
    ON DUPLICATE KEY UPDATE {update_clause};
    """

    query = text(query)
    return query


def select_query_func(table_name: str):
    """
    Select SQL Query Func
    """

    query = f"""
    SELECT * FROM {table_name};
    """

    query = text(query)
    return query
