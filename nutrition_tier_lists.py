import json
import os.path
import sys
from colorama import Fore, Back, Style
import subprocess



col = input(Fore.GREEN + "Which collections of food would you like to view? (Enter nothing if you wish to stop the program): " + Fore.WHITE)
if col == '':
    print('Thank you!')
    exit()




while not os.path.isfile(f'{col}/{col}.json'):
    ans = input(Fore.GREEN + 'There is no such collection: would you like to create one (Y/n): ' + Fore.WHITE)
    if ans.lower() == 'y':
        x = input("Type up all the categories you want to store besides vitamins enter a number denoting the number of vitamins to stop: ")
        cats = []
        while not x.isnumeric():
            cats.append(x)
            x = input("Next: ")
        
        subprocess.run(f"mkdir {col}", shell=True)
        subprocess.run(f"cp nf.sh {col}", shell=True)
        subprocess.run(f"chmod +x {col}/nf.sh", shell=True)
        subprocess.run(f"cp template.txt {col}", shell=True)
        bio = input(Fore.CYAN + "Enter a bio for this category of food: " + Style.RESET_ALL)
        f = open(f'{col}/{col}.json', 'w')
        f.write(json.dumps({'Title': col, 'Categories': cats, 'NumVitamins': int(x),'Bio': bio, 'Foods': {}}))
        f.close()
    else:
        col = input(Fore.GREEN + 'Which collections of passwords would you like to view? (Enter nothing if you wish to stop the program): ' + Fore.WHITE)
        if col == '':
            print('Thank you!')
            exit()


bad = False
with open(f'{col}/{col}.json') as json_file:
    data = json.load(json_file)
    inp = 0
    first = True
    while True:
        subprocess.run('clear', shell=True)
        if first:
            print(Fore.CYAN + data['Bio'] + Style.RESET_ALL)
        if bad:
            print(Fore.RED + 'No Instruction Found\n' + Style.RESET_ALL)
            bad = False
        
        print(Style.BRIGHT  + Fore.MAGENTA + "Note: All nutrient quantities are based on 100g of Food and % DV are based on 2,000 Calorie Diet")
        print(Fore.GREEN + "What type of query do you want to make:" + Fore.WHITE)
        print(Fore.LIGHTRED_EX + "0" + Fore.WHITE + ") " + Style.BRIGHT + Fore.CYAN + "List" + Style.RESET_ALL + " all foods of this category") 
        print(Fore.LIGHTRED_EX + "1" + Fore.WHITE + ") " + Style.BRIGHT + Fore.YELLOW + "Find" + Style.RESET_ALL+ " info on a specific food")
        print(Fore.LIGHTRED_EX + "2" + Fore.WHITE + ") " + Style.BRIGHT + Fore.GREEN + "Add/Replace "+ Style.RESET_ALL+ "an entry")
        print(Fore.LIGHTRED_EX + "3" + Fore.WHITE + ") " + Style.BRIGHT + Fore.LIGHTRED_EX + "Remove"+ Style.RESET_ALL+ " an entry")
        print(Fore.LIGHTRED_EX + "4" + Fore.WHITE + ") " + Style.BRIGHT + "Save " + Style.RESET_ALL + "changes and exit this application")
        print(Fore.LIGHTRED_EX + "5" + Fore.WHITE + ") " + Style.BRIGHT + "Quit " + Style.RESET_ALL + "and exit this application")

        inp = input()
        if inp == '0':
            s = sorted([food for food in data['Foods'].keys() if food != 'template'])
            for food in s:
                print(Style.BRIGHT + '- ' + Fore.CYAN + food + Style.RESET_ALL)
            input('press enter to clear')
        elif inp == '1':
            query = input(Fore.GREEN + 'What food are you looking for: ' + Style.RESET_ALL)
            for name, food in data['Foods'].items():
                if name.lower() == query.lower():
                    print(Fore.CYAN + name + Style.RESET_ALL)
                    print(Style.BRIGHT + food['Bio'] + Style.RESET_ALL)
                    print()
                    for a,b,c in zip(food['Stats'][::3],food['Stats'][1::3],food['Stats'][2::3]):
                        print(Style.BRIGHT + Fore.GREEN + '{:<30}{:<30}{:<}'.format(a,b,c) + Style.RESET_ALL)
            input('press enter to clear')
        elif inp == '2':
            dir = input(Fore.GREEN + "From which directory should I add the foods or should I add it directly (Type 'direct' if the later anythin else if former): " + Style.RESET_ALL)
            entry = {}
            #macr = ['SS', 'Calories', 'Protein', 'Fat', 'SF', 'MUF', 'PUF']
            #macr = ['SS', 'Calories', 'Carbs', 'Fiber']
            macr = data['Categories']
            nv = data['NumVitamins']
            if dir.lower() == 'direct':
                entry['name'] = input(Fore.GREEN + 'Name: ' + Style.RESET_ALL)
                for s in macr:
                    entry[s] = input(Fore.GREEN + s +': ' + Style.RESET_ALL)

                entry['Vitamins'] = []
                for i in range(nv):
                    res = input(Fore.GREEN + 'Micro. Nutrient Name and DV ' + str(i+1) + ': ' + Style.RESET_ALL).split()
                    while len(res) != 2:
                        res = input(Fore.RED + 'Need exactly 2 entries (name and daily value): ' + Style.RESET_ALL).split()
                    entry['Vitamins'].append(res)
                entry['Bio'] = input(Fore.GREEN + "Bio: " + Style.RESET_ALL)

                entry['Stats'] = [x + ': ' + entry[x] for x in macr]
                for i in range(nv):
                    entry['Stats'].append(entry['Vitamins'][i][0] + ': ' + entry['Vitamins'][i][1])
            else:
                for filename in os.listdir(col):
                    f = os.path.join(col, filename)
                    if os.path.isfile(f) and filename[-3:] == 'txt':
                        entry = {}
                        entry['name'] = filename[:-4]
                        entry['Vitamins'] = []
                        entry['Bio'] = ""
                        with open(f, 'r') as liners:
                            lines = liners.read()
                            index = 0
                            for line in lines.split('\n'):
                                if len(line) < 3:
                                    continue
                                if index < len(macr):
                                    entry[macr[index]] = line.split()[-1]
                                elif index < len(macr) + nv:
                                    items= line.split()
                                    entry["Vitamins"].append(items)
                                else:
                                    entry['Bio'] += (line + '\n')
                                index += 1
                            entry['Stats'] = [x + ': ' + entry[x] for x in macr]
                            for i in range(len(entry['Vitamins'])):
                                if len(entry['Vitamins'][i]) != 2:
                                    print('Problem with food ' + entry['name']+ ' ' + entry['Vitamins'][i][0])
                                entry['Stats'].append(entry['Vitamins'][i][0] + ': ' + entry['Vitamins'][i][1])
                        entry['Bio'] = entry['Bio'][:-1]
                        data['Foods'][entry['name']] = entry
            input('Press anything to reset')
        elif inp == '3':
            rem = input(Fore.RED + "What food do you want to remove: " + Style.RESET_ALL)
            data['Foods'].pop(rem, None)
            input(Fore.RED + "Removed! Press enter to reset" + Style.RESET_ALL)
        elif inp == '4':
            subprocess.run(f"rm {col}/{col}.json", shell=True)
            f = open(f'{col}/{col}.json', 'w')
            f.write(json.dumps(data))
            f.close()
            print(Fore.GREEN + "Saved!" + Style.RESET_ALL)
            exit()
        elif inp == '5':
            print(Fore.GREEN + "Left!" + Style.RESET_ALL)
            exit()
        else:
            bad = True
