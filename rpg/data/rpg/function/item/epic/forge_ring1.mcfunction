# 施法者标签只在本次同步调用内存活；内层把 @s 换成受击者后，
# 仍能精确找回真正施法者，不会把伤害记给站得更近的同款持有者。
tag @s add rpg.forge.cast
particle dust_color_transition{from_color:16553767,to_color:9445636,scale:2} ~ ~0.4 ~ 1.5 0.3 1.5 0.05 40
particle flame ~ ~0.4 ~ 1.5 0.2 1.5 0.02 20
playsound minecraft:entity.blaze.shoot player @a[distance=..20] ~ ~ ~ 0.8 0.8
execute as @e[distance=0.1..3,type=!player,type=!minecraft:item,type=!minecraft:experience_orb] at @s run damage @s 5 minecraft:player_attack by @a[tag=rpg.forge.cast,limit=1]
execute as @e[distance=0.1..3,type=!player,type=!minecraft:item,type=!minecraft:experience_orb] at @s run function rpg:item/epic/forge_push
tag @s remove rpg.forge.cast
