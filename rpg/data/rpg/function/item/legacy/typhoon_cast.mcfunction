# 风之回响 · 狂风：三道横列风路，无 armor_stand、无 @p 定向。
scoreboard players set @s rpg_wind_chg 31
tag @a[tag=rpg.wind.source] remove rpg.wind.source
tag @s add rpg.wind.source
execute at @s positioned ^-2 ^ ^2 run function rpg:item/legacy/wind_lane
execute at @s positioned ^ ^ ^2 run function rpg:item/legacy/wind_lane
execute at @s positioned ^2 ^ ^2 run function rpg:item/legacy/wind_lane
tag @s remove rpg.wind.source
playsound minecraft:entity.breeze.shoot player @a[distance=..24] ~ ~ ~ 1 0.7
function rpg:hud/m12
