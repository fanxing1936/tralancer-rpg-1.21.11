execute if score @s rpg_pa_tsd matches ..40 if score @s rpg_pa_20 matches 1..899 run function rpg:paths/hermit_dead
execute if score @s rpg_pa_20 matches 900.. run return 0
execute unless entity @s[tag=rpg.pl.in] run return 0
execute if entity @a[distance=0.1..48,gamemode=!spectator] run return 0
execute in rpg:paradise_lost positioned 0 83 0 if entity @s[distance=561..] run scoreboard players add @s rpg_pa_20 1
execute if score @s rpg_pa_20 matches 900 run tellraw @s ["",{"text":"[路径] ","color":"#C9A646","bold":true,"italic":false},{"text":"隐者的十五分钟够了，","color":"#9C9A94","bold":false,"italic":false},{"text":"活着走出失乐园","color":"#C9A646","bold":true,"italic":false},{"text":"就算走完。","color":"#9C9A94","bold":false,"italic":false}]
