#ANY OF THE HEADS ALONG THE WAY CAN BE VIEWED BY ADDING PRINT INFRONT
#This is a basic script that can recomend movies based on other movies, at the moment it can recomend based on the Starwars
#movie and LiarLiar - this works. Results can be seen in the terminal.
import pandas as pd
#Matlab used for graphing and tables
import matplotlib.pyplot as plt 
import seaborn as sns 

#Configures matlab
sns.set_style('white')
# %matplotlib inline

#Getting the data - this will be changed to use the API
#Sets the column names equal to the headers - these will be changed.
column_names = ['user_id', 'item_id', 'rating', 'timestamp'] 

#This links to the website of the test tsv file - this will be changed to use the TMDb api

path = 'https://media.geeksforgeeks.org/wp-content/uploads/file.tsv'

#Sets a df var eq to the result of calling pd(pandas).read on the path.

df = pd.read_csv(path, sep='\t', names=column_names)

#Checks the head of the data
df.head()

#Check out all movies and their corresponding IDs
movies_titles = pd.read_csv('https://media.geeksforgeeks.org/wp-content/uploads/Movie_Id_Titles.csv')
movies_titles.head()

#Merges the movie titles and the df vars together
data = pd.merge(df, movies_titles, on='item_id')
data.head()

#This calculates the mean rating of all movies
data.groupby('title')['rating'].mean().sort_values(ascending=False).head()

#Calculates the total amount of ratings a movie has been given
data.groupby('title')['rating'].count().sort_values(ascending=False).head()

#Creates a dataFrame with rating count values
ratings = pd.DataFrame(data.groupby('title')['rating'].mean())

ratings['num of ratings'] = pd.DataFrame(data.groupby('title')['rating'].count())

ratings.head()

#Plots the number of ratings graph - no clue how to see this
plt.figure(figsize =(10,4))
ratings['num of ratings'].hist(bins = 70)


#Plots the ratings graph - no clue how to see this
plt.figure(figsize =(10,4))
ratings['rating'].hist(bins = 70)

#Sorts values according to the num of rating column
moviemat = data.pivot_table(index ='user_id', columns ='title', values ='rating')
moviemat.head()
ratings.sort_values('num of ratings', ascending = False).head(10)

#Analyse the correlation between similar movies
starwars_user_ratings = moviemat['Star Wars (1977)']
liarliar_user_ratings = moviemat['Liar Liar (1997)']
batman_forever_user_ratings = moviemat['Batman Forever (1995)']
starwars_user_ratings.head()

#Additional correlation between movies - this part will be a bastard to implement with an API
similar_to_starwars = moviemat.corrwith(starwars_user_ratings)
similar_to_liarliar = moviemat.corrwith(liarliar_user_ratings)
similar_to_batmanforever = moviemat.corrwith(batman_forever_user_ratings)
corr_starwars = pd.DataFrame(similar_to_starwars, columns = ['Correlation'])
corr_starwars.dropna(inplace = True)
corr_starwars.head()

#Similar movies to 'STARWARS' -

corr_starwars.sort_values('Correlation', ascending = False).head(10)
corr_starwars = corr_starwars.join(ratings['num of ratings'])
corr_starwars.head()
print(corr_starwars[corr_starwars['num of ratings']>100].sort_values('Correlation', ascending = False).head())

#Similar movies to 'LIARLIAR' - 
corr_liarliar = pd.DataFrame(similar_to_liarliar, columns = ['Correlation'])
corr_liarliar.dropna(inplace = True)

corr_liarliar = corr_liarliar.join(ratings['num of ratings']) 
print(corr_liarliar[corr_liarliar['num of ratings']>100].sort_values('Correlation', ascending = False).head())

#Similar movies to 'BATMAN FOREVER'-
corr_batmanforever = pd.DataFrame(similar_to_batmanforever, columns = ['Correlation'])
corr_batmanforever.dropna(inplace=True)
corr_batmanforever = corr_batmanforever.join(ratings['num of ratings'])
print(corr_batmanforever[corr_batmanforever['num of ratings']>100].sort_values('Correlation', ascending = False).head())