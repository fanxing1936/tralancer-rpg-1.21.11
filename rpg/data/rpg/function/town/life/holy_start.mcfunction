# 圣火庇护开始（as 玩家）
execute store result score @s rpg_tl_born run time query gametime
tag @s add rpg.tl.holy
tellraw @s ["",{"text":"〖城镇〗","color":"#C9A646","bold":true,"italic":false},{"text":"  教堂前的圣火护着你：受到的伤害降低，死去时东西不会掉，在故乡醒来。两个游戏日后，或到原质第 2 阶为止。","color":"#C9A646","bold":false,"italic":false}]
