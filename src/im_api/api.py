import requests

from im_api.models import (
    BaseResponse, Credentials, GetInvoicesHistory, GetPaymentsHistory, InvoicesHistoryList,
    InvoicesResponse, OperationCode, PaymentsHistoryList, PaymentsResponse,
    UserToken, UserTokenData)


class ApiException(Exception):
    pass


def _get_data(part_of_url: str, data: dict, timeout: int = 30) -> dict:
    data = requests.post(f'https://api.intellectmoney.ru/personal/{part_of_url}',
                         data=data,
                         headers={'Accept': 'text/json'},
                         timeout=timeout).json()
    resp = BaseResponse(**data)
    if resp.OperationState.Code != OperationCode.Success:
        raise ApiException(data)
    return data


def getUserToken(credentials: Credentials) -> UserToken:
    data = _get_data('user/getUserToken', credentials.dict())
    return UserTokenData(**data).UserToken


def getPaymentsHistory(reqData: GetPaymentsHistory) -> PaymentsHistoryList:
    data = _get_data('payment/getPaymentsHistory', reqData.dict())
    return PaymentsResponse(**data).Result


def getInvoicesHistory(reqData: GetInvoicesHistory) -> InvoicesHistoryList:
    data = _get_data('payment/getInvoicesHistory', reqData.dict())
    return InvoicesResponse(**data).Result
