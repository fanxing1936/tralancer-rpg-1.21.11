# 跟随。近了就站着，远了就走过去，掉队太远直接归队。
# 踩进水里也直接召回：尸壳泡水会转化成普通僵尸，而转化是**换一个实体** ——
# 标签和记分板一起没了，队员就这么凭空消失。所以佣兵不下水。
execute if block ~ ~ ~ water unless entity @a[tag=rpg.sq.boss,distance=..3] run tp @s @a[tag=rpg.sq.boss,limit=1]
execute if entity @a[tag=rpg.sq.boss,distance=34..] run tp @s @a[tag=rpg.sq.boss,limit=1]
execute if entity @s[scores={rpg_sq_slot=0}] if entity @a[tag=rpg.sq.boss,distance=2.6..] run return run function rpg:squad/walk_boss0
execute if entity @s[scores={rpg_sq_slot=1}] if entity @a[tag=rpg.sq.boss,distance=3.4..] run return run function rpg:squad/walk_boss1
execute if entity @s[scores={rpg_sq_slot=2}] if entity @a[tag=rpg.sq.boss,distance=4.2..] run return run function rpg:squad/walk_boss2
execute if entity @s[scores={rpg_sq_slot=3}] if entity @a[tag=rpg.sq.boss,distance=5.0..] run return run function rpg:squad/walk_boss3
execute unless score @s rpg_sq_slot = @s rpg_sq_slot if entity @a[tag=rpg.sq.boss,distance=2.6..] run function rpg:squad/walk_boss0
