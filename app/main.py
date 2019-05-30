# -*- coding: utf-8 -*-

import falcon
from app.database import init_session


class App(falcon.API):

    def _init__(self, *args, **kwargs):
        super(App, self).__init__(*args, **kwargs)


init_session()
application = App()
