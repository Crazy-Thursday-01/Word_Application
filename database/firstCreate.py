from sqlalchemy import create_engine, Column, String, Integer, Boolean,DateTime,Float,ForeignKey
from sqlalchemy.orm import sessionmaker, relationship,declarative_base
from datetime import datetime
from dotenv import load_dotenv
import os


Base = declarative_base()
# MySQL数据库连接URL，替换为你自己的数据库信息
# db_url = "mysql+mysqlconnector://admin:123456@localhost:3306/疯狂星期四"
load_dotenv(dotenv_path="../infomation.env")
db_url= f"mysql+mysqlconnector://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_IP_ADDRESS')}:{str(os.getenv('MYSQL_PORT'))}/{os.getenv('MYSQL_DATABASE')}"
engine = create_engine(db_url)

class UserActivity(Base):
    __tablename__ = 'user_activity'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)
    time = Column(DateTime, nullable=False)
    article = Column(String(255), nullable=True)
    Duplication_rate = Column(Float, nullable=True)


class User(Base):
    __tablename__ = 'user'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), unique=True, nullable=False)
    account = Column(String(255),unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)  # Default to False for regular users




try:
    # 在数据库中创建表
    Session = sessionmaker(bind=engine)
    session = Session()
    Base.metadata.create_all(engine)
    # 添加一个admin和一个user的示例


    # admin用户
    admin = User(username='admin', account='admin', password='password', is_admin=True)
    session.add(admin)

    # 普通用户
    user = User(username='user', account='user', password='123456', is_admin=False)
    session.add(user)

    session.commit()
    session.close()
    print("Tables created successfully.")
except Exception as e:
    print(f"Error creating tables: {e}")
    print("Tables might already exist or there is an issue with the connection.")



