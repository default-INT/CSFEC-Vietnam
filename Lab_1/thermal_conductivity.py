import numpy as np
import math

class ThermalConductivity():
    
    def __init__(self, L = 0.1, T0 = 20, T_left = 300, T_right = 100, t = 15, Ro = 7800, N = 45,
                       lamba = 46, c = 460, q = 42, convection = 50, radius = 1):
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
        self.radius = radius

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
        k = 0 
        for i in T:
            L_arr.append(k)
            k+=h
        return T, L_arr

    def FEM_update(self):
        c = self.q 
        Ro = self.Ro
        r = self.radius               #радиус стержня
        lamba = self.lamba            #коэфициент теплопроводности
        conv = self.convection
        start_T = self.T0
        q = self.q
        T_inf = 0                     #температура окружающей среды
        cRo = c * Ro                  #удельная теплоёмкость * плотность
        dt = self.t / 30
        Len_shaft = self.L            #длина стержня
        n_el = self.N                 #количество разбиений стержня
        len_i = Len_shaft / n_el      #длина i го элемента == h
        A = 0.0001                    #площадь поперечного сечения

        #матрицы для каждого i-ых элементов стержня
        c_i = (cRo * A * len_i / 6) * np.array([[2, 1],
                                                [1, 2]], dtype='double')
        k_i = (A * lamba) / len_i * np.array([[1, -1],
                                              [-1, 1]], dtype='double')
                                              
        T = np.zeros(n_el + 1)
        for i in range(n_el + 1):
            T[i] = start_T
        
        F = np.zeros(n_el + 1)
        F[0] = -q
        F[1] = -q
        F[n_el-1] = -conv
        F[n_el] = -conv

        K = np.zeros((n_el+1, n_el+1), dtype=np.float32)
        C = np.zeros((n_el+1, n_el+1), dtype=np.float32)
        #формируем матрицы K и C из k_i и c_i
        for i in range(n_el):
            K[i, i] += k_i[0, 0]
            K[i, i+1] += k_i[0, 1]
            K[i+1, i] += k_i[1, 0]
            K[i+1, i+1] += k_i[1, 1]

            C[i, i] += c_i[0, 0]
            C[i, i+1] += c_i[0, 1]
            C[i+1, i] += c_i[1, 0]
            C[i+1, i+1] += c_i[1, 1]

        B = K + 2/dt * C
        P = 2/dt * C - K
        time = 0
        #inv_B = np.linalg.inv(B)
        while time < self.t:
            T = np.linalg.solve(B, P.dot(T) - F)
            time += dt

        L_arr = list()
        k = 0 
        for i in T:
            L_arr.append(k)
            k+=len_i
        
        return T, L_arr