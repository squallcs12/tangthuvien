'''
Created on Jul 29, 2013

@author: antipro
'''
import factory
from book.models.chapter_model import Chapter

class ChapterFactory(factory.Factory):

    FACTORY_FOR = Chapter

    title = factory.Sequence(lambda n: 'chapter-title-{0}'.format(n))
    content = factory.Sequence(lambda n : '''
    {0}
    <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam adipiscing dapibus orci ut fermentum. Ut in felis vehicula, imperdiet justo in, laoreet tellus. Nam porta lorem sed lorem elementum, at elementum dolor cursus. Nam nec gravida nulla. In justo urna, congue eget lectus hendrerit, tempus iaculis tellus. Nulla interdum neque id ante placerat iaculis. Aliquam tincidunt orci vel tincidunt mattis. Cras vestibulum aliquet nisl, ac suscipit elit pulvinar id. Duis eget commodo risus. Maecenas pellentesque libero eu turpis feugiat luctus. Duis convallis at massa et ornare. Cras venenatis, turpis eu bibendum interdum, augue augue dignissim libero, vitae aliquet erat nibh vel enim. Vestibulum non risus nec lacus vestibulum commodo in id enim. Suspendisse at tincidunt sapien. Proin a faucibus diam, pulvinar dignissim massa. In hac habitasse platea dictumst.</p>
<p>Sed nec pretium nisl. Morbi tincidunt tincidunt dictum. Suspendisse sit amet tellus id erat sollicitudin feugiat id at eros. Nunc venenatis bibendum ipsum dignissim aliquam. Nullam a augue dui. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Donec rutrum neque a tincidunt rutrum. Pellentesque et varius enim. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum in orci tellus. Donec tristique sapien vitae fringilla eleifend.</p>
    '''.format(n))

