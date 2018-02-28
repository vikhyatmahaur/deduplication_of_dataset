import numpy as np
import pandas as pd
from fuzzywuzzy import fuzz as f


#Reading the Dataset which is provided, Change the name of the file while opening
df = pd.read_csv('Duplication1.csv')

# Returns the indeces of duplicate databases

def return_same(array, index_list):
    '''
    Input: Each group(date of birth and the gender) formed by a unique first name, last name as a key combination.
    Output: Provides with the list of indeces where the data containes is same.
    '''
    Similar_index_list = []
    visited = [0]*len(array)
    for i in range(len(array)):
        temp = []
        condition = False
        x = array[i]
        if(visited[i]==0):
            condition = True
            visited[i] = 1
            dob_x = x[0].split(' ')
            gn_x = x[1].split(' ')
            temp.append(index_list[i])
            for j in range(len(array)):
                y = array[j]
                if(visited[j] == 0):
                    dob_y = y[0].split(' ')
                    gn_y = y[1].split(' ')
                    if(f.ratio(dob_x[0],dob_y[0])>70
                       and (f.ratio(gn_x[0],gn_y[0])>70)
                       and (f.ratio(x[0]+' '+x[1], y[0]+' '+y[1])>80)):
                        temp.append(index_list[j])
                        visited[j] = 1
        if(condition):
            Similar_index_list.append(temp)
    return Similar_index_list


#Grouping the provided data set by last name and first name
df1 = df.groupby(['ln','fn'])

#Getting the values of different indexes grouped in df1
unique_df1 = df1.groups

# Defining a dict type variable to save values under different keys
Similar = {}
for k in unique_df1.keys():
    ind = return_same(list(df.ix[unique_df1[k]][['dob','gn']].values), list(unique_df1[k]))
    Similar[k] = ind

new_DF = pd.DataFrame()

#Using the indexes we got from the function to identify elements in the DataFrame and copying them into the new DataFrame
for key in Similar:
    for i in Similar[key]:
        new_DF = new_DF.append(df.loc[i[0]], ignore_index=True)
        #print(df.loc[i[0]])
        #print('\n')

print('Printing the new DataFrame that we created')
print(new_DF)
#Saving the new DataFrame as follows
save = str(input('Enter the name of the file you want to save without the extension: '))
save = save + '.csv'
new_DF.to_csv(save)
print('Your file has been saved')

