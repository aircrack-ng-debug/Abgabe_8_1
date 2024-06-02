class EllipticCurve:
    def __init__(self, a, b, p):
        self.a = a
        self.b = b
        self.p = p

    def mod_inv(self, x, p):
        return pow(x, p - 2, p)

    def add(self, P, Q):
        if P is None:
            return Q
        if Q is None:
            return P

        if P == Q:
            if P[1] == 0:
                return None
            l = (3 * P[0] ** 2 + self.a) * self.mod_inv(2 * P[1], self.p) % self.p
        else:
            if P[0] == Q[0]:
                return None
            l = (Q[1] - P[1]) * self.mod_inv(Q[0] - P[0], self.p) % self.p

        x = (l ** 2 - P[0] - Q[0]) % self.p
        y = (l * (P[0] - x) - P[1]) % self.p
        return (x, y)

    def multiply(self, P, k):
        R = None
        while k > 0:
            if k % 2 == 1:
                R = self.add(R, P)
            P = self.add(P, P)
            k //= 2
        return R


# Parameter der elliptischen Kurve
p = 1151
a = 1
b = 679
curve = EllipticCurve(a, b, p)
P = (501, 449)

# Private Schlüssel
kpr_A = 199
kpr_B = 211

# Berechnung der öffentlichen Schlüssel
kpub_A = curve.multiply(P, kpr_A)
kpub_B = curve.multiply(P, kpr_B)

print(f"Der öffentliche Schlüssel von Alice ist {kpub_A}")
print(f"Der öffentliche Schlüssel von Bob ist {kpub_B}")

# Berechnung des gemeinsamen Geheimnisses
shared_secret_A = curve.multiply(kpub_B, kpr_A)
shared_secret_B = curve.multiply(kpub_A, kpr_B)

print(f"Das gemeinsame Geheimnis (aus Alice's Sicht) ist {shared_secret_A}")
print(f"Das gemeinsame Geheimnis (aus Bob's Sicht) ist {shared_secret_B}")
