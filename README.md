## VG Samsurin Reseller - Transaction Screens

### Make a Virtual Env using
python -m venv env

### Activate virtual env
source ./env/Scripts/activate

### Run app locally [stay in src folder]
uvicorn main:app --reload

### Build Docker Image
docker build -t reseller_1 .

### Run Docker Image
docker run -p 8000:8000 reseller_1

### Authentication
The JWT token is sent for correct username and password of reseller.
The token expires after 12 hours from the time of generation.
The PyJWT Library is used, and bearer and handlers are responsible for signing and decoding tokens.

### AutoFormatting Query-InsertVars-UpdateVars-Arguments
<!-- for i in p:
    # print('\"',i,'\" : ','\"\",',sep='')
    # print(':',i,', \\',sep="")
    # print(i,' = ','EXCLUDED.',i,', \\',sep="")
    # print('\"',i,'\" : fabric.',i,',',sep="") -->