# 盾碎：此后不再格挡，护甲归零。
tag @s add rpg.tg.broken
attribute @s minecraft:armor base set 0
execute on passengers if entity @s[tag=rpg.tg.p.shield] run data modify entity @s item.components."minecraft:item_model" set value "rpg:empty"
data merge entity @s {NoAI:1b}
scoreboard players set @s rpg_tg_st 5
scoreboard players set @s rpg_tg_ta 0
function rpg:tower_guard/anim/enter/shield_break
