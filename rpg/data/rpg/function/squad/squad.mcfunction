# 佣兵小队每刻入口。
# 只有一条玩家作用域判定；真正的遍历在雇主自己那一段里，而且限距。
execute as @a[tag=rpg.sq.lead] at @s run function rpg:squad/lead
execute as @a[scores={rpg_sq_t=1..}] run scoreboard players remove @s rpg_sq_t 1
