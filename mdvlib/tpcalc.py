from math import pi, tan, radians, atan, sqrt, exp

TON_SILA=9806.65  #число Ньютонов в 1 т*с
        
def s_truba(d, l):
    """ Area of pipe. d - diametr,  l - dlina. d and l must be same measurment  """
    return l * pi * d 

def v_truba(d, l):
    """ Volume of pipe. d - diametr,  l - dlina. d and l must be same measurment  """
    return l * pi * d**2/4

def get_k_n(d, p):
    """
    Значение коэффициента надежности по ответственности трубопровода kн для газопроводов (СП 36.13330.2012 табл. 12)
    d - диаметр трубы, м
    р - давление газа в трубе, Па
    """
    
    if (not isinstance(d, (float, int))) or (not isinstance(p, (float, int))):
        raise Exception("D and P must be a number")
        
    if d < 0 or p < 0:
        raise Exception("D or P is negative")
        
    p_MPA = p / 10**6
    
    if p_MPA <= 5.5:
        if d<=1.020:
            return 1.1
        else:
            return 1.155
    elif p_MPA <= 7.5:
        if d<=1.020:
            return 1.1
        if d<=1.220:
            return 1.155
        else:
            return 1.210
    elif p_MPA <= 10.0:
        if d<=0.530:
            return 1.1
        if d<=1.020:
            return 1.155
        if d<=1.220:
            return 1.210
        else:
            return 1.265
    else: 
        raise Exception("P is greater 10MPa")
    
    
def R1_calc(R1_n, m, k1, k_n):
    """
    Расчетные сопротивления растяжению (сжатию) R1, Па по СП36.13330.2012 формула (2) п 12.1.2
    m - коэффициент условий работы трубопровода (В=0.66  I,II=0.825 III,IV=0.99)
    R1_n - Нормативные сопротивления растяжению (сжатию) металла труб и сварных соединений = значениям временного сопротивления по ТУ на трубу, Па
    k1 -  коэффициент надежности по материалу (по табл. 10 СП36.13330.2012)
    k_n - коэффициент надежности по ответственности трубопровода (по табл. 12 СП36.13330.2012) или get_k_n()
    """
    
    return R1_n * m / (k1 * k_n)

    
def R2_calc(R2_n, m, k2, k_n):
    """
    Расчетные сопротивления растяжению (сжатию) R2, Па по СП36.13330.2012 формула (3) п 12.1.2
    m - коэффициент условий работы трубопровода (В=0.66  I,II=0.825 III,IV=0.99)
    R2_n - Нормативные сопротивления растяжению (сжатию) металла труб и сварных соединений = значениям предела текучести по ТУ на трубу, Па
    k2 -  коэффициент надежности по материалу (по табл. 11 СП36.13330.2012)
    k_n - коэффициент надежности по ответственности трубопровода (по табл. 12 СП36.13330.2012) или get_k_n()
    """
    
    return R2_n * m / (k2 * k_n)


def calc_futlar(D_k, H, R2, y_gr, fi_gr, k_0, f_gr, h_pk, E_p, mu_p, P, x):
    """
    расчет стенки футляра трубопровода на прочность по "Типовые сооружения при ремонте газонефтепроводов" Л.И.Быков
    D_k=1.42  #диаметр футляра (кожуха), м
    H=3.5 #Глубина заложения футляра, м
    R2=R2_calc(R2_n,m,k2,k_n) Расчетные сопротивления растяжению материала кожуха
    y_gr=20400 #Удельный вес грунта, Н/м3 (изыскания)
    fi_gr=20   #Угол внутреннего трения грунта, град (изыскания)
    k_0=25000000 #Коэффициент постели грунта, Н/м3 (таб. 2.14 Справочник Быкова)
    f_gr=0.6 #Коэффициент крепости породы (справочник Быкова табл. 5.18, стр. 525)
    h_pk=0.45 #Толщина покрытия дороги, м (табл. 8.7, 8.9 СП 34.13330.2012 или табл.5.20, стр.528 Быков)
    E_p=27.5*10**6 #Модуль упругости материала полотна дороги, Па (табл. 5.19, стр. 527 справ. Быкова)
    mu_p=0.35 #Коэффициент Пуассона материала полотна дороги, (табл. 5.19, стр. 527 справ. Быкова) 
    P=100000 #Нагрузка на заднюю ось а/м, Н  (табл. 5.22, стр. 531 справочник Быкова) 1т*с=9806,65Н
    x=1.6 #Расстояние между задними осями, м (если осей всего две-передняя и задняя то 0 м)
    """
    ret = {}

    ret["n_gr"] = n_gr = 1.2   #Коэффициент надежности по нагрузке от веса грунта (Быков)
    ret["I_p"] = I_p = h_pk**3 / 12 #Момент инерции материала полотна дороги, м4
    ret["D_p"] = D_p = E_p * I_p / (1 - mu_p**2) #Цилиндрическая жесткость полотна дороги, Н*м2
    ret["a_j"] = a_j = (k_0 / (4 * D_p))**0.25 #Коэффициент жесткости полотна дороги, 1/м
    ret["B"] = B = D_k * (1 + tan(radians(45 - fi_gr / 2))) #Ширина свода обрушения, м
    ret["h_sv"] = h_sv = B / (2 * f_gr) #Высота свода обрушения, м
    ret["min_h"] = min_h = min(H, h_sv)
    ret["q_gr_v"] = q_gr_v = n_gr * y_gr * min_h #Расчетная вертикальная нагрузка от веса грунта, Па
    ret["q_gr_b"] = q_gr_b = n_gr * y_gr * (min_h + D_k / 2) * tan(radians(45 - fi_gr / 2))**2 #Расчетная боковая нагрузка  от веса грунта, Па
    ret["alpha"] = alpha = 3 * pi / (4 * a_j) #Параметр α', м (формула 5.311 справочник Быкова)
    ret["a2_x"] = a2_x = alpha * 2 + x #Зона распространения суммарной эпюры реакции основания, м
    ret["fi_max"] = fi_max = P * a_j / 2 #Реакция основания (нагрузка максимальна при х=0), Н
    ret["ha"] = ha = a2_x / 2
    ret["ksi_z"] = ksi_z = fi_max/pi*(atan(ha/H)*2)-2*ha*fi_max*H*(0-H**2-ha**2)/(pi*((H**2-ha**2)+4*ha**2*H**2)) #нагрузка от транспорта
    ret["q_p"] = q_p = 1.1 * ksi_z #Расчетное давление от подвижного транспорта, Па
    ret["r_k"] = r_k = 0.5 * D_k #радиус кожуха
    ret["N"] = N = -r_k * (q_gr_v + q_p) #Расчетное сжимающее усилие, Н/м
    ret["M"] = M = 0.25 * r_k**2 * (q_gr_v + q_p - q_gr_b) #Расчетный изгибающий момент
    ret["sigma"] = -N / (2 * R2) + sqrt(((N / (2 * R2))**2 + 6 * M / R2)) #Расчетная толщина стенки футляра, м
    
    return(ret)
    
def pipe_pushing(q_c, D_k, s, gamma_0, L, tan_fi, y_gr, f_gr):
    """ Расчет усилия для продавливания трубопровода под землей
    #удельное сопротивление сдавливанию ножа в грунт, кН, равное для глинистых грунтов (50-70) кН, 
    #для песчаных грунтов (70-100) кН, для прочных грунтов (200-600) кН на 1 м длины ножа
    q_c = 70
    #– коэффициент бокового давления грунта, равный для песка 0,35-0,41, для суглинка 0,5-0,7, для глины 0,7-0,74
    gamma_0 = 0.7
    #длина бестраншейной проходки, м
    L = 66
    #коэффициент трения кожуха о грунт, равный для глин 0,4-0,5, для песков 0,6-0,65
    tan_fi = 0.5
    #толщина стенки кожуха, мм
    s = 18.7
    y_gr=20400 #Удельный вес грунта, Н/м3 (изыскания)
    fi_gr=20   #Угол внутреннего трения грунта, град (изыскания)
    """
    ret = {}
    ret["p1"] = p1 = y_gr * D_k**2 / (3 * f_gr)
    ret["l"] = l = pi * D_k
    ret["q_k"] = q_k = (pi * D_k**2 - pi * (D_k - 2 * s)**2) / 4 * 7850 * 9.8
    ret["p"] = p = q_c * l + (2 * (1 + gamma_0) * p1 + q_k) * L * tan_fi
    return(ret)
    
def GetTExp(t_n, t_k, l_kc, x_kc):
    """ расчет температуры газа в заданной точке газопровода
    t_n - температура в начале газопровода
    t_k - температура в конце газопровода
    l_kc - длина газопровода
    x_kc - расстояние от начала до заданной точки
    """
    x = x_kc / l_kc
    return t_n - (t_n - t_k) * (1 + (x - 1) * exp (-x))
    
    