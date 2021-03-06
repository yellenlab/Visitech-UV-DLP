''' Functions to write to a sequence file for the Visitech DLP
'''

from datetime import datetime as dt

def write_command(file, command, name='', val='', wait='1'):
    if command == 'Label':
        print(f'#------------------------------------------------------------',
          f'\n# {name}', file=file)
    print('{:<18} {:<18} {:<18} {:<18}'.format(command, 
                                               name,
                                               val,
                                               wait), file=file)

def header(file):
    print(f"#-----------------------------------------------------------------------\n"
          f"# This file was generated by create_sequence_file.py \n"
          f"# on {dt.now()} \n"
          f"#\n" +
          '# {:<16} {:<18} {:<18} {:<18} \n'.format('Command', 
                                        'Options', 'Value', 'Waitfor') +
          f"#-----------------------------------------------------------------------", 
          file=file)

def timed_image_seq(duration, filename, path):
    with open(path+filename+'.txt', "w") as f:
        header(f)
        write_command(f, 'AssignVar', name='num_pic', val=0)
        write_command(f, 'Label', 'ResetInum')
        write_command(f, 'AssignVar', name='inum', val=0)
        write_command(f, 'AssignVar', name='currpic', val=1)
        write_command(f, 'Label', 'Start')
        write_command(f, 'ResetGlobal', wait=16)
        write_command(f, 'LightSetWord', val=1, wait=3)
        write_command(f, 'LoadGlobal', val='inum', wait=duration)
        write_command(f, 'Add', name='currpic', val=1)
        write_command(f, 'LightSetWord', val=0, wait=3)
        write_command(f, 'Label', name='EndHere')
        write_command(f, 'JumpIf', name='currpic   >', val='num_pic  EndHere')
        write_command(f, 'Add', name='inum', val=1)
        write_command(f, 'Wait')
        write_command(f, 'Jump', name='Start')