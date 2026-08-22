# 环形寒潮：冻结、减速、外推。
scoreboard players set @s rpg_tide 0
particle dust_color_transition{from_color:[0.50,0.78,0.88],to_color:[0.90,0.98,1.0],scale:2} ~ ~0.6 ~ 3.2 0.4 3.2 0.06 120
particle snowflake ~ ~0.8 ~ 3 0.5 3 0.1 80
particle minecraft:flash{color:8374496} ~ ~1 ~ 0 0 0 0 1
playsound minecraft:block.glass.break player @a[distance=..20] ~ ~ ~ 1 0.7
playsound minecraft:entity.player.hurt_freeze player @a[distance=..20] ~ ~ ~ 1 0.9
execute as @e[distance=0.1..6,type=!player,type=!minecraft:item,type=!minecraft:experience_orb] at @s run effect give @s minecraft:slowness 6 4 true
execute as @e[distance=0.1..6,type=!player,type=!minecraft:item,type=!minecraft:experience_orb] at @s run effect give @s minecraft:mining_fatigue 6 2 true
execute as @e[distance=0.1..6,type=!player,type=!minecraft:item,type=!minecraft:experience_orb] at @s run damage @s 5 minecraft:freeze
execute as @e[distance=0.1..6,type=!player,type=!minecraft:item,type=!minecraft:experience_orb] at @s facing entity @p[tag=rpg.h.tide_tag1] feet run tp @s ^ ^ ^-0.9
