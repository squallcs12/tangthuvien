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
<p>Vestibulum hendrerit elementum sodales. Suspendisse euismod ligula eu felis dapibus tempor. Duis varius metus velit, ac pharetra massa bibendum sed. Ut lectus lacus, condimentum ut scelerisque vitae, lacinia ut dui. Fusce eget sagittis libero. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas porttitor arcu vel aliquam pellentesque. Duis sed mollis arcu. Nunc dapibus ligula sem, eget posuere felis varius et.</p>
<p>Nam eu tempus neque. Pellentesque massa sem, accumsan interdum ultrices at, egestas quis ipsum. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Curabitur sodales lacinia dolor. Duis scelerisque erat ac nisi lobortis, in eleifend libero lobortis. Donec sit amet dui sapien. Sed at magna vitae nunc porttitor fringilla consequat ac tortor. Sed consectetur justo vel hendrerit dictum. Aliquam posuere velit a laoreet sodales. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin vitae sem sagittis, porttitor nunc in, convallis sem. Fusce consequat sapien nibh. Aliquam luctus, enim at pulvinar blandit, augue purus tempus ante, eget viverra velit neque vulputate felis. Quisque malesuada, ante quis posuere viverra, magna elit commodo nisi, vel venenatis lacus nisl in sem. Proin hendrerit adipiscing tempus. Nunc tincidunt elit urna, in porttitor risus interdum eget.</p>
<p>Nunc molestie mi vehicula condimentum pellentesque. Ut venenatis risus ac euismod auctor. Morbi sodales tincidunt neque, nec tincidunt arcu mattis a. Quisque elementum est magna. Maecenas dapibus diam libero, vel ultrices nunc hendrerit vitae. Sed sodales at lacus sed placerat. Duis tincidunt ligula eu lorem euismod viverra. Suspendisse tempus erat non placerat pretium. Pellentesque ac purus non ligula pretium ultricies. Cras quis odio quis enim convallis gravida.</p>
    '''.format(n))

