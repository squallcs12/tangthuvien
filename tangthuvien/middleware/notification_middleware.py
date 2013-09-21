'''
Created on Sep 21, 2013

@author: antipro
'''
class Notification(object):
    def process_request(self, request):
        request.notification = NotificationObject(request)

    def process_template_response(self, request, response):
        response.context_data['notification'] = request.notification
        return response

class NotificationObject(object):

    def __init__(self, request):
        self.request = request
        if 'notification_messages' not in request.session:
            self.init()

    def init(self):
        self.request.session['notification_messages'] = {
                'success': [],
                'danger': [],
                'warning': [],
                'info': [],
            }

    @property
    def messages(self):
        messages = self.request.session['notification_messages']
        self.init()
        return messages

    def add_message(self, kind, message):
        if not isinstance(message, str):
            message = message.__unicode__() if hasattr(message, '__unicode__') else message.__str__()
        self.request.session['notification_messages'][kind].append(message)
        self.request.session.modified = True

    def success(self, message):
        self.add_message('success', message)

    def danger(self, message):
        self.add_message('danger', message)

    error = danger

    def warning(self, message):
        self.add_message('warning', message)

    def information(self, message):
        self.add_message('info', message)
