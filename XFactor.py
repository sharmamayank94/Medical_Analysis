import mysql.connector
import pandas as pd
from datetime import timedelta
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

db = mysql.connector.connect(host="localhost", database="medical", user="root", passwd = "test")

dbcursor = db.cursor()
dbcursor.execute("Select Medicine_name, date, sum(bill_quantity) from bill where Medicine_name = 'Chlorpheniramine' group by date ")
myresult = dbcursor.fetchall()


regressor = LinearRegression()


df = pd.DataFrame(myresult)


#df2 = pd.DataFrame()
#df2['date'] = pd.date_range(start = '3/1/2020', periods=35, freq='D')

firstdate = df[1][0]
lastdate = df[1][len(df)-1]
while firstdate<lastdate:
    
    firstdate = firstdate + timedelta(days = 1)
    
    if firstdate in df[1].values:
        pass
    else:
        df=df.append({0: 'Chlorpheniramine', 1:firstdate, 2:0}, ignore_index=True)
  
df = df.sort_values(1)
#df=df.iloc[-4:, 1:3]
print(df[1:10][0:])
x = pd.to_datetime(df[1])
print(x.values.reshape(-1,1))
print(df[1].values.reshape(-1,1))

regressor.fit(x.values.reshape(-1,1), df[2])
plt.figure(figsize=(15,6))
plt.bar(df[1], df[2])
plt.plot(x.values.reshape(-1,1), regressor.predict(x.values.astype(float).reshape(-1,1)))
plt.xticks(df[1], rotation='80')
x_pred = np.asarray(['2021-07-30'])
x_pred = pd.to_datetime(x_pred)
print(regressor.predict(x_pred.values.astype(float).reshape(-1,1)))
#fig=plt.figure(figsize=(12,6))
#axes= fig.add_axes([1,1,0.5,0.8]) 

#axes.bar(df[1], df[2])


#plt.show()


