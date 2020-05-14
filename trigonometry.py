#from decimal import *

def Fatorial(n):
	num = n
	fat = 1

	while (num > 0):
		fat = fat*num
		num = num - 1
	return fat

def ConverteRad(ang_grau):
	grau = ang_grau
	cont = 0
	pi = 0

	while (cont <= 10000000):
		pi = pi + (4*((-1) ** cont))/((2 * cont)+1)
		cont = cont + 1

	rad = (2*pi*grau)/360
	return rad

def Seno(ang):
	sen = 0
	grau = ang
	cont = 0
	ang_conv = ConverteRad(grau)

	while (cont <= 84):
		sen = sen + (((-1) ** cont)*(ang_conv ** ((2*cont)+1)))/(Fatorial((2*cont)+1))
		cont = cont + 1
	return sen

def Cosseno(ang):
	cos = 0
	grau = ang
	cont = 0
	ang_conv = ConverteRad(grau)

	while (cont <= 84):
		cos = cos + (((-1) ** cont)*(ang_conv ** (2*cont)))/(Fatorial(2*cont))
		cont = cont + 1
	return cos


x = int(input("Digite um número qualquer: "))
seno = Seno(x)
cosseno = Cosseno(x)

if (cosseno == 0):
	tangente = "Não existe tangente de " + str(x)
else:
	tangente = seno/cosseno

print("Seno de " + str(x) + "º: " + str(seno))
print("Cosseno de " + str(x) +"º: " + str(cosseno))
print("Tangente de " + str(x) + "º:" + str(tangente))
