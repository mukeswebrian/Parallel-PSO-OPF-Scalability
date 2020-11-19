import os

files = [f.strip() for f in open('file_list.txt', 'r').readlines()]

to_send = ' '.join(files)

#print(to_send)
#os.system('set files_to_copy='+to_send)
#os.system('echo %files_to_copy%')
os.system('scp {} s1895870@login.cirrus.ac.uk:/lustre/home/dc116/s1895870/dissertation'.format(to_send))
