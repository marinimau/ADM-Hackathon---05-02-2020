import psycopg2

connection = None
cursor = None

class AnalysisUI:

    def run_all(self):
        try:
            self.init_connection()
        except:
            print("Not able to connection")
            return self.handle_close()
        finally:
            while 1:
                self.start()
                input=self.detect_input()
                self.handle_input(input)
                pass
        return


    def init_connection(self):
        global connection
        global cursor
        connection = psycopg2.connect("dbname=visa user=postgres host='localhost' port='5431' password=postgres")
        cursor = connection.cursor()
        return


    def close_connection(self):
        global connection
        global cursor
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
        return

    def start(self):
        print("-----------------------------------------------------------\n")
        print("|                     VISA ANALYST                        |\n")
        print("-----------------------------------------------------------\n")
        print("Please select a query:\n")
        print("a) purchases volume last 15 minutes (splitted by shop category)\n")
        print("b) category of most expensive purchase (last 30 minutes)\n")
        print("c) purchases density for km^2 (splitted by neighbourhood)\n")
        print("write 'quit' to close")
        return

    def detect_input(self):
        return (raw_input()).lower()

    def handle_input(self, input):
        if input == 'a':
            self.handle_a()
        elif input == 'b':
            self.handle_b()
        elif input == 'c':
            self.handle_c()
        elif input == 'quit':
            self.handle_close()
        else:
            self.error()

    def error(self):
        print("Please, give a valid input\n")
        return

    def handle_close(self):
        self.close_connection()
        raise SystemExit(0)

    def handle_a(self):
        a_query = "SELECT count(p.*) AS quanity, SUM(p.price) AS amount, p.s_category FROM visa.nyc_purchases p WHERE p.p_time >= current_timestamp - interval '15 minutes' GROUP BY s_category;"
        try:
            global cursor
            cursor.execute(a_query)
            records = cursor.fetchall()

            print("Results\n")

            for row in records:
                 print("-----------------------------------------------------------\n")
                 print("Quantity: ", row[0], )
                 print("Total: ", row[1])
                 print("Shop Category: ", row[2])
                 print("-----------------------------------------------------------\n")
        except (Exception, psycopg2.Error) as error :
            print ("Fetching error", error)
        return

    def handle_b(self):
        b_query = "SELECT p.s_category FROM visa.nyc_purchases p WHERE p.p_time >= current_timestamp - interval '30 minutes' AND ST_DWithin(p.s_coords, (SELECT geom FROM visa.nyc_subway_stations s WHERE s.name = 'Broad St'), 500) AND p.price >= ALL (SELECT price FROM visa.nyc_purchases p1 WHERE p1.p_time >= current_timestamp - interval '30 minutes' AND ST_DWithin(p1.s_coords, (SELECT geom FROM visa.nyc_subway_stations s WHERE s.name = 'Broad St'), 500));"
        try:
            global cursor
            cursor.execute(b_query)
            records = cursor.fetchall()

            print("Results\n")

            for row in records:
                 print("-----------------------------------------------------------\n")
                 print("Shop Category: ", row[0])
                 print("-----------------------------------------------------------\n")
        except (Exception, psycopg2.Error) as error :
            print ("Fetching error", error)
        return

    def handle_c(self):
        c_query = "SELECT count(p)/(ST_Area(Geography(ST_Transform(n.geom,4326)))/1000000.0), n.name as purchases_for_km FROM visa.nyc_neighborhoods n JOIN visa.nyc_purchases p ON ST_Intersects(p.s_coords, Geography(ST_Transform(n.geom,4326))) WHERE p.p_time >= current_timestamp - interval '15 minutes' GROUP BY n.id, n.geom;"
        try:
            global cursor
            cursor.execute(c_query)
            records = cursor.fetchall()
            print("Results\n")
            for row in records:
                 print("-----------------------------------------------------------\n")
                 print("Neighboorhood name: ", row[1])
                 print("Purchases density for km (groupped by neighbourhood): ", row[0], )
                 print("-----------------------------------------------------------\n")
        except (Exception, psycopg2.Error) as error :
            print ("Fetching error", error)
        return


ui_instance = AnalysisUI()
ui_instance.run_all()
