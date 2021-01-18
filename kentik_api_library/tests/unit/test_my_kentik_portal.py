from http import HTTPStatus

from kentik_api.public.tenant import Tenant, TenantUser
from kentik_api.api_calls.api_call import APICall
from kentik_api.api_calls.api_call import APICallMethods
from kentik_api.api_calls.my_kentik_portal import *

DUMMY_API_URL = "/mykentik/tenant"
DUMMY_USR_URL = "user"
DUMMY_TEN_ID = "dummy_ten_id"
DUMMY_USR_ID = "dummy_usr_id"


def test_get_tenants_return_apiCall():

    # WHEN
    call = get_tenants()

    # THEN
    assert isinstance(call, APICall)
    assert call.url_path == f"{DUMMY_API_URL}s"
    assert call.method.name == "GET"


def test_get_tenant_info__return_apiCall():

    # WHEN
    call = get_tenant_info(DUMMY_TEN_ID)

    # THEN
    assert isinstance(call, APICall)
    assert call.url_path == f"{DUMMY_API_URL}/{DUMMY_TEN_ID}"
    assert call.method.name == "GET"


def test_create_tenant_user__return_apiCall():

    # WHEN
    call = create_tenant_user(DUMMY_TEN_ID)

    # THEN
    assert isinstance(call, APICall)
    assert call.url_path == f"{DUMMY_API_URL}/{DUMMY_TEN_ID}/{DUMMY_USR_URL}"
    assert call.method.name == "POST"


def test_delete_tenant_user__return_apiCall():

    # WHEN
    call = delete_tenant_user(DUMMY_TEN_ID, DUMMY_USR_ID)

    # THEN
    assert isinstance(call, APICall)
    assert call.url_path == f"{DUMMY_API_URL}/{DUMMY_TEN_ID}/{DUMMY_USR_URL}/{DUMMY_USR_ID}"
    assert call.method.name == "DELETE"


def test_create_tenant_user_success(client, connector) -> None:
    # given
    create_response_payload = """
    {
        "id":"148148",
        "user_email":"user2@testtenant.com",
        "last_login":null,
        "tenant_id":"577",
        "company_id":"74333"
    }"""
    connector.response_text = create_response_payload
    connector.response_code = HTTPStatus.OK

    # when
    to_create_email = "user2@testtenant.com"
    tenant_id = 577
    created = client.my_kentik_portal.create_tenant_user(tenant_id, to_create_email)

    # then
    assert connector.last_url_path == "/mykentik/tenant/577/user"
    assert connector.last_method == APICallMethods.POST
    assert connector.last_payload is not None
    assert connector.last_payload["user"]["user_email"] == "user2@testtenant.com"

    assert created.id == "148148"
    assert created.email == "user2@testtenant.com"
    assert created.last_login is None
    assert created.tenant_id == "577"
    assert created.company_id == "74333"


def test_get_tenant_success(client, connector) -> None:
    # given
    get_response_payload = """
        {
            "id":577,
            "name":"test_tenant",
            "description":"This is test tenant",
            "users": [
                {
                    "id":"148099",
                    "user_email":"test@tenant.user",
                    "last_login":null,
                    "tenant_id":"577",
                    "company_id":"74333"
                },{
                    "id":"148113",
                    "user_email":"user@testtenant.com",
                    "last_login":null,
                    "tenant_id":"577",
                    "company_id":"74333"
                }],
            "created_date":"2020-12-21T10:55:52.449Z",
            "updated_date":"2020-12-21T10:55:52.449Z"
        }"""
    connector.response_text = get_response_payload
    connector.response_code = HTTPStatus.OK
    tenant_id = 577

    # when
    tenant = client.my_kentik_portal.get(tenant_id)

    # then
    assert connector.last_url_path == f"/mykentik/tenant/577"
    assert connector.last_method == APICallMethods.GET
    assert connector.last_payload is None

    assert tenant.id == 577
    assert tenant.name == "test_tenant"
    assert tenant.description == "This is test tenant"
    assert tenant.users[0].id == "148099"
    assert tenant.users[1].id == "148113"
    assert tenant.cdate == "2020-12-21T10:55:52.449Z"


def test_delete_tenant_user_success(client, connector) -> None:
    # given
    delete_response_payload = ""  # deleting user responds with empty body
    connector.response_text = delete_response_payload
    connector.response_code = HTTPStatus.NO_CONTENT

    # when
    tenant_id = 577
    tenant_user_id = 148099
    delete_successful = client.my_kentik_portal.delete_tenant_user(tenant_id, tenant_user_id)

    # then
    assert connector.last_url_path == f"/mykentik/tenant/577/user/148099"
    assert connector.last_method == APICallMethods.DELETE
    assert connector.last_payload is None
    assert delete_successful is True
