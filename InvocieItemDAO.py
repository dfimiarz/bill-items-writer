# Class tht handles the connection to the database

import mysql.connector

class InvoiceItemDAO:
    '''Class that handles the connection to the database'''
    
    # Constructor
    def __init__(self):
        # Create a connection to the database
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="bill_items"
        )

    def bulkInsert(self, bill_items):
        '''Inserts a bill item into the database'''
        # Create a cursor
        cursor = self.conn.cursor()

        # Create the SQL statement
        sql = "INSERT INTO core_invoice_item (id, status_id, created, invoice, pi, details, service_id, service_time, quantity, rate, note) VALUES (NULL, 1, now(), NULL, %s, %s, %s, %s, %s, %s, %s)"

        # Execute the SQL statement
        cursor.execute(sql, bill_items)

        # Commit the changes to the database
        self.conn.commit()

        # Close the cursor
        cursor.close()

    def close(self):
        '''Closes the connection to the database'''
        self.conn.close()