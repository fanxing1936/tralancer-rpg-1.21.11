function rpg:inquest/tool/place/nail
tag @s add rpg.rite.nailed
scoreboard players add @s rpg_ex_stab 20
execute if score @s rpg_ex_stab matches 101.. run scoreboard players set @s rpg_ex_stab 100
clear @a[tag=rpg.rite.user,distance=..6,limit=1] minecraft:paper[minecraft:custom_data~{rpg_nail:1b}] 1
scoreboard players add @a[tag=rpg.rite.user,distance=..6,limit=1] rpg_ex_xp 3
tag @a[tag=rpg.rite.user,distance=..6] remove rpg.rite.user
function rpg:inquest/stability/show
playsound minecraft:block.anvil.place player @a[distance=..16] ~ ~ ~ 0.7 1.8
