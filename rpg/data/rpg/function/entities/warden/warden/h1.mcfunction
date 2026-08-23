# 这 2 行原本各自在 `as @e` 的循环里再问一遍 `if entity @e[tag=devil]` —— 那是 O(n²)，
# 而那个判定与当前是哪个实体无关。现在由上层一次判定后统一进入。
# 行内容与顺序原样保留。
execute as @e on attacker at @s run effect clear @s minecraft:invisibility
execute as @e on attacker at @s run effect give @s minecraft:glowing 1 1 true
