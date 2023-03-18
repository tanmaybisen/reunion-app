from sqlalchemy import create_engine, text, exc
from sqlalchemy.orm import sessionmaker

try:
    engine = create_engine('postgresql://zsfgynmh:6EGr32EPrRS2Br130ZiYpmZAfGGtjX4v@mel.db.elephantsql.com/zsfgynmh', pool_size=3, max_overflow=1)
    session = sessionmaker(autocommit=False, autoflush=False, bind = engine)
except exc.SQLAlchemyError:
    # import warnings
    # warnings.warn("SQL Connection Failed")
    print('SQL Connection Failed')