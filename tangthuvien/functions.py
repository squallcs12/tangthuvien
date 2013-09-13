'''
Created on Sep 14, 2013

@author: antipro
'''
from . import settings as st

def disqus_append(data):
    data.update(
        DISQUS_SHORTNAME=st.DISQUS_SHORTNAME,
        DISQUS_DEVELOPER=st.DISQUS_DEVELOPER
    )