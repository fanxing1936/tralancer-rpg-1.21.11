function rpg:inquest/tool/place/incense
scoreboard players set @s rpg_ex_toolcd 200
scoreboard players add @s rpg_ex_stab 15
execute if score @s rpg_ex_stab matches 101.. run scoreboard players set @s rpg_ex_stab 100
clear @a[tag=rpg.rite.user,distance=..6,limit=1] minecraft:paper[minecraft:custom_data~{rpg_incense:1b}] 1
effect clear @a[distance=..6,gamemode=!spectator] minecraft:slowness
effect clear @a[distance=..6,gamemode=!spectator] minecraft:weakness
effect clear @a[distance=..6,gamemode=!spectator] minecraft:blindness
effect clear @a[distance=..6,gamemode=!spectator] minecraft:darkness
effect clear @a[distance=..6,gamemode=!spectator] minecraft:nausea
tag @a[tag=rpg.rite.user,distance=..6] remove rpg.rite.user
function rpg:inquest/stability/show
particle campfire_cosy_smoke ~ ~0.4 ~ 1.2 0.3 1.2 0.03 35 force
