# 每 10 刻碾一次：生物受伤后约有 10 刻无敌帧，打得更密只是浪费。
scoreboard players set @s rpg_levi_beat 10
particle minecraft:flash{color:1195644} ~ ~0.8 ~ 0 0 0 0 1
particle splash ~ ~0.5 ~ 1 0.3 1 0.3 30
playsound minecraft:entity.player.attack.crit hostile @a[distance=..20] ~ ~ ~ 1 0.6
execute as @e[distance=..7,type=!player,type=!minecraft:item,type=!minecraft:experience_orb,type=!minecraft:marker] at @s run damage @s 6 minecraft:drown
execute as @e[distance=..7,type=!player,type=!minecraft:item,type=!minecraft:experience_orb,type=!minecraft:marker] at @s run particle dust_color_transition{from_color:8374496,to_color:532802,scale:2} ~ ~1 ~ 0.3 0.5 0.3 0.05 18
