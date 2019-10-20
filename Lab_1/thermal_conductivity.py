import numpy as np
import math

class ThermalConductivity():
    
    def __init__(self, L = 0.1, T0 = 20, T_left = 300, T_right = 100, t = 15, Ro = 7800, N = 45,
                       lamba = 46, c = 460):
        self.L = L
        self.N = N
        self.lamba = lamba
        self.Ro = Ro
        self.c = c
        self.T0 = T0
        self.T_left = T_left
        self.T_right = T_right
        self.t = t

    def create_T(self):
        T = list()
        for i in range(self.N):
            T.append(self.T0)
        return T

    def remember_last_T(self, T):
        TT = list()
        for i in T:
            TT.append(i)
        return TT

    def FDM(self):
        a = self.lamba / (self.Ro * self.c)
        h = self.L / (self.N - 1)
        tau = h ** 2 / (4 * a)
        T0 = self.T0
        T = self.create_T()
        T[0] = self.T_left
        T[self.N-1] = self.T_right
        time = 0
        while time <= self.t:
            time += tau 
            TT = T
            for i in range(1, self.N - 1):
                T[i] = TT[i] + a * tau / (h ** 2) * (TT[i+1] - 2 * TT[i] + TT[i-1])
        k = 0
        L_arr = list()
        while (k < self.L):
            L_arr.append(k)
            k+=h
        return T, L_arr

    def FEM(self):
        a = self.lamba / (self.Ro * self.c)
        len_i = self.L / (self.N - 1) #длина i-го эл.
        tau = len_i ** 2 / (4 * a) #шаг по времени
        C_i = (self.c * self.Ro * math.pi * len_i) / 6 * np.array([[2, 1], [1, 2]], dtype='double')
        K_i = (math.pi * self.lamba) / len_i * np.array([[1, -1], [-1, 1]], dtype='double')

'''    
L = 0.1
lamba = 46
Ro = 7800
c = 460
T0 = 20
T_left = 300
T_right = 100
t = 60

thermCond = ThermalConductivity(L, lamba, Ro, c, T0, T_left, T_right, t)
arr = thermCond.FDM()
print(arr)
'''
