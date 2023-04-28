import math
import pandas as pd

df = pd.read_csv('./545blow_basic_pitch.csv', usecols=range(4))
print("original dataset")
print(df.to_string())

#filtering out notes that are too quiet
df = df[df.velocity >= 55]

#sort results by pitch and by start time
df = df.sort_values(['pitch_midi', 'end_time_s'],ascending=[True,True])
print("sorted results of dataframe")
print(df.to_string())

##create dataframe of notes that are identical and have less than 20ms release and reapply (most likely the same note)
#temp data converter
data=df

#creating differential column for dataset
diffData=[]
for i in range(1, len(data)):
    diffData.append((data.iloc[i,0]) - (data.iloc[i-1,1]))

data['diff']=[0] + diffData
print
print(data)


def getStartEnd(tempData,THRESHOLD):
    tempData=tempData.reset_index()
    finalData=[]
    startTime=tempData.loc[0,'start_time_s']
    print(tempData.loc[0,'start_time_s'])

    print("tempData:")
    print(tempData)

    for i in range(1,len(tempData)):
        if THRESHOLD > tempData.loc[i, 'diff'] >= 0 and (tempData.loc[i, 'pitch_midi'] == tempData.loc[i - 1, 'pitch_midi']):

            if i == 1:
                finalData.append([startTime, tempData.loc[i,'end_time_s'], tempData.loc[i,'pitch_midi']])
                tempData = tempdata
            else:
                finalData.append([tempData.loc[i-1,'start_time_s'], tempData.loc[i, 'end_time_s'], tempData.loc[i, 'pitch_midi']])
            startTime=tempData.loc[i,'start_time_s']



            #delete both old rows after appending in finaldata



    return(pd.DataFrame(finalData))


finalData=pd.DataFrame()

print("finalData:")
print(finalData)

print("tempData:")
print(tempData)

#call function and place results back into itself
finalData=pd.concat([finalData,getStartEnd(data,0.02)])
print("final results")
print(finalData)


#replace split notes from from original
