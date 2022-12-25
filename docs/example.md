```python
import pyrounding
```


```python
f = 123.456
pyrounding.rounding(value=f,digit=1,return_type=str,decimal_bool=True)
```




    '123.5'




```python
i = 99518
pyrounding.rounding(value=i,digit=2,return_type=float,decimal_bool=False)
```




    99500.0




```python
import numpy as np
a = np.linspace(0,1,8).reshape(2,4)
a
```




    array([[0.        , 0.14285714, 0.28571429, 0.42857143],
           [0.57142857, 0.71428571, 0.85714286, 1.        ]])




```python
pyrounding.rounding(value=a,digit=1,return_type=str,decimal_bool=True)
```




    array([['0.0', '0.1', '0.3', '0.4'],
           ['0.6', '0.7', '0.9', '1.0']], dtype='<U3')




```python
pyrounding.rounding(value=a,digit=2,return_type=float,decimal_bool=True)
```




    array([[0.  , 0.14, 0.29, 0.43],
           [0.57, 0.71, 0.86, 1.  ]])




```python
b = np.arange(145,155,1).reshape(2,5)
b
```




    array([[145, 146, 147, 148, 149],
           [150, 151, 152, 153, 154]])




```python
pyrounding.rounding(value=b,digit=1,return_type=str,decimal_bool=False)
```




    array([['150', '150', '150', '150', '150'],
           ['150', '150', '150', '150', '150']], dtype='<U3')




```python
pyrounding.rounding(value=b,digit=2,return_type=int,decimal_bool=False)
```




    array([[100, 100, 100, 100, 100],
           [200, 200, 200, 200, 200]])


