# Created by Humza Malak & Alon Solomon
from __future__ import print_function
from requests   import get

import math
import csv
import pandas as pd
import numpy as np
import sys
import json
from pprint     import pprint
import sys

REGS_PATH       = "country-info.csv"
ARTICLES_PATH   = "generated-author-info.csv"

PUBS_PATH       = "test.csv"

FIELDS_MAP          = {
	"ai"				: "AI",
	"aaai"				: "AI",
	"ijcai"				: "AI",
	"vision"			: "Vision",
	"cvpr"				: "Vision",
	"eccv"				: "Vision",
	"iccv"				: "Vision",
	"mlmining"			: "ML",
	"icml"				: "ML",
	"kdd"				: "ML",
	"nips"				: "ML",
	"nlp"				: "NLP",
	"acl"				: "NLP",
	"emnlp"				: "NLP",
	"naacl"				: "NLP",
	"ir"				: "Web+IR",
	"sigir"				: "Web+IR",
	"www"				: "Web+IR",
	"arch"				: "Arch",
	"asplos"			: "Arch",
	"isca"				: "Arch",
	"micro"				: "Arch",
	"hpca"				: "Arch",
	"comm"				: "Networks",
	"sigcomm"			: "Networks",
	"nsdi"				: "Networks",
	"sec"				: "Security",
	"ccs"				: "Security",
	"oakland"			: "Security",
	"usenixsec"			: "Security",
	"ndss"				: "Security",
	"pets"				: "Security",
	"mod"				: "DB",
	"sigmod"			: "DB",
	"vldb"				: "DB",
	"icde"				: "DB",
	"pods"				: "DB",
	"hpc"				: "HPC",
	"sc"				: "HPC",
	"hpdc"				: "HPC",
	"ics"				: "HPC",
	"mobile"			: "Mobile",
	"mobicom"			: "Mobile",
	"mobisys"			: "Mobile",
	"sensys"			: "Mobile",
	"metrics"			: "Metrics",
	"imc"				: "Metrics",
	"sigmetrics"		: "Metrics",
	"ops"				: "OS",
	"sosp"				: "OS",
	"osdi"				: "OS",
	"fast"				: "OS",
	"usenixatc"			: "OS",
	"eurosys"			: "OS",
	"pldi"				: "PL",
	"popl"				: "PL",
	"icfp"				: "PL",
	"oopsla"			: "PL",
	"plan"				: "PL",
	"soft"				: "SE",
	"fse"				: "SE",
	"icse"				: "SE",
	"ase"				: "SE",
	"issta"				: "SE",
	"act"				: "Theory",
	"focs"				: "Theory",
	"soda"				: "Theory",
	"stoc"				: "Theory",
	"crypt"				: "Crypto",
	"crypto"			: "Crypto",
	"eurocrypt"			: "Crypto",
	"log"				: "Logic",
	"cav"				: "Logic",
	"lics"				: "Logic",
	"graph"				: "Graphics",
	"siggraph"			: "Graphics",
	"siggraph-asia"		: "Graphics",
	"chi"				: "HCI",
	"chiconf"			: "HCI",
	"ubicomp"			: "HCI",
	"uist"				: "HCI",
	"robotics"			: "Robotics",
	"icra"				: "Robotics",
	"iros"				: "Robotics",
	"rss"				: "Robotics",
	"bio"				: "Comp. Bio",
	"ismb"				: "Comp. Bio",
	"recomb"			: "Comp. Bio",
	"da"				: "EDA",
	"dac"				: "EDA",
	"iccad"				: "EDA",
	"bed"				: "Embedded",
	"emsoft"			: "Embedded",
	"rtas"				: "Embedded",
	"rtss"				: "Embedded",
	"visualization"	    : "Visualization",
	"vis"				: "Visualization",
	"vr"				: "Visualization",
	"ecom"				: "ECom",
	"ec"				: "ECom",
	"wine"				: "ECom",
	}
FIELDS_NAMES_MAP    = {
	"AI" 		    : "Artificial intelligence"         ,
	"Vision" 	    : "Computer vision"                 ,
	"ML" 		    : "Machine learning & data mining"  ,
	"NLP" 		    : "Natural language processing"     ,
	"Web+IR" 		: "The Web & information retrieval" ,
	"Arch" 		    : "Computer architecture"           ,
	"Networks" 	    : "Computer networks"               ,
	"Security" 		: "Computer security"               ,
	"DB" 		    : "Databases"                       ,
	"HPC" 		    : "High-performance computing"      ,
	"PL" 		    : "Programming languages"           ,
	"Comp. Bio"     : "Comp. bio & bioinformatics"      ,
	"Logic" 	    : "Logic & verification"            ,
	"Crypto" 	    : "Cryptography"                    ,
	"Robotics" 	    : "Robotics"                        ,
	"EDA" 		    : "Design automation"               ,
	"ECom" 		    : "Economics & computation"         ,
	"Theory" 	    : "Algorithms & complexity"         ,
	"OS" 		    : "Operating systems"               ,
	"Metrics" 	    : "Measurement & perf. analysis"    ,
	"HCI" 		    : "Human-computer interaction"      ,
	"Mobile" 	    : "Mobile computing"                ,
	"Visualization" : "Visualization"                   ,
	"Embedded" 		: "Embedded & real-time systems"    ,
	"Graphics" 		: "Computer graphics"               ,
	"SE"            : "Software engineering"            }

CHARS               = [
		"|",
		"/",
		"―",
		"\\",
		"|",
		"/",
		"―",
		"\\"
		]

# The number of fields used to rank
#   The lesser the better are the chances scoring higher
#   Setting this to a values other than 4 requires changes to the UI 
N_FIELDS        = 4
MIN_PAGE_COUNT  = 6 
SYNC            = False

def sync():
	"""
			Syncs the data to the latest version github.
	"""
	# Articles and countries urls
	articles_url    = 'https://github.com/emeryberger/CSrankings/blob/gh-pages/generated-author-info.csv?raw=true'
	countries_url   = 'https://github.com/emeryberger/CSrankings/blob/gh-pages/country-info.csv?raw=True'

	# Using python requests, we download the articles csv.
	r = get(articles_url, stream = True)
	with open(ARTICLES_PATH,'wb') as f:
		i = 0
		print('Downloading articles ...                 ')
		for ch in r.iter_content(chunk_size= 1024*200):
			print('Downloading articles {}'.format(CHARS[i]), end='\r')
			f.write(ch)
			f.flush()
			i = (i+1)%8

	# Using python requests, we download the countries csv.
	r = get(countries_url, stream = True)
	with open(REGS_PATH,'wb') as f:
		print('Downloading countries ...                 ')
		for ch in r.iter_content():
			f.write(ch)
			f.flush()

def g_df(
		path    , # Path of the csv file
		columns ):# Column names, or None
	"""
		Loads the csv file into a pandas data frame.
	"""

	# Read the given csv into a pandas dataframe.
	#   If columns are given use, else use first row as
	#   a header.
	return  pd.read_csv(path, names= columns) if columns\
			else pd.read_csv(path)

def create_csv():
	"""
		Creates the fields csv from the countries and users info csv
	"""
	# Load regions csv into a  data frame and set the index to institution
	regs_df     = g_df(REGS_PATH        , None ).set_index('institution')
	# Load users csv into a  data frame and set the index to department
	art_df      = g_df(ARTICLES_PATH    , None ).set_index('dept')

	# Add the region column to the users data
	art_df      = art_df.join(regs_df)

	# Set all rows with no region to usa
	art_df.loc[art_df["region"].isna(), "region"] = "usa"#

	# For each area, add a field column with the correct filed from field map
	art_df["field"] = art_df["area"].apply(lambda x: FIELDS_NAMES_MAP[FIELDS_MAP[x]])


	# Rename the column index to institution
	art_df          = art_df.reset_index().rename(columns= {"index": "institution"})

	# Save the csv for future use
	art_df.to_csv(PUBS_PATH)
	return art_df


def c_scores(
		pubs_df):# Publications data fame
	"""
		Creates the scores for all universities
	"""
	# First, let's group the data by institution, field, adjustedcount then sort it by field
	pubs_df                 = pubs_df.copy()[["institution","field","adjustedcount"]].sort_values(by="field")

	#Remove all scores that are <=0
	pubs_df                  = pubs_df[pubs_df["adjustedcount"]> 0]

	# For each field, calculate the score of a field, it is 1+ the sum of all areas
	pubs_df["adjustedcount"] = 1+ pubs_df.groupby(["institution","field"])['adjustedcount'].transform('sum')

	# Remove all columns, leave only institution, field, adjustedcount
	pubs_df                  = pubs_df[["institution", "field", "adjustedcount"]]

	# Group by institution, field and select only the first value for each field
	pubs_df                  = pubs_df.groupby(["institution","field"]).first()

	return pubs_df

def c_rank(
		university  , # University
		score_df    ,):# The scores data frame
	"""
		Returns the scores for all universities
	"""
	# Get the total number of areas
	area_cpt                = len(score_df['field'].unique())

	# Set score to the product of all field scores
	score_df["score"]       = score_df.groupby(["institution"])["adjustedcount"].transform('prod')

	print(score_df[score_df['institution'] == 'Yale University'])

	# Keep only first row for each institution
	score_df                = score_df.groupby(["institution"]).first()

	# Calculate final score score ^(1/n_areas)
	score_df["score"]       = round(score_df["score"] ** (1/area_cpt),1)

	# Return only he score of the university
	score_df["rank"]        = score_df["score"].rank(ascending=False, method = "min")

	return score_df.loc[university]

def g_best_score(
		n_fields    ,   # Number of fields to return
		university  ,   # Name of the university
		start_year  ,   # start year
		end_year    ,   # end year
		region      ,   # Region
		areas     =[]):  # Areas selected from the interface
	"""
		Gets the fields for which the given university scores the best.
	"""
	# Get publications df
	pubs_df     = g_df(PUBS_PATH    , None )
	regs_df     = g_df(REGS_PATH    , None )

	# Filter by years, only between start and end year
	pubs_df     = pubs_df[(pubs_df["year"]>=start_year) & (pubs_df["year"]<= end_year)]

	# If areas list is sent from the interface, use the selected areas only
	if areas != [] :
		pubs_df = pubs_df[pubs_df['area'].isin(areas)]
	# If region is northamerica, include both canada and usa
	if region == "northamerica":
		region = "usa canada"

	# Create a list of all selected regions
	region          = region.lower().replace('the',' ').replace('and',' ').\
					  replace('h a','ha').split()

	# If regions are not world, select only the given regions
	if "world" not in  region:
		pubs_df         = pubs_df.loc[pubs_df["region"].isin(region)]

	# Calculates the scores
	score_df        = c_scores(pubs_df)

	# Get best fields sorting by field score, select only top n_fields
	fields          = score_df.loc[university].\
					  sort_values(by="adjustedcount" , ascending =False)[:n_fields].index.values

	# Resest the index and copy the data frame
	score_df        = score_df.reset_index()
	field_score_df  = score_df.copy()
	# The new data frame will only have the top fields for the university
	field_score_df  = field_score_df[field_score_df["field"].isin(fields)]

	# Get the old score(all fields selected)
	old = c_rank(university, score_df)
	# Get the best rank possible, top n_fields selected
	new = c_rank(university, field_score_df)

	# Return the result
	result = {
		"old_score" : old["score"]  ,
		"old_rank"  : old["rank"]   ,
		"new_score" : new["score"]  ,
		"new_rank"  : new["rank"]   ,
		"fields"    : list(fields)  }

	return result

def g_uvs(region):
	"""
		Used by the server to return institutions for a given region
	"""

	# If north america
	if region == "northamerica":
		region = "usa canada"
	# Load the publications df
	pubs_df     = g_df(PUBS_PATH    , None )
	# Process region value and create a list of locations
	region      = region.lower().replace('the',' ').replace('and',' ').\
					  replace('h a','ha').split()
	print(region)

	# If region is not world, select institutions within given regions
	if "world" not in  region:
		pubs_df         = pubs_df.loc[pubs_df["region"].isin(region)]

	# Return the list of universities
	return list(pubs_df["institution"].unique())

def main():

	# Calculate the scores and ranks
	res = g_best_score(
		N_FIELDS            ,
		sys.argv[1]         ,
		int(sys.argv[2])    ,
		int(sys.argv[3])    ,
		sys.argv[4]         )
	pprint(res)

if SYNC :
	sync()
	create_csv()

if __name__ == "__main__":
	main()
