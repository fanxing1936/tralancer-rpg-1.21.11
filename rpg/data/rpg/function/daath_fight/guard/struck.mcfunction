# 格反中被打到：从正面就还手（as 影子）
execute at @s positioned ^ ^ ^2 unless entity @a[tag=rpg.dt.me,distance=..3.2] run return 0
scoreboard players set #pc rpg_dt 0
tag @s add rpg.dt.rip
