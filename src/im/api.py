import requests

from im.models import (
    BaseResponse, Credentials, GetInvoicesHistory, GetPaymentsHistory, InvoicesHistoryList,
    InvoicesResponse, OperationCode, PaymentsHistoryList, PaymentsResponse, UserToken,
    UserTokenData)


class ApiException(Exception):
    pass


def _get_result(part_of_url: str, data: dict, timeout: int = 30) -> dict:
    data = requests.post(f'https://api.intellectmoney.ru/personal/{part_of_url}',
                         data=data,
                         headers={'Accept': 'text/json'},
                         timeout=timeout).json()
    resp = BaseResponse(**data)
    if resp.OperationState.Code != OperationCode.Success:
        raise ApiException(data)
    return resp.Result


def getUserToken(credentials: Credentials) -> UserToken:
    data = _get_result('user/getUserToken', credentials.dict())
    return UserTokenData(**data).UserToken


def getPaymentsHistory(reqData: GetPaymentsHistory) -> PaymentsHistoryList:
    return PaymentsHistoryList(**_get_result('payment/getPaymentsHistory', reqData.dict()))


def getInvoicesHistory(reqData: GetInvoicesHistory) -> InvoicesHistoryList:
    return InvoicesHistoryList(**_get_result('payment/getInvoicesHistory', reqData.dict()))
