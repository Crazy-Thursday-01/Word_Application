# 导入所需的模块和库
from sqlalchemy import create_engine, Column, String, Integer, Boolean, DateTime, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from datetime import datetime
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv(dotenv_path="../infomation.env")

# 创建数据库表的基类
Base = declarative_base()

# 创建MySQL数据库连接URL，使用环境变量中的信息
db_url = f"mysql+mysqlconnector://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_IP_ADDRESS')}:{os.getenv('MYSQL_PORT')}/{os.getenv('MYSQL_DATABASE')}"

# 定义用户活动表的ORM类
class UserActivity(Base):
    __tablename__ = 'user_activity'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)
    time = Column(DateTime, nullable=False)
    article = Column(String(255), nullable=True)
    Duplication_rate = Column(Float, nullable=True)

# 定义用户表的ORM类
class User(Base):
    __tablename__ = 'user'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), unique=True, nullable=False)
    account = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)  # 默认为False，表示普通用户

# 定义普通用户类
class nomal_user:
    def __init__(self, username, account, password, is_admin):
        # 从环境变量中加载数据库连接信息
        load_dotenv(dotenv_path="../infomation.env")

        self.db_url = f"mysql+mysqlconnector://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_IP_ADDRESS')}:{str(os.getenv('MYSQL_PORT'))}/{os.getenv('MYSQL_DATABASE')}"
        self.username = username
        self.account = account
        self.password = password
        self.is_admin = is_admin
        self.engine = create_engine(self.db_url)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def get_activities(self):
        # 查询用户的所有活动记录
        activities = self.session.query(UserActivity).filter_by(username=self.username).all()
        return activities

    def add_activity(self, article, duplication_rate):
        try:
            # 创建新的用户活动记录
            activity = UserActivity(
                username=self.username,
                is_admin=self.is_admin,
                time=datetime.now(),
                article=article,
                Duplication_rate=duplication_rate
            )

            # 将新的活动添加到用户的活动列表中
            self.session.add(activity)
            self.session.commit()
            self.session.close()
            return True
        except Exception as e:
            print("Error adding activity:", e)
            return False

    def __del__(self):
        # 在对象销毁时关闭数据库会话
        self.session.close()

# 定义管理员类，继承自普通用户类
class Admin(nomal_user):
    def __init__(self, username, account, password, is_admin):
        load_dotenv(dotenv_path="../infomation.env")
        self.db_url = f"mysql+mysqlconnector://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_IP_ADDRESS')}:{str(os.getenv('MYSQL_PORT'))}/{os.getenv('MYSQL_DATABASE')}"

        self.username = username
        self.account = account
        self.password = password
        self.is_admin = is_admin
        self.engine = create_engine(self.db_url, echo=True)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def get_activities(self):
        try:
            # 查询所有的UserActivity记录
            activities = self.session.query(UserActivity).all()
            return activities
        except Exception as e:
            print(f"An error occurred while getting activities: {e}")

    def add_activity(self, article, duplication_rate):
        # 调用User类中的add_activity方法
        try:
            return super().add_activity(article=article, duplication_rate=duplication_rate)
        except Exception as e:
            print(e)

    def get_users_info(self):
        try:
            # 查询所有的UserActivity记录
            activities = self.session.query(User).all()
            return activities
        except Exception as e:
            print(f"An error occurred while getting users information: {e}")

    def delete_user(self, username):
        try:
            # 查询要删除的用户记录
            user_to_delete = self.session.query(User).filter_by(username=username).first()

            # 如果用户存在，删除记录
            if user_to_delete:
                self.session.delete(user_to_delete)
                self.session.commit()
                print(f"User {username} has been deleted.")
            else:
                print(f"User {username} not found.")
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"An error occurred while deleting user {username}: {e}")

    def add_user(self, username, account, password, is_admin):
        try:
            # 检查是否存在相同账号的用户
            existing_user = self.session.query(User).filter_by(account=account).first()
            if existing_user:
                raise ValueError(f"账号 {account} 已存在，请选择其他账号")

            # 创建新用户
            new_user = User(username=username, account=account, password=password, is_admin=is_admin)

            # 添加用户到数据库
            self.session.add(new_user)
            self.session.commit()

            print(f"用户 {username} 添加成功")
        except Exception as e:
            self.session.rollback()
            print(f"添加用户时发生错误: {e}")

    def __del__(self):
        # 在对象销毁时关闭数据库会话
        self.session.close()

# 定义数据库操作类
class DatabaseHandler:
    def __init__(self):
        load_dotenv(dotenv_path="../infomation.env")
        self.db_url = f"mysql+mysqlconnector://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_IP_ADDRESS')}:{os.getenv('MYSQL_PORT')}/{os.getenv('MYSQL_DATABASE')}"
        self.engine = create_engine(self.db_url, echo=True)

    def verify_login(self, account, password):
        Session = sessionmaker(bind=self.engine)
        session = Session()

        # 查询用户是否存在，验证登录
        user = session.query(User).filter_by(account=account, password=password).first()
        session.close()

        return user

    def is_username_exists(self, username):
        Session = sessionmaker(bind=self.engine)
        session = Session()

        # 查询是否存在相同用户名的用户
        existing_user = session.query(User).filter_by(username=username).first()
        session.close()

        return existing_user is not None

    def is_account_exists(self, account):
        Session = sessionmaker(bind=self.engine)
        session = Session()

        # 查询是否存在相同账号的用户
        existing_user = session.query(User).filter_by(account=account).first()
        session.close()

        return existing_user is not None

    def register_user(self, username, account, password):
        if self.is_username_exists(username):
            return False

        if self.is_account_exists(account):
            return False

        Session = sessionmaker(bind=self.engine)
        session = Session()

        # 创建新用户并添加到数据库
        new_user = User(username=username, account=account, password=password, is_admin=False)

        session.add(new_user)
        session.commit()
        session.close()

        return True

    def log_user_activity(self, username, account, is_admin, article, duplication_rate):
        Session = sessionmaker(bind=self.engine)
        session = Session()

        # 记录用户活动
        activity = UserActivity(
            username=username,
            account=account,
            is_admin=is_admin,
            time=datetime.now(),
            article=article,
            Duplication_rate=duplication_rate
        )
        session.add(activity)
        session.commit()
        session.close()

# 在main块中创建Admin实例，并打印管理员用户的活动文章
if __name__ == '__main__':
    admin = Admin("admin", "admin", "password", True)
    for element in admin.get_activities():
        print(element.article)
