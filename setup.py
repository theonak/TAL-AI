from distutils.core import setup



package_dir = {'':'talai',
               'champs':'talai',
               'data':'talai',
               'models':'talai',
               'utils':'talai',}

setup(name='talai',
      version='0.1',
      description='Team Analysis for League of Legends - AI',
      author='AlexAuragan, Theonakk',
      author_email='alexauragan@gmail.com',
      url='https://github.com/AlexAuragan/TAL-AI/',
      packages=['talai'],
      package_dir=package_dir 
     )