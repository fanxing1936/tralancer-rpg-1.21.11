# 右键了镇上的人或告示板（as/at 玩家）
advancement revoke @s only rpg:town/talk
scoreboard players set #role rpg_tl 0
scoreboard players set #folk rpg_tl 0
execute as @e[tag=rpg.tnpc,distance=..8,limit=1,sort=nearest] run function rpg:town/life/whoami
execute if score #role rpg_tl matches 0 run return 0
scoreboard players operation @s rpg_tl_t = #t rpg_tl
scoreboard players enable @s rpg_tl_do
execute if score #role rpg_tl matches 1 run return run function rpg:town/life/d/priest
execute if score #role rpg_tl matches 2 run return run function rpg:town/life/d/elder
execute if score #role rpg_tl matches 3 run return run function rpg:town/life/d/bard
execute if score #role rpg_tl matches 4 run return run function rpg:town/life/d/watchman
execute if score #role rpg_tl matches 5 run return run function rpg:town/life/d/child
execute if score #role rpg_tl matches 6 run return run function rpg:town/life/d/board
execute if score #role rpg_tl matches 7 run return run function rpg:town/life/d/folk
execute if score #role rpg_tl matches 8 if score #run rpg_te matches 1.. if score #kind rpg_te matches 3 run return run function rpg:town/ev/w/hood_talk
execute if score #role rpg_tl matches 9 if score #run rpg_te matches 1.. run return run function rpg:town/ev/w/witch_talk
execute if score #role rpg_tl matches 9 run return run function rpg:town/demon/witch_talk
execute if score #role rpg_tl matches 8 run return run function rpg:town/demon/hood_talk
execute if score #role rpg_tl matches 10 run return run function rpg:town/demon/altar
