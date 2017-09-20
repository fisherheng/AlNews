# coding: utf-8
#!/usr/bin/env python
import os
from sqlalchemy import *
from sqlalchemy.orm import *

import logging.config

# Init log
logging.config.fileConfig(os.path.join(os.path.dirname(__file__), "../../conf/log.conf"), disable_existing_loggers=False)
logger = logging.getLogger(__name__)

# Settings to connect to mysql database
database_setting = {'database_type': 'mysql',
                    'connector': 'mysqlconnector',
                    'user_name': 'root',
                    'password': 'zhang@heng0617M',
                    'host_name': 'localhost',
                    'database_name': 'platform',
                    'charset': 'charset=utf8'
                    }


# Class: Company
# Writer: Heng
class Company(object):
    def __init__(self, company_name, company_province, company_provincecode,
                 company_city, company_citycode, company_area, company_areacode,
                 company_address, company_email, company_telephone, company_fax,
                 company_website):
        self.company_name = company_name
        self.company_province = company_province
        self.company_provincecode = company_provincecode
        self.company_city = company_city
        self.company_citycode = company_citycode
        self.company_area = company_area
        self.company_areacode = company_areacode
        self.company_address = company_address
        self.company_email = company_email
        self.company_telephone = company_telephone
        self.company_fax = company_fax
        self.company_website = company_website


# Class: CompanyManagerORM
# Writer: Heng
class CompanyManagerORM():

    # Name: __init__
    # Writer: Heng
    # function: Construction method.
    def __init__(self):
        self.engine = create_engine(
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
        )   # Construct connection string.

        self.metadata = MetaData(self.engine)
        self.company_table = Table('company', self.metadata,
                                autoload=True)

        mapper(Company, self.company_table)

        self.Session = sessionmaker()
        self.Session.configure(bind=self.engine)
        self.session = self.Session()

    # Name: CreateNewCompany
    # Writer: Heng
    # Function: Write new company information to database.
    def CreateNewCompany(self, company_info):
        new_company = Company(
            company_info['company_name'],
            company_info['company_province'],
            company_info['company_provincecode'],
            company_info['company_city'],
            company_info['company_citycode'],
            company_info['company_area'],
            company_info['company_areacode'],
            company_info['company_address'],
            company_info['company_email'],
            company_info['company_telephone'],
            company_info['company_fax'],
            company_info['company_website']
        )
        self.session.add(new_company)
        self.session.commit()

    # Name: GetCompanyByName
    # Writer: Heng
    # Function: Get company information from database, searching by name.
    def GetCompanyByName(self, company_name):
        return self.session.query(Company).filter_by(
            company_name=company_name).all()[0]

    # Name: GetAllCompany
    # Writer: Heng
    # Function: Get all companies' information.
    def GetAllCompany(self):
        return self.session.query(Company)

    # Name: UpdateCompanyInfoByNmae
    # Writer: Heng
    # Function: Update one piece of company's information,searching by company's name.
    def UpdateCompanyInfoByName(self, company_info):
        company_name = company_info['company_name']
        company_info_without_name = {'company_province': company_info['company_province'],
                                  'email': company_info['email'],
                                  'telphone': company_info['telphone'],
                                  'fax': company_info['fax'],
                                  'website': company_info['website']
                                     }
        try:
            self.session.query(Company).filter_by(company_name=company_name).update(
                company_info_without_name)
            self.session.commit()
        except Exception as e:
            logger.error(e)
            logger.info('Update company\' info failed')
        else:
            logger.info('Update company\'s info successfully')

    # Name: DeleteCompanyByName
    # Writer: Heng
    # Function: Delete one piece of company's information, searching by company's name.
    def DeleteCompanyByName(self, company_name):
        company_need_to_delete = self.session.query(Company).filter_by(
            company_name=company_name).all()[0]
        try:
            self.session.delete(company_need_to_delete)
            self.session.commit()
        except Exception as e:
            logger.error(e)
            logger.info('Delete company\' info failed')
        else:
            logger.info('Delete company\'s info successfully')
