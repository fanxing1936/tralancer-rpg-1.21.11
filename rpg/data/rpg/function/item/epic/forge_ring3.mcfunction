particle dust_color_transition{from_color:16553767,to_color:9445636,scale:2} ~ ~0.4 ~ 3.5 0.3 3.5 0.05 80
particle flame ~ ~0.4 ~ 3.5 0.2 3.5 0.02 40
playsound minecraft:entity.blaze.shoot player @a[distance=..20] ~ ~ ~ 0.8 1.4
execute as @e[distance=0.1..7,type=!player,type=!minecraft:item,type=!minecraft:experience_orb] at @s run damage @s 5 minecraft:player_attack by @p[tag=rpg.h.forge_tag1]
execute as @e[distance=0.1..7,type=!player,type=!minecraft:item,type=!minecraft:experience_orb] at @s run function rpg:item/epic/forge_push
