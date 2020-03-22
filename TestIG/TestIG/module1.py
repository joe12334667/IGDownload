import re

file = open("2020-03-10_04-40-43_UTC.txt" ,  encoding = 'utf8')

#print(  file.readlines())

for line in file.readlines():
    print(line)
    print(re.findall( "\B#\w\w+" ,line))
    
file.close()







