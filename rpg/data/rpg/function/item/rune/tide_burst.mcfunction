# 施法者标签只在本次同步调用内存活；内层把 @s 换成受击者后，
# 仍能精确找回真正施法者，不会把伤害记给站得更近的同款持有者。
tag @s add rpg.tide.cast
# 环形寒潮：冻结、减速、外推。
scoreboard players set @s rpg_tide 0
particle dust_color_transition{from_color:[0.50,0.78,0.88],to_color:[0.90,0.98,1.0],scale:2} ~ ~0.6 ~ 3.2 0.4 3.2 0.06 120
particle snowflake ~ ~0.8 ~ 3 0.5 3 0.1 80
particle minecraft:flash{color:8374496} ~ ~1 ~ 0 0 0 0 1
playsound minecraft:block.glass.break player @a[distance=..20] ~ ~ ~ 1 0.7
playsound minecraft:entity.player.hurt_freeze player @a[distance=..20] ~ ~ ~ 1 0.9
execute as @e[distance=0.1..6,type=!player,type=!minecraft:item,type=!minecraft:experience_orb] at @s run effect give @s minecraft:slowness 6 4 true
execute as @e[distance=0.1..6,type=!player,type=!minecraft:item,type=!minecraft:experience_orb] at @s run effect give @s minecraft:mining_fatigue 6 2 true
execute as @e[distance=0.1..6,type=!player,type=!minecraft:item,type=!minecraft:experience_orb] at @s run damage @s 5 minecraft:freeze by @a[tag=rpg.tide.cast,limit=1]
execute as @e[distance=0.1..6,type=!player,type=!minecraft:item,type=!minecraft:experience_orb] at @s facing entity @a[tag=rpg.tide.cast,limit=1] feet run tp @s ^ ^ ^-0.9
tag @s remove rpg.tide.cast
