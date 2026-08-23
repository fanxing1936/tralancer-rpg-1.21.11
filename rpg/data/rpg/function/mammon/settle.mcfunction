# @s 是射手。蓄力无论如何都清零 —— 下一箭重新攒。
scoreboard players set @s rpg_mam_c 0
execute if score #gold rpg_mam matches 1 run return run function rpg:mammon/buyout
function rpg:mammon/toll
