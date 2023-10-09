import polars as pl
import pandas as pd
from typing import Union

def prep_freq_table(data:Union[pl.DataFrame,pd.DataFrame], group_vars: Union[list,str]):
    if isinstance(data,pd.DataFrame):
        data = pl.DataFrame(data)
    if isinstance(group_vars,str):
        return data.groupby(group_vars).agg(
            pl.count()
        ).with_columns(
            (pl.col("count") / pl.sum("count")).alias("proportion")
        )
    else:
        prep_table = data.groupby(group_vars[1:]).agg(
            pl.col(group_vars[0]).apply(lambda s: s.value_counts().to_dict())
        ).unnest(group_vars[0]).explode(["","counts"]).rename(
            {"": group_vars[0]}
        ).with_columns(
            (pl.col("counts") / pl.sum("counts")).alias("proportion")
        )
        for var in group_vars:
            prep_table = prep_table.with_columns(
            (pl.col("proportion") / pl.col("proportion").sum().over(var)).alias(f"prop_{var}"),
            )
        return prep_table.to_pandas()