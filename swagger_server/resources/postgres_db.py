import psycopg2, json
from psycopg2 import sql
from swagger_server.config.access import access
from swagger_server.utils.logging import log as logging

from swagger_server.encoder import info_encoder

class PostgresClient:

    def __init__(self):
        credendiatls_db = PostgresClient.get_credentials()
        self.log = logging()
        self.username = credendiatls_db["USER"]
        self.password = credendiatls_db["PASSWORD"]
        self.host = credendiatls_db["HOST"]
        self.db_name = credendiatls_db["DB_NAME"]
        self.cursor = None

    def __enter__(self):
        self.log.info("Inicio de conexión")
        self.connect()
        return self
        

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.log.info("Fin de conexión")
        self.disconnect()

    def connect(self):
        self.connection = psycopg2.connect(
            host=self.host,
            user=self.username,
            password=self.password,
            database=self.db_name
        )
        self.connection.set_session(autocommit=False, readonly=False, deferrable=False)
        self.cursor = self.connection.cursor()

    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    # CONSULTAR DATOS
    def execute_query(self, query):
        try:
            # ejecutar el query
            self.cursor.execute(query)
            # obtine elos valores de la repsuesta de la consulta
            rows = self.cursor.fetchall()

            # obtener nombre de columnas        
            column_names = [desc[0] for desc in self.cursor.description]

            # registros que se consultaron
            result = []
            if len(rows) > 0:
                for row in rows:
                    row_dict = dict(zip(column_names, row))
                    result.append(row_dict)
                
                # comprabar el formato a recibir el objeto
                result_json = json.dumps(result, default=info_encoder)
                result_dict = json.loads(result_json)
                return result_dict
            else:
                return None
        except(psycopg2.Error, Exception) as error:
            self.log.critical(str(error))
            raise ValueError(str(error))

    # INSERCION DE DATOS
    def execute_insert(self, table, values):
        try:
            # sacar los nombre de las columnas a insertas
            columns = ','.join(values.keys())
            # valor %s por cantidad de columnas
            placeholders  = ','.join(['%s'] * len(values))
            # query que se va a ejecutar 
            query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders}) RETURNING*"
            # ejecuta el query
            self.cursor.execute(query, list(values.values()))
            #Obtenemos el registro insertado
            inserted_row = self.cursor.fetchone()

            # obtenemos el nombre de cabecera de las columnas
            column_names = [desc[0] for desc in self.cursor.description]
            # realizamos un zip de el nombre de las collumnas con los valores obtenidos de la insercion
            # como resultado tendremos un diccionario
            inserted_dict = dict(zip(column_names, inserted_row))
            # realizamos un forat al diccionario
            task_json = json.dumps(inserted_dict, default=info_encoder)
            task_dict = json.loads(task_json)
            #realizamos le commit a la base de datos
            self.connection.commit()
            return task_dict
        except(psycopg2.Error, Exception) as error:
            self.log.critical(str(error))
            raise ValueError(str(error))
        
    # ELIMINACION DE DATOS
    def execute_delete(self, table, condition):
        try:
            # query que se va a ejecutar
            query = f"DELETE FROM {table} WHERE {condition}"
            # ejecucion del query
            self.cursor.execute(query)
            # el commit d ela trasanccion
            self.connection.commit()
            return True
        except(psycopg2.Error, Exception) as error:
            self.log.critical(str(error))
            raise ValueError(str(error))
        
    # funcion para actualizar registros
    def execute_update(self, table, values, condition):
        try:
            # description = "hola"
            # name = "nombre"
            # description = 'hola', name = 'nombre'
            set_values = ', '.join([f"{key} = %s" for key in values.keys()])
            query = f"UPDATE {table} SET {set_values} WHERE {condition} RETURNING*"
            self.cursor.execute(query, list(values.values()))
            updated_row = self.cursor.fetchone()

            column_names = [desc[0] for desc in self.cursor.description]
            updated_dict = dict(zip(column_names, updated_row))
            task_json = json.dumps(updated_dict, default=info_encoder)
            task_dict = json.loads(task_json)
            self.connection.commit()
            return task_dict
        except(psycopg2.Error, Exception) as error:
            self.log.critical(str(error))
            raise ValueError(str(error))
        
    def execute_query_paginated(self, query, page=None, size=None):
        try:
            if page is not None and size is not None:
                offset = (page - 1 ) * size
                query = sql.SQL("{} OFFSET {} LIMIT {}").format(sql.SQL(query), sql.Literal(offset), sql.Literal(size))
            
            self.cursor.execute(query)
            rows = self.cursor.fetchall()

            column_names = [desc[0] for desc in self.cursor.description]
            
             # registros que se consultaron
            result = []
            if len(rows) > 0:
                for row in rows:
                    row_dict = dict(zip(column_names, row))
                    result.append(row_dict)
                
                # comprabar el formato a recibir el objeto
                result_json = json.dumps(result, default=info_encoder)
                result_dict = json.loads(result_json)
                return result_dict
            else:
                return None
        except(psycopg2.Error, Exception) as error:
            self.log.critical(str(error))
            raise ValueError(str(error))

    @staticmethod
    def get_credentials():
        response_json = access()
        credentials_db = response_json["DB"]["POSTGRES"]["TASK"]
        response = {
            "HOST": credentials_db["HOST"],
            "DB_NAME": credentials_db["DB_NAME"],
            "USER": credentials_db["USER"],
            "PASSWORD": credentials_db["PASSWORD"]
        }
        return response
