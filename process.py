import math
import pandas as pd

df = pd.read_csv('./545blow_basic_pitch.csv', usecols=range(4))

print(df.to_string())

df = df[df.velocity >= 55]




df = df.sort_values(['pitch_midi', 'end_time_s'],ascending=[True,True])

print(df.to_string())




print(math.isclose(0.626938776, 0.638548753, abs_tol = 0.02))

new_df = df[df['start_time_s'].isin(df['end_time_s'].values)]

print(new_df.to_string())

#cols = ['start_time_s', 'end_time_s']
#index = 3
#df2 = df[(df[cols]==df.loc[index, cols]).all(1)]


#df2 = df[df.duplicated(keep=False)]
#print(df2)





#for x in df.index:
#    if df[]
#  print(x)

data=df

diffData=[]
for i in range(1, len(data)):
    diffData.append((data.iloc[i,0]) - (data.iloc[i-1,1]))

#print(diffData)

data['diff']=[0] + diffData
print(data)

print("testing loc")


def getStartEnd(tempData,THRESHOLD):
    tempData=tempData.reset_index()
    finalData=[]
    startTime=tempData.loc[0,'start_time_s']
    for i in range(1,len(tempData)):
        if tempData.loc[i,'diff'] < THRESHOLD and tempData.loc[i,'diff'] >= 0 and (tempData.loc[i,'pitch_midi'] == tempData.loc[i-1,'pitch_midi']):
            finalData.append([startTime,tempData.loc[i-1,'end_time_s'], [tempData.loc[i,'pitch_midi']]])
            startTime=tempData.loc[i,'start_time_s']
    #finalData.append([startTime,tempData.loc[i,'end_time_s'],[tempData.loc[i,'pitch_midi']]])
    return(pd.DataFrame([finalData]))

finalData=pd.DataFrame(columns=['start_time_s','end_time_s','pitch_midi'])
for user in data['pitch_midi']:
    finalData=pd.concat([finalData,getStartEnd(data,0.02)])

print(finalData)
