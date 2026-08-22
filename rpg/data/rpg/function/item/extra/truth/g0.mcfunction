# 3 行原本各自扫一遍全实体表找 @e[tag=rpg.hurt]；现在由上层一次判定后统一进入。
# 行内容与顺序原样保留。
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={truth=0..},tag=rpg.h.truth_tag1] run tag @s add rpg.truth.src
execute as @e[tag=rpg.hurt] at @s if entity @a[tag=rpg.truth.src,distance=..7] run particle end_rod ~ ~1 ~ 0.3 0.5 0.3 0.02 18
execute as @e[tag=rpg.hurt] at @s if entity @a[tag=rpg.truth.src,distance=..7] run effect give @s minecraft:glowing 6 0 true
