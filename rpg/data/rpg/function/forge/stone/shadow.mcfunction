tag @s add rpg.fg.caster
scoreboard players set #i rpg_fg 24
execute anchored eyes positioned ^ ^ ^1 run function rpg:forge/stone/shadow_ray
execute unless entity @e[tag=rpg.fg.tgt] run scoreboard players set @s rpg_fg_en 100
execute unless entity @e[tag=rpg.fg.tgt] run tellraw @s ["",{"text":"[锻造]","color":"#E39745","bold":true,"italic":false},{"text":"　12 格内没有可以影步的目标，能量已退回","color":"#FF6B5E","italic":false}]
execute if entity @e[tag=rpg.fg.tgt] run particle minecraft:large_smoke ~ ~1 ~ 0.3 0.6 0.3 0.02 20
execute as @e[tag=rpg.fg.tgt,limit=1] at @s rotated as @s rotated ~ 0 positioned ^ ^ ^-1.6 run tp @a[tag=rpg.fg.caster,limit=1] ~ ~ ~ facing entity @s eyes
execute if entity @e[tag=rpg.fg.tgt] run scoreboard players set @s rpg_fg_shd 60
execute if entity @e[tag=rpg.fg.tgt] at @s run particle minecraft:reverse_portal ~ ~1 ~ 0.3 0.6 0.3 0.05 40
execute if entity @e[tag=rpg.fg.tgt] at @s run playsound minecraft:entity.enderman.teleport player @a[distance=..16] ~ ~ ~ 0.8 0.7
tag @e[tag=rpg.fg.tgt] remove rpg.fg.tgt
tag @s remove rpg.fg.caster
