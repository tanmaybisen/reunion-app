### Make a Virtual Env using
python -m venv env

### Activate virtual env
source ./env/Scripts/activate

### Run app locally [stay in src folder]
uvicorn main:app --reload

### Build Docker Image
docker build -t reunion .

### Run Docker Image
docker run -p 8000:8000 reunion
