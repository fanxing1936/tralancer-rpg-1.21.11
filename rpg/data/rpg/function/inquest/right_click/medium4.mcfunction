function rpg:inquest/tool/place/medium4
tag @s add rpg.rite.medium
scoreboard players add @s rpg_ex_stab 25
execute if score @s rpg_ex_stab matches 101.. run scoreboard players set @s rpg_ex_stab 100
clear @a[tag=rpg.rite.user,distance=..6,limit=1] minecraft:paper[minecraft:custom_data~{rpg_medium:4b}] 1
scoreboard players add @a[tag=rpg.rite.user,distance=..6,limit=1] rpg_ex_xp 6
tag @a[tag=rpg.rite.user,distance=..6] remove rpg.rite.user
function rpg:inquest/stability/show
tellraw @a[distance=..16,gamemode=!spectator] ["",{"text":"[弱点媒介] ","color":"#5A6B1E","italic":false,"bold":true},{"text":"毒马铃薯 · 腐宴残食已布入法阵。","color":"gray","italic":false}]
