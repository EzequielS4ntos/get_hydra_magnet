import json
import subprocess

comando = "strings -a ~/.config/hydralauncher/hydra-db/* 2>/dev/null | grep -Ei 'magnet:\\?|https?://' > logs.txt"
subprocess.run(comando, shell=True, executable="/bin/bash")

with open('logs.txt', 'r') as file:
    content = file.readlines()

links = []

search = input('Search term (type just one like "spider" ou "redemption"): ').lower()

for line in content:
    if 'magnet:' in line:
        target_line = line.replace('\n', '')
        if search in target_line.lower():
            if target_line[0] == '{' and target_line[-1] == '}':
                try:
                    links.append(json.loads(target_line))
                except:
                    pass

check = set()
unique = [
    d for d in links if not (d['uri'] in check or check.add(d['uri']))
]


find_downloads = []
indice = 1
print('\nFound downloads:')
for i in unique:
    print(f'{indice} - {i['folderName']}')

    find_downloads.append({
        'indice': indice,
        'name': i['folderName'],
        'link': i['uri']
    })

    indice += 1

valid_indice = False
while not valid_indice:
    try:
        selected = int(input('\nChoose a download index: '))

        for f in find_downloads:
            if f['indice'] == selected:
                command = f'wl-copy "{f['link']}"'

                subprocess.run(command, shell=True, executable='/bin/bash')

                print('\nLink copied to the clipboard')

        valid_indice = True
    except:
        print('Invalid index, try again')