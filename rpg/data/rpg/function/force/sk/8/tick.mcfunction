# 殉道（as/at 施放者，每刻）：8 格内队友的抗性挡下多少，按比例算到施放者头上
execute if score @s rpg_fo_mt <= #now rpg_fo run return run scoreboard players set @s rpg_fo_mt 0
particle minecraft:end_rod ~ ~1.2 ~ 0.3 0.5 0.3 0 1
tag @s add rpg.fo.mtc
scoreboard players operation #zt rpg_fo = #now rpg_fo
scoreboard players operation #zt rpg_fo %= #10 rpg_fo
execute if score #zt rpg_fo matches 0 run effect give @a[distance=..8,tag=!rpg.fo.mtc,gamemode=!spectator] minecraft:resistance 1 2 true
execute if score #zt rpg_fo matches 0 as @a[distance=..8,tag=!rpg.fo.mtc,gamemode=!spectator] at @s run particle minecraft:end_rod ~ ~2.2 ~ 0.1 0.1 0.1 0 1
scoreboard players set #x rpg_fo 0
execute as @a[distance=..8,tag=!rpg.fo.mtc,scores={rpg_fo_dr=1..}] run function rpg:force/sk/8/sum
tag @s remove rpg.fo.mtc
execute unless score #x rpg_fo matches 1.. run return 0
scoreboard players operation #dmg rpg_fo = #x rpg_fo
execute if score @s rpg_fo_mlv matches 1 run scoreboard players set #pc rpg_fo 60
execute if score @s rpg_fo_mlv matches 2 run scoreboard players set #pc rpg_fo 50
execute if score @s rpg_fo_mlv matches 3 run scoreboard players set #pc rpg_fo 40
scoreboard players operation #dmg rpg_fo *= #pc rpg_fo
scoreboard players operation #dmg rpg_fo /= #100 rpg_fo
scoreboard players set #hm rpg_fo 10
execute if score #dmg rpg_fo matches 1.. run function rpg:force/hit
