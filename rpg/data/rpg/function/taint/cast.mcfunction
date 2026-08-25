# 该他出手了。先上锁再分流 —— 归属靠这个标签认人，
# 命令是单线程的，同一刻不可能有第二个降临者挂着它。
scoreboard players set @s rpg_dm_cd 70
# 每第四次出手改为罪约。计数跟着实体走，多只恶魔互不借拍；
# ult_start 会清零并进入自己的蓄势阶段。
scoreboard players add @s rpg_dm_casts 1
execute if entity @s[scores={rpg_dm_casts=4..}] run return run function rpg:taint/ult_start
tag @s add rpg.dm.cast
function rpg:taint/skill
tag @s remove rpg.dm.cast
