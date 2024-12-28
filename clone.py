import os
import csv

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

def read_replace_code(relative):
    mapping = {}
    with open(f'{relative}/replace.csv', 'r') as f:
        for line in f:
            src, dst = line.strip().split(',')
            mapping[src] = dst
    return mapping

if __name__ == '__main__':
    os.system('mkdir repos')
    os.chdir('repos')

    replaces = read_replace_code('..')
    repo_infos = parse_csv_to_tuples('../mapping.csv')
    for item in repo_infos:
        src = item[0]
        dst = item[1]
        branches = item[2]
        # clone repo
        if not os.path.exists(dst):
            os.system('git clone https://github.com/rel4team/' + src + ' ' + dst)
        else:
            os.system('rm -rf ' + dst)
            os.system('git clone https://github.com/rel4team/' + src + ' ' + dst)
        os.chdir(dst)
        os.system('git fetch --all')
        # checkout branch，如果有->，则表示需要重命名分支
        for branch in branches:
            if '->' in branch:
                src_branch = branch.split('->')[0].strip()
                dst_branch = branch.split('->')[1].strip()
                os.system('git checkout ' + src_branch)
                os.system('git checkout -b ' + dst_branch)
                os.system('git branch -D ' + src_branch)
            else:
                os.system('git checkout ' + branch)

        # 已保留更改后的分支名
        local_branches = []
        for branch in branches:
            if '->' in branch:
                branch = branch.split('->')[1].strip()
            local_branches.append(branch)

        print(f'url: {dst}, branches: {local_branches}')
        print('start replace code...')
        # 替换代码分支依赖
        for branch in local_branches:
            os.system('git checkout ' + branch)
            for src_, dst_ in replaces.items():
                os.system(f'LC_CTYPE=C find . -type f -exec sed -i \'\' "s/{src_}/{dst_}/g" {{}} +')
            os.system('git add .')
            os.system('git commit -m "modify branch name"')
        os.chdir('..')

    # 删除rust-sel4和rust-root-task-demo
    os.chdir('rel4-dev-repo')
    os.system('git checkout main')
    os.system('git pull')
    os.system("sed -i '' '/<project name=\"rust-sel4.git\" path=\"rust-sel4\" revision=\"master_unstable\" upstream=\"master_unstable\" dest-branch=\"master_unstable\" \/>/d' default.xml")
    os.system("sed -i '' '/<project name=\"rust-root-task-demo-master.git\" path=\"root-task-demo\" \/>/d' default.xml")
    os.system('git add .')
    os.system('git commit -m "remove rust-sel4 and rust-root-task-demo"')
    
    

