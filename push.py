import os
import csv

# 读取当前目录下的映射文件mapping.csv
def parse_csv_to_tuples(file_path):
    tuples_list = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # 跳过表头
        for row in reader:
            raw = row[0]
            replace_repo = row[1]
            replace_branchs = row[2] if len(row) > 2 else None
            branchs = replace_branchs.split(':') if replace_branchs else []
            tuples_list.append((raw, replace_repo, branchs))
    return tuples_list

if __name__ == '__main__':
    mapping = parse_csv_to_tuples()
    # 将所有仓库的推送到新的远程仓库中
    for item in mapping:
        dst = item[1]
        os.chdir(dst)
        os.system('git remote remove origin upstream')
        os.system(f'gh repo create reL4team2/{dst} --public --confirm')
        os.system(f'git remote add origin https://github.com/reL4team2/{dst}.git')
        os.system('git push origin --all')
        os.chdir('..')