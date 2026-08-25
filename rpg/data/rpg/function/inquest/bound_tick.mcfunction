scoreboard players add @s rpg_ex_hitcd 0
execute if score @s rpg_ex_hitcd matches 1.. run scoreboard players remove @s rpg_ex_hitcd 1
execute store result score @s rpg_ex_hp run data get entity @s Health 1
execute if score @s rpg_ex_hp matches ..419 if score @s rpg_ex_hitcd matches ..0 run function rpg:inquest/boss_hit
data merge entity @s {Health:420f,CustomNameVisible:1b}
effect give @s minecraft:resistance 2 3 true
effect give @s minecraft:slowness 2 255 true
effect give @s minecraft:glowing 2 0 true
effect clear @s minecraft:invisibility
function rpg:inquest/phase2/lock_boss
particle enchant ~ ~1 ~ 0.55 0.9 0.55 0.04 2 normal
scoreboard players set #anchor_found rpg_ex_tmp 0
tag @s add rpg.rite.subject
execute as @e[type=minecraft:item_display,tag=rpg.rite.anchor,distance=..14] if score @s rpg_rite_id = @e[type=minecraft:vindicator,tag=rpg.rite.subject,limit=1] rpg_rite_id run scoreboard players set #anchor_found rpg_ex_tmp 1
tag @s remove rpg.rite.subject
execute if score #anchor_found rpg_ex_tmp matches 0 run function rpg:inquest/fail
