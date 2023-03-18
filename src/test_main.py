from fastapi.testclient import TestClient
from models.CustomerLogin import CustomerLogin
from main import app  # assuming the main FastAPI instance is defined in a file named main.py

client = TestClient(app)

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyaWQiOjEsInJ1c2VyaWQiOiJVLTEiLCJ1c2VybmFtZSI6InJlc2VsbGVyX3Rlc3RfdXNlciIsInNob3J0bmFtZSI6IlJUVSIsInVzZXJlbWFpbCI6InJlc2VsbGVyQHRlc3QuY29tIiwiYWNjb3VudHR5cGUiOiJSICAgICIsImN1c3RvbWVycmVzZWxsZXJpZCI6bnVsbCwiaXNhY3RpdmUiOnRydWUsImNvbXBhbnlfbmFtZSI6IlJlc2VsbGVyIGNvbXBhbnkiLCJ1c2VyY291bnRyeSI6IlVTQSIsImV4cGlyZXMiOjE2Nzg0MDA1NTMuNTcyMTQ0M30.mlZoRdrAVx3sk6ui0dMMpayTN6t4hAuvi637uNV8nbY"

def test_userlogin():
    # test case 1: correct credentials
    user = CustomerLogin(ruserid="U-1", password="2023febpass")
    response = client.post("/api/user/login", json=user.dict())
    assert response.status_code == 200
    assert "access_token" in response.json()
    
    # test case 2: incorrect username
    user = CustomerLogin(ruserid="wronguser", password="2023febpass")
    response = client.post("/api/user/login", json=user.dict())
    assert response.status_code == 401
    assert "Access Denied" in response.json()
    
    # test case 3: incorrect password
    user = CustomerLogin(ruserid="U-1", password="wrongpassword")
    response = client.post("/api/user/login", json=user.dict())
    assert response.status_code == 401
    assert "Access Denied" in response.json()
    
def test_add_new_customer():
    payload = {
        "username": "BackendDEV",
        "shortname": "Test User",
        "useremail": "testuser@example.com",
        "userpassword": "password",
        "accounttype": "basic",
        "company_name": "Test Company",
        "usercountry": "US",
        "address_dl_contactperson": "John Smith",
        "address_dl1": "123 Main St",
        "address_dl2": "",
        "address_dl3": "",
        "address_dl_city": "Anytown",
        "address_dl_state": "CA",
        "address_dl_country": "US",
        "address_dl_pincode": "12345",
        "emailid": "testuser@example.com",
        "cellularphoneno": "555-555-5555",
        "phoneno1": "555-555-5555",
        "image_url": "",
        "address1": "123 Main St",
        "address2": "",
        "address3": "",
        "address_city": "Anytown",
        "address_state": "CA",
        "address_country": "US",
        "address_pincode": "12345"
    }

    global token    
    response = client.post("/api/reseller/customer/new", headers={"Authorization": f"Bearer {token}"}, json=payload)

    assert response.status_code == 200
    assert response.json()["Success"] == "Row inserted"
    
def test_get_all_customers():

    global token
    response = client.get("/api/reseller/customer", headers={"Authorization": f"Bearer {token}"},)

    db_entry_1=[1, 'U-1', 'reseller_test_user', 'RTU', 'reseller@test.com', '2023febpass', 'R    ', None, True, 'Reseller company', 'USA',None,None,None,None,None,None,None,None,'reseller@secondary.com', '+1 (555) 555-1234', '(555) 555-1234', 'https://i.samsurinonline.com/no_image.png', '132, My street','','', 'kingston', 'new york',None ,'12401', '2023-02-22T13:39:06.430216', 0, '2023-02-22T13:39:06.430216', 0]

    assert response.status_code == 200
    assert (response.json())[0]["userid"] == db_entry_1[0]
    assert (response.json())[0]["ruserid"] == db_entry_1[1]
    assert (response.json())[0]["username"] == db_entry_1[2]
    assert (response.json())[0]["shortname"] == db_entry_1[3]
    assert (response.json())[0]["useremail"] == db_entry_1[4]
    assert (response.json())[0]["accounttype"] == db_entry_1[6]
    assert (response.json())[0]["customerresellerid"] == db_entry_1[7]
    assert (response.json())[0]["company_name"] == db_entry_1[9]
    assert (response.json())[0]["usercountry"] == db_entry_1[10]
    assert (response.json())[0]["address_dl_contactperson"] == db_entry_1[11]
    assert (response.json())[0]["address_dl1"] == db_entry_1[12]
    assert (response.json())[0]["address_dl2"] == db_entry_1[13]
    assert (response.json())[0]["address_dl3"] == db_entry_1[14]
    assert (response.json())[0]["address_dl_city"] == db_entry_1[15]
    assert (response.json())[0]["address_dl_state"] == db_entry_1[16]
    assert (response.json())[0]["address_dl_country"] == db_entry_1[17]
    assert (response.json())[0]["address_dl_pincode"] == db_entry_1[18]
    assert (response.json())[0]["emailid"] == db_entry_1[19]
    assert (response.json())[0]["cellularphoneno"] == db_entry_1[20]
    assert (response.json())[0]["phoneno1"] == db_entry_1[21]
    assert (response.json())[0]["image_url"] == db_entry_1[22]
    assert (response.json())[0]["address1"] == db_entry_1[23]
    assert (response.json())[0]["address2"] == db_entry_1[24]
    assert (response.json())[0]["address3"] == db_entry_1[25]
    assert (response.json())[0]["address_city"] == db_entry_1[26]
    assert (response.json())[0]["address_state"] == db_entry_1[27]
    assert (response.json())[0]["address_country"] == db_entry_1[28]
    assert (response.json())[0]["address_pincode"] == db_entry_1[29]
    assert (response.json())[0]["created_at"] == db_entry_1[30]
    assert (response.json())[0]["created_by"] == db_entry_1[31]
    assert (response.json())[0]["updated_at"] == db_entry_1[32]
    assert (response.json())[0]["updated_by"] == db_entry_1[33]
    
def test_edit_customer():
    payload = {
                "userid": 38,
                "username": "DemoUser" ,
                "shortname": "" ,
                "useremail": "" ,
                "userpassword": "" ,
                "accounttype": "" ,
                "company_name": "" ,
                "usercountry": "" ,
                "address_dl_contactperson": "" ,
                "address_dl1": "" ,
                "address_dl2": "" ,
                "address_dl3": "" ,
                "address_dl_city": "" ,
                "address_dl_state": "" ,
                "address_dl_country": "" ,
                "address_dl_pincode": "" ,
                "emailid": "" ,
                "cellularphoneno": "" ,
                "phoneno1": "" ,
                "image_url": "" ,
                "address1": "" ,
                "address2": "" ,
                "address3": "" ,
                "address_city": "" ,
                "address_state": "" ,
                "address_country": "" ,
                "address_pincode": ""
            }

    global token
    response = client.put("/api/reseller/customer", headers={"Authorization": f"Bearer {token}"}, json=payload)

    assert response.status_code == 200
    assert response.json()["Success"] == "Row Updated"
    
    
def test_search_customer():
    payload = {
                "username": "Tanmay Bisen" ,
                "useremail": "mail@mail.com" ,
                "cellularphoneno": "1234567890"
            }

    data = {
    "userid": 69,
    "ruserid": "C-8",
    "username": "Tanmay Bisen",
    "shortname": "",
    "useremail": "Tanmay Bisen@C-8.com",
    "accounttype": "     ",
    "customerresellerid": "U-1",
    "company_name": "Tv News",
    "usercountry": "USA",
    "address_dl_contactperson": "",
    "address_dl1": "Some street ",
    "address_dl2": "stree 2",
    "address_dl3": "",
    "address_dl_city": "Pune",
    "address_dl_state": "Maharashtra",
    "address_dl_country": "India",
    "address_dl_pincode": "123456",
    "emailid": "",
    "cellularphoneno": "",
    "phoneno1": "",
    "image_url": "https://s3.amazonaws.com/vgconfigurator/no_image.png",
    "address1": "Los Angeles",
    "address2": "212 b baker",
    "address3": "",
    "address_city": "Los Angeles",
    "address_state": "California",
    "address_country": "USA",
    "address_pincode": "123456",
    "created_at": "2023-02-22T13:39:06.430216",
    "created_by": 1,
    "updated_at": "2023-02-22T13:39:06.430216",
    "updated_by": 1
  }

    global token
    response = client.post("/api/reseller/customer", headers={"Authorization": f"Bearer {token}"}, json=payload)

    assert response.status_code == 200
    assert (response.json())[0]["userid"] == data.get("userid")
    assert (response.json())[0]["ruserid"] == data.get("ruserid")
    assert (response.json())[0]["username"] == data.get("username")
    assert (response.json())[0]["shortname"] == data.get("shortname")
    assert (response.json())[0]["useremail"] == data.get("useremail")
    assert (response.json())[0]["accounttype"] == data.get("accounttype")
    assert (response.json())[0]["customerresellerid"] == data.get("customerresellerid")
    assert (response.json())[0]["company_name"] == data.get("company_name")
    assert (response.json())[0]["usercountry"] == data.get("usercountry")
    assert (response.json())[0]["address_dl_contactperson"] == data.get("address_dl_contactperson")
    assert (response.json())[0]["address_dl1"] == data.get("address_dl1")
    assert (response.json())[0]["address_dl2"] == data.get("address_dl2")
    assert (response.json())[0]["address_dl3"] == data.get("address_dl3")
    assert (response.json())[0]["address_dl_city"] == data.get("address_dl_city")
    assert (response.json())[0]["address_dl_state"] == data.get("address_dl_state")
    assert (response.json())[0]["address_dl_country"] == data.get("address_dl_country")
    assert (response.json())[0]["address_dl_pincode"] == data.get("address_dl_pincode")
    assert (response.json())[0]["emailid"] == data.get("emailid")
    assert (response.json())[0]["cellularphoneno"] == data.get("cellularphoneno")
    assert (response.json())[0]["phoneno1"] == data.get("phoneno1")
    assert (response.json())[0]["image_url"] == data.get("image_url")
    assert (response.json())[0]["address1"] == data.get("address1")
    assert (response.json())[0]["address2"] == data.get("address2")
    assert (response.json())[0]["address3"] == data.get("address3")
    assert (response.json())[0]["address_city"] == data.get("address_city")
    assert (response.json())[0]["address_state"] == data.get("address_state")
    assert (response.json())[0]["address_country"] == data.get("address_country")
    assert (response.json())[0]["address_pincode"] == data.get("address_pincode")
    assert (response.json())[0]["created_at"] == data.get("created_at")
    assert (response.json())[0]["created_by"] == data.get("created_by")
    assert (response.json())[0]["updated_at"] == data.get("updated_at")
    assert (response.json())[0]["updated_by"] == data.get("updated_by")
    
    
def test_add_new_order():
    payload = {
        "ordernumber": "1-UnitTest",
        "orderdate": "",
        "ordersource": "",
        "ordertype": "",
        "orderpriority": "",
        "resellerid": "",
        "customerid": "C-1",
        "customername": "",
        "customermobile": "",
        "ordertakenby": "",
        "ordertakenby_username": "",
        "ordermeasuredby": "",
        "ordermeasuredby_shortname": "",
        "ordermeasure_date": "",
        "price_intl_amount": 0,
        "price_intl_currency": "",
        "price_local_amount": 0,
        "price_local_currency": "",
        "customernotes": "",
        "is_vip_order": False,
        "address_dl_contactperson": "",
        "address_dl1": "",
        "address_dl2": "",
        "address_dl3": "",
        "address_dl_city": "",
        "address_dl_state": "",
        "address_dl_country": "",
        "address_dl_pincode": "",
        "customer_emailid": "",
        "phoneno1": "",
        "address1": "",
        "address2": "",
        "address3": "",
        "address_city": "",
        "address_state": "",
        "address_country": "",
        "address_pincode": ""
        }

    global token    
    response = client.post("/api/reseller/order/new", headers={"Authorization": f"Bearer {token}"}, json=payload)

    assert response.status_code == 200
    # assert response.json()["orderid"] == 14
    assert response.json()["Success"] == "Row inserted"

def test_add_new_items():
    payload = {
        "orderid": 20,
        "ordernumber": "NO-01",
        "customerid": "C-30",
        "items": [
            {
            "productid": 12,
            "productshortname": "J",
            "quantity": 2
            },
            {
            "productid": 2,
            "productshortname": "P",
            "quantity": 2
            },
            {
            "productid": 8,
            "productshortname": "T",
            "quantity": 2
            }
        ]
    }

    resp = {
        "Success": "Added All Items",
        "barcodes": [
            "12-08-000020-01",
            "12-08-000020-02",
            "02-08-000020-03",
            "02-08-000020-04",
            "08-08-000020-05",
            "08-08-000020-06"
            ]
        }

    global token
    response = client.post("/api/reseller/items", headers={"Authorization": f"Bearer {token}"}, json = payload)

    assert response.status_code == 200
    assert response.json()["Success"] == "Added All Items"
    assert response.json()["barcodes"] == resp["barcodes"]