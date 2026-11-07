# 圣卫一刻的战斗（as、at 载体）。
execute unless score @s rpg_tg_st matches 0.. run function rpg:tower_guard/ai/init
execute if entity @s[tag=rpg.hurt,tag=!rpg.tg.broken] run function rpg:tower_guard/ai/shield_hit
execute if score @s rpg_tg_st matches 1 run return run function rpg:tower_guard/ai/attack
execute if score @s rpg_tg_st matches 2 run return run function rpg:tower_guard/ai/charge
execute if score @s rpg_tg_st matches 3 run return run function rpg:tower_guard/ai/brake
execute if score @s rpg_tg_st matches 4 run return run function rpg:tower_guard/ai/stun
execute if score @s rpg_tg_st matches 5 run return run function rpg:tower_guard/ai/break_tick
# 空闲：举盾挡下正面飞来的投射物。
execute if entity @s[tag=!rpg.tg.broken] positioned ^ ^1.2 ^1.2 as @e[type=#minecraft:impact_projectiles,distance=..2.5] at @s run function rpg:tower_guard/ai/deflect
scoreboard players remove @s[scores={rpg_tg_cd=1..}] rpg_tg_cd 1
scoreboard players remove @s[scores={rpg_tg_cc=1..}] rpg_tg_cc 1
execute if score @s rpg_tg_cd matches 0 if entity @a[distance=..3.2,gamemode=!spectator,gamemode=!creative] run return run function rpg:tower_guard/ai/attack_start
execute if score @s rpg_tg_cc matches 0 if entity @a[distance=6..16,gamemode=!spectator,gamemode=!creative] run function rpg:tower_guard/ai/charge_start
