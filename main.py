from server import app
from insert_data import insert_data
from config import port_number

if __name__ == '__main__':
    insert_data()
    app.run(port=port_number)