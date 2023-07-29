import opendota 
import polars as pl
from time import strftime, localtime #for converting epoch time to readable time
#Initialise the API-connection object
client = opendota.OpenDota()
client.get_match("7232263097")



#first find all the matches of moxie
#need player ids of each member
players=["mankiddyman","ancient_thunderhide","zenox","kai-z-kite","smugmonkey","4gg"]
player_ids=["121240193","150357103","432167804","194740620","113084194","147172172"]

player_metadata=pl.DataFrame({"Players":players,"Player_ID":player_ids})


df=pl.DataFrame({"Game_#":None,"Game_ID":None,"Date":None,"Radiant_or_Dire":None})

pos_columnnames=["Pos1_Player","Pos1_Hero","Pos1_K/D/A","Pos1_CS @ 10"]

for pos,i in enumerate(list(range(1,6))):
    cols=[string.replace("1",str(pos+1))for string in pos_columnnames]
    #add each column to the dataframe
    for col in cols:
        df=df.with_columns(pl.Series(col,[[]]))        

df
#now that all collumns are ready



matches_df=pl.DataFrame({"Game_ID":None,"Date":None,"n_members_present":None,"Radiant_or_Dire":None,"time":None})

match_ids=[]
dates=[]
n_members_present=[]
times=[]
source_player=[]
#loop through each player and find the matches they played
for ID in player_ids:
    n_matches=len(client.get_player_matches(ID))
    for match in range(0,int(str(n_matches))):
        match_ids.append(client.get_player_matches(ID)[match]["match_id"])
        #time is in epoch time
        #but how do we know the timezone?
        start_time=client.get_player_matches(ID)[match]["start_time"]
        date,time=(strftime('%Y-%m-%d %H:%M:%S', localtime(start_time))).split(" ")
        dates.append(date)
        times.append(time)
        source_player.append(players[player_ids.index(ID)])
        #identify matches where at least 5 moxie members are present
#going to add the match ids and dates to the dataframe

#increase the size of the dataframe 
dfs=[matches_df]*len(match_ids)
matches_df=pl.concat(dfs)

col=pl.Series("Game_ID",match_ids),pl.Series("Date",dates),pl.Series("time",times),pl.Series("source_player",source_player)

matches_df=matches_df.with_columns(col)


#now removing duplicates and filling in n_present
#identify rows with count >=5
match_counts=matches_df['Game_ID'].value_counts()

matches=pl.DataFrame()
print("Total Unique match ids",len(match_counts))
for i in range(0,len(match_counts)):
    #if the count is >5 record the match id
   
          

    if match_counts.row(i)[1]>=5:
        print("size_before",len(matches))    

        #find index of the row containing match id in matches_df
        id=match_counts.row(i)[0]        
        
        matches=pl.concat([matches,matches_df.filter(pl.col("Game_ID")==id)])

        print("size_after",len(matches))
#parse the data and add to df

matches_df=matches

for i in range(0,len(matches_df)):
    df['Game_#'].append(i+1)
    df['Game_ID'].append(matches_df['Game_ID'][i])
    df['Date'].append(matches_df['Date'][i])
    
    match=client.get_match(matches_df['Game_ID'][i])
    
    players=match['players']
#here

    df['Radiant_or_Dire']


# do these guys think they are good..?
'''
  _____ __  ___    __  ___ ______ ___ _____   __ __  ____   ___ ___  
 |_   _/__\| _,\ /' _/| __/ _/ _ \ __|_   _| |  V  |/__\ \_/ / | __| 
   | || \/ | v_/ `._`.| _| \_| v / _|  | |   | \_/ | \/ > , <| | _|  
   |_| \__/|_|   |___/|___\__/_|_\___| |_|   |_| |_|\__/_/ \_\_|___| 
'''
for i,ID in enumerate(player_ids):
    print(f"TOP SECRET {players[i]} MMR",client.get_player(ID)['mmr_estimate']['estimate'])
