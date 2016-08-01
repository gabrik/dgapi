from setuptools import setup

setup(name='DG-API',
      version='0.1',
      description='Drive Green API',
      author='Gabriele Baldoni',
      author_email='gabriele.baldoni@gmail.com',
      url='http://www.gabrielebaldoni.it',
      install_requires=['Flask>=0.11.1', 'PyMongo>=3.3.0' , 'Flask-SQLAlchemy==0.16'],
     )
