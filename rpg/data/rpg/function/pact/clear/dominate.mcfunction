# 打败了从自己身上挣出来的东西。
scoreboard players set @s rpg_pact_dom 1
scoreboard players set @s rpg_taint 0
scoreboard players set @s rpg_fall 0
tag @s remove rpg.taint.full
attribute @s minecraft:attack_damage modifier remove rpg:fall
function rpg:pact/attr
function rpg:pact/book/resync
playsound minecraft:block.end_portal.spawn master @s ~ ~ ~ 0.8 0.9
execute at @s run particle end_rod ~ ~1 ~ 0.6 0.8 0.6 0.2 60
execute if score @s rpg_pact matches 1 run function rpg:pact/clear/title1
execute if score @s rpg_pact matches 2 run function rpg:pact/clear/title2
execute if score @s rpg_pact matches 3 run function rpg:pact/clear/title3
execute if score @s rpg_pact matches 4 run function rpg:pact/clear/title4
execute if score @s rpg_pact matches 5 run function rpg:pact/clear/title5
execute if score @s rpg_pact matches 6 run function rpg:pact/clear/title6
execute if score @s rpg_pact matches 7 run function rpg:pact/clear/title7
