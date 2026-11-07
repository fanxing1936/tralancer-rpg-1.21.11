# 判定：全场玩家先记上，站在圣所里的再摘掉。
execute at @e[type=minecraft:marker,tag=rpg.pf.center,limit=1] run tag @a[distance=..30,gamemode=!spectator,gamemode=!creative] add rpg.pf.doomed
execute as @e[type=minecraft:text_display,tag=rpg.pf.refuge] at @s run tag @a[distance=..4.0] remove rpg.pf.doomed
execute as @a[tag=rpg.pf.doomed] at @s run function rpg:pope_fight/boss/doom_hit
tag @a[tag=rpg.pf.doomed] remove rpg.pf.doomed
kill @e[type=minecraft:text_display,tag=rpg.pf.refuge]
kill @e[type=minecraft:item_display,tag=rpg.pf.refdisc]
execute at @e[type=minecraft:marker,tag=rpg.pf.center,limit=1] run particle flash{color:16773800} ~ ~1 ~ 0 0 0 0 1 normal
playsound minecraft:entity.lightning_bolt.thunder hostile @a[distance=..64] ~ ~ ~ 2 0.8
playsound minecraft:entity.generic.explode hostile @a[distance=..64] ~ ~ ~ 1.5 0.7
execute at @e[type=minecraft:marker,tag=rpg.pf.center,limit=1] rotated 0 0 positioned ^ ^ ^20 positioned over motion_blocking_no_leaves run function rpg:pope_fight/fx/pillar
execute at @e[type=minecraft:marker,tag=rpg.pf.center,limit=1] rotated 36 0 positioned ^ ^ ^20 positioned over motion_blocking_no_leaves run function rpg:pope_fight/fx/pillar
execute at @e[type=minecraft:marker,tag=rpg.pf.center,limit=1] rotated 72 0 positioned ^ ^ ^20 positioned over motion_blocking_no_leaves run function rpg:pope_fight/fx/pillar
execute at @e[type=minecraft:marker,tag=rpg.pf.center,limit=1] rotated 108 0 positioned ^ ^ ^20 positioned over motion_blocking_no_leaves run function rpg:pope_fight/fx/pillar
execute at @e[type=minecraft:marker,tag=rpg.pf.center,limit=1] rotated 144 0 positioned ^ ^ ^20 positioned over motion_blocking_no_leaves run function rpg:pope_fight/fx/pillar
execute at @e[type=minecraft:marker,tag=rpg.pf.center,limit=1] rotated 180 0 positioned ^ ^ ^20 positioned over motion_blocking_no_leaves run function rpg:pope_fight/fx/pillar
execute at @e[type=minecraft:marker,tag=rpg.pf.center,limit=1] rotated 216 0 positioned ^ ^ ^20 positioned over motion_blocking_no_leaves run function rpg:pope_fight/fx/pillar
execute at @e[type=minecraft:marker,tag=rpg.pf.center,limit=1] rotated 252 0 positioned ^ ^ ^20 positioned over motion_blocking_no_leaves run function rpg:pope_fight/fx/pillar
execute at @e[type=minecraft:marker,tag=rpg.pf.center,limit=1] rotated 288 0 positioned ^ ^ ^20 positioned over motion_blocking_no_leaves run function rpg:pope_fight/fx/pillar
execute at @e[type=minecraft:marker,tag=rpg.pf.center,limit=1] rotated 324 0 positioned ^ ^ ^20 positioned over motion_blocking_no_leaves run function rpg:pope_fight/fx/pillar
# 他也耗尽了：这几秒没有护甲，也不出手。
attribute @s minecraft:armor base set 0
function rpg:pope_fight/clip/idle
