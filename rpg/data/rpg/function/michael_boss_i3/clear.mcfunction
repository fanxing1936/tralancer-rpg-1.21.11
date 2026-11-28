# 清除米迦勒战的全部实体：载体与部件、守望者、骨柱与特效；血条与音乐一起收掉。
tag @e[tag=rpg.unit,distance=0..] remove rpg.mkb.hit
tag @e[tag=rpg.unit,distance=0..] remove rpg.mkb.att
tag @e[tag=rpg.unit,distance=0..] remove rpg.mkb.pend
scoreboard players reset @e[tag=rpg.unit,distance=0..] rpg_mk_fl
scoreboard players reset @e[tag=rpg.unit,distance=0..] rpg_mk_fu
scoreboard players reset @e[tag=rpg.unit,distance=0..] rpg_mk_r
tag @e[tag=rpg.unit,distance=0..] remove rpg.mkb.flamed
execute as @e[type=minecraft:vindicator,tag=rpg.mkb,tag=!rpg.mk.preview,distance=0..] run function rpg:michael_boss_i3/clear_unit
execute as @e[type=minecraft:vindicator,tag=rpg.mkb.w,distance=0..] run function rpg:michael_boss_i3/clear_unit
kill @e[type=minecraft:marker,tag=rpg.mkb.center,distance=0..]
kill @e[type=minecraft:marker,tag=rpg.mkb.lag,distance=0..]
kill @e[type=minecraft:marker,tag=rpg.mkb.last,distance=0..]
scoreboard players set #ghost rpg_mk_i3 0
kill @e[tag=rpg.mkb.fx,distance=0..]
bossbar set rpg:michael_boss_i3 visible false
bossbar set rpg:michael_boss_i3 players
stopsound @a[distance=0..] record rpg:bgm.michael1
stopsound @a[distance=0..] record rpg:bgm.michael2
scoreboard players set #fight rpg_mk_i3 0
scoreboard players set #stage rpg_mk_i3 0
