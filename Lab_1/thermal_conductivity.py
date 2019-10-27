import numpy as np
import math

class ThermalConductivity():
    
    def __init__(self, L = 0.1, T0 = 20, T_left = 300, T_right = 100, t = 15, Ro = 7800, N = 45,
                       lamba = 46, c = 460, q = 42, convection = 50):
        self.L = L
        self.N = N
        self.lamba = lamba
        self.Ro = Ro
        self.c = c
        self.T0 = T0
        self.T_left = T_left
        self.T_right = T_right
        self.t = t
        self.q = q
        self.convection = convection

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
        A = math.pi
        a = self.lamba / (self.Ro * self.c)
        len_i = self.L / (self.N - 1) #длина i-го эл.
        tau = len_i ** 2 / (4 * a) #шаг по времени
        h = 10

        k = 0
        L_arr = list()
        while (k < self.L):
            L_arr.append(k)
            k+=len_i

        T = self.create_T()
        C_i = (self.c * self.Ro * A * len_i) / 6 * np.array([[2, 1], [1, 2]], dtype='double')
        K_i = (A * self.lamba) / len_i * np.array([[1, -1], [-1, 1]], dtype='double')
        
        f = list()
        i = 0
        while i < self.L: #L not int !!!!!!! 
            f.append(-
            (self.T0 * A * self.L - self.q * A + h * self.convection * A)/2 * \
                2 * np.array([[1], [1]], dtype='double'))
            i += len_i
        K = np.zeros(self.N+1, self.N+1)
        C = np.zeros(self.N+1, self.N+1)
        for i in range(self.N):
            K[i, i] += K_i[0, 0]
            K[i, i+1] += K_i[0, 1]
            K[i+1, i] += K_i[1, 0]

            C[i, i] += C_i[0, 0]
            C[i, i+1] += C_i[0, 1]
            C[i+1, i] += C_i[1, 0]

            if (i+1) == self.N:
                K[i+1, i+1] += K_i[1, 1]
                C[i+1, i+1] += C_i[1, 1]
            else:
                K[i+1, i+1] += (K_i[1, 1] + K_i[0, 0])
                C[i+1, i+1] += (C_i[1, 1] + C_i[0, 0])
        B = K + (2 / tau) * C
        P = (2 / tau) * C - K

        F = np.zeros(self.N+1)
        F[0] = -self.q
        F[1] = -self.q
        F[self.N - 1] = - self.convection
        F[self.N] = - self.convection
        time = 0

        while time < self.t:
            T = np.linalg.solve(B, P*T - 2 * F)
            time += tau
        return T, L_arr
        '''
        K = np.zeros(self.N, self.N)
        C = np.zeros(self.N, self.N)
        for i in range(self.N):
            C[i, i] += C_i[0, 0]
            C[i, i+1] += C_i[0, 1]
            C[i+1, i] += C_i[1, 0]
            C[i+1, i+1] += C_i[1, 1]

            K[i, i] += K_i[0, 0]
            K[i, i+1] += K_i[0, 1]
            K[i+1, i] += K_i[1, 0]
            K[i+1, i+1] += K_i[1, 1]

        B = np.zeros(self.N, self.N + 1)
        P = np.zeros(self.N, self.N)

        for i in range(self.N):
            for j in range(self.N):
                B[i, j] += K[i, j] + (2 / tau) * C[i, j]
                P[i, j] += (2 / tau) * C[i, j] - K[i, j]
        f = np.zeros(self.N)
        f[0] = -self.q
        f[1] = -self.q
        f[self.N - 2] = - self.convection
        f[self.N - 1] = - self.convection

        countTime = int(self.t / tau)
        prevTemp = np.zeros(self.N)
        prevTemp += self.T0
        temp = np.zeros(countTime, self.N)
        temp[0, :] = prevTemp
        for i in range(1, countTime):
            d1 = P * prevTemp
            d2 = f * 2
            d3 = d1 - d2

            matrix = B
            matrix[:, self.N] = d3
        '''

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
