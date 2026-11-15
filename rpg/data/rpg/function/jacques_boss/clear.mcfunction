# 清除雅克战的全部实体：载体与部件、大卫的幽灵、召来的圣卫、特效；诅咒印记与血条一起收掉。
execute as @e[tag=rpg.unit,tag=rpg.jqb.cursed] run function rpg:jacques_boss/curse/clear
tag @e[tag=rpg.unit] remove rpg.jqb.hit
tag @e[tag=rpg.unit] remove rpg.jqb.rolled
execute as @e[type=minecraft:vindicator,tag=rpg.jqb,tag=!rpg.jqb.preview] run function rpg:jacques_boss/clear_unit
execute as @e[type=minecraft:vindicator,tag=rpg.jqd] run function rpg:jacques_boss/clear_unit
execute as @e[tag=rpg.jqb.guard] run function rpg:holy_guard/remove
kill @e[type=minecraft:marker,tag=rpg.jqb.center]
kill @e[tag=rpg.jqb.fx]
bossbar set rpg:jacques_boss visible false
bossbar set rpg:jacques_boss players
stopsound @a record minecraft:boss1
stopsound @a record minecraft:boss3
scoreboard players set #fight rpg_jq 0
scoreboard players set #stage rpg_jq 0
