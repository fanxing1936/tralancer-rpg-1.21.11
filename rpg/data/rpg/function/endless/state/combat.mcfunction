scoreboard players add @s rpg_end_time 1
function rpg:endless/enemy/refresh
tp @e[tag=rpg.end.enemy.current,distance=48.01..] ~ ~1 ~
execute store result score #alive rpg_end_tmp if entity @e[tag=rpg.end.enemy.current]
execute store result bossbar rpg:endless value run scoreboard players get #alive rpg_end_tmp
bossbar set rpg:endless name ["",{"text":"回廊清剿｜第 ","color":"#D4AF37","bold":true,"italic":false},{"score":{"name":"#floor","objective":"rpg_end_tmp"},"color":"#FFF2A8","bold":true,"italic":false},{"text":" 层　剩余 ","color":"#AAB4C3","bold":false,"italic":false},{"score":{"name":"#alive","objective":"rpg_end_tmp"},"color":"#FF665E","bold":true,"italic":false}]
execute if score @s rpg_end_time matches 20.. unless entity @e[tag=rpg.end.enemy.current,limit=1] run function rpg:endless/floor/clear
