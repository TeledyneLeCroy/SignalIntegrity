import os
import shutil
import zipfile

root=os.path.dirname(os.path.realpath(__file__))
fileList=[os.path.join(path, name) for path, subdirs, files in os.walk(root) for name in files]
filteredFileList=[]
for fullFileName in fileList:
    filenameWithExtension=os.path.basename(fullFileName)
    filename,fileextension = os.path.splitext(filenameWithExtension)
    relpath=os.path.relpath(fullFileName, root)
    if relpath == filenameWithExtension: # this is a file in the root directory
        if fileextension != '.py': # not a python file
            if filenameWithExtension not in ['LICENSE.txt','README.md']:
                continue
    if filename[0]=='.': # hidden directory
        continue
    if relpath.startswith('.git'):
        continue
    if fileextension == '.pyc':
        continue
    if '_pycache_' in fullFileName:
        continue
    if fileextension == '.p':
        continue
    if relpath.startswith('SignalIntegrity.egg-info/'):
        continue
    if filenameWithExtension in ['LinkDoc.sh',
                                 'LinkHelp.sh',
                                 'UnlinkDoc.sh',
                                 'UnlinkHelp.sh']:
        continue
    if relpath.startswith('Doc/'):
        if filenameWithExtension != 'README.md':
            continue
    if relpath.startswith('Test/'):
        continue
    if relpath.startswith('SignalIntegrity/App/Help'):
        continue
    if relpath.startswith('SignalIntegrity/App/Examples/PowerIntegrity'):
        continue
    filteredFileList.append(fullFileName)
from SignalIntegrity.__about__ import __version__
destFileList=[os.path.abspath(os.path.join('../SignalIntegrity-'+__version__+'/',
                                           os.path.relpath(fullFileName,root)))
                                           for fullFileName in filteredFileList]
try:
    shutil.rmtree(os.path.abspath('../SignalIntegrity-'+__version__))
except (NotADirectoryError,FileNotFoundError):
    pass
try:
    os.remove(os.path.abspath('../SignalIntegrity-'+__version__+'.zip'))
except FileNotFoundError:
    pass
for input,output in zip(filteredFileList,destFileList):
    if not os.path.isdir(os.path.dirname(output)):
        os.makedirs(os.path.dirname(output),exist_ok=True)
    shutil.copyfile(input,output)
zipf = zipfile.ZipFile(os.path.abspath(os.path.join(root,'../SignalIntegrity-'+__version__+'.zip')), 'w', zipfile.ZIP_DEFLATED)
for input,output in zip(filteredFileList,destFileList):
    zipf.write(output,os.path.join('SignalIntegrity-'+__version__,os.path.relpath(input, root)))
os.chdir(os.path.abspath(os.path.join(root,'../SignalIntegrity-'+__version__)))
result = os.system('python3 setup.py bdist_wheel --universal')
# os.system('twine upload dist/*')
# os.system('twine upload --repository-url https://test.pypi.org/legacy/ dist/*')
pass



