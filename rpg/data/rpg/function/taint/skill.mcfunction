# 谁在出手 —— 看他是哪一柱挣出来的。没有柱位的落到最后一行。
execute if entity @s[scores={rpg_dm_lord=1}] run return run function rpg:taint/sk1
execute if entity @s[scores={rpg_dm_lord=2}] run return run function rpg:taint/sk2
execute if entity @s[scores={rpg_dm_lord=3}] run return run function rpg:taint/sk3
execute if entity @s[scores={rpg_dm_lord=4}] run return run function rpg:taint/sk4
execute if entity @s[scores={rpg_dm_lord=5}] run return run function rpg:taint/sk5
execute if entity @s[scores={rpg_dm_lord=6}] run return run function rpg:taint/sk6
execute if entity @s[scores={rpg_dm_lord=7}] run return run function rpg:taint/sk7
particle sculk_soul ~ ~1 ~ 2 1 2 0.1 60
particle large_smoke ~ ~1 ~ 1.5 1 1.5 0.05 40
playsound minecraft:entity.warden.roar hostile @a[distance=..32] ~ ~ ~ 1 1.4
execute as @a[distance=..8,gamemode=!spectator,gamemode=!creative] run function rpg:taint/sk_none_hit
