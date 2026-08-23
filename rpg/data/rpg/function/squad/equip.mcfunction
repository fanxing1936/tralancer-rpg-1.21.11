# 右键佣兵 —— 由 rpg:item/squad_equip 触发。
# 空手：把他手里那件收回来。拿着东西：换上去。潜行：解雇。
#
# 进度触发器不会告诉我们点的是哪一个，所以取身边最近的自己人 ——
# 你得贴着他才点得到，这个近似是安全的。
advancement revoke @s only rpg:item/squad_equip
execute if entity @s[scores={rpg_sq_t=1..}] run return 0
scoreboard players set @s rpg_sq_t 10
scoreboard players operation #sq rpg_squad = @s rpg_squad
tag @s add rpg.sq.boss
execute as @e[type=minecraft:husk,tag=rpg.squad,distance=..6,limit=1,sort=nearest] if score @s rpg_squad = #sq rpg_squad run function rpg:squad/on_member
tag @s remove rpg.sq.boss
