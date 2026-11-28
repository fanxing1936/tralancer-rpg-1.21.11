# 新手开局结束（as 玩家，原来的「回到出生位置」换成这里）：去故乡（开局里抽到国家时就已经排上队）
scoreboard players operation @s rpg_tw_gm = @s rpg_ob_gm
execute unless score @s rpg_tw_home matches 1.. run function rpg:town/home/pick
function rpg:town/home/go
