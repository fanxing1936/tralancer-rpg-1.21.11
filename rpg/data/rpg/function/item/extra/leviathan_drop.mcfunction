# 锚咬住海床，漩涡张开。
summon minecraft:marker ~ ~ ~ {Tags:["rpg.levi.new"]}
execute unless entity @a[tag=rpg.levi.airborne,distance=..24] run scoreboard players set @e[type=minecraft:marker,tag=rpg.levi.new] rpg_levi_time 100
execute if entity @a[tag=rpg.levi.airborne,distance=..24] run scoreboard players set @e[type=minecraft:marker,tag=rpg.levi.new] rpg_levi_time 160
scoreboard players set @e[type=minecraft:marker,tag=rpg.levi.new] rpg_levi_beat 10
tag @e[type=minecraft:marker,tag=rpg.levi.new] add rpg.levi.anchor
tag @e[type=minecraft:marker,tag=rpg.levi.new] remove rpg.levi.new

particle minecraft:flash{color:8374496} ~ ~0.6 ~ 0 0 0 0 1
particle splash ~ ~0.4 ~ 1.2 0.3 1.2 0.4 60
particle bubble_column_up ~ ~ ~ 1.4 0.2 1.4 0.05 50
particle dust_color_transition{from_color:1195644,to_color:8374496,scale:2} ~ ~0.6 ~ 1.5 0.4 1.5 0.06 70
playsound minecraft:block.anvil_land hostile @a[distance=..28] ~ ~ ~ 1 0.5
playsound minecraft:entity.generic.splash hostile @a[distance=..24] ~ ~ ~ 1 0.6
