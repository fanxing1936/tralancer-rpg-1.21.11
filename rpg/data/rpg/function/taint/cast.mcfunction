# 该他出手了。先上锁再分流 —— 归属靠这个标签认人，
# 命令是单线程的，同一刻不可能有第二个降临者挂着它。
scoreboard players set @s rpg_dm_cd 70
tag @s add rpg.dm.cast
function rpg:taint/skill
tag @s remove rpg.dm.cast
