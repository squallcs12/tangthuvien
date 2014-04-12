'''
Created on Jul 28, 2013

@author: antipro
'''
from book.models import Author
import factory


class AuthorFactory(factory.Factory):
    FACTORY_FOR = Author

    name = factory.Sequence(lambda n: unicode('Author {0}'.format(n)))
    information = factory.Sequence(lambda n: '''
        {0}
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam adipiscing dapibus orci ut fermentum. Ut in felis vehicula, imperdiet justo in, laoreet tellus. Nam porta lorem sed lorem elementum, at elementum dolor cursus. Nam nec gravida nulla. In justo urna, congue eget lectus hendrerit, tempus iaculis tellus. Nulla interdum neque id ante placerat iaculis. Aliquam tincidunt orci vel tincidunt mattis. Cras vestibulum aliquet nisl, ac suscipit elit pulvinar id. Duis eget commodo risus. Maecenas pellentesque libero eu turpis feugiat luctus. Duis convallis at massa et ornare. Cras venenatis, turpis eu bibendum interdum, augue augue dignissim libero, vitae aliquet erat nibh vel enim. Vestibulum non risus nec lacus vestibulum commodo in id enim. Suspendisse at tincidunt sapien. Proin a faucibus diam, pulvinar dignissim massa. In hac habitasse platea dictumst.
    '''.format(n))
