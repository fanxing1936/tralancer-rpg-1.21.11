# 6 行原本各自扫一遍全实体表找 @e[tag=burn]；现在由上层一次判定后统一进入。
# 行内容与顺序原样保留。
execute as @e[tag=burn] at @s unless block ~ ~-0.1 ~ air run kill @s
execute as @e[tag=burn] at @s unless block ~ ~0.1 ~ air run kill @s
execute as @e[tag=burn] at @s unless block ~0.1 ~ ~ air run kill @s
execute as @e[tag=burn] at @s unless block ~-0.1 ~ ~ air run kill @s
execute as @e[tag=burn] at @s unless block ~ ~ ~-0.1 air run kill @s
execute as @e[tag=burn] at @s unless block ~ ~ ~0.1 air run kill @s
