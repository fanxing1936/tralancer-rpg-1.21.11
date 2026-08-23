# 迈一步。`rotated ~ 0` 把俯仰归零 —— 不然朝着高处的目标会走上天。
#
# 位移用 tp 而不是 Motion：Motion 要先把朝向换算成 xz 分量，而 tp 沿
# `^ ^ ^` 走一步不需要任何三角函数。客户端的走路动画是按位置变化算的，
# 所以 tp 出来的佣兵看起来仍然在走路。
execute rotated ~ 0 positioned ^ ^ ^0.22 unless block ~ ~ ~ #minecraft:replaceable if block ~ ~1 ~ #minecraft:replaceable positioned ~ ~1 ~ run tp @s ~ ~ ~
execute rotated ~ 0 positioned ^ ^ ^0.22 if block ~ ~ ~ #minecraft:replaceable run tp @s ~ ~ ~
