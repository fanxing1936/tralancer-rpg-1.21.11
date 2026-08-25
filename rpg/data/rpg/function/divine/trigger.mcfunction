advancement revoke @s only rpg:divine/covenant
execute if score @s rpg_lt_div_t matches 1.. run return 0
scoreboard players set @s rpg_lt_div_t 8
execute if score @s rpg_lt_divine matches 0 run return run function rpg:divine/sign
execute unless items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_divine_signed:1b}] run return run function rpg:divine/reissue
execute if entity @e[type=minecraft:item_display,tag=rpg.totem.lit,distance=..6,limit=1] run return run function rpg:divine/renounce
execute if score @s rpg_lt_div_cd matches 1.. run return run function rpg:divine/cooling
execute if score @s rpg_lt_divine matches 1 run return run function rpg:divine/invoke_old
execute if score @s rpg_lt_divine matches 2 run return run function rpg:divine/invoke_new
