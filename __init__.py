#!/urs/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from decimal import Decimal, ROUND_HALF_UP

def rounding(value,digit,return_type=str,decimal_bool=True):
    """
    スカラーだけでなく、配列に関しても四捨五入するための関数
    value : 四捨五入したいスカラーまたは配列.  配列はnumpy.ndarrayのほか、listでも可.
    digit : decimal_bool=Trueの場合、小数点以下第digit+1位を四捨五入.
            decimal_bool=Falseの場合、digit桁目を四捨五入.
    return_type : 返り値の値もしくは配列の型 (ex. float, int)
    decimal_bool : 小数点以下に対する四捨五入か否か。Falseの場合は整数桁に関して四捨五入が行われる。
    """        

    if decimal_bool:
        vectorized_func = np.vectorize(one_decimal)
    else:
        vectorized_func = np.vectorize(one_integer)

    return_value = vectorized_func(value,digit,return_type)
    if return_value.ndim==0:
        return_value = np.array([return_value],dtype=return_type)[0]
    return return_value

def one_decimal(value,digit,return_type=str):
    """
    スカラーに関して小数点以下を四捨五入するための関数
    value : 四捨五入したいスカラー.
    digit : 小数点以下第digit+1位を四捨五入する.
    return_type : 返り値の型 (ex. float, int)
    """        
    if digit==0:
        decimal_value = '0'
    else:
        decimal_value = '1'
        for i in range(digit-1):
            decimal_value = '0'+decimal_value
        decimal_value = '0.'+decimal_value
    decimal_object = Decimal(str(value)).quantize(Decimal(decimal_value),rounding=ROUND_HALF_UP)
    return_value = np.array([decimal_object],dtype=return_type)[0]
    return return_value

def one_integer(value,digit,return_type=str):
    """
    スカラーに関して整数桁を四捨五入するための関数
    value : 四捨五入したいスカラー.
    digit : 四捨五入したい桁の数 (一の位->1, 十の位->2, ...)
    return_type : 返り値の型 (ex. str, float, int)
    """        
    decimal_value = f'1E{digit}'
    decimal_object = int(Decimal(str(value)).quantize(Decimal(decimal_value),rounding=ROUND_HALF_UP))
    return_value = np.array([decimal_object],dtype=return_type)[0]
    return return_value
