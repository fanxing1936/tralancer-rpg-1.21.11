function rpg:inquest/tool/place/chalk3
tag @s add rpg.layout.haste
scoreboard players remove @s rpg_ex_slots 1
scoreboard players add @s rpg_ex_stab 10
execute if score @s rpg_ex_stab matches 101.. run scoreboard players set @s rpg_ex_stab 100
clear @a[tag=rpg.rite.user,distance=..6,limit=1] minecraft:paper[minecraft:custom_data~{rpg_chalk:3b}] 1
scoreboard players add @a[tag=rpg.rite.user,distance=..6,limit=1] rpg_ex_xp 2
tag @a[tag=rpg.rite.user,distance=..6] remove rpg.rite.user
function rpg:inquest/stability/show
playsound minecraft:block.calcite.place player @a[distance=..16] ~ ~ ~ 0.8 1.4
