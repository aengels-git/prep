from typing import Union

import pandas as pd
import polars as pl

def prep_info(
        df:Union[pl.DataFrame, pd.DataFrame], 
        id:Union[str, list] = ["PERS_PERSON_RSK"], 
        return_data:bool = False):
    """
    A left join that raises an error if the id of the right dataset is not unique!
    """
    if isinstance(id, str):
        id = [id]
    if any([x not in df.columns for x in id]):
        raise KeyError(f"{id} not found in columns")

    #if isinstance(df, pd.DataFrame):
    #    df = pl.DataFrame(df)
    result = {"n":df.shape[0]}
    for i in id:
        result.update({f"n_unique_{i}":len(df[i].unique())})
    if len(id) > 1:  
        if isinstance(df, pd.DataFrame):
            result.update({"n_unique_ids":df.loc[:,id].drop_duplicates().shape[0]})
        else:
            result.update({"n_unique_ids":df.select(id).unique().shape[0]})

    if return_data:
        return pd.DataFrame(result, index = [0]).T.reset_index().rename(columns={0:"value","index":"stat"})
    else:
        for key, value in result.items():
            print(f"{key}: {value}")

