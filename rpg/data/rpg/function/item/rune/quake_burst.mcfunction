# 施法者标签只在本次同步调用内存活；内层把 @s 换成受击者后，
# 仍能精确找回真正施法者，不会把伤害记给站得更近的同款持有者。
tag @s add rpg.quake.cast
# 砸地：环形击飞并致盲。
scoreboard players set @s rpg_quake 0
particle block{block_state:"minecraft:deepslate"} ~ ~0.2 ~ 3 0.2 3 1 160
particle explosion ~ ~0.4 ~ 1.5 0.2 1.5 0 8
particle dust_color_transition{from_color:[0.73,0.54,0.27],to_color:[0.35,0.28,0.18],scale:3} ~ ~0.6 ~ 3 0.4 3 0.05 90
playsound minecraft:item.mace.smash_ground_heavy player @a[distance=..24] ~ ~ ~ 1 0.7
playsound minecraft:entity.generic.explode player @a[distance=..24] ~ ~ ~ 0.7 0.6
execute as @e[distance=0.1..6,type=!player,type=!minecraft:item,type=!minecraft:experience_orb] at @s run damage @s 8 minecraft:player_attack by @a[tag=rpg.quake.cast,limit=1]
execute as @e[distance=0.1..6,type=!player,type=!minecraft:item,type=!minecraft:experience_orb] at @s run effect give @s minecraft:blindness 5 0 true
execute as @e[distance=0.1..6,type=!player,type=!minecraft:item,type=!minecraft:experience_orb] at @s run data merge entity @s {Motion:[0d,0.85d,0d]}
tag @s remove rpg.quake.cast
