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
                finalData.append([startTime, tempData.loc[i,'end_time_s'], tempData.loc[i,'pitch_midi'],i])
            else:
                finalData.append([tempData.loc[i-1,'start_time_s'], tempData.loc[i, 'end_time_s'], tempData.loc[i, 'pitch_midi'],i])

            startTime=tempData.loc[i,'start_time_s']

            #delete both old rows after appending in finaldata

            print("new start time is")
            print(startTime)
        else:
            #finalData.append([tempData.loc[i,'start_time_s'], tempData.loc[i, 'end_time_s'], tempData.loc[i, 'pitch_midi'],420])
            print("loopfixer")

    #finalData.append([tempData.loc[i-1, 'start_time_s'], tempData.loc[i, 'end_time_s'], tempData.loc[i,'pitch_midi']])
    #finalData=finalData.reset_index()
    return(pd.DataFrame(finalData))


finalData=pd.DataFrame()


#call function and place results back into itself
finalData=pd.concat([finalData,getStartEnd(data,0.02)])
print("final results")
print(finalData)


#replace split notes from from original
"""
finalData.between(0,1).any()

patients_data_list = []

for patient_id, patient_df in gb_patient:
   patient_df = patient_df.sort_values(by=['Date', 'Time'])
   patient_data = {
       "patient_id": patient_id,
       "start_time": patient_df.Date.values[0] + patient_df.Time.values[0],
       "end_time": patient_df.Date.values[-1] + patient_df.Time.values[-1]
   }

   patients_data_list.append(patient_data)

new_df = pd.DataFrame(patients_data_list)

finalData = finalData.sort_values()
for i in finalData.index:
        other_start = df.loc[i, 'start_time_s']
        other_end = df.loc[i, 'end_time_s']
        if (start > other_start) & (start < other_end):
            overlaps += 1
"""
finalData.columns = ['start_time_s', 'end_time_s', 'pitch_midi', 'note_group']
finalData = finalData.sort_values(['start_time_s'],ascending=[False])

print(finalData)
"""
for f in range(1,len(finalData)):
    start = finalData.loc[f, 'start_time_s']
    end = finalData.loc[f, 'end_time_s']
    interval = pd.Interval(left=start, right=end)
    print(1 in interval)

    """
"""
def groupNotes(tempData):
    #tempData = tempData.reset_index()
    print(tempData)
    for f in range(0,len(tempData)):
        #start = tempData.loc[[f+1], ['start_time_s']]
        print(start)
        #end = tempData.loc[f+1, 'end_time_s']

        #interval = pd.Interval(left=start, right=end)
        #nextstartval = finalData.loc[f, 'start_time_s']
        #print(nextstartval)
        #if nextstartval in interval == True:
        #    print ("index ")

    return(pd.DataFrame(tempData))

finalData=groupNotes(finalData)
"""