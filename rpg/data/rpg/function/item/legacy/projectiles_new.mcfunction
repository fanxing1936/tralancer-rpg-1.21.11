# 首次见到箭时，优先读箭保存的发射武器快照；射后立即换手也不会丢技能。
execute as @e[type=#minecraft:arrows,tag=!rpg.legacy.seen,nbt={weapon:{components:{"minecraft:custom_data":{bubble_tag:1b}}}}] run tag @s add rpg.legacy.bubble
execute as @e[type=#minecraft:arrows,tag=!rpg.legacy.seen,nbt={weapon:{components:{"minecraft:custom_data":{burn_tag:1b}}}}] run tag @s add rpg.legacy.burn
execute as @e[type=#minecraft:arrows,tag=!rpg.legacy.seen,nbt={weapon:{components:{"minecraft:custom_data":{hunter_tag:1b}}}}] run tag @s add rpg.legacy.hunter
# 兼容没有 weapon 快照的旧世界箭：从实体自己的 origin 认领，而不是按附近玩家猜。
execute if entity @a[tag=rpg.h.bubble_tag1] as @e[type=#minecraft:arrows,tag=!rpg.legacy.seen,tag=!rpg.legacy.bubble] at @s on origin if entity @s[tag=rpg.h.bubble_tag1] run tag @e[type=#minecraft:arrows,distance=..0.01,limit=1,sort=nearest] add rpg.legacy.bubble
execute if entity @a[tag=rpg.h.burn_tag1] as @e[type=#minecraft:arrows,tag=!rpg.legacy.seen,tag=!rpg.legacy.burn] at @s on origin if entity @s[tag=rpg.h.burn_tag1] run tag @e[type=#minecraft:arrows,distance=..0.01,limit=1,sort=nearest] add rpg.legacy.burn
execute if entity @a[tag=rpg.h.hunter_tag1] as @e[type=#minecraft:arrows,tag=!rpg.legacy.seen,tag=!rpg.legacy.hunter] at @s on origin if entity @s[tag=rpg.h.hunter_tag1] run tag @e[type=#minecraft:arrows,distance=..0.01,limit=1,sort=nearest] add rpg.legacy.hunter
execute if entity @a[tag=rpg.h.hunter_tag1] as @e[type=#minecraft:arrows,tag=rpg.legacy.hunter,tag=!rpg.legacy.taxed] at @s on origin run damage @s 2 minecraft:magic
tag @e[type=#minecraft:arrows,tag=rpg.legacy.hunter] add rpg.legacy.taxed
tag @e[type=#minecraft:arrows,tag=rpg.legacy.bubble] add rpg.legacy.active
tag @e[type=#minecraft:arrows,tag=rpg.legacy.burn] add rpg.legacy.active
tag @e[type=#minecraft:arrows,tag=rpg.legacy.hunter] add rpg.legacy.active
tag @e[type=#minecraft:arrows,tag=!rpg.legacy.seen] add rpg.legacy.seen
