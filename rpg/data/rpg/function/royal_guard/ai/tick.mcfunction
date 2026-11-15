# 重盾一刻（as/at 载体）。0 举盾自由，1 砸锤，2 放盾喘息。
execute unless score @s rpg_rg_st matches 0.. run function rpg:royal_guard/ai/init
execute if entity @s[tag=rpg.hurt] unless score @s rpg_rg_st matches 2 run function rpg:royal_guard/ai/guard
execute if score @s rpg_rg_st matches 1 run return run function rpg:royal_guard/ai/attack
execute if score @s rpg_rg_st matches 2 run return run function rpg:royal_guard/ai/rest
# 举盾：正面飞来的投射物挡下
execute positioned ^ ^1.2 ^1.2 as @e[type=#minecraft:impact_projectiles,distance=..2.5] at @s run function rpg:royal_guard/ai/deflect
scoreboard players remove @s[scores={rpg_rg_cd=1..}] rpg_rg_cd 1
execute if score @s rpg_rg_cd matches 0 if entity @e[tag=rpg.unit.f,distance=..3.0] run function rpg:royal_guard/ai/attack_start
