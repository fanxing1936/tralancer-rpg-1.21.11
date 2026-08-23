# 5 行原本各自扫一遍全实体表找 @e[tag=rpg.vine.strike]；现在由上层一次判定后统一进入。
# 行内容与顺序原样保留。
execute as @e[tag=rpg.vine.strike] at @s run particle minecraft:tinted_leaves{color:12835692} ~ ~0.9 ~ 0.45 0.55 0.45 0.02 24
execute as @e[tag=rpg.vine.strike] at @s run particle crit ~ ~0.9 ~ 0.3 0.35 0.3 0.12 10
execute as @e[tag=rpg.vine.strike] at @s run particle sweep_attack ~ ~0.9 ~ 0.2 0.2 0.2 0 1
execute as @e[tag=rpg.vine.strike] at @s if entity @a[tag=rpg.h.vine_tag1,distance=..20] run damage @s 2 minecraft:player_attack by @a[tag=rpg.h.vine_tag1,limit=1,sort=nearest]
execute as @e[tag=rpg.vine.strike] at @s unless entity @a[tag=rpg.h.vine_tag1,distance=..20] run damage @s 2 minecraft:player_attack
