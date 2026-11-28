# 第一次到故乡（as 玩家）：圣火庇护开始，提示去找神父
execute if score @s rpg_tl_gift matches 1.. run return 0
execute unless entity @s[tag=rpg.tl.holy] unless score @s rpg_tl_born matches 1.. run function rpg:town/life/holy_start
tellraw @s ["",{"text":"〖城镇〗","color":"#C9A646","bold":true,"italic":false},{"text":"  去教堂门口找神父报到，他那里有给新人的东西。","color":"#E6DFCF","bold":false,"italic":false}]
