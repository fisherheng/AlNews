# coding: utf-8
#!/usr/bin/env python
import os
import logging.config
import tornado.web

from alnews.model import Company

Company_orm = Company.CompanyManagerORM()  # 创建一个全局ORM对象

logging.config.fileConfig(os.path.join(os.path.dirname(__file__), "../../conf/log.conf"), disable_existing_loggers=False)
logger = logging.getLogger(__name__)

class MainHandler(tornado.web.RequestHandler):  # 主Handler，用来响应首页的URL
    def get(self):
        title = '今日铝信'  # 这个title将会被发送到UserManager.html中的{{title}}部分
        companys = Company_orm.GetAllCompany()  # Get all companies.
        for company in companys:
            logger.debug(company)
        self.render('templates/index.html', title=title, companys=companys)

    def post(self):
        pass  # Do nothing


# Name: CreateCompanyHandler
# Writer: Heng
class CreateCompanyHandler(tornado.web.RequestHandler):

    def get(self):
        logger.debug('jump to son page')
        self.render('templates/create.html')

    def post(self):
        pass


# Name: AddCompanyHandler
# Writer: Heng
class AddCompanyHandler(tornado.web.RequestHandler):

    def get(self):
        pass

    def post(self):
        company_info = {
            'company_name': self.get_argument('name'),
            'company_province': self.get_argument('province'),
            'company_provincecode': self.get_argument('province'),
            'company_city': self.get_argument('city'),
            'company_citycode': self.get_argument('city'),
            'company_area': self.get_argument('area'),
            'company_areacode': self.get_argument('area'),
            'company_address': self.get_argument('address'),
            'company_email': self.get_argument('email'),
            'company_telephone': self.get_argument('telephone'),
            'company_fax': self.get_argument('fax'),
            'company_website': self.get_argument('website')
        }

        Company_orm.CreateNewCompany(company_info)  # 调用ORM的方法将新建的用户信息写入数据库

        self.redirect('/')  # Redirect to index.


# Name: EditCompanyHandler
# Writer: Heng
class EditCompanyHandler(tornado.web.RequestHandler):

    def get(self):
        company_info = Company_orm.GetCompanyByName(self.get_argument('company_name'))
        self.render('templates/EditUserInfo.html', company_info=company_info)

    def post(self):
        pass


# Name: UpdateCompanyInfoHandler
# Writer: Heng
class UpdateCompanyInfoHandler(tornado.web.RequestHandler):

    def get(self):
        pass

    def post(self):
        Company_orm.UpdateCompanyInfoByName({
            'company_name': self.get_argument('company_name'),
            'address': self.get_argument('address'),
            'email': self.get_argument('email'),
            'telphone': self.get_argument('telphone'),
            'fax': self.get_argument('fax'),
            'website': self.get_argument('website'),
        })
        self.redirect('/')  #Redirect to index.


# Name: DeleteCompanyHandler
# Writer: Heng
class DeleteCompanyHandler(tornado.web.RequestHandler):

    def get(self):
        try:
            Company_orm.DeleteCompanyByName(self.get_argument('company_name'))
        except BaseException as e:
            logger.error(e)
            logger.info('Delete company info failed!')
        else:
            logger.info('Delete company info successfully!')
            try:
                self.redirect('/')      # Redirect to index.html
            except Exception as e:
                logger.error(e)
            else:
                logger.info('Redirect to index successfully!')

    def post(self):
        pass


# Name: WechatHandler
# Writer: Heng
class WechatHandler(tornado.web.RequestHandler):

    def get(self):
        title = '今日铝信'  # 这个title将会被发送到UserManager.html中的{{title}}部分
        companys = Company_orm.GetAllCompany()  # Get all companies.
        for company in companys:
            logger.debug(company)
        self.render('templates/wechat/index.html', title=title, companys=companys)

    def post(self):
        pass    # Do nothing.


# Name: DetailCompanyHandler
# Writer: Heng
class DetailCompanyHandler(tornado.web.RequestHandler):

    def get(self):
        company = Company_orm.GetCompanyByName(self.get_argument('company_name'))  # 利用ORM获取指定用户的信息
        title = '%s' % self.get_argument('company_name')
        try:
            self.render('templates/detail.html', title=title, company=company)  # Show this page:index.html.
        except Exception as e:
            logger.error(e)
        else:
            logger.info("Show detail information successfully!")

    def post(self):
        pass    # Do nothing.


# Name: RegisterHandler
# Writer: Heng
class RegisterHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('templates/wechat/register.html', title='第一步', step='手机号验证')

    def post(self):
        pass

sub_handlers = [  # 这里就是路由表，确定了哪些URL由哪些Handler响应
        (r'/', MainHandler),
        (r'/AddCompany', AddCompanyHandler),
        (r'/EditCompany', EditCompanyHandler),
        (r'/DeleteCompany', DeleteCompanyHandler),
        (r'/UpdateCompanyInfo', UpdateCompanyInfoHandler),
        (r'/DetailCompany', DetailCompanyHandler),
        (r'/CreateCompany', CreateCompanyHandler),
        (r'/Wechat/', WechatHandler),    # handle the request from wechat.
        (r'/Wechat/Register', RegisterHandler)
    ]