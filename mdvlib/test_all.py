import pytest

from . tpcalc import get_k_n, s_truba

def test_get_k_n():
    assert get_k_n(0, 0) == 1.1
    assert get_k_n(1.02, 5.5*10**6) == 1.1
    assert get_k_n(1.03, 5.5*10**6) == 1.155
    assert get_k_n(1.02, 7.5*10**6) == 1.1
    assert get_k_n(1.22, 7.5*10**6) == 1.155
    assert get_k_n(1.23, 7.5*10**6) == 1.210
    assert get_k_n(0.53, 10*10**6) == 1.1
    assert get_k_n(1.02, 10*10**6) == 1.155
    assert get_k_n(1.22, 10*10**6) == 1.210
    assert get_k_n(1.23, 10*10**6) == 1.265
    
    with pytest.raises(Exception) as excinfo:   
        get_k_n(10000,11*10**6)
    assert "P is greater 10MPa" in str(excinfo.value)

    with pytest.raises(Exception) as excinfo:
        get_k_n(-1, 5.4*10**6)
    assert "D or P is negative" in str(excinfo.value)
        
    with pytest.raises(Exception) as excinfo:
        get_k_n(1.02, -5.4*10**6)
    assert "D or P is negative" in str(excinfo.value)
        
    with pytest.raises(Exception) as excinfo:
        get_k_n(-1, -5.4*10**6)
    assert "D or P is negative" in str(excinfo.value)

    with pytest.raises(Exception) as excinfo:
        get_k_n("", "")
    assert "D and P must be a number" in str(excinfo.value)
        
        
def test_s_truba():
    assert s_truba(0,0)==0
                    