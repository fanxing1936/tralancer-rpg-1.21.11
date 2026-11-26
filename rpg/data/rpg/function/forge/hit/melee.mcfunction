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
