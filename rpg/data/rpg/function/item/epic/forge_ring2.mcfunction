particle dust_color_transition{from_color:16553767,to_color:9445636,scale:2} ~ ~0.4 ~ 2.5 0.3 2.5 0.05 60
particle flame ~ ~0.4 ~ 2.5 0.2 2.5 0.02 30
playsound minecraft:entity.blaze.shoot player @a[distance=..20] ~ ~ ~ 0.8 1.1
execute as @e[distance=0.1..5,type=!player,type=!minecraft:item,type=!minecraft:experience_orb] at @s run damage @s 5 minecraft:player_attack by @p[tag=rpg.h.forge_tag1]
execute as @e[distance=0.1..5,type=!player,type=!minecraft:item,type=!minecraft:experience_orb] at @s run function rpg:item/epic/forge_push
