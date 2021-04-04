import pytest
import requests
from jsonpath import jsonpath
from middleware.handler import YZHandler


def login(phone, pwd):
    """提取并封装login模块中复用的代码"""
    user = {"mobile_phone": phone,
            "pwd": pwd
            }
    resp = requests.request(method='POST',
                            url=YZHandler.yaml_config['host'] + '/member/login',
                            headers={'X-Lemonban-Media-Type': 'lemonban.v2'},
                            json=user
                            )
    resp_json = resp.json()

    # token = resp_json["data"]["token_info"]["token"]
    # token_type = resp_json["data"]["token_info"]["token_type"]

    token = jsonpath(resp_json, '$..token')[0]
    token_type = jsonpath(resp_json, '$..token_type')[0]
    id = jsonpath(resp_json, '$..id')[0]
    leave_amount = jsonpath(resp_json, '$..leave_amount')[0]

    token = " ".join([token_type, token])
    return {"id": id,
            "token": token,
            "leave_amount": leave_amount
            }


@pytest.fixture()
def investor_login():
    """投资人登录，得到 id, token, leave_amount
    """
    user = {"mobile_phone": YZHandler.user_config['investor_user']['phone'],
            "pwd": YZHandler.user_config['investor_user']['pwd']
            }
    return login(user['mobile_phone'], user['pwd'])


@pytest.fixture()
def admin_login():
    """管理员登录"""
    user = {"mobile_phone": YZHandler.user_config['admin_user']['phone'],
            "pwd": YZHandler.user_config['admin_user']['pwd']
            }
    return login(user['mobile_phone'], user['pwd'])


@pytest.fixture()
def loan_login():
    """借款人登录"""
    user = {"mobile_phone": YZHandler.user_config['loan_user']['phone'],
            "pwd": YZHandler.user_config['loan_user']['pwd']
            }
    return login(user['mobile_phone'], user['pwd'])


@pytest.fixture()
def add_loan(loan_login):
    headers = {'X-Lemonban-Media-Type': 'lemonban.v2',
               'Authorization': loan_login['token']}

    data = {'member_id': loan_login['id'],
            'title': '贷款买房',
            'amount': '500000.00',
            'loan_rate': '5.0',
            'loan_term': 12,
            'loan_date_type': 1,
            'bidding_days': 10}

    resp = requests.request(method='POST',
                            url=YZHandler.yaml_config['host'] + '/loan/add',
                            headers=headers,
                            json=data)
    resp_json = resp.json()
    loan_id = jsonpath(resp_json, '$..id')[0]
    return loan_id


@pytest.fixture()
def db():
    """管理数据库连接的夹具"""
    db_conn = YZHandler.db_class()
    yield db_conn
    db_conn.close()
