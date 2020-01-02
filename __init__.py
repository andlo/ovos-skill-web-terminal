from mycroft import MycroftSkill, intent_file_handler


class WebSsh(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('ssh.web.intent')
    def handle_ssh_web(self, message):
        self.speak_dialog('ssh.web')


def create_skill():
    return WebSsh()

