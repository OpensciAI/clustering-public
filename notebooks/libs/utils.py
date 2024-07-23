"""
Util file contains frequently used utility methods.
"""

def extractSymptoms(answer):
    """
    Given a comma seperated list of symptoms, return the symptoms as an array.
    """
    return answer.split(',')

def calSymptomBurden(db, window_size=7):
    """
    Calculate the average symptom burden per day, during the symptom window. 
    
    Parameters
    ----------
    db : Database object.
    window_size : Window size in days.
    """
    
    query = """
        with f as (
          select s.*, day(s.datetime - ss.first_symptom_date) days_offset
            from symptompp s
            inner join first_symptom_date ss
            on s.uid = ss.uid
        )
        select uid, name, sum(severity) sum_severity, 
          count(distinct(days_offset)) days_recorded,
          sum(severity) / count(distinct(days_offset)) "avg_burden_per_day"
          from f
          where days_offset < {window} and allday = false and severity > 0
          group by uid, name
          order by uid, name
    """.format(window = window_size)
    
    results = db.execQuery(query, cached=True)
    
    return results

def clusterMatrix(data):
    """
    Take in a symptom burden frame and convert it into a matrix that is ready for clustering.
    
    data : The raw symptom burden matrix generated by calling `calSymptomBurden`
    """
    
    frame = pd.DataFrame()  # Empty dataframe that will contain all the dataset.
    uidmap = {}
    # Start breaking the users frame and extract data from it to add to the data matrix.
    temp = None  # Temp dictionary that holds the symptom counts for each user.
    for uid, sname, scount in zip(data['uid'].values, data['name'].values, data['avg_burden_per_day'].values):
        if not (uid in uidmap):
            # If temp is not None (everything except for the first uid then we will concat the last uid to the frame.
            if not (temp is None):
                temp = pd.Series(temp)
                temp = temp.to_frame().T
                frame = pd.concat([frame, temp], ignore_index=True)
            temp = {}  # Start fresh again.
            temp['uid'] = uid
            uidmap[uid] = 1
        temp[sname] = scount
    frame = frame.set_index(['uid']) # Set the 'uid' as the index, so it becomes easier to query.
    frame = frame.fillna(0)
    
    return frame

## If the block above throws an error - use this. 
def getTopSymptoms(users, top=5):
    if len(users) == 0:
        return pd.DataFrame(columns=['name', 'occ'])  # Return an empty DataFrame if no users in the segment
    
    where_query = "uid IN ('{}')".format("','".join(users))
    
    query = """
        SELECT name, COUNT(name) AS occ FROM symptoms 
        WHERE {where}
        GROUP BY name
        ORDER BY occ DESC
        LIMIT {top}
    """.format(where=where_query, top=top)
    
    results = db.execQuery(query, cached=True)
    return results

def symPercentages(frame, top=100):
    # Calculate the total count of each symptom type (sum across columns)
    symptom_totals = frame.sum(axis=0)

    # Calculate the total count of all symptoms
    total_symptom_count = symptom_totals.sum()

    # Calculate the percentage of each symptom type's count relative to the total count of all symptoms
    symptom_percentages = (symptom_totals / total_symptom_count) * 100

    # Sort the symptom_percentages in descending order (most frequent to least frequent)
    symptom_percentages_sorted = symptom_percentages.sort_values(ascending=False)

    # Print out each symptom type and its corresponding percentage in the sorted order
    c = 0
    for symptom, count in zip(symptom_percentages_sorted.index, symptom_percentages_sorted.values):
        c += 1
        print(f"{symptom}: {count:.2f}%")
        if c >= top:
            break
