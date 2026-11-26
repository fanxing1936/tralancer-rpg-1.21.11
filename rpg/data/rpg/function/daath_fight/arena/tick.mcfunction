# 场地每刻（as/at 中心标记）
execute if entity @a[tag=rpg.dt.in,distance=..90] run scoreboard players set @s rpg_dt_e 0
execute unless entity @a[tag=rpg.dt.in,distance=..90] run scoreboard players add @s rpg_dt_e 1
execute if score @s rpg_dt_e matches 1200.. run return run function rpg:daath_fight/arena/timeout
# 保险：打着打着影子没了（被指令杀掉之类），还东西、送回去
execute if entity @a[tag=rpg.dt.in,distance=..90,scores={rpg_dt_ph=3}] unless entity @e[type=minecraft:vindicator,tag=rpg.dtb,distance=..120] run return run function rpg:daath_fight/arena/gone
execute as @e[type=minecraft:item_display,tag=rpg.dt.trs,distance=..40] at @s run rotate @s ~0.6 0
execute as @e[type=minecraft:item_display,tag=rpg.dt.trr,distance=..40] at @s run rotate @s ~-1 0
execute as @e[type=minecraft:interaction,tag=rpg.dt.lamp,distance=..30] at @s run function rpg:daath_fight/lamp/tick
execute as @e[type=minecraft:marker,tag=rpg.dt.pool,distance=..30] at @s run function rpg:daath_fight/lamp/pool
