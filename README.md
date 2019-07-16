Computer Science Rankings
=========================
CSRankings is a website developed by academia, that allows users to interact with the site to see the research intensities of different universities. We were tasked with creating and adding a function that enables a user to find out which research area(s) give the best rank for a given university. 

This is a project I did with a fellow student, it uses Python, Pandas and NumPy to fulfillthe task we were given. 
It works as follows:
You will select the region, like Europe, followed by the University of your choice and then selecting the publication years of your choice which can be set to 2010 - 2019. Furthermore, you can finish on selecting four research areas and then clicking "Best Ranking". The output of this will be the old rank of the university and the new rank. The score for the universitites is also displayed. 

### Trying it out at home
Download this repo 

Before running the server, you will need to direct yourself to wherever you have placed the unzipped CSRankings-V5
In order to run the server, you will need to execute the command “python server.py” within the folder containing the server.py file. 

To access the site, you will need to enter into the search bar at the top “localhost:8000”
Upon pressing enter you will be brought to our CSRankings page. 
To interact with our site, you can select from the available dropdowns such as region, publication years, universities and the number of research areas you would like for the chosen University. 
Upon selecting the different choices within the dropdown lists you can then press “Best Ranking” which will output the data for the chosen University and give you its best ranking and new score. We have also added the old rank and score to show what difference the algorithm has made. 
We can see this is correct for example if we look at the old score when all research areas are selected for the University of Kent 
And then compare this with the selected research areas which are Programming Languages, Logic & Verification, Artificial Intelligence and Computer Networks. 
f for example, we feel that the data provided is not in line with the original CSRankings.org website, then we can always run a sync with our server and change the code. For example, if we open our script in PyCharm and change the sync to True, then our server ensures all the data is in sync. 



### Acknowledgements
This project wouldnt be possible without the work of [Emery Berger](https://emeryberger.com). 
