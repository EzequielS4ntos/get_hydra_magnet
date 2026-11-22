import json
import subprocess

comando = "strings -a ~/.config/hydralauncher/hydra-db/* 2>/dev/null | grep -Ei 'magnet:\\?|https?://' > logs.txt"
subprocess.run(comando, shell=True, executable="/bin/bash")

with open('logs.txt', 'r') as file:
    content = file.readlines()

links = []

for line in content:
    if 'uri' in line:
        target_line = line.replace('\n', '')
        if target_line[0] == '{' and target_line[-1] == '}':
            try:
                raw_jason = json.loads(target_line)
                links.append(raw_jason)
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
    title:str = i['folderName']
    print(f'{indice} - {title}')

    find_downloads.append({
        'indice': indice,
        'name': title,
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
