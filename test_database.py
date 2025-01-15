# test if the sqlite db connection works fine 
from database import engine, metadata

def test_database():
    try:
        #create all tables
        metadata.create_all(engine)
        print("Database connection successful. Tables created.")
    except Exception as e:
        print(f"An error occured: {e}")

if __name__ == "__main__":
    test_database()

#This is a test file
# test if the db connection works fine 
#Type in CLI : % python test_database()