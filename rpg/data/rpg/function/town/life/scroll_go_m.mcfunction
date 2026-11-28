$execute unless score #s$(i) rpg_tw matches 3 run return run tellraw @s ["",{"text":"〖城镇〗","color":"#C9A646","bold":true,"italic":false},{"text":"  故乡还没建起来，余烬没有地方可去。","color":"#FF6B5E","bold":false,"italic":false}]
clear @s minecraft:paper[minecraft:custom_data~{rpg_home:1b}] 1
particle minecraft:flame ~ ~1 ~ 0.3 0.6 0.3 0.05 30
function rpg:town/home/arrive
