from .base import *

DEBUG = env.bool('DJANGO_DEBUG', default=True)
SECRET_KEY = env('DJANGO_SECRET_KEY', default='%6w+me3$$38$m^&9&nuu1l(jfzed2+5=qg!b)5sy(886*63)kn')
