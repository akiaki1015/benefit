from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Model import *
from user_settings import DB


class DBClient:
    # DB情報
    DATABASE = 'mysql+pymysql://%s:%s@%s/%s?charset=utf8' % (
        DB['user'],
        DB['password'],
        DB['host'] + ':' + DB['port'],
        DB['name']
    )
    engine = ""
    session = ""

    def __init__(self):
        if self.engine == "":
            self.engine = create_engine(self.DATABASE)

    def get_connect(self):
        if self.session == "":
            Session = sessionmaker(bind=self.engine)
            self.session = Session()
            # print(self.session.query(History).all())
        return self.session

    def create_table(self):
        # create table
        Base.metadata.create_all(bind=self.engine, checkfirst=True)
