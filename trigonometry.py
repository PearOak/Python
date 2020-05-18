def Factorial(a):
	fat = 1
	num = a

	while (num > 0):
		fat = fat * num
		num = num - 1

	return fat

def CalculatePi():
	pi = 0
	exp = 0
	while (exp < 10000001):
		pi = pi + (4*((-1)**exp)/((2*exp)+1))
		exp = exp + 1

	return pi

def LapNumbers(b):
	ang = b
	laps = int(ang/360)

	return laps

def EquivalentAngle(c):
	ang = c
	equi_ang = ang % 360

	return equi_ang

def ConvertToRad(d):
	ang = d
	eq_ang = EquivalentAngle(ang)
	pi = CalculatePi()
	ang_rad = (eq_ang*pi)/180

	return ang_rad

def Sine(e):
	ang = e
	ang_rad = ConvertToRad(ang)
	pi = CalculatePi()
	exp = 0
	sin = 0

	if (ang == 90 or ang == -270):
		sin = 1
		return sin
	if (ang == 270 or ang == -90):
		sin = -1
		return sin
	if (ang == 180 or ang == -180):
		sin = 0
		return sin
	else:
		while (exp <= 84):
			sin = sin + (((-1)**exp)*(ang_rad ** ((2*exp)+1)))/(Factorial((2*exp) + 1))
			exp = exp + 1
		return sin


def Cossine(f):
	ang = f
	ang_rad = ConvertToRad(ang)
	pi = CalculatePi()
	exp = 0
	cos = 0

	if (ang == 90 or ang == -270):
		cos = 0
		return cos
	if (ang == 180 or ang == -180):
		cos = -1
		return cos
	if (ang == 270 or ang == -90):
		cos = 0
		return cos
	else:
		while (exp <= 84):
			cos = cos + (((-1)**exp)*(ang_rad ** ((2*exp))))/(Factorial((2*exp)))
			exp = exp + 1
		return cos


def Tangent(g):
	ang = g
	sin = Sine(g)
	cos = Cossine(g)

	if (cos == 0):
		tan = "It doesn't exist!"
		return tan
	if (ang == 45 or ang == -315):
		tan = 1
		return tan
	if (ang == 135 or ang == -225):
		tan = -1
		return tan
	else:
		tan = sin/cos
		return tan


def TFR(h):
	ang = h
	sin = Sine(h)
	cos = Cossine(h)
	tfr = (sin**2)+(cos**2)
	return tfr

x = int(input("Please, input an angle (degrees): "))
rad = ConvertToRad(x)
laps = LapNumbers(x)
eq_angle = EquivalentAngle(x)
sin = Sine(x)
cos = Cossine(x)
tan = Tangent(x)
tfr = TFR(x)

print(str(x) + "º is equal to the angle " + str(eq_angle) + "º")
print(str(x) + " as radians: " + str(rad))
print("Number of laps: " + str(laps))
print("Sine of " + str(x) + ": " + str(sin))
print("Cossine of " + str(x) + ": " + str(cos))
print("Tangent of " + str(x) + ": " + str(tan))
print("Trigonometry Fundamental Relation = " + str(tfr))
print("Done! All counts are finished! ;)")
