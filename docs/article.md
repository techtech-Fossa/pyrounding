# Pythonで使える四捨五入関数を作ってみた

# はじめに
Pythonでデータを扱う場合、整数や小数に対して小学校でならうようないわゆる四捨五入をいい感じでしてくれる関数がなかったので自作してみました。  
整数と小数それぞれの四捨五入方法に関しては、[こちら](https://note.nkmk.me/python-round-decimal-quantize/)のページを参考にさせて頂きました。  
完成形のコードだけ見たいよという方は私の[Github](https://github.com/techtech-Fossa/pyrounding)からどうぞ。  

# 環境  
OS : AlmaLinux release 8.7  
Python 3.8.0  
numpy 1.23.4  
  
とりあえず必要なライブラリ・モジュールをimportしておきます。


```python
import numpy as np
from decimal import Decimal, ROUND_HALF_UP
```

## 方向性
decimalモジュールのDecimal()オブジェクトに対して、quantizeメソッドで引数rounding=ROUND_HALF_UPを指定することで一般的な四捨五入を行っていきます。  


# 小数  
まずは簡単に挙動を確認していきます。


```python
f = 123.456
print(f)
print("'0'")
print(Decimal(str(f)).quantize(Decimal('0'), rounding=ROUND_HALF_UP))
print("'0.1'")
print(Decimal(str(f)).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP))
print("'0.01'")
print(Decimal(str(f)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))
```

    123.456
    '0'
    123
    '0.1'
    123.5
    '0.01'
    123.46


小数点第n位(n>1)を四捨五入したい場合は、quantizeメソッドの第一引数にDecimal($10^{n-1}$のstr型)を指定すればよいことがわかりました。  
小数点第一位を四捨五入したい場合はDecimal('0')のようですね。  
以上を踏まえて作成した小数に対する四捨五入用の関数がこちらです。  


```python
def one_decimal(value,digit,return_type=str):
    """
    value : 四捨五入したいスカラー.
    digit : 四捨五入して最終的に小数点第何位までにしたいか
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
```

## 説明
### 引数
第二引数digitで、第一引数valueを四捨五入して最終的に小数点第何位までにしたいかを指定します。つまり、小数点以下第digit+1位を四捨五入します。    
第三引数return_valueでは、返り値の型を指定します。  
### 中身  



まずdigitが0か1以上かで、quantizeメソッドで指定する文字列を分けて作ります。  
digitが1上の場合は、digit-1個の'0'を'1'の左側に書いたのち、'0.'をつけます。  
例えばdigit=3であれば、'1'の左側に'00'を付けたのちに左側に'0.'を付けます.  
これで小数点以下第4(digit+1)位を四捨五入して小数点第3(digit)位までにできます。  

```python
if digit==0:
    decimal_value = '0'
else:
    decimal_value = '1'
    for i in range(digit-1):
        decimal_value = '0'+decimal_value
    decimal_value = '0.'+decimal_value
```

先ほど挙動確認した方法で、第一引数valueの小数点第digit+1位を四捨五入します。

```python
decimal_object = Decimal(str(value)).quantize(Decimal(decimal_value),rounding=ROUND_HALF_UP)
```

返り値の型を、numpy.ndarrayを経由して変換しています。

```python
return_value = np.array([decimal_object],dtype=return_type)[0]
```

## 関数の挙動確認


```python
f = 123.456
args = [[f,0,str],
        [f,0,float],
        [f,1,str],
        [f,1,float],
        [f,2,str],
        [f,2,float]]

for arg in args:
    value,digit,return_type = arg
    return_value = one_decimal(value,digit,return_type)
    print(f'{value}, {digit}, {return_type} : {return_value} {type(return_value)}')
```

    123.456, 0, <class 'str'> : 123 <class 'numpy.str_'>
    123.456, 0, <class 'float'> : 123.0 <class 'numpy.float64'>
    123.456, 1, <class 'str'> : 123.5 <class 'numpy.str_'>
    123.456, 1, <class 'float'> : 123.5 <class 'numpy.float64'>
    123.456, 2, <class 'str'> : 123.46 <class 'numpy.str_'>
    123.456, 2, <class 'float'> : 123.46 <class 'numpy.float64'>


# 整数 
こちらもまずは簡単に挙動を確認していきます。


```python
i = 99518
print(i)
print("型変換なし '10'")
print(Decimal(i).quantize(Decimal('10'), rounding=ROUND_HALF_UP))
print("型変換なし '1E1'")
print(Decimal(i).quantize(Decimal('1E1'), rounding=ROUND_HALF_UP))
print("int '1E1'")
print(int(Decimal(i).quantize(Decimal('1E1'), rounding=ROUND_HALF_UP)))
print("int '1E2'")
print(int(Decimal(i).quantize(Decimal('1E2'), rounding=ROUND_HALF_UP)))
print("int '1E3'")
print(int(Decimal(i).quantize(Decimal('1E3'), rounding=ROUND_HALF_UP)))
```

    99518
    型変換なし '10'
    99518
    型変換なし '1E1'
    9.952E+4
    int '1E1'
    99520
    int '1E2'
    99500
    int '1E3'
    100000


まずquantizeメソッドの第一引数のDecimalの中身は、Eによる指数表記にしなければ得たい結果が得られないことが分かります。  
また、型変換なしの場合、Eによる指数表記のオブジェクトが返ってきてしまうので、int型に変換する必要があります。  


```python
def one_integer(value,digit,return_type=str):
    """
    value : 四捨五入したいスカラー.
    digit : 四捨五入する位の数 (1の位->1, 10の位->2, ...)
    return_type : 返り値の型 (ex. str, float, int)
    """        
    decimal_value = f'1E{digit}'
    decimal_object = int(Decimal(str(value)).quantize(Decimal(decimal_value),rounding=ROUND_HALF_UP))
    return_value = np.array([int(decimal_object)],dtype=return_type)[0]
    return return_value

```

## 説明
### 引数
第二引数digitで、第一引数valueの何桁目を四捨五入したいかを指定します。一の位であれば1、十の位であれば2となります。      
第三引数return_valueでは、返り値の型を指定します。  
### 中身  


小数の時よりシンプルであり、'1E'の後ろにdigitをつけた文字列をつくります。

```python
if decimal_value = f'1E{digit}'
```

先ほど挙動確認した方法で、第一引数valueのdigit桁目を四捨五入します。

```python
decimal_object = int(Decimal(str(value)).quantize(Decimal(decimal_value),rounding=ROUND_HALF_UP))
```

返り値の型を、numpy.ndarrayを経由して変換しています。

```python
return_value = np.array([decimal_object],dtype=return_type)[0]
```

## 関数の挙動確認


```python
i = 99518
args = [[i,1,str],
        [i,1,float],
        [i,1,int],
        [i,2,str],
        [i,2,float],
        [i,2,int]
        ]

for arg in args:
    value,digit,return_type = arg
    return_value = one_integer(value,digit,return_type)
    print(f'{value}, {digit}, {return_type} : {return_value} {type(return_value)}')
```

    99518, 1, <class 'str'> : 99520 <class 'numpy.str_'>
    99518, 1, <class 'float'> : 99520.0 <class 'numpy.float64'>
    99518, 1, <class 'int'> : 99520 <class 'numpy.int64'>
    99518, 2, <class 'str'> : 99500 <class 'numpy.str_'>
    99518, 2, <class 'float'> : 99500.0 <class 'numpy.float64'>
    99518, 2, <class 'int'> : 99500 <class 'numpy.int64'>


# 配列にも適用
ひとつひとつの値を四捨五入するだけならdecimalモジュールで十分なので、配列にも適用できるようにします。  
今回は、numpyのvectorizeメソッドを使用してone_decimalとone_integerをユニバーサル関数化します。    
関数の完成形は次の通りです。


```python
def rounding(value,digit,return_type=str,decimal_bool=True):
    """
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
```

## 説明
### 引数
第四引数のdecimal_boolは、one_decimalを使うかone_integerを使うかを指定するbooleanです。デフォルトではTrueとなっています。  
value,digit,return_valueの意味はすべてone_decimalとone_integerのものと同一ですが、digitについてはdecimal_boolによって意味するところが変わります。  
### 中身  


decimal_boolによって、one_decimalとone_integerのどちらをnp.vectorizeでユニバーサル関数化するかを決めます。

```python
if decimal_bool:
    vectorized_func = np.vectorize(one_decimal)
else:
    vectorized_func = np.vectorize(one_integer)
```

返り値を取得する際、引数valueがスカラーの場合には0-dimensional arrayが返ってきてしまうので、1-dimensional arrayにしてから取り出す。

```python
return_value = vectorized_func(value,digit,return_type)
if return_value.ndim==0:
    return_value = np.array([return_value],dtype=return_type)[0]
```

## 関数の挙動確認
### 配列


```python
a = np.linspace(0,1,8).reshape(2,4)
print(a)
```

    [[0.         0.14285714 0.28571429 0.42857143]
     [0.57142857 0.71428571 0.85714286 1.        ]]



```python
decimal_bool = True
args = [[a,0,str],
        [a,0,float],
        [a,1,str],
        [a,1,float]]

for arg in args:
    value,digit,return_type = arg
    return_value = rounding(value,digit,return_type,decimal_bool)
    print(f'{digit}, {return_type} :')
    print(return_value)
    print(return_value.dtype)

```

    0, <class 'str'> :
    [['0' '0' '0' '0']
     ['1' '1' '1' '1']]
    <U1
    0, <class 'float'> :
    [[0. 0. 0. 0.]
     [1. 1. 1. 1.]]
    float64
    1, <class 'str'> :
    [['0.0' '0.1' '0.3' '0.4']
     ['0.6' '0.7' '0.9' '1.0']]
    <U3
    1, <class 'float'> :
    [[0.  0.1 0.3 0.4]
     [0.6 0.7 0.9 1. ]]
    float64



```python
b = np.arange(145,155,1).reshape(2,5)
print(b)
```

    [[145 146 147 148 149]
     [150 151 152 153 154]]



```python
decimal_bool = False
args = [[b,1,str],
        [b,1,float],
        [b,1,int],
        [b,2,str],
        [b,2,float],
        [b,2,int]
        ]

for arg in args:
    value,digit,return_type = arg
    return_value = rounding(value,digit,return_type,decimal_bool)
    print(f'{digit}, {return_type} :')
    print(return_value)
    print(return_value.dtype)
```

    1, <class 'str'> :
    [['150' '150' '150' '150' '150']
     ['150' '150' '150' '150' '150']]
    <U3
    1, <class 'float'> :
    [[150. 150. 150. 150. 150.]
     [150. 150. 150. 150. 150.]]
    float64
    1, <class 'int'> :
    [[150 150 150 150 150]
     [150 150 150 150 150]]
    int64
    2, <class 'str'> :
    [['100' '100' '100' '100' '100']
     ['200' '200' '200' '200' '200']]
    <U3
    2, <class 'float'> :
    [[100. 100. 100. 100. 100.]
     [200. 200. 200. 200. 200.]]
    float64
    2, <class 'int'> :
    [[100 100 100 100 100]
     [200 200 200 200 200]]
    int64


### スカラー


```python
f = 123.456
decimal_bool = True
args = [[f,0,str],
        [f,0,float],
        [f,1,str],
        [f,1,float],
        [f,2,str],
        [f,2,float]]

for arg in args:
    value,digit,return_type = arg
    return_value = rounding(value,digit,return_type,decimal_bool)
    print(f'{value}, {digit}, {return_type} : {return_value} {type(return_value)}')
    
i = 99518
decimal_bool = False
args = [[i,1,str],
        [i,1,float],
        [i,1,int],
        [i,2,str],
        [i,2,float],
        [i,2,int]
        ]

for arg in args:
    value,digit,return_type = arg
    return_value = rounding(value,digit,return_type,decimal_bool)
    print(f'{value}, {digit}, {return_type} : {return_value} {type(return_value)}')
```

    123.456, 0, <class 'str'> : 123 <class 'numpy.str_'>
    123.456, 0, <class 'float'> : 123.0 <class 'numpy.float64'>
    123.456, 1, <class 'str'> : 123.5 <class 'numpy.str_'>
    123.456, 1, <class 'float'> : 123.5 <class 'numpy.float64'>
    123.456, 2, <class 'str'> : 123.46 <class 'numpy.str_'>
    123.456, 2, <class 'float'> : 123.46 <class 'numpy.float64'>
    99518, 1, <class 'str'> : 99520 <class 'numpy.str_'>
    99518, 1, <class 'float'> : 99520.0 <class 'numpy.float64'>
    99518, 1, <class 'int'> : 99520 <class 'numpy.int64'>
    99518, 2, <class 'str'> : 99500 <class 'numpy.str_'>
    99518, 2, <class 'float'> : 99500.0 <class 'numpy.float64'>
    99518, 2, <class 'int'> : 99500 <class 'numpy.int64'>


# まとめ
これでをsite-packagesに入れておけばいつでも四捨五入が出来そうです。  
今回が初投稿だったためだいぶ冗長な説明になっていました...  
ここまでお付き合いいただきありがとうございました。  

# 参考
- [Pythonで小数・整数を四捨五入するroundとDecimal.quantize](https://note.nkmk.me/python-round-decimal-quantize/)
- [【NumPy入門】np.vectorizeでPython関数を簡単にユニバーサル関数化!](https://www.sejuku.net/blog/73778)

