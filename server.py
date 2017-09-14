# coding: utf-8
#!/usr/bin/env python

import tornado.httpserver  # 引入tornado的一些模块文件
import tornado.ioloop
import tornado.options
import tornado.web

import logging.config

logging.config.fileConfig('log.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

from tornado.options import define, options

import orm

define('port', default=9999, help='run on the given port', type=int)

Company_orm = orm.CompanyManagerORM()  # 创建一个全局ORM对象


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

        self.redirect('/')  #Redirect to index.


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

    def post(self): # Do nothing
        pass

# Name: MainProcess
# Writer: Heng
# Function: Main process.
def MainProcess():
    tornado.options.parse_command_line()
    application = tornado.web.Application([  # 这里就是路由表，确定了哪些URL由哪些Handler响应
        (r'/', MainHandler),
        (r'/AddCompany', AddCompanyHandler),
        (r'/EditCompany', EditCompanyHandler),
        (r'/DeleteCompany', DeleteCompanyHandler),
        (r'/UpdateCompanyInfo', UpdateCompanyInfoHandler),
        (r'/DetailCompany', DetailCompanyHandler),
        (r'/CreateCompany', CreateCompanyHandler)
    ])

    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)    # Listening port.
    tornado.ioloop.IOLoop.instance().start()  # Start server.


if __name__ == '__main__':  # 文件的入口
    logger.info('==============================logging start==============================')
    MainProcess()