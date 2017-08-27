# coding: utf-8
#!/usr/bin/env python

# This is a Web Server for UserManager

import tornado.httpserver  # 引入tornado的一些模块文件
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options

import orm  # 引入刚刚编写的orm层代码

define('port', default=9999, help='run on the given port', type=int)

Company_orm = orm.CompanyManagerORM()  # 创建一个全局ORM对象


class MainHandler(tornado.web.RequestHandler):  # 主Handler，用来响应首页的URL
    ''''' 
        MainHandler shows all data and a form to add new user 
    '''

    def get(self):  # 处理主页面(UserManager.html)的GET请求
        # show all data and a form
        title = 'Company Manager V0.1'  # 这个title将会被发送到UserManager.html中的{{title}}部分

        companys = Company_orm.GetAllCompany()  # 使用ORM获取所有用户的信息
        # 下面这一行会将title和users两个变量分别发送到指定模板的对应变量中去
        self.render('index.html', title=title, companys=companys)  # 并显示该模板页面

    def post(self):
        pass  # 这里不处理POST请求


class AddCompanyHandler(tornado.web.RequestHandler):  # 响应/AddUser的URL
    ''''' 
        AddUserHandler collects info to create new user 
    '''

    def get(self):
        pass

    def post(self):  # 这个URL只响应POST请求，用来收集用户信息并新建帐号
        # Collect info and create a user record in the database
        print(self.get_argument('address'))
        company_info = {
            'company_name': self.get_argument('company_name'),
            'address': self.get_argument('address'),
            'email': self.get_argument('email'),
            'telphone': self.get_argument('telphone'),
            'fax': self.get_argument('fax'),
            'website': self.get_argument('website')
        }

        print(company_info['address'])

        Company_orm.CreateNewCompany(company_info)  # 调用ORM的方法将新建的用户信息写入数据库

        self.redirect('http://47.93.4.14:9999')  # 页面转到首页


class EditCompanyHandler(tornado.web.RequestHandler):  # 响应/EditUser的URL
    ''''' 
        Show a page to edit user info, 
        user name is given by GET method 
    '''

    def get(self):  # /EditUser的URL中，响应GET请求
        company_info = Company_orm.GetCompanyByName(self.get_argument('company_name'))  # 利用ORM获取指定用户的信息
        self.render('templates/EditUserInfo.html', company_info=company_info)  # 将该用户信息发送到EditUserInfo.html以供修改

    def post(self):
        pass


class UpdateCompanyInfoHandler(tornado.web.RequestHandler):  # 用户信息编辑完毕后，将会提交到UpdateUserInfo，由此Handler处理
    ''''' 
        Update user info by given list 
    '''

    def get(self):
        pass

    def post(self):  # 调用ORM层的UpdateUserInfoByName方法来更新指定用户的信息
        Company_orm.UpdateCompanyInfoByName({
            'company_name': self.get_argument('company_name'),
            'address': self.get_argument('address'),
            'email': self.get_argument('email'),
            'telphone': self.get_argument('telphone'),
            'fax': self.get_argument('fax'),
            'website': self.get_argument('website'),
        })
        self.redirect('localhost:9999')  # 数据库更新后，转到首页


class DeleteCompanyHandler(tornado.web.RequestHandler):  # 这个Handler用来响应/DeleteUser的URL
    ''''' 
        Delete user by given name 
    '''

    def get(self):
        # 调用ORM层的方法，从数据库中删除指定的用户
        Company_orm.DeleteCompanyByName(self.get_argument('company_name'))

        self.redirect('http://47.93.4.14:9999')  # 数据库更新后，转到首页

    def post(self):
        pass


def MainProcess():  # 主过程，程序的入口
    tornado.options.parse_command_line()
    application = tornado.web.Application([  # 这里就是路由表，确定了哪些URL由哪些Handler响应
        (r'/', MainHandler),  # 路由表中的URL是用正则表达式来过滤的
        (r'/AddCompany', AddCompanyHandler),
        (r'/EditCompany', EditCompanyHandler),
        (r'/DeleteCompany', DeleteCompanyHandler),
        (r'/UpdateCompanyInfo', UpdateCompanyInfoHandler),
    ])

    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)  # 在上面的的define中指定了端口为9999
    tornado.ioloop.IOLoop.instance().start()  # 启动服务器


if __name__ == '__main__':  # 文件的入口
    MainProcess()