# 施法者标签只在本次同步调用内存活；内层把 @s 换成受击者后，
# 仍能精确找回真正施法者，不会把伤害记给站得更近的同款持有者。
tag @s add rpg.shade.cast
# 噬影：遁入影中，出现在最近敌人背后并重创。
# `facing entity … ` 后再 `^ ^ ^1.2` 就是"绕到它背后一步"。
scoreboard players set @s rpg_shade 0
particle smoke ~ ~1 ~ 0.4 0.7 0.4 0.05 40
particle dust_color_transition{from_color:[0.42,0.31,0.63],to_color:[0.08,0.05,0.14],scale:2} ~ ~1 ~ 0.5 0.8 0.5 0.05 60
playsound minecraft:entity.enderman.teleport player @a[distance=..20] ~ ~ ~ 1 0.8
execute if entity @e[distance=0.1..14,type=!player,type=!minecraft:item,type=!minecraft:experience_orb,limit=1,sort=nearest] at @s facing entity @e[distance=0.1..14,type=!player,type=!minecraft:item,type=!minecraft:experience_orb,limit=1,sort=nearest] feet positioned ^ ^ ^1.2 run tp @s ~ ~ ~
execute as @e[distance=0.1..3,type=!player,type=!minecraft:item,type=!minecraft:experience_orb,limit=1,sort=nearest] at @s run damage @s 12 minecraft:magic by @a[tag=rpg.shade.cast,limit=1]
execute as @e[distance=0.1..3,type=!player,type=!minecraft:item,type=!minecraft:experience_orb,limit=1,sort=nearest] at @s run particle minecraft:flash{color:7032224} ~ ~1 ~ 0 0 0 0 1
execute at @s run particle smoke ~ ~1 ~ 0.4 0.7 0.4 0.05 40
playsound minecraft:entity.player.attack.crit player @a[distance=..20] ~ ~ ~ 1 0.7
tag @s remove rpg.shade.cast
