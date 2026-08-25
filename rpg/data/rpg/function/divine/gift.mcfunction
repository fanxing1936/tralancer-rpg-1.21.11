execute unless score @s rpg_lt_divine matches 2 run return run function rpg:divine/authority/no_covenant
execute unless score @s rpg_lt_auth matches 35.. run return run function rpg:divine/authority/insufficient
tag @a remove rpg.divine.gift.target
tag @s add rpg.divine.gift.giver
execute unless entity @a[tag=!rpg.divine.gift.giver,gamemode=!spectator,distance=..12,limit=1] run return run function rpg:divine/gift/no_target
tag @a[tag=!rpg.divine.gift.giver,gamemode=!spectator,distance=..12,sort=nearest,limit=1] add rpg.divine.gift.target
scoreboard players remove @s rpg_lt_auth 35
scoreboard players set @s rpg_lt_auth_t 0
execute as @a[tag=rpg.divine.gift.target,limit=1] at @s run function rpg:divine/gift/receive
tellraw @s ["",{"text":"[圣子恩赐] ","color":"#FFF2A8","bold":true,"italic":false},{"text":"生命已在","color":"gray","bold":false,"italic":false},{"selector":"@a[tag=rpg.divine.gift.target,limit=1]","color":"#E8F4FF","italic":false},{"text":"身上续行。","color":"gray","bold":false,"italic":false}]
particle minecraft:end_rod ~ ~1 ~ 0.5 0.8 0.5 0.05 28 force
playsound minecraft:block.beacon.activate player @s ~ ~ ~ 0.8 1.75
function rpg:hud/m64
tag @a[tag=rpg.divine.gift.target] remove rpg.divine.gift.target
tag @s remove rpg.divine.gift.giver
