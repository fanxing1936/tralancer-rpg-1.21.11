# 清除扫罗战的全部实体：载体与部件、幻影、碎甲、蛛网与特效；血条与音乐一起收掉。
tag @e[tag=rpg.unit] remove rpg.slb.hit
tag @e[tag=rpg.unit] remove rpg.slb.failed
tag @e[tag=rpg.unit] remove rpg.slb.att
execute as @e[type=minecraft:vindicator,tag=rpg.slb,tag=!rpg.slb.preview] run function rpg:saul_boss/clear_unit
execute as @e[type=minecraft:vindicator,tag=rpg.slg] run function rpg:saul_boss/clear_unit
kill @e[type=minecraft:marker,tag=rpg.slb.center]
kill @e[tag=rpg.slb.fx]
bossbar set rpg:saul_boss visible false
bossbar set rpg:saul_boss players
stopsound @a record minecraft:boss1
stopsound @a record minecraft:boss2
scoreboard players set #fight rpg_sl 0
scoreboard players set #stage rpg_sl 0
