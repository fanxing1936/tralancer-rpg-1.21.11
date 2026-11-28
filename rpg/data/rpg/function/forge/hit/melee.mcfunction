# 处决：目标生命低于 25%
execute if entity @a[tag=rpg.fg.atk,tag=rpg.fg.r.execute] run function rpg:forge/rune/execute
# 背刺：攻击者站在目标身后
execute if entity @a[tag=rpg.fg.atk,tag=rpg.fg.r.backstab] at @s rotated ~ 0 positioned ^ ^ ^-1.5 if entity @a[tag=rpg.fg.atk,distance=..1.7] run function rpg:forge/rune/backstab
# 蓄势：2 秒没出手
execute if entity @a[tag=rpg.fg.atk,tag=rpg.fg.r.poise,scores={rpg_fg_idle=40..}] run function rpg:forge/rune/poise
# 追猎标记：标记它的人近战 +25%
execute if score @s rpg_fg_mt matches 1.. run function rpg:forge/rune/hunt_bonus
# 反震、影步窗口
execute if entity @a[tag=rpg.fg.atk,scores={rpg_fg_rw=1..}] run scoreboard players add #pct rpg_fg 40
scoreboard players set @a[tag=rpg.fg.atk] rpg_fg_rw 0
execute if entity @a[tag=rpg.fg.atk,scores={rpg_fg_shd=1..}] run scoreboard players add #pct rpg_fg 60
scoreboard players set @a[tag=rpg.fg.atk] rpg_fg_shd 0
# 余烬、回响
execute if entity @a[tag=rpg.fg.atk,tag=rpg.fg.r.ember] run function rpg:forge/rune/ember
execute if entity @a[tag=rpg.fg.atk,tag=rpg.fg.r.echo] run function rpg:forge/rune/echo
# 路径赐福（add_paths.py）
execute if entity @a[tag=rpg.fg.atk,scores={rpg_ps_31=2}] if entity @s[type=#minecraft:undead] run scoreboard players add #pct rpg_fg 4
execute if entity @a[tag=rpg.fg.atk,scores={rpg_ps_31=2}] if entity @s[type=#rpg:wl_nether] run scoreboard players add #pct rpg_fg 4
execute if entity @a[tag=rpg.fg.atk,scores={rpg_ps_29=2}] unless predicate rpg:paths/day run scoreboard players add #pct rpg_fg 5
execute if entity @a[tag=rpg.fg.atk,scores={rpg_ps_24=3}] if entity @s[type=#minecraft:undead] run scoreboard players add #pct rpg_fg 6
execute if entity @a[tag=rpg.fg.atk,scores={rpg_ps_18=3},predicate=rpg:paths/sprinting] run scoreboard players add #pct rpg_fg 15
execute if entity @a[tag=rpg.fg.atk,scores={rpg_ps_17=3}] if items entity @a[tag=rpg.fg.atk,limit=1] weapon.offhand #rpg:daath/weapon run scoreboard players add #pct rpg_fg 4
execute if entity @a[tag=rpg.fg.atk,scores={rpg_ps_16=3}] if entity @s[type=#rpg:wl_nether] run scoreboard players add #pct rpg_fg 5
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
execute if items entity @a[tag=rpg.fg.atk,limit=1] weapon.mainhand #minecraft:swords run scoreboard players add @a[tag=rpg.fg.atk] rpg_ms_sword 1
execute if items entity @a[tag=rpg.fg.atk,limit=1] weapon.mainhand #minecraft:swords if entity @a[tag=rpg.fg.atk,tag=rpg.ms.sword1] run scoreboard players add #pct rpg_fg 3
execute if items entity @a[tag=rpg.fg.atk,limit=1] weapon.mainhand #minecraft:swords if entity @a[tag=rpg.fg.atk,tag=rpg.ms.sword2] run scoreboard players add #pct rpg_fg 3
execute if items entity @a[tag=rpg.fg.atk,limit=1] weapon.mainhand #minecraft:swords if entity @a[tag=rpg.fg.atk,tag=rpg.ms.sword3] run scoreboard players add #pct rpg_fg 3
execute if items entity @a[tag=rpg.fg.atk,limit=1] weapon.mainhand #minecraft:axes run scoreboard players add @a[tag=rpg.fg.atk] rpg_ms_axe 1
execute if items entity @a[tag=rpg.fg.atk,limit=1] weapon.mainhand #minecraft:axes if entity @a[tag=rpg.fg.atk,tag=rpg.ms.axe1] run scoreboard players add #pct rpg_fg 3
execute if items entity @a[tag=rpg.fg.atk,limit=1] weapon.mainhand #minecraft:axes if entity @a[tag=rpg.fg.atk,tag=rpg.ms.axe2] run scoreboard players add #pct rpg_fg 3
execute if items entity @a[tag=rpg.fg.atk,limit=1] weapon.mainhand #minecraft:axes if entity @a[tag=rpg.fg.atk,tag=rpg.ms.axe3] run scoreboard players add #pct rpg_fg 3
execute if items entity @a[tag=rpg.fg.atk,limit=1] weapon.mainhand minecraft:mace run scoreboard players add @a[tag=rpg.fg.atk] rpg_ms_mace 1
execute if items entity @a[tag=rpg.fg.atk,limit=1] weapon.mainhand minecraft:mace if entity @a[tag=rpg.fg.atk,tag=rpg.ms.mace1] run scoreboard players add #pct rpg_fg 3
execute if items entity @a[tag=rpg.fg.atk,limit=1] weapon.mainhand minecraft:mace if entity @a[tag=rpg.fg.atk,tag=rpg.ms.mace2] run scoreboard players add #pct rpg_fg 3
execute if items entity @a[tag=rpg.fg.atk,limit=1] weapon.mainhand minecraft:mace if entity @a[tag=rpg.fg.atk,tag=rpg.ms.mace3] run scoreboard players add #pct rpg_fg 3
execute if items entity @a[tag=rpg.fg.atk,limit=1] weapon.mainhand minecraft:mace if entity @a[tag=rpg.fg.atk,tag=rpg.ms.mace1] run attribute @s minecraft:armor modifier add rpg:mastery_mace -3 add_value
