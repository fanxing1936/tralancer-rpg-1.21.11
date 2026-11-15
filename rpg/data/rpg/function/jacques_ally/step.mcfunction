# 朝当前朝向走一步（as 他，rotated 走向）：前面空就走，前面一格高的台阶就上去。
execute if block ^ ^0.3 ^0.6 #minecraft:replaceable if block ^ ^1.5 ^0.6 #minecraft:replaceable run return run tp @s ^ ^ ^0.3 ~ 0
execute if block ^ ^1.3 ^0.6 #minecraft:replaceable if block ^ ^2.3 ^0.6 #minecraft:replaceable run tp @s ^ ^1 ^0.3 ~ 0
