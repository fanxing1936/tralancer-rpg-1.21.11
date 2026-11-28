# 清除米迦勒战的全部实体：载体与部件、守望者、骨柱与特效；血条与音乐一起收掉。
tag @e[tag=rpg.unit,predicate=!rpg:in_prologue] remove rpg.mkb.hit
tag @e[tag=rpg.unit,predicate=!rpg:in_prologue] remove rpg.mkb.att
tag @e[tag=rpg.unit,predicate=!rpg:in_prologue] remove rpg.mkb.pend
scoreboard players reset @e[tag=rpg.unit,predicate=!rpg:in_prologue] rpg_mk_fl
scoreboard players reset @e[tag=rpg.unit,predicate=!rpg:in_prologue] rpg_mk_fu
scoreboard players reset @e[tag=rpg.unit,predicate=!rpg:in_prologue] rpg_mk_r
tag @e[tag=rpg.unit,predicate=!rpg:in_prologue] remove rpg.mkb.flamed
execute as @e[type=minecraft:vindicator,tag=rpg.mkb,tag=!rpg.mk.preview,predicate=!rpg:in_prologue] run function rpg:michael_boss/clear_unit
execute as @e[type=minecraft:vindicator,tag=rpg.mkb.w,predicate=!rpg:in_prologue] run function rpg:michael_boss/clear_unit
kill @e[type=minecraft:marker,tag=rpg.mkb.center,predicate=!rpg:in_prologue]
kill @e[type=minecraft:marker,tag=rpg.mkb.lag,predicate=!rpg:in_prologue]
kill @e[type=minecraft:marker,tag=rpg.mkb.last,predicate=!rpg:in_prologue]
scoreboard players set #ghost rpg_mk 0
kill @e[tag=rpg.mkb.fx,predicate=!rpg:in_prologue]
bossbar set rpg:michael_boss visible false
bossbar set rpg:michael_boss players
stopsound @a[predicate=!rpg:in_prologue] record rpg:bgm.michael1
stopsound @a[predicate=!rpg:in_prologue] record rpg:bgm.michael2
scoreboard players set #fight rpg_mk 0
scoreboard players set #stage rpg_mk 0
