import mftool as mf
from models import *
import dbconnection
from dbconnection import session_scope
import datetime
import time

print('Initializing Database connection')
dbconnection.DBSession.initdsn("postgres:postgresspass@0.0.0.0:5432/app")

#get all scheme codes
def save_all_scheme_codes():
    mftool = mf.Mftool
    all_schemes_codes = mftool.get_scheme_codes()
    rows=[]
    print('Downloaded ' + len(all_schemes_codes), 'scheme codes')
    for scheme_codes in all_schemes_codes:
        try:
            scheme_code =  create_scheme_code(scheme_codes)
            rows.append(scheme_code)
        except Exception as ex:  
            print (scheme_codes)     
            print (ex)
    for row in rows:
        save_to_database_bulk([row], 5000)

#get daily NAV for all scheme codes
def save_nav_data_daily():
    mftool = mf.Mftool()
    all_schemes_nav = mftool.get_all_scheme_quote() # getting all scheme codes
    
    rows = []
    print('Downloaded ', len(all_schemes_nav), 'scheme codes')
    for data in all_schemes_nav:       
        try:
            data['last_updated'] = datetime.datetime.strptime(data['last_updated'], '%d-%b-%Y')
            nav = create_nav(data)
            rows.append(nav)
        except Exception as ex:  
            print (data)         
            print (ex)
    for row in rows:
        save_to_database_bulk([row], 1)

#get all schemes related information
def save_all_schemes():
    mftool = mf.Mftool()
    scheme_codes = mftool.get_scheme_codes() #get all scheme codes
    
    for scheme_code, scheme_name in scheme_codes.items():
        scheme_details = mftool.get_scheme_details(scheme_code)  #get scheme details for scheme code      
        rows = []
        print('Downloading data for ', scheme_name)
        try:
            scheme_detail = create_scheme_details(scheme_details)
            #print(scheme_details)
            #new_row['scheme_start_date'] = scheme_details['scheme_start_date']
            #new_row['scheme_category'] = scheme_details['scheme_category']
            #new_row['scheme_code'] = scheme_details['scheme_code']
            #new_row['scheme_name'] = scheme_details['scheme_name']
            #new_row['scheme_type'] = scheme_details['scheme_type']
            #new_row['fund_house'] = scheme_details['fund_house']
            rows.append(scheme_detail)        
        except Exception as ex:
            print (scheme_code, scheme_name)         
            print (ex)
        for row in rows:
            save_to_database_bulk([row], 5000)

#get all historical data
def save_nav_data_historical():
    mftool = mf.Mftool()
    schemes = mftool.get_scheme_codes()

    for scheme_code, scheme_name in sorted(schemes.items(), key= lambda x:x[0].lower(), reverse=True):

        print('Downloading data for ', scheme_name)
        historical_data = mftool.get_scheme_historical_nav(scheme_code)
        
        rows = []
        for data in historical_data['data']:
            if historical_data['scheme_code'] is not None and historical_data['scheme_name'] is not None and data['nav'] is not None :
                try:
                    print(data['date'])
                    new_row = {}
                    new_row['scheme_code'] = historical_data['scheme_code']
                    new_row['scheme_name']= historical_data['scheme_name']
                    new_row['last_updated']= datetime.datetime.strptime(data['date'], '%d-%m-%Y')
                    new_row['nav'] = float(data['nav'])
                    rows.append(create_nav(new_row))
                except Exception as ex:
                    print (data)         
                    print (ex)
        
        save_to_database_bulk(rows, 3000)
        print('Sleeping for 10 seconds')
        time.sleep(0)


#data builder 
def create_nav(data):
    nav = NAV()
    nav.scheme_code = int(data['scheme_code'])
    nav.scheme_name = data['scheme_name']
    nav.last_updated = data['last_updated']
    nav.nav = float(data['nav'])
    nav.created_date = datetime.datetime.now()   
    return nav

# data builder
def create_scheme_details(data):
    scheme_details = SCHEME_DETAILS()
    scheme_start_date_value = data['scheme_start_date']
    print("Scheme start data value is=>" + scheme_start_date_value["date"] + scheme_start_date_value["nav"])
    scheme_details.scheme_start_date = datetime.datetime.strptime(scheme_start_date_value["date"], '%d-%m-%Y')
    scheme_details.scheme_start_date_nav = scheme_start_date_value["nav"]
    scheme_details.scheme_category = data['scheme_category']
    scheme_details.scheme_code = int(data['scheme_code'])
    scheme_details.scheme_name = data['scheme_name']
    scheme_details.scheme_type = data['scheme_type']
    scheme_details.fund_house = data['fund_house']
    return scheme_details

#data builder to write to db
def create_scheme_code(data):
    scheme_codes = SCHEME_CODES()
    scheme_codes.scheme_code = int(data['scheme_code'])
    scheme_codes.created_date = datetime.datetime.now()
    return scheme_codes

#write in db
def save_to_database_bulk(rows, batch_size):
    
    with session_scope() as session:
        try:
            for i in range(0, len(rows), batch_size):
                session.add_all(rows)                 
                session.flush()
                session.bulk_save_objects(rows[i:i+batch_size])
                session.commit()
                
                print('Committed from ', i , ' to', min(i + batch_size, len(rows)))
        except Exception as ex:
            print('Failed to commit data from index', i, 'to index', i + batch_size, ex)
            session.rollback()

#call these actions as per need
print('Started')
if __name__ == "__main__":

    #save_nav_data_daily()
    #save_nav_data_historical()
    #save_all_schemes()
    #save_all_scheme_codes()