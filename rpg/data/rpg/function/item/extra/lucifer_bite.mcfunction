# 种下原罪：10 秒，期间受伤加重，并会向近旁蔓延
tag @s add rpg.luci.sin
scoreboard players set @s rpg_luci_sin 200
scoreboard players set @s rpg_luci_cd 0
effect give @s minecraft:poison 8 1 true
effect give @s minecraft:glowing 10 0 true
particle dust_color_transition{from_color:14344834,to_color:2257486,scale:2} ~ ~1 ~ 0.4 0.5 0.4 0.05 26
particle minecraft:flash{color:14344834} ~ ~1.1 ~ 0 0 0 0 1
playsound minecraft:entity.ender_dragon.hurt hostile @a[distance=..20] ~ ~ ~ 0.5 1.9
