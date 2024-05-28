# import os
#
# from dotenv import load_dotenv
#
#
# class ConfigService:
#     _instance = None
#
#     def __new__(cls, *args, **kwargs):
#         if not getattr(cls, "_instance"):
#             cls._instance = super(ConfigService, cls).__new__(cls, *args, **kwargs)
#             cls.__set_props(cls._instance, *args, **kwargs)
#         return cls._instance
#
#     def __set_props(self, is_test=False):
#         load_dotenv()
#         self.instance_name = os.getenv("INSTANCE_NAME")
#
#         if not is_test and not os.getenv("IS_TEST"):
#             self.db_name = os.getenv("DB_NAME")
#             self.db_user = os.getenv("DB_USER")
#             self.db_password = os.getenv("DB_PWD")
#             self.db_host = os.getenv("DB_HOST")
#             self.db_port = os.getenv("DB_PORT")
#         else:
#             self.db_name = os.getenv("DB_NAME_TEST")
#             self.db_user = os.getenv("DB_USER_TEST")
#             self.db_password = os.getenv("DB_PWD_TEST")
#             self.db_host = os.getenv("DB_HOST_TEST")
#             self.db_port = os.getenv("DB_PORT_TEST")
#
#         self.kc_client = os.getenv("KC_CLIENT")
#         self.kc_realm = os.getenv("KC_REALM")
#         self.kc_url = os.getenv("KC_URL")
#         self.kc_prefix = os.getenv("KC_PREFIX")
#         self.production = os.getenv("PRODUCTION") in ("TRUE", "true", "True", "1")
#         self.db_pool_size = (
#             5 if not os.getenv("DB_POOL_SIZE") else int(os.getenv("DB_POOL_SIZE"))
#         )
#         self.ldap_integration_url = os.getenv("LDAP_INTEGRATION_URL")
#         self.file_store_access_key = os.getenv("FILE_STORE_ACCESS_KEY")
#         self.file_store_secret_key = os.getenv("FILE_STORE_SECRET_KEY")
#         self.file_store_uri = os.getenv("FILE_STORE_URI")
#         # AISMV
#         self.aismv_integration_url = os.getenv("AISMV_INTEGRATION_URL")
#         self.sender_route = os.getenv("SENDER_ROUTE")
#         self.receiver_route = os.getenv("RECEIVER_ROUTE")
#         # BUSS
#         self.rabbit_user = os.getenv("RABBIT_USER")
#         self.rabbit_pwd = os.getenv("RABBIT_PWD")
#         self.rabbit_address = os.getenv("RABBIT_ADDRESS")
#         self.rabbit_port = os.getenv("RABBIT_PORT")
#         self.office_url = os.getenv("OFFICE_URL")
#
#     def __repr__(self):
#         res = "ConfigService("
#         for k, v in self.__dict__.items():
#             res += f"{k}={v}, "
#         res += ")"
#         return res
#
#
# def get_config() -> ConfigService:
#     return ConfigService()


from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")