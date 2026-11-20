# 清除米迦勒战的全部实体：载体与部件、守望者、骨柱与特效；血条与音乐一起收掉。
tag @e[tag=rpg.unit] remove rpg.mkb.hit
tag @e[tag=rpg.unit] remove rpg.mkb.att
tag @e[tag=rpg.unit] remove rpg.mkb.pend
scoreboard players reset @e[tag=rpg.unit] rpg_mk_fl
scoreboard players reset @e[tag=rpg.unit] rpg_mk_fu
scoreboard players reset @e[tag=rpg.unit] rpg_mk_r
tag @e[tag=rpg.unit] remove rpg.mkb.flamed
execute as @e[type=minecraft:vindicator,tag=rpg.mkb,tag=!rpg.mk.preview] run function rpg:michael_boss/clear_unit
execute as @e[type=minecraft:vindicator,tag=rpg.mkb.w] run function rpg:michael_boss/clear_unit
kill @e[type=minecraft:marker,tag=rpg.mkb.center]
kill @e[type=minecraft:marker,tag=rpg.mkb.lag]
kill @e[tag=rpg.mkb.fx]
bossbar set rpg:michael_boss visible false
bossbar set rpg:michael_boss players
stopsound @a record minecraft:boss1
stopsound @a record minecraft:boss2
scoreboard players set #fight rpg_mk 0
scoreboard players set #stage rpg_mk 0
