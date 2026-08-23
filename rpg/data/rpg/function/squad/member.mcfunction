# 一名队员的一刻。@s 是队员，执行位置在它自己脚下。
execute if entity @s[scores={rpg_sq_cd=1..}] run scoreboard players remove @s rpg_sq_cd 1
execute if entity @s[scores={rpg_sq_mode=2}] run function rpg:squad/engage
execute if entity @s[scores={rpg_sq_mode=0}] run function rpg:squad/follow
# 姿态 1 是驻守：站着不动，什么都不做
