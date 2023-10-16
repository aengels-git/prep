import polars as pl
import pandas as pd
from typing import Union

def prep_freq_table(data:Union[pl.DataFrame,pd.DataFrame], 
                    group_vars: Union[list,str], 
                    report:bool = False, 
                    percentage:bool = True, 
                    digits:int = 2):
    if isinstance(data,pd.DataFrame):
        data = pl.DataFrame(data)
    if isinstance(group_vars,str):
        tab =  data.groupby(group_vars).agg(
            pl.count()
        ).with_columns(
            (pl.col("count") / pl.sum("count")).alias("proportion")
        ).to_pandas()
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
        tab = prep_table.to_pandas()
    if report:
        if percentage:
            format_mapping = {col: f"{{:,.{digits}%}}" for col in tab.filter(regex="^prop",axis="columns").columns}
        else:
            format_mapping = {col: f"{{:,.{digits}f}}" for col in tab.filter(regex="^prop",axis="columns").columns}
        for key, value in format_mapping.items():
            tab[key] = tab[key].apply(value.format)
    return tab