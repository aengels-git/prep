from typing import Union
import pandas as pd
import polars as pl

def safe_left_join(
    left:Union[pl.DataFrame, pd.DataFrame], 
    right:Union[pl.DataFrame, pd.DataFrame], 
    on:Union[str, list],
    force_uniqueness:bool = True):
    """
    A left join that raises an error if the id of the right dataset is not unique!
    """
    if isinstance(left,pd.DataFrame):
        if isinstance(right, pl.DataFrame):
            right = right.to_pandas()
    else:
        if isinstance(right, pd.DataFrame):
            right = pl.DataFrame(right)
    if isinstance(right, pd.DataFrame):
        n_unique = right.loc[:,on].drop_duplicates().shape[0] 
    else:
        n_unique = right.select(on).unique().shape[0]
    print(f"Right dataframe has {n_unique} unique Ids!")
    if force_uniqueness and (n_unique != right.shape[0]):
        raise ValueError("Right dataframe does not have unique ids!")
    else:
        if isinstance(left, pd.DataFrame):
            return left.merge(right, on=on,how="left")
        else:
            left = left.with_columns(
                pl.col(on).cast(str)
            )
            right = right.with_columns(
                pl.col(on).cast(str)
            )
            return left.join(right, on=on,how="left")

