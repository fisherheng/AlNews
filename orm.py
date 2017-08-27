# coding: utf-8
#!/usr/bin/env python

from sqlalchemy import *
from sqlalchemy.orm import *

# Settings to connect to mysql database
database_setting = {'database_type': 'mysql',  # 数据库类型
                    'connector': 'mysqlconnector',  # 数据库连接器
                    'user_name': 'root',  # 用户名，根据实际情况修改
                    'password': 'zhang@heng0617M',  # 用户密码，根据实际情况修改
                    'host_name': '47.93.4.14',  # 在本机上运行
                    'database_name': 'platform',
                    'charset': 'charset=utf8'
                    }


# 下面这个类就是实体类，对应数据库中的user表
class Company(object):
    def __init__(self, company_name,
                 address, email, telphone, fax, website):
        self.company_name = company_name
        self.address = address
        self.email = email
        self.telphone = telphone
        self.fax = fax
        self.website = website

        # 这个类就是直接操作数据库的类


class CompanyManagerORM():
    def __init__(self):
        ''''' 
            # 这个方法就是类的构造函数，对象创建的时候自动运行 
        '''
        self.engine = create_engine(  # 生成连接字符串，有特定的格式
            database_setting['database_type'] +
            '+' +
            database_setting['connector'] +
            '://' +
            database_setting['user_name'] +
            ':' +
            database_setting['password'] +
            '@' +
            database_setting['host_name'] +
            '/' +
            database_setting['database_name'] +
            '?' +
            database_setting['charset']
        )

        self.metadata = MetaData(self.engine)
        self.company_table = Table('company', self.metadata,
                                autoload=True)

        # 将实体类User映射到user表
        mapper(Company, self.company_table)

        # 生成一个会话类，并与上面建立的数据库引擎绑定
        self.Session = sessionmaker()
        self.Session.configure(bind=self.engine)

        # 创建一个会话
        self.session = self.Session()

    def CreateNewCompany(self, company_info):
        ''''' 
            # 这个方法根据传递过来的用户信息列表新建一个用户 
            # user_info是一个列表，包含了从表单提交上来的信息 
        '''
        print(company_info['address'])
        new_company = Company(
            company_info['company_name'],
            company_info['address'],
            company_info['email'],
            company_info['telphone'],
            company_info['fax'],
            company_info['website']
        )
        self.session.add(new_company)  # 增加新用户
        self.session.commit()  # 保存修改

    def GetCompanyByName(self, company_name):  # 根据用户名返回信息
        return self.session.query(Company).filter_by(
            company_name=company_name).all()[0]

    def GetAllCompany(self):  # 返回所有用户的列表
        return self.session.query(Company)

    def UpdateCompanyInfoByName(self, company_info):  # 根据提供的信息更新用户资料
        company_name = company_info['company_name']
        company_info_without_name = {'address': company_info['address'],
                                  'email': company_info['email'],
                                  'telphone': company_info['telphone'],
                                  'fax': company_info['fax'],
                                  'website': company_info['website']
                                  }
        self.session.query(Company).filter_by(company_name=company_name).update(
            company_info_without_name)
        self.session.commit()

    def DeleteCompanyByName(self, company_name):  # 删除指定用户名的用户
        company_need_to_delete = self.session.query(Company).filter_by(
            company_name=company_name).all()[0]
        self.session.delete(company_need_to_delete)
        self.session.commit()