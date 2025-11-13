from sqlalchemy.testing.suite.test_reflection import users

allocation = 0 #### make a col in the databas
def weight_algo(weight):
    if weight == 1:
        allocation = 1/21;
    elif weight == 2:
        allocation = 2/21;
    elif weight == 3:
        allocation = 3/21;
    elif weight == 4:
        allocation = 4/21;
    elif weight == 5:
        allocation = 5/21;
    elif weight == 6:
        allocation = 6/21;

def time_algo( ):
    time = session.get('duration')    # take the time form teh dataset
    return allocation *

