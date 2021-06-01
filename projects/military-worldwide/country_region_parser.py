import pickle

file_list = "country_list.txt"
lines = None
with open(file_list, 'r', encoding="utf8") as f: 
    lines = f.readlines()

country_region_pairs = []
for line in lines:
    tabs = []
    c_count = 0
    line = line.strip()
    for c in line:
        if c == '\t':
            tabs.append(c_count)
        c_count += 1
    if len(tabs) > 0:
        country_region = (line[:tabs[0]], line[tabs[-1] + 1:])
        country_region_pairs.append(country_region)

for pair in country_region_pairs:
    print(pair)

new_file_list = 'country-region_list.txt'
with open(new_file_list, 'wb') as f:
    pickle.dump(country_region_pairs, f)
    
    
    

    
