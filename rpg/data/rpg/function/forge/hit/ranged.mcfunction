execute if entity @a[tag=rpg.fg.atk,tag=rpg.fg.r.hunt] run function rpg:forge/rune/hunt_mark
execute if entity @a[tag=rpg.fg.atk,tag=rpg.fg.r.split,scores={rpg_fg_crit=1..}] run function rpg:forge/rune/split
# 见闻录（add_explore.py）：怪物情报 +5%、武器熟练
execute if entity @s[type=minecraft:zombie] if entity @a[tag=rpg.fg.atk,tag=rpg.in.zombie] run scoreboard players add #pct rpg_fg 5
execute if entity @s[type=minecraft:husk] if entity @a[tag=rpg.fg.atk,tag=rpg.in.husk] run scoreboard players add #pct rpg_fg 5
execute if entity @s[type=minecraft:drowned] if entity @a[tag=rpg.fg.atk,tag=rpg.in.drowned] run scoreboard players add #pct rpg_fg 5
execute if entity @s[type=minecraft:skeleton] if entity @a[tag=rpg.fg.atk,tag=rpg.in.skeleton] run scoreboard players add #pct rpg_fg 5
execute if entity @s[type=minecraft:stray] if entity @a[tag=rpg.fg.atk,tag=rpg.in.stray] run scoreboard players add #pct rpg_fg 5
execute if entity @s[type=minecraft:bogged] if entity @a[tag=rpg.fg.atk,tag=rpg.in.bogged] run scoreboard players add #pct rpg_fg 5
execute if entity @s[type=minecraft:spider] if entity @a[tag=rpg.fg.atk,tag=rpg.in.spider] run scoreboard players add #pct rpg_fg 5
execute if entity @s[type=minecraft:cave_spider] if entity @a[tag=rpg.fg.atk,tag=rpg.in.cave_spider] run scoreboard players add #pct rpg_fg 5
execute if entity @s[type=minecraft:creeper] if entity @a[tag=rpg.fg.atk,tag=rpg.in.creeper] run scoreboard players add #pct rpg_fg 5
execute if entity @s[type=minecraft:enderman] if entity @a[tag=rpg.fg.atk,tag=rpg.in.enderman] run scoreboard players add #pct rpg_fg 5
execute if entity @s[type=minecraft:witch] if entity @a[tag=rpg.fg.atk,tag=rpg.in.witch] run scoreboard players add #pct rpg_fg 5
execute if entity @s[type=minecraft:pillager] if entity @a[tag=rpg.fg.atk,tag=rpg.in.pillager] run scoreboard players add #pct rpg_fg 5
execute if entity @s[type=minecraft:vindicator] if entity @a[tag=rpg.fg.atk,tag=rpg.in.vindicator] run scoreboard players add #pct rpg_fg 5
execute if entity @s[type=minecraft:evoker] if entity @a[tag=rpg.fg.atk,tag=rpg.in.evoker] run scoreboard players add #pct rpg_fg 5
execute if entity @s[type=minecraft:ravager] if entity @a[tag=rpg.fg.atk,tag=rpg.in.ravager] run scoreboard players add #pct rpg_fg 5
execute if entity @s[type=minecraft:phantom] if entity @a[tag=rpg.fg.atk,tag=rpg.in.phantom] run scoreboard players add #pct rpg_fg 5
execute if entity @s[type=minecraft:slime] if entity @a[tag=rpg.fg.atk,tag=rpg.in.slime] run scoreboard players add #pct rpg_fg 5
execute if entity @s[type=minecraft:silverfish] if entity @a[tag=rpg.fg.atk,tag=rpg.in.silverfish] run scoreboard players add #pct rpg_fg 5
execute if entity @s[type=minecraft:blaze] if entity @a[tag=rpg.fg.atk,tag=rpg.in.blaze] run scoreboard players add #pct rpg_fg 5
execute if entity @s[type=minecraft:wither_skeleton] if entity @a[tag=rpg.fg.atk,tag=rpg.in.wither_skeleton] run scoreboard players add #pct rpg_fg 5
execute if entity @s[type=minecraft:magma_cube] if entity @a[tag=rpg.fg.atk,tag=rpg.in.magma_cube] run scoreboard players add #pct rpg_fg 5
execute if entity @s[type=minecraft:ghast] if entity @a[tag=rpg.fg.atk,tag=rpg.in.ghast] run scoreboard players add #pct rpg_fg 5
execute if entity @s[type=minecraft:piglin_brute] if entity @a[tag=rpg.fg.atk,tag=rpg.in.piglin_brute] run scoreboard players add #pct rpg_fg 5
execute if entity @s[type=minecraft:hoglin] if entity @a[tag=rpg.fg.atk,tag=rpg.in.hoglin] run scoreboard players add #pct rpg_fg 5
execute if entity @s[type=minecraft:guardian] if entity @a[tag=rpg.fg.atk,tag=rpg.in.guardian] run scoreboard players add #pct rpg_fg 5
execute if entity @s[type=minecraft:breeze] if entity @a[tag=rpg.fg.atk,tag=rpg.in.breeze] run scoreboard players add #pct rpg_fg 5
execute if items entity @a[tag=rpg.fg.atk,limit=1] weapon.mainhand minecraft:bow run scoreboard players add @a[tag=rpg.fg.atk] rpg_ms_bow 1
execute if items entity @a[tag=rpg.fg.atk,limit=1] weapon.mainhand minecraft:bow if entity @a[tag=rpg.fg.atk,tag=rpg.ms.bow1] run scoreboard players add #pct rpg_fg 3
execute if items entity @a[tag=rpg.fg.atk,limit=1] weapon.mainhand minecraft:bow if entity @a[tag=rpg.fg.atk,tag=rpg.ms.bow2] run scoreboard players add #pct rpg_fg 3
execute if items entity @a[tag=rpg.fg.atk,limit=1] weapon.mainhand minecraft:bow if entity @a[tag=rpg.fg.atk,tag=rpg.ms.bow3] run scoreboard players add #pct rpg_fg 3
execute if items entity @a[tag=rpg.fg.atk,limit=1] weapon.mainhand minecraft:crossbow run scoreboard players add @a[tag=rpg.fg.atk] rpg_ms_crossbow 1
execute if items entity @a[tag=rpg.fg.atk,limit=1] weapon.mainhand minecraft:crossbow if entity @a[tag=rpg.fg.atk,tag=rpg.ms.crossbow1] run scoreboard players add #pct rpg_fg 3
execute if items entity @a[tag=rpg.fg.atk,limit=1] weapon.mainhand minecraft:crossbow if entity @a[tag=rpg.fg.atk,tag=rpg.ms.crossbow2] run scoreboard players add #pct rpg_fg 3
execute if items entity @a[tag=rpg.fg.atk,limit=1] weapon.mainhand minecraft:crossbow if entity @a[tag=rpg.fg.atk,tag=rpg.ms.crossbow3] run scoreboard players add #pct rpg_fg 3
