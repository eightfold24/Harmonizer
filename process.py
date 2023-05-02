import math
import pandas as pd



# read in csv and ignore pitch bend section
df = pd.read_csv('./pianoman_basic_pitch.csv', usecols=range(4))

# filtering out notes that are too quiet
df = df[df.velocity >= 55]

# sort results by pitch and by start time
df = df.sort_values(['pitch_midi', 'end_time_s'], ascending=[True, True])
print("sorted original data:")
print(df.to_string())

# create dataframe of notes that are identical and have less than 20ms release and reapply (most likely the same note)

data = df

# creating differential column for dataset
diffData = []
for i in range(1, len(data)):
    diffData.append((data.iloc[i, 0]) - (data.iloc[i - 1, 1]))

data['diff'] = [0] + diffData
print("data with appended diff column:")
print(data)


def getStartEnd(tempData, THRESHOLD):
    tempData = tempData.reset_index(drop=True)
    finalData = pd.DataFrame(columns=['start_time_s','end_time_s','pitch_midi','note_group', 'total_length'])
    startTime = tempData.loc[0, 'start_time_s']
    is_duplicates = True

    while is_duplicates:
        templength = len(tempData)
        tempData = tempData.reset_index(drop=True)
        print("tempData fed into note splicer:")
        print(tempData)

        for i in range(1, templength):
            if THRESHOLD > tempData.loc[i, 'diff'] >= 0 and (tempData.loc[i, 'pitch_midi'] == tempData.loc[i - 1, 'pitch_midi']):

                if i == 1:
                    #finalData.append([startTime, tempData.loc[i, 'end_time_s'], tempData.loc[i, 'pitch_midi'], i])
                    finalData.loc[i-1] = [startTime, tempData.loc[i, 'end_time_s'], tempData.loc[i, 'pitch_midi'], i,i]
                else:
                    #finalData.append([tempData.loc[i - 1, 'start_time_s'], tempData.loc[i, 'end_time_s'], tempData.loc[i, 'pitch_midi'],i])
                    finalData.loc[i-1] = [tempData.loc[i - 1, 'start_time_s'], tempData.loc[i, 'end_time_s'], tempData.loc[i, 'pitch_midi'],i,i]
                startTime = tempData.loc[i, 'start_time_s']

            else:
                #finalData.append([tempData.loc[i,'start_time_s'], tempData.loc[i, 'end_time_s'], tempData.loc[i, 'pitch_midi'],420])
                finalData.loc[i-1] = [tempData.loc[i,'start_time_s'], tempData.loc[i, 'end_time_s'], tempData.loc[i, 'pitch_midi'],420,i]

                # finalData.append([tempData.loc[i-1, 'start_time_s'], tempData.loc[i, 'end_time_s'], tempData.loc[i,'pitch_midi']])

        print("finaldata dump")
        print(finalData)
        output = pd.DataFrame.from_records(data)

        finalData = finalData.drop_duplicates(subset='start_time_s', keep="last")
        print("final data from splicing notes(output):")
        print(finalData)
        is_duplicates = finalData.duplicated(subset=['start_time_s']).any()
        print(is_duplicates)
        tempData = finalData

    return finalData
    #return pd.DataFrame(finalData)


finalData = pd.DataFrame()

# call function and place results back into itself
#finalData = pd.concat([finalData, getStartEnd(data, 0.02)])
finalData = getStartEnd(data, 0.02)

#finalData.columns = ['start_time_s', 'end_time_s', 'pitch_midi', 'note_group']
finalData = finalData.sort_values(['start_time_s'])
# finalData = finalData.sort_values(['start_time_s'], ascending=[True])

print("final data without repeats is:")
print(finalData)


def groupNotes(tempdata):
    notegroup = 1
    tempdata = tempdata.reset_index(drop=True)
    nextstart = 0
    indexcount = tempdata.index.size - 1

    print("tempData fed into note grouper:")
    print(tempdata)

    for i in tempdata.index:
        start = tempdata.loc[i, 'start_time_s']
        end = tempdata.loc[i, 'end_time_s']
        interval = pd.Interval(left=start, right=end, closed='both')

        if i != indexcount:
            nextstart = tempdata.loc[i + 1, 'start_time_s']

            if i == 0:
                tempdata.loc[i, 'note_group'] = notegroup


            if nextstart in interval:
                tempdata.loc[i+1, 'note_group'] = notegroup

            else:
                notegroup = notegroup + 1
                tempdata.loc[i+1, 'note_group'] = notegroup

        else:
            print("reached last note")

    return pd.DataFrame(tempdata)


groupeddata = pd.DataFrame()
groupeddata = groupNotes(finalData)
groupeddata['pitch_midi'] = groupeddata['pitch_midi'].astype('int')
groupeddata['note_group'] = groupeddata['note_group'].astype('int')
print(groupeddata)


# replace split notes from original

# get mean of each note group

def noteEncoding(tempdata):
    loopdf = pd.DataFrame(tempdata, columns=['start_time_s','end_time_s','pitch_midi','note_group', 'total_length','direction'])
    finaldata = pd.DataFrame(columns=['start_time_s','end_time_s','avg_pitch_midi','note_group', 'total_length','direction'])
    print("loopdf:", loopdf)
    print("started encoding to harmonica notation")

    notesum = tempdata['note_group'].iloc[-1]

    blowmap = pd.read_csv('./blowencode.csv')
    drawmap = pd.read_csv('./drawencode.csv')
    print("mapping frame is")
    print(blowmap)
    noteval = 77
    idx = blowmap['note_avg'].sub(noteval).abs().idxmin()
    df1 = pd.DataFrame(columns=['actual_note'])
    df1 = blowmap.loc[[idx],'actual_note']
    print(df1)

    for i in range(1, notesum+1):
        loopdf = pd.DataFrame(tempdata, columns=['start_time_s','end_time_s','pitch_midi','note_group', 'total_length', 'direction'])
        loopdf = loopdf.loc[loopdf['note_group'] == i]
        notemean = loopdf['pitch_midi'].mean()
        starttime = loopdf['start_time_s'].min()
        endtime = loopdf['end_time_s'].max()
        totallength = endtime - starttime

        # if the notes in a note group are any possible blow value, set variable to true
        blow = loopdf['pitch_midi'].isin([60, 64, 67, 72, 76, 79, 84, 88, 91]).any()

        print("direction is:", blow)
        if blow:

            idx = blowmap['note_avg'].sub(notemean).abs().idxmin()

            df1 = blowmap.loc[[idx], 'actual_note']
            acval = df1.iloc[[0][0]]
            print("acval is:", acval)
            #print(df1)
        else:
            idx = drawmap['note_avg'].sub(notemean).abs().idxmin()

            df1 = drawmap.loc[[idx], 'actual_note']
            acval = df1.iloc[[0][0]]
            print("acval is:",acval)
            #print(df1)

        print("notemean:",notemean,"start time:",starttime, "end time:", endtime,"note length:",totallength,"blow:",blow)
        list_row = [starttime, endtime, acval, int(i), totallength, blow]
        finaldata.loc[len(finaldata)] = list_row
        print(finaldata)



    finaldata.reset_index(drop=True)
    return finaldata

print("data to be passed into the frontend:")
print(noteEncoding(groupeddata))
