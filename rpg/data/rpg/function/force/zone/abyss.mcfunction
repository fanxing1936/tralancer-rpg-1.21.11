tp @s ~ ~ ~ ~-20 0
particle minecraft:reverse_portal ^ ^0.1 ^2.5 0 0 0 0.02 3 force
particle minecraft:reverse_portal ^ ^0.1 ^-2.5 0 0 0 0.02 3 force
particle minecraft:squid_ink ~ ~0.1 ~ 0.6 0 0.6 0.01 2
particle minecraft:sculk_soul ~ ~0.3 ~ 1.5 0.1 1.5 0.01 1
execute as @e[type=#rpg:seal_hostile,tag=!rpg.ally,tag=!rpg.pope,tag=!rpg.mkb,tag=!rpg.jqb,tag=!rpg.lub,tag=!rpg.slb,tag=!rpg.usb,distance=0.8..3.5] at @s facing entity @e[type=minecraft:marker,tag=rpg.fo.zone,limit=1,sort=nearest] feet run tp @s ^ ^ ^0.18
execute unless score #zt rpg_fo matches 0 run return 0
scoreboard players operation #zt rpg_fo = @s rpg_fo_end
scoreboard players operation #zt rpg_fo -= #now rpg_fo
scoreboard players operation #zt rpg_fo %= #20 rpg_fo
execute unless score #zt rpg_fo matches 0 run return 0
execute if score #lv rpg_fo matches 1 run scoreboard players set #dmg rpg_fo 20
execute if score #lv rpg_fo matches 2 run scoreboard players set #dmg rpg_fo 30
execute if score #lv rpg_fo matches 3 run scoreboard players set #dmg rpg_fo 40
scoreboard players set #hm rpg_fo 10
execute as @e[type=#rpg:seal_hostile,tag=!rpg.ally,distance=..3.5] at @s run function rpg:force/hit
effect give @e[type=#rpg:seal_hostile,tag=!rpg.ally,distance=..3.5] minecraft:slowness 1 1 true
