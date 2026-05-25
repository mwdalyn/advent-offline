"""
This was a file to scrape in bulk all inputs and puzzle premises for past years.
Wanted to take it offline. Should only be run once. Pauses are built in. 

TODO: Need to rework to account for project restructuring.
"""
import os, re, time, requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

# Parameters
BASE_URL = r'https://adventofcode.com' 
YEARS = [2019,2020,2021,2022,2023,2024] # 2022-2024 added January 2026
HEADERS = {} # Holds session_id and user_agent

# Functions
def parse_puzzle_text(response_text):
	'''Parse out the premise and log if answered or not.'''
	# Response to soup
	soup = BeautifulSoup(response_text, "lxml")
	text = soup.get_text(separator=" ", strip=True)
	# Trim everything before the first '---' and after the section 'Answer:' (inclusive) 
	text = "".join(['---',text.split('---', 1)[1]])
	# Inject newline after each sentence
	text = re.sub(r'([.!?])\s+', r'\1\n', text)
	text = re.sub(r':\s+', ':\n', text)
	# Remove ending or answer (if already submit in browser)
	if 'Your puzzle answer' in text:
		answered = 1
	elif 'Answer:' in text:
		answered = 0
	else:
		answered = 0 # TODO: Throw error for a day if the day contains neither; convention may have changed
	text = re.split(r'Answer:', text, 1)[0] # Yet unanswered "end" of premise
	text = re.split(r'Your puzzle answer', text, 1)[0] # Previously answered "end" of premise
	return text, answered

def check_if_answered(response_text):
	'''If parsing unnecessary, simple function to test if answered.'''
	# Remove ending or answer (if already submit in browser)
	if 'Answer:' in response_text:
		return False
	return True

if __name__ == "__main__":
	# Stash answered status
	completion_grid = []
	# Open headers
	with open('aoc_session_id.txt') as f: # Need session_id, lasts 1 year from creation
		for line in f:
			key, value = line.strip().split(':', 1)
			key, value = key.replace("'","").strip(), value.replace("'","").strip()
			HEADERS[key] = value
		SESSION_ID = HEADERS['Session-Id'] # Account with AOC; linked to gh
		USER_AGENT = HEADERS['User-Agent']
	# Iterate through years of interest (all with 25 puzzles)
	for year in YEARS:
		print('Start year: {}'.format(year))
		# Init
		if not os.path.isdir(str(year)):
			os.makedirs(str(year))
			os.makedirs(os.path.join(str(year),'input'))
			os.makedirs(os.path.join(str(year),'premise'))
		# Review days
		for n in np.arange(1,25,1): # 25 days each year chosen
			print("Starting year " + str(year) + ", day " + str(n) + ".")
			puzzle = BASE_URL + r'/' + str(year) + r'/day/' + str(n)
			# Pull the "premise" of the problem as well
			puzzle_premise = requests.get(puzzle, cookies={'session':SESSION_ID})
			puzzle_text, puzzle_answered = parse_puzzle_text(puzzle_premise.text) 
			# Stash puzzle_text
			with open(str(year)+"/premise/day"+str(n)+".txt", "w", encoding="utf-8") as f:
				f.write(puzzle_text) # Writes puzzle details/instructions to text file
			time.sleep(25) # Courtesy sleep per request of @ericwastl
			# Log puzzle_answered
			# TODO: Develop a way to log which puzzles have been answered (separately? is there a better way?)
			completion_grid.append([year, n, puzzle_answered])
			# Grab input
			puzzle_input = requests.get(puzzle + r'/input', cookies={'session':SESSION_ID}) # Rejected, need to log in
			with open(str(year)+"/input/day"+str(n)+".txt", "w", encoding="utf-8") as f:
				f.write(puzzle_input.text)
			time.sleep(25) # Courtesy sleep per request of @ericwastl
			print("Done with day " + str(n) + ", on to the next.")
	# Store completion_grid
	completion_df = pd.DataFrame(completion_grid, columns=['year', 'day', 'complete'])
	completion_df['updated_on'] = pd.Timestamp.now()
	completion_df.to_csv('current_completion_grid.csv')

