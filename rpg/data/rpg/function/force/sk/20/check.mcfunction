# 不死（as 刚挨打的玩家；rpg:forge/hit/hurt_player 里调）
execute unless score @s rpg_force matches 2..3 run return 0
execute if score @s rpg_fo_und > #now rpg_fo run return 0
execute store result score #h rpg_fo run data get entity @s Health
execute unless score #h rpg_fo matches ..5 run return 0
effect give @s minecraft:resistance 3 4 true
effect give @s minecraft:regeneration 3 2 true
scoreboard players add @s rpg_taint 6
scoreboard players operation @s rpg_fo_und = #now rpg_fo
execute if score @s rpg_k20 matches 1 run scoreboard players add @s rpg_fo_und 3600
execute if score @s rpg_k20 matches 2 run scoreboard players add @s rpg_fo_und 3000
execute if score @s rpg_k20 matches 3 run scoreboard players add @s rpg_fo_und 2400
playsound minecraft:item.totem.use player @a[distance=..16] ~ ~ ~ 0.5 0.6
particle minecraft:soul ~ ~1 ~ 0.4 0.8 0.4 0.05 40
tellraw @s ["",{"text":"[力] ","color":"#C9A646","bold":true,"italic":false},{"text":"不死：","color":"#A276BE","bold":true,"italic":false},{"text":"你在致命的一击里撑住了。","color":"#E6DFCF","bold":false,"italic":false}]
