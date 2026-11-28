# 进镇标题（as/at 玩家）
scoreboard players set #w rpg_tw 0
execute in minecraft:overworld as @e[type=minecraft:marker,tag=rpg.tw.c,distance=..100,limit=1,sort=nearest] run scoreboard players operation #w rpg_tw = @s rpg_tw_id
execute if score #w rpg_tw = @s rpg_tw_at run return 0
scoreboard players operation @s rpg_tw_at = #w rpg_tw
execute if score #w rpg_tw matches 0 run return 0
function rpg:explore/town_visit
execute if score #w rpg_tw = @s rpg_tw_home run return run function rpg:town/title_home
function rpg:town/title
