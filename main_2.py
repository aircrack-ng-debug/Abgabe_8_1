class EllipticCurve:
    def __init__(self, a, b, p):
        self.a = a
        self.b = b
        self.p = p

    def mod_inv(self, x, p):
        return pow(x, p -2, p)

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
        print(f"Add: λ = {l}, x = {x}, y = {y}")
        return (x, y)

    def multiply(self, P, k):
        R = None
        add_steps = []
        while k > 0:
            if k % 2 == 1:
                R = self.add(R, P)
                add_steps.append(R)
            P = self.add(P, P)
            add_steps.append(P)
            k //= 2
        print(f"Multiply steps: {add_steps}")
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
print("Berechnung des öffentlichen Schlüssels von Alice:")
kpub_A = curve.multiply(P, kpr_A)
print(f"Öffentlicher Schlüssel von Alice: {kpub_A}\n")

print("Berechnung des öffentlichen Schlüssels von Bob:")
kpub_B = curve.multiply(P, kpr_B)
print(f"Öffentlicher Schlüssel von Bob: {kpub_B}\n")

# Berechnung des gemeinsamen Geheimnisses
print("Berechnung des gemeinsamen Geheimnisses aus Alice's Sicht:")
shared_secret_A = curve.multiply(kpub_B, kpr_A)
print(f"Gemeinsames Geheimnis (Alice): {shared_secret_A}\n")

print("Berechnung des gemeinsamen Geheimnisses aus Bob's Sicht:")
shared_secret_B = curve.multiply(kpub_A, kpr_B)
print(f"Gemeinsames Geheimnis (Bob): {shared_secret_B}\n")
