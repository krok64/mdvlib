import re
from math import ceil, pi

def float_or_none(s):
    """Если не нуль то преобразовать в число с плавающей точкой"""
    if s:
        return float(s)
    else:
        return s

def int_or_none(s):
    """Если не нуль то преобразовать в целое число"""
    if s:
        return int(s)
    else:
        return s

class NumPunkt():
    """ класс для нумерации через точку  1.2.3
    """
    def __init__(self, n1, n2=0, n3=0):
        self.n1 = n1
        self.n2 = n2
        self.n3 = n3
        
    def gets(self):
        val = str(self.n1)
        if self.n2 > 0:
            val += "." + str(self.n2)
        if self.n3 > 0:
            val += "." + str(self.n3)
        return val
        
    def add_n1(self, dn=1):
        self.n1 += dn
        self.n2 = 0
        self.n3 = 0
        return self.gets()
        
    def add_n2(self, dn=1):
        self.n2 += dn
        self.n3 = 0
        return self.gets()
        
    def add_n3(self, dn=1):
        self.n3 += dn
        return self.gets()

def split_str_space(s, num):
#разбивает строку на подстроки не длиннее num символов по пробелам
    if not s:
        return []
    lst=[]
    news=""
    for j in s.split():
        if news=="":
            news = j
        elif len(news+" "+j) > num:
            lst.append(news)
            news=j
        else:
            news = news+" " + j
    if news:
        lst.append(news)            
    return lst
         
def plural(num, word):
    """ 
    !!! НЕ ИСПОЛЬЗОВАТЬ. Есть модуль pymorphy2 
    num - количество
    word - слово для склонения (в зависимости от количества)
    склоняет существительное в соответствии с числительным:
    1 - комплект
    2-4 - комплекта
    5-10 - комплектов
    Исключение: 11-20 комплектов
    """
    ost = int(num % 100)
    if ost > 4 and ost < 21:
        return word + "ов"
    num = int(num % 10)
    if num == 1:
        return word
    if num > 1 and num < 5:
        return word + "а"
    return word + "ов"
    
    
def dict_inc(dic, key, v_add):
    """ Increase dic[key] or create it 
        не использовать!!!! т.к. есть
        from collections import defaultdict
        a = defaultdict(float)
    """
    if key in dic:
        dic[key] += v_add
    else:
        dic[key] = v_add


def frange(x, y, jump):
    """
    Реализация range() для чисел с плавающей точкой
    """
    while x < y:
        yield x
        x += jump    
            
            
def str_to_float(s):
    """ 
    Преобразовать строку в число с плавающей точкой. 
    Принимаем за разделитель целой и десятичной части как . так и ,
    """
    s=str(s)
    s=re.sub(",", ".", s)
    return float(s)

def str_to_arr_rus_float(s):
#преобразовать строку чисел разделенных пробелами в массив float
    s=re.sub(",", ".", s)
    return [float(x) for x in s.split()]
            
def rup(num, exp):
#округление числа вверх до exp разрядов 
    return ceil(num * 10**exp)/10**exp

def test():
    print("%f %f" % (rup(pi, -1), pi) )
    print("%f %f" % (rup(pi, 0), pi))
    print("%f %.1f" % (rup(pi, 1), pi))
    print("%f %.2f" % (rup(pi, 2), pi))
    print("%f %.3f" % (rup(pi, 3), pi))
    print("%f %.4f" % (rup(pi, 4), pi))

if __name__ == '__main__':
    test()        