# 3 行原本各自扫一遍全实体表找 @e[tag=devil]；现在由上层一次判定后统一进入。
# 行内容与顺序原样保留。
execute as @e[tag=devil] at @s run effect give @s minecraft:invisibility 1 1 true
execute as @e[tag=devil] at @s run particle large_smoke ~0.1 ~1.5 ~0.1 -0.2 -0.5 -0.2 0.1 1
execute as @e[tag=devil] at @s run particle squid_ink ~0.1 ~1.5 ~0.1 -0.2 -0.5 -0.2 0.1 5
