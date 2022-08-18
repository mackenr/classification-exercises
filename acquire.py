import os
from rcm_library import *
from sklearn.model_selection import train_test_split

######################### Titanic
#########################

def new_titanic_data():
    return pd.read_sql('SELECT * FROM passengers', get_db_url('titanic_db'))

#########################

def get_titanic_data():
    filename = "titanic.csv"
    
    # if file is available locally, read it
    if os.path.isfile(filename):
        return pd.read_csv(filename)
    
    # if file not available locally, acquire data from SQL database
    # and write it as csv locally for future use
    else:
        # read the SQL query into a dataframe
        df = new_titanic_data()
        
        # Write that dataframe to disk for later. Called "caching" the data for later.
        df.to_csv(filename)

        # Return the dataframe to the calling code

        return df  


######################### Iris
#########################



def new_iris_data():
    '''
    This function reads the iris data from the Codeup db into a df.
    '''
    sql_query = """
                SELECT 
                    *
                FROM measurements
                JOIN species USING(species_id)
                """
    
    # Read in DataFrame from Codeup db.
    df = pd.read_sql(sql_query, get_db_url('iris_db'))
    
    return df
#########################

def get_iris_data():
    '''
    This function reads in iris data from Codeup database, writes data to
    a csv file if a local file does not exist, and returns a df.
    '''
    if os.path.isfile('iris_df.csv'):
        
        # If csv file exists read in data from csv file.
        df = pd.read_csv('iris_df.csv', index_col=0)
        
    else:
        
        # Read fresh data from db into a DataFrame
        df = new_iris_data()
        
        # Cache data
        df.to_csv('iris_df.csv')
        
    return df

######################### Telco
#########################


def new_telco_data():
    '''
    This function reads the telco data from the Codeup db into a df.
    '''
    sql_query = """
                select * from customers
                join contract_types using (contract_type_id)
                join internet_service_types using (internet_service_type_id)
                join payment_types using (payment_type_id)
                """
    
    # Read in DataFrame from Codeup db.
    df = pd.read_sql(sql_query, get_db_url('telco_churn'))
    
    return df

def get_telco_data():
    '''
    This function reads in telco data from Codeup database, writes data to
    a csv file if a local file does not exist, and returns a df.
    '''
    if os.path.isfile('telco.csv'):
        
        # If csv file exists read in data from csv file.
        df = pd.read_csv('telco.csv', index_col=0)
        
    else:
        
        # Read fresh data from db into a DataFrame
        df = new_telco_data()
        
        # Cache data
        df.to_csv('telco.csv')
        
    return df



def uploaded_db_explore(df):
    obj_col = df.columns [df.dtypes == 'object']
    
    for col in obj_col:

        print('------------------------------')
        
        display(pd.DataFrame(df[col].describe(include='all')).T)
        display(pd.DataFrame(df[col].value_counts(dropna=False)).T)

        display(pd.DataFrame(df[col].value_counts(normalize=True, dropna=False)).T)
        print('------------------------------')
        

### Edit this one
def numerical_cols_viz(df):
    '''
    needs to be edited more
    
    
    '''

    num_col = df.select_dtypes(include='number').columns
    width=len(num_col)*3.25
    fig=plt.figure(figsize=(width,3))
    fig.subplots_adjust(hspace=2.5, wspace=1.5)
  
    for i,col in enumerate(num_col):
        ax = fig.add_subplot(int(f'1{len(num_col)}{i+1}'))
        ax.text(0.5, 0.5, str(int(f'1{len(num_col)}{i+1}')),
           fontsize=2, ha='center')
      
        plt.title(col),
        plt.hist(df[col])
        
    fig




def prep_iris(iris):
    iris=prep_data_frame(iris)
   
    return iris


def prep_titanic(titanic):
    titanic=prep_data_frame(titanic)
   
    return titanic


def prep_telco(telco):
    telco=prep_data_frame(telco)
   
    return telco
    




def split_data(df,tostratify=None, test_size=.2,validate_size=.25):
    '''
    Takes in a dataframe and return train, validate, test subset dataframes
    '''
    if tostratify!=None:
        train, test = train_test_split(df, test_size=test_size, 
                               random_state=123, stratify=df[tostratify])
        train, validate = train_test_split(train, test_size=validate_size, 
                 random_state=123, stratify=train[tostratify])
    else:
        train, test = train_test_split(df, test_size=test_size, 
                               random_state=123)
        train, validate = train_test_split(train, test_size=validate_size, 
                 random_state=123)
    # df=pd.DataFrame([{['Prepared Data',,,,,,,]:df.shape},{'Train':train.shape},{'Validate':validate.shape},{'Test':test.shape}])
    df=pd.DataFrame([df.shape,train.shape,validate.shape,test.shape],index=['Prepared Data','Train','Validate','Test'],columns=['Length','Width'])
    display(df)
    return train, validate, test
    

   

    