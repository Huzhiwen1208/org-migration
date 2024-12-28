# org-migration

将 rel4team 下的仓库，迁移到 reL4team2 下。

## 仓库名以及分支名迁移
见 mapping.csv
- raw: 原仓库名
- replace_repo: 新仓库名
- replace_branchs: 保留的分支名以及对应的新分支名

## 默认分支约定
- 默认分支为 master，一般是由 mi-dev 分支迁移而来
- 如果默认分支不是 master，可能该仓库只有一个 main/dev/v1.0 样式的分支名。

## 必要文件说明

| 文件名      | 说明                             |
| ----------- | -------------------------------- |
| mapping.csv | 原仓库名与新仓库名的映射关系     |
| replace.csv | 关键词替代，主要用在分支的依赖中 |

## 执行

```shell
make migration # 执行迁移
```

## 改进
- 可以将 Cargo.toml中 crate 依赖的 branch = master 去掉，因为默认分支是 master。