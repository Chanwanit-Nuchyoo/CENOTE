import os
import subprocess
import sys
import threading
import pathlib
import webbrowser

global server_pid

# The .bat file contains "python manageserver.py" for restart command using wt Windows Terminal
batch_file = 'server.bat'

subproc = list()
command = ''
def dir_path():
    path = os.path.dirname(os.path.realpath(__file__))
    dir_= pathlib.PurePath(path)
    return dir_.name

HEADLINE= f'(console) {dir_path()}> '

def execute_arg():
    try:
        arg = sys.argv[1]
    except:
        arg = None
    
    if arg is not None:
        exec_command(arg)

def main_loop():
    while True:
        print(HEADLINE,end='')
        command = input()
        try:
            exec_command(command)
        except Exception as e:
            print(f'{str(e)}')

            
def welcome_message(hide=False):
    if not hide:
        text = """Django server management shell """
        print(text)
        print(pathlib.Path(__file__).parent.resolve())
    
def help_message():
    text = """ 
    run (alias r, runserver, server, start)     Starts a lightweight development web server on the local machine [python manage.py runserver].
    migrate          Synchronizes the database state with the current set of models and migrations [python manage.py migrate].
    makemigrations   Creates new migrations based on the changes detected to your models [python manage.py migrate].
    shell            Starts the Python interactive interpreter.
    createsupseruser Creates a superuser account [python manage.py createsuperuser].
    code             Open project in vs code.
    web              Open http://127.0.0.1:8000 in default web browser.
    restart          to restart this shell using Windows Terminal.

    begin the command with . to use the os command.
    """
    return text
    
# def aaaaaaaaaaaaaaaaaaaaa(a,**kwargs):
#     try:
#         shell = kwargs.get('shell')
#     except KeyError:
#         shell=True
       
#     print(shell) 
#     print(a)
#     proc = subprocess.Popen(a, shell)
#     subproc.append(proc)
#     return proc

global urls
urls = [
    '',
    '/admin',
]

def read_urls_from_file():
    global urls
    from_file = []
    try:
        with open('urls.txt','r') as file:
            data = file.readlines()
            for url in data:
                from_file.append(url.strip())
    except FileNotFoundError:
        pass

    urls += from_file

    return from_file

def write_urls_to_file(url_):
    global urls
    with open('urls.txt','w') as file:
        rv = file.write(str(url))
    return rv
    
def exec_command(command=''):
    command = command.lower()
    if command in ['run','runserver','server','start','r']:
        proc = subprocess.Popen('start /wait python manage.py runserver',shell=True)
        print('process id :',proc.pid)
        return
        
    if command in ['migrate','mg','mig']:
        proc = subprocess.Popen('python manage.py migrate',shell=True)
        print('process id :',proc.pid)
        return

    if command in ['makemigrations','mkmigrations','mkmig','mkmg','mm']:
        proc = subprocess.Popen('python manage.py makemigrations',shell=True)
        print('process id :',proc.pid)
        return

    if command in ['shell','sh']:
        exec_command('.start cmd /k python manage.py shell')
        # proc = subprocess.Popen('start /wait python manage.py shell',shell=True)
        print('process id :',proc.pid)
        return

    if command in ['createsuperuser','superuser','super','createsup','createsuper']:
        exec_command('.start cmd /k python manage.py createsuperuser')
        # proc = subprocess.Popen('start /wait python manage.py createsuperuser',shell=True)
        print('process id :',proc.pid)
        return

    if command in ['stop',]:
        for proc in subproc:
            print(f'killing {proc.pid}')
            proc.kill()
        return

    if command in ['vs code','code','code .','opencode']:
        exec_command('.code .')
        return

    if command.split()[0] in ['web','webbrowser','openweb',]:
        try:
            url = command.split()[1]        
        except IndexError:
            url = "http://127.0.0.1:8000/"
        webbrowser.open(url, new=0, autoraise=True)
        return

    if command[0] in ['/']:
        url = "http://127.0.0.1:8000/"
        url += command[1:]
        webbrowser.open(url, new=0, autoraise=True)
        return

    if command in ['start .']:
        exec_command('.start .')
        return

    if command in ['native','pipenv shell','pipshell']:
        exec_command('.start cmd /k pipenv shell')
        return

    if command in ['dir','ls',]:
        os.system('dir')
        return

    if command in ['windows terminal','wt']:
        exec_command('.start wt ')
        return

    if command in ['cls','clear']:
        # not call on new thread
        os.system('cls')
        return

    if command in ['restart','reset']:
        # Use Windows Terminal to restart
        # proc = subprocess.Popen('py manageserver.py')
        exec_command('.start wt '+batch_file)

        # subprocess.run('start cmd /k '+batch_file)
        # subprocess.run(['start','wt','/k',batch_file])

        exit()

    if command == 'exit':
        print("exit... ")
        exit()

    if command == 'proc':
        print('processes running : [\n')
        for proc in subproc:
            if proc.returncode == 0:
                subproc.remove(proc)
        for proc in subproc:
            print(proc)
        print('\n]')
        return

    if command in ['help']:
        message = help_message()
        print(message)

    if command.startswith('.'):
        def func():
            os.system(command[1:])
        th = threading.Thread(target=func,)
        th.start()
        return

    if command == '':
        return
    # command is not recognized
    raise Exception(f'"{command}" is not a recognized as a command, use "help" to see available commands.')


if __name__ == "__main__":
    welcome_message()
    # read_urls_from_file()
    execute_arg()
    main_loop()
    