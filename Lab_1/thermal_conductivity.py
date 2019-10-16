import numpy
import math

class ThermalConductivity():
    
    def __init__(self, L, lamba, Ro, c, T0, T_left, T_right, t):
        self.L = L
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
        self.N = 45
        self.t = 15
        a = self.lamba / (self.Ro * self.c)
        h = self.L / (self.N - 1)
        tau = h ** 2 / (4 * a)
        T0 = self.T0
        T = self.create_T()
        T[0] = T_left
        T[self.N-1] =T_right
        time = 0
        while time <= self.t:
            #print(tau)
            time += tau 

            TT = self.remember_last_T(T)
            for i in range(1, self.N - 1):
                T[i] = TT[i] + a * tau / math.sqrt(h) * (TT[i+1] - 2 * TT[i] + TT[i-1])
                    
        return T
    
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
