import requests
from bs4 import BeautifulSoup
import re

# get the data
data = requests.get('http://cs.qau.edu.pk/faculty.php')

#This will extract all the text in the faculty page
text = data.text
soup = BeautifulSoup(text, 'html.parser')

faculty_table = soup.find('table', {'class': 'tbl'})
tbody = faculty_table.find('tbody')

tbody = tbody.text

# Patterns for extracting emails, names, and phone Numbers of the faculty members of qau
pattern1  = re.compile(r'[:][+]\d{2}[-]\d{2}[-]\d{4}\s\d{4}')
pattern2  = re.compile(r'([\d\w\.]+@[\d\w\.\-]+\.\w+)')

pattern3  = re.compile(r'Dr\.?\s*([A-Z]\w*\.?\s){1,4}')
pattern4 = re.compile(r'Memoona(\s\w*){1,2}')
pattern5 = re.compile(r'Ifrah(\s\w*){1,6}')


contacts = pattern1.findall(text)
contacts = [word.replace(':+','+') for word in contacts]

emails = pattern2.findall(text)
names = pattern3.finditer(tbody)
name4 = pattern4.finditer(tbody)
name5 =  pattern5.finditer(tbody)



faculty_names = list()
for name in names:
    faculty_names.append(name.group(0))

for name in name4:
    faculty_names.append(name.group(0))
    
for name in name5:
    faculty_names.append(name.group(0))


# This will replace the extra garbage extracted with the real data
faculty_names = [word.replace('Assistant',' ') for word in faculty_names]
faculty_names = [word.replace('\n',' ') for word in faculty_names]
faculty_names = [word.replace('Lecturer',' ') for word in faculty_names]
faculty_names = [word.replace('    ','') for word in faculty_names]


for fn in faculty_names:
    print(fn)


print('\n\n')


# numbers = dict.fromkeys(contacts).keys()
# list[numbers]
for match in contacts:
    print(match)

print('\n\n')

email_addresses = dict.fromkeys(emails).keys()
list[email_addresses]
for match in email_addresses:
    print(match)


print('\n\n')

# Writing to the text file all the rocords fetched from the faculty link
file1 = open('facultyRecords.txt', 'w')

file1.write('Name\t\t\t\t\t\t\t\t Phone\t\t\t\t\t\t\t\tEmail\n\n')

for (nAME, pHONE, eMAIL) in zip(faculty_names, contacts, email_addresses):
    file1.write('{:<35} {:<35} {:<20}'.format(nAME, pHONE, eMAIL))
    file1.write('\n')
    


file1.close()
