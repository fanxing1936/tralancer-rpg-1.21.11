# 3 行原本各自扫一遍全实体表找 @e[type=minecraft:spectral_arrow,tag=burn_tag]；现在由上层一次判定后统一进入。
# 行内容与顺序原样保留。
execute as @e[type=minecraft:spectral_arrow,tag=burn_tag] at @s unless block ~ ~-0.1 ~ air run damage @e[limit=1,sort=nearest,distance=0.1..1] 5 minecraft:on_fire
execute as @e[type=minecraft:spectral_arrow,tag=burn_tag] at @s unless block ~ ~-0.1 ~ air run particle lava ~1 ~1 ~1 0 -2 -2 1 100 force
execute as @e[type=minecraft:spectral_arrow,tag=burn_tag] at @s unless block ~ ~-0.1 ~ air run kill @s
