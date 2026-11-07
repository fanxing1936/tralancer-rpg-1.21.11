scoreboard players add @s rpg_pact_lv 1
scoreboard players set @s rpg_pact_bond 30
function rpg:pact/attr
function rpg:pact/book/resync
function rpg:hud/m82
playsound minecraft:block.end_portal.spawn master @s ~ ~ ~ 0.8 0.7
playsound minecraft:entity.wither.spawn master @a[distance=..32] ~ ~ ~ 0.4 1.4
execute at @s run particle sculk_charge_pop ~ ~1 ~ 0.5 0.8 0.5 0.1 60
execute if score @s rpg_pact matches 1 run function rpg:pact/up_title1
execute if score @s rpg_pact matches 2 run function rpg:pact/up_title2
execute if score @s rpg_pact matches 3 run function rpg:pact/up_title3
execute if score @s rpg_pact matches 4 run function rpg:pact/up_title4
execute if score @s rpg_pact matches 5 run function rpg:pact/up_title5
execute if score @s rpg_pact matches 6 run function rpg:pact/up_title6
execute if score @s rpg_pact matches 7 run function rpg:pact/up_title7
