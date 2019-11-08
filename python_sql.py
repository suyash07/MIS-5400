import pyodbc

server = 'MSI'
database = 'suyash'
cnxn = pyodbc.connect(
    'DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + database,
    autocommit=True)
cursor = cnxn.cursor()

cursor.execute(
    '''
create table ScorePerGame(
    Player varchar(50),
Pos varchar(50),
Age int,
Tm varchar(50),
G int,
GS int,
MP decimal(10,3),
FG decimal(10,3),
FGA decimal(10,3),
FG_PERCENT decimal(10,3),
tHREE_P decimal(10,3),
THREE_PA decimal(10,3),
THREE_P_PERCENT decimal(10,3),
TWO_P decimal(10,3),
TWO_PA decimal(10,3),
TWO_P_PERCENT decimal(10,3),
eFG_PERCENT decimal(10,3),
FT decimal(10,3),
FTA decimal(10,3),
FT_PERCENT decimal(10,3),
ORB decimal(10,3),
DRB decimal(10,3),
TRB decimal(10,3),
AST decimal(10,3),
STL decimal(10,3),
BLK decimal(10,3),
TOV decimal(10,3),
PF decimal(10,3),
PTS decimal(10,3)
    )

    '''
)

bulk_insert_sql = """
    bulk insert ScorePerGame
    from 'C:/Users/Suyash/Desktop/MIS-5400/export_data_pergame.csv' with (
    FIELDTERMINATOR = ',',
    ROWTERMINATOR='\n'
    );
"""

cursor.execute(bulk_insert_sql)
cnxn.commit()
cursor.close()
cnxn.close()
