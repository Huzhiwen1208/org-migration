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
    replaces = read_replace_code('..')
    repo_infos = parse_csv_to_tuples()
    # 对于mapping中的key，将其作为git仓库的url，value作为本地目录名，执行git clone命令，如果已经存在则跳过
    for item in repo_infos:
        src = item[0]
        dst = item[1]
        branches = item[2]
        if not os.path.exists(dst):
            os.system('git clone https://github.com/rel4team/' + src + ' ' + dst)
        else:
            os.system('rm -rf ' + dst)
            os.system('git clone https://github.com/rel4team/' + src + ' ' + dst)
    # 将所有仓库的远程分支更新到本地, 并将所有远程分支checkout到本地
        os.chdir(dst)
        os.system('git fetch --all')
        # 查看所有分支, 将分支拉到本地，方便后续上传远程分支
        for branch in branches:
            if '->' in branch:
                src_branch = branch.split('->')[0].strip()
                dst_branch = branch.split('->')[1].strip()
                os.system('git checkout ' + src_branch)
                os.system('git checkout -b ' + dst_branch)
                os.system('git branch -D ' + src_branch)
            else:
                os.system('git checkout ' + branch)

        # 将所有代码中的mi-dev替换成my-dev
        local_branches = []
        for branch in branches:
            if '->' in branch:
                branch = branch.split('->')[1].strip()
            local_branches.append(branch)

        print(f'url: {dst}, branches: {local_branches}')
        print('start replace code...')
        for branch in local_branches:
            os.system('git checkout ' + branch)
            for src_, dst_ in replaces.items():
                os.system(f'LC_CTYPE=C find . -type f -exec sed -i \'\' "s/{src_}/{dst_}/g" {{}} +')
            os.system('git add .')
            os.system('git commit -m "modify branch name"')

            if branch == 'master':
                os.system('gh repo edit --default-branch ' + branch)

        os.chdir('..')