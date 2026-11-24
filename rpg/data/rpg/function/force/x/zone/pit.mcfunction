particle minecraft:sculk_soul ~ ~0.2 ~ 2.5 0.1 2.5 0.01 2
particle minecraft:ash ~ ~0.5 ~ 2.5 0.4 2.5 0 6
effect give @e[type=#rpg:seal_hostile,tag=!rpg.ally,distance=..5] minecraft:slowness 1 3 true
execute as @e[type=#rpg:seal_hostile,tag=!rpg.ally,tag=!rpg.pope,tag=!rpg.mkb,tag=!rpg.jqb,tag=!rpg.lub,tag=!rpg.slb,tag=!rpg.usb,distance=..5] at @s if block ~ ~-0.2 ~ #rpg:force/pass run tp @s ~ ~-0.05 ~
execute unless score #zt rpg_fo matches 0 run return 0
scoreboard players operation #zt rpg_fo = @s rpg_fo_end
scoreboard players operation #zt rpg_fo -= #now rpg_fo
scoreboard players operation #zt rpg_fo %= #20 rpg_fo
execute unless score #zt rpg_fo matches 0 run return 0
scoreboard players set #dmg rpg_fo 30
scoreboard players set #hm rpg_fo 10
execute as @e[type=#rpg:seal_hostile,tag=!rpg.ally,distance=..5] at @s run function rpg:force/hit
