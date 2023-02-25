'''
f = open('alumnos.txt', 'r')
nombres = f.read()
print(nombres)

nombres2 = f.readlines()
print(nombres2)
f.close()

for items in nombres2:
    print(items,end='')
    #print('{}',end=''.format(items))
f = open('alumnos2.txt','w')
f.write('Hola Mundo!')
f.close()
'''
f = open('alumnos.txt','a')
alumno = {'Matricula':12345, 'Nombre':'Mario', 'Apellidos':'Lopez','Correo':'mlopez@' }
for x in alumno:
    f.write('\n'+str(alumno[x]))

#f.write('\n'+'Mario')
#f.write('\n'+'Pedro')
f.close()