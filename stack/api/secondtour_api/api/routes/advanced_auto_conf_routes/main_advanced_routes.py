from datetime import datetime
from http.client import HTTPException
import logging
from sqlite3 import ProgrammingError
import traceback
from typing import Optional, List, Dict
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
import mysql.connector
from pydantic import BaseModel, Field
import os

from security import main_security

router = APIRouter()

from database.config import db

sensible_tables = os.getenv('SENSIBLE_TABLES').split(",")

'''OBJECTS IN'''

class User(BaseModel):
    username: str = Field(None, title='Username')
    password: str = Field(None, title='Password')
    class Config:
        schema_extra = {
            "example": {
                "username": "Admin",
                "password": "AdminPassword",
            }
        }
    
class UserContentTableName(BaseModel):
    username: str = Field(None, title='Username')
    password: str = Field(None, title='Password')
    content: dict = Field({}, title='Name of all the table you want to retreive')
    class Config:
        schema_extra = {
            "example": {
                "username": "Admin",
                "password": "AdminPassword",
                "content": {
                    "creneau": "",
                    "salle": "",
                    "liste_matiere": ""
                }
            }
        }
    
class UserContentTableDescription(BaseModel):
    username: str = Field(None, title='Username')
    password: str = Field(None, title='Password')
    content: dict = Field({}, title='The necessary elements to insert a row')
    class Config:
        schema_extra = {
            "example": {
                "username": "Admin",
                "password": "AdminPassword",
                "content": {
                    "numero": "D002"
                }
            }
        }
        
class UserContentTableDescriptionFull(BaseModel):
    username: str = Field(None, title='Username')
    password: str = Field(None, title='Password')
    content: dict = Field({}, title='The necessary elements to insert a row')
    class Config:
        schema_extra = {
            "example": {
                "username": "Admin",
                "password": "AdminPassword",
                "content": {
                    "id_salle": "null",
                    "numero": "D002"
                }
            }
        }
        
class UserContentUpdate(BaseModel):
    username: str = Field(None, title='Username')
    password: str = Field(None, title='Password')
    content: dict = Field({}, title='The necessary elements to insert a row')
    class Config:
        schema_extra = {
            "example": {
                "username": "Admin",
                "password": "AdminPassword",
                "content": {
                    "filter": {
                        "id_salle": "1"
                    },
                    "data": {
                        "numero": "D002"
                    }
                }
            }
        }
        
        
'''OBJECTS OUT'''
class fetchOut(BaseModel):
    rows_list: List[Dict] = [{
        "id_salle": 1,
        "numero": "D001"
    },
    {
        "id_salle": 2,
        "numero": "D002"
    }]

class fetchFilterOut(BaseModel):
    rows_list: List[Dict] = [{
        "id_salle": 2,
        "numero": "D002"
    }]

class fetchMultiOut(BaseModel):
    tables_list: List[List] = [
        [],
        [{
            "id_salle": 1,
            "numero": "D001"
        },
        {
            "id_salle": 2,
            "numero": "D002"
        }],
        [{
            "id_liste_matiere": 1,
            "id_professeur": 1,
            "id_matiere": 1
        }]
    ]

class returnId(BaseModel):
    id: int = 1


@router.post("/fetch/{table}", status_code=200, response_model=fetchOut)
def get_table(table: str, user: User, row_id: Optional[int] = None):
    if not main_security.test_connection(user):
        logging.warning(f"Incorrect username or password, {user}")
        output = JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'error': "Incorrect identifiers"})
    elif table in (item.lower() for item in sensible_tables):
        logging.warning(f"This table cannot be accessed due to his privacy policy, {table}")
        output = JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED ,content={'error': "This table cannot be accessed due to his privacy settings"})
    else:
        try:
            logging.warning(f"get_table: table={table} id={row_id}")
            if not row_id:
                output = JSONResponse(status_code=status.HTTP_200_OK, content=db.query(f"SELECT * FROM {table};"))
            else:
                output = JSONResponse(status_code=status.HTTP_200_OK, content=db.query(f"SELECT * FROM {table} WHERE id_{table} = {row_id};"))
        except mysql.connector.errors.ProgrammingError:
            logging.warning(traceback.format_exc())
            output = JSONResponse(status_code=status.HTTP_404_NOT_FOUND ,content={'error': "Error while fetching data"})
        except Exception:
            logging.warning(traceback.format_exc())
            output = JSONResponse(status_code=status.HTTP_404_NOT_FOUND ,content={'error': traceback.format_exc()})
    return output

@router.post("/fetchfilter/{table}", status_code=200, response_model=fetchFilterOut)
def get_table_by_filter(table: str, user: UserContentTableDescription):
    if not main_security.test_connection(user):
        logging.warning(f"Incorrect username or password, {user}")
        output = JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'error': "Incorrect identifiers"})
    else:
        logging.warning(f"Selecting rows in {table}, rows informations : {user.content}")
        content = user.content
        keys = list(content.keys())
        values_brute = list(content.values())
        values = []
        for value in values_brute:
            values.append(value if value == "null" or str(value).isnumeric() or value == "true" or value == "false" else f"'{value}'")
        try:
            condition = ""
            for i in range(0, len(keys)):
                condition += keys[i] + " = " + str(values[i]) + " AND "
            content = db.query(f"SELECT * FROM {table} WHERE " + condition +" 1 = 1;")
            output = JSONResponse(status_code=status.HTTP_200_OK, content=content)
        except mysql.connector.errors.ProgrammingError:
            logging.warning(traceback.format_exc())
            output = JSONResponse(status_code=status.HTTP_404_NOT_FOUND ,content={'error': "Error while inserting data"})
        except Exception:
            logging.warning(traceback.format_exc())
            output = JSONResponse(status_code=status.HTTP_404_NOT_FOUND ,content={'error': traceback.format_exc()})
    return output


@router.post("/fetchmulti", status_code=200, response_model=fetchMultiOut)
def get_many_tables(user: UserContentTableName):
    if not main_security.test_connection(user):
        logging.warning(f"Incorrect username or password, {user}")
        output = JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'error': "Incorrect identifiers"})
    else:
        try:
            output = []
            for table in user.content:
                try:
                    logging.warning(f"get_table_multi: table={table}")
                    if table in (item.lower() for item in sensible_tables):
                        logging.warning(f"This table cannot be accessed due to his privacy policy, {table}")
                        output_in = {'error': "This table cannot be accessed due to his privacy settings"}
                    else:
                        output_in = db.query(f"SELECT * FROM {table};")
                except Exception:
                    output_in = {'error': traceback.format_exc()}
                output.append(output_in)
            output = JSONResponse(status_code=status.HTTP_200_OK ,content=output)
        except mysql.connector.errors.ProgrammingError:
            logging.warning(traceback.format_exc())
            output = JSONResponse(status_code=status.HTTP_404_NOT_FOUND ,content={'error': "Error while fetching data"})
        except Exception:
            logging.warning(traceback.format_exc())
            output = JSONResponse(status_code=status.HTTP_404_NOT_FOUND ,content={'error': traceback.format_exc()})
    return output

@router.post("/insert/{table}", status_code=201, response_model=returnId)
def insert_a_row(table: str, user: UserContentTableDescriptionFull):
    if not main_security.test_connection(user):
        logging.warning(f"Incorrect username or password, {user}")
        output = JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'error': "Incorrect identifiers"})
    else:
        logging.warning(f"Inserting row in {table}, row informations : {user.content}")
        content = user.content
        keys = ",".join(list(content.keys()))
        values_brute = list(content.values())
        values = []
        for value in values_brute:
            try:
                values.append("'"+datetime.strptime(value, "%a %b %d %H:%M:%S %Y").strftime('%Y-%m-%d %H:%M:%S')+"'")
            except Exception:
                values.append(str(value) if value == "null" or str(value).isnumeric() or value == "true" or value == "false" else f"'{value}'")
        values = ",".join(values)
        try:
            content = db.query(f"INSERT INTO {table} ({keys}) VALUES ({values});")
            output = JSONResponse(status_code=status.HTTP_201_CREATED, content=content)
        except mysql.connector.errors.ProgrammingError:
            logging.warning(traceback.format_exc())
            output = JSONResponse(status_code=status.HTTP_404_NOT_FOUND ,content={'error': "Error while inserting data"})
        except Exception:
            logging.warning(traceback.format_exc())
            output = JSONResponse(status_code=status.HTTP_404_NOT_FOUND ,content={'error': traceback.format_exc()})
    return output

@router.post("/delete/{table}", status_code=202, response_model=returnId)
def delete_row(table: str, user: User, row_id: Optional[int] = None):
    if not main_security.test_connection(user):
        logging.warning(f"Incorrect username or password, {user}")
        output = JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'error': "Incorrect identifiers"})
    else:
        try:
            logging.warning(f"delete_row: table={table} id={row_id}")
            if not row_id:
                output = JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=db.query(f"DELETE FROM {table};"))
            else:
                output = JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=db.query(f"DELETE FROM {table} WHERE id_{table} = {row_id};"))
        except mysql.connector.errors.ProgrammingError:
            logging.warning(traceback.format_exc())
            output = JSONResponse(status_code=status.HTTP_404_NOT_FOUND ,content={'error': "Error while fetching data"})
        except Exception:
            logging.warning(traceback.format_exc())
            output = JSONResponse(status_code=status.HTTP_404_NOT_FOUND ,content={'error': traceback.format_exc()})
    return output

@router.post("/deletefilter/{table}", status_code=200, response_model=returnId)
def delete_row(table: str, user: UserContentTableDescription):
    if not main_security.test_connection(user):
        logging.warning(f"Incorrect username or password, {user}")
        output = JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'error': "Incorrect identifiers"})
    else:
        logging.warning(f"Selecting rows in {table}, rows informations : {user.content}")
        content = user.content
        keys = list(content.keys())
        values_brute = list(content.values())
        values = []
        for value in values_brute:
            values.append(value if value == "null" or value.isnumeric() or value == "true" or value == "false" else f"'{value}'")
        try:
            condition = ""
            for i in range(0, len(keys)):
                condition += keys[i] + " = " + values[i] + " AND "
            content = db.query(f"DELETE FROM {table} WHERE " + condition +" 1 = 1;")
            output = JSONResponse(status_code=status.HTTP_200_OK, content=content)
        except mysql.connector.errors.ProgrammingError:
            logging.warning(traceback.format_exc())
            output = JSONResponse(status_code=status.HTTP_404_NOT_FOUND ,content={'error': "Error while deleting data"})
        except Exception:
            logging.warning(traceback.format_exc())
            output = JSONResponse(status_code=status.HTTP_404_NOT_FOUND ,content={'error': traceback.format_exc()})
    return output


@router.post("/deleteall", status_code=202, response_model=returnId)
def delete_all_the_database(user: User):
    if not main_security.test_connection(user):
        logging.warning(f"Incorrect username or password, {user}")
        output = JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'error': "Incorrect identifiers"})
    else:
        try:
            logging.warning(f"delete_all_the_database")
            tables = db.query(f"SHOW TABLES;")
            for table in tables:
                output = JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=db.query(f"DELETE FROM {list(table.values())[0]};"))
        except mysql.connector.errors.ProgrammingError:
            logging.warning(traceback.format_exc())
            output = JSONResponse(status_code=status.HTTP_404_NOT_FOUND ,content={'error': "Error while fetching data"})
        except Exception:
            logging.warning(traceback.format_exc())
            output = JSONResponse(status_code=status.HTTP_404_NOT_FOUND ,content={'error': traceback.format_exc()})
    return output

@router.post('/updatefilter/{table}', status_code=200, response_model=returnId)
def update_table_by_filter(table: str, user: UserContentUpdate):
    if not main_security.test_connection(user):
        logging.warning(f"Incorrect username or password, {user}")
        output = JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'error': "Incorrect identifiers"})
    else:
        logging.warning(f"Updating rows in {table}, rows informations : {user.content}")
        content = user.content
        data_content = content["data"]
        filter_content = content["filter"]
        keys = list(data_content.keys())
        values_brute = list(data_content.values())
        values = []
        for value in values_brute:
            values.append(value if value == "null" or value.isnumeric() or value == "true" or value == "false" else f"'{value}'")
        row_content = ""
        for i in range(len(keys)):
            if i != 0:
                row_content += " , "
            row_content += f"{keys[i]} = {values[i]}"
        try:
            condition = ""
            for i in range(0, len(list(filter_content.keys()))):
                if i != 0:
                    condition += " AND "
                condition += list(filter_content.keys())[i] + " = " + list(filter_content.values())[i]
            content = db.query(f"UPDATE {table} SET " + row_content + f" WHERE {condition};")
            output = JSONResponse(status_code=status.HTTP_200_OK, content=content)
        except mysql.connector.errors.ProgrammingError:
            logging.warning(traceback.format_exc())
            output = JSONResponse(status_code=status.HTTP_404_NOT_FOUND ,content={'error': "Error while inserting data"})
        except Exception:
            logging.warning(traceback.format_exc())
            output = JSONResponse(status_code=status.HTTP_404_NOT_FOUND ,content={'error': traceback.format_exc()})
    return output