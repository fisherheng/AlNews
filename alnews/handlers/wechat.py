# coding: utf-8
#!/usr/bin/env python
import os
import logging.config
import tornado.web

from alnews.model import Company

Company_orm = Company.CompanyManagerORM()  # 创建一个全局ORM对象

logging.config.fileConfig(os.path.join(os.path.dirname(__file__), "../../conf/log.conf"), disable_existing_loggers=False)
logger = logging.getLogger(__name__)

# Name: WechatHandler
# Writer: Heng
class WechatHandler(tornado.web.RequestHandler):

    def get(self):
        title = '今日铝信'  # 这个title将会被发送到UserManager.html中的{{title}}部分
        companys = Company_orm.GetAllCompany()  # Get all companies.
        for company in companys:
            logger.debug(company)
        self.render('wechat/index.html', title=title, companys=companys)

    def post(self):
        pass    # Do nothing.

# Name: RegisterHandler
# Writer: Heng
class RegisterHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('wechat/register.html', title='第一步', step='手机号验证')

    def post(self):
        pass

# Urls: /Wechat
# Writer: Heng
sub_handlers = [
        (r'/Wechat/', WechatHandler),
        (r'/Wechat/Register', RegisterHandler)
    ]