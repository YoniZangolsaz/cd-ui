import os
import sys
import fileinput
import yaml
from yaml import loader

def configmap(namespace, workdir, imageName , home):
    os.chdir(workdir)
    os.system('pwd')
    os.chdir(workdir+'/'+imageName)
    file=os.listdir()
    os.system ('pwd')
    # if file.endswith('.env'):
    if '.env' in file:
        os.chdir(workdir+'/'+imageName)
        env = open(file,"r+").read() 
        data = open(home+"/home_dir/"+imageName+'/'+imageName+"-test-configmap.yaml","w+")
        tab = ""
        data.write(tab+ str(env))
    os.chdir(home+'/home_dir/'+imageName)
    o=os.listdir()
    if imageName in o:
        os.chdir(home+'/home_dir/'+imageName)
        d=os.listdir()
        if imageName+'-configmap.yaml' in d:
            for i, line in enumerate(fileinput.input(home+'/home_dir/'+imageName+'/'+imageName+'-test-configmap.yaml', inplace=1)):
                sys.stdout.write(line.replace('=', ': '))  

            configmap="""
            apiVersion: v1
            kind: ConfigMap
            metadata:
                name: {}ConfigMap
                namespace: {}
            data:
                master: refael """.format(imageName, namespace, )
            os.chdir(home+'/home_dir/'+imageName)
            with open(imageName+'-configmap.yaml', 'w+' ) as file:
                docs = yaml.load(configmap,  Loader=yaml.BaseLoader)
                yaml.dump(docs, file, sort_keys=False)
            with open(home+'/home_dir/'+imageName+'/'+imageName+'-test-configmap.yaml','r+')as file:
                with open(home+'/home_dir/'+imageName+'/'+imageName+'-configmap.yaml','a+')as fil:
                    a = yaml.load(file , Loader=loader.BaseLoader)
                    yaml.dump(a,fil, sort_keys=False)
            imagename=imageName.lower()
            os.system('kubectl delete configmap {} -n {}'.format(imagename, namespace))
            os.system('kubectl create configmap {} --from-file={}-configmap.yaml -n {}'.format(imagename, imageName, namespace))   
    os.system('rm -rf {}/{}'.format(workdir, imageName))    