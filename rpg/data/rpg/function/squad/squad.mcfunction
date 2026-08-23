# 佣兵小队每刻入口。
# 只有一条玩家作用域判定；真正的遍历在雇主自己那一段里，而且限距。
execute as @a[tag=rpg.sq.lead] at @s run function rpg:squad/lead
execute as @a[scores={rpg_sq_t=1..}] run scoreboard players remove @s rpg_sq_t 1

# 佣兵没了，骑在他身上的信息板会掉下来 —— 收走。带类型且限距，很便宜。
execute if entity @e[type=minecraft:text_display,tag=rpg.sq.board,limit=1] run function rpg:squad/sweep

# 刚到场的人，等装备的属性生效之后再画一次信息板。
execute if entity @e[type=minecraft:husk,tag=rpg.sq.fresh,limit=1] run function rpg:squad/fresh
