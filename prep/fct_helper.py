from pandas.api.types import CategoricalDtype
import pandas as pd
from typing import Union
import polars as pl

def fct_ordered(series:Union[pd.Series,pl.Series], ordered_levels:list):
    """
    Create ordered factor from string or normal cat series
    Example: diamonds.cut = fct_ordered(diamonds.cut,ordered_levels=["Fair","Good","Very Good","Premium","Ideal"])
             pl_diamonds.with_columns(
                 fct_ordered(pl.col("cut"),["Fair","Good","Very Good","Premium","Ideal"])
             ).sort("cut")
    """
    if isinstance(series, pd.Series):
        cat_type = CategoricalDtype(ordered_levels, ordered = True)
        return series.astype(cat_type)
    else:
        with pl.StringCache():
            pl.Series(ordered_levels).cast(pl.Categorical)
            return series.cast(pl.Categorical).cat.set_ordering('physical')


def fct_levels(series:Union[pd.Series,pl.Series]):
    """
    Return categories of a series 
    provide polars series as df.get_column('name')
    """
    if isinstance(series, pd.Series):
        return list(series.astype('category').cat.categories)   
    else:
        return list(series.unique())