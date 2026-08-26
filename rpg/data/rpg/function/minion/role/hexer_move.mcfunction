# 咒使补偿寻路：幻术师原生 AI 在脱离袭击后可能不主动接近玩家。
# 每十刻只在远距离、前方两格可通行时迈进，不穿墙且保留远程站位。
data merge entity @s {NoAI:0b}
execute facing entity @a[distance=10..28,sort=nearest,limit=1,gamemode=!spectator,gamemode=!creative] feet if block ^ ^ ^0.7 minecraft:air if block ^ ^1 ^0.7 minecraft:air run tp @s ^ ^ ^0.45
