scoreboard players remove #rain rpg_pl 1
scoreboard players operation #q rpg_pl = #rain rpg_pl
scoreboard players set #2r rpg_pl 2
scoreboard players operation #q rpg_pl %= #2r rpg_pl
execute if score #q rpg_pl matches 0 in rpg:paradise_lost positioned 0 83 0 as @a[distance=0..] at @s run playsound minecraft:weather.rain weather @s ~ ~4 ~ 0.35 0.7
# 门外的怪：强化并补满一次
execute in rpg:paradise_lost positioned 0 83 0 as @e[type=#rpg:elite_pool,distance=38..,tag=!rpg.pl.r,tag=!rpg.pl.g] run function rpg:pl/rain/buff
execute in rpg:paradise_lost positioned 0 83 0 as @e[tag=rpg.pl.g,distance=38..,tag=!rpg.pl.r] run function rpg:pl/rain/buff_only
execute if score #rain rpg_pl matches 0 in rpg:paradise_lost positioned 0 83 0 run tellraw @a[distance=0..] ["",{"text":"〖失乐园・血雨〗","color":"#E0483C","bold":true,"italic":false},{"text":" 𝔅𝔩𝔬𝔬𝔡 ℜ𝔞𝔦𝔫","color":"#8F7430","bold":false,"italic":false},{"text":"  雨停了。","color":"#9C9A94","bold":false,"italic":false}]
