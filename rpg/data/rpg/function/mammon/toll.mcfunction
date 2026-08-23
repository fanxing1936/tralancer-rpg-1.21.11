# 什一税。玛门从不白干活，每一箭都要拿走点什么 —— 掷点决定拿哪一样。
#
# 签了第七柱的人例外：他欠的不是钱，是魂。
execute if entity @s[tag=rpg.pact,scores={rpg_pact=7}] run return run function rpg:mammon/toll_pact

execute store result score #t rpg_mam run random value 1..100
execute if score #t rpg_mam matches 1..34 run return run function rpg:mammon/toll1
execute if score #t rpg_mam matches 35..58 run return run function rpg:mammon/toll2
execute if score #t rpg_mam matches 59..78 run return run function rpg:mammon/toll3
execute if score #t rpg_mam matches 79..92 run return run function rpg:mammon/toll4
function rpg:mammon/toll5
