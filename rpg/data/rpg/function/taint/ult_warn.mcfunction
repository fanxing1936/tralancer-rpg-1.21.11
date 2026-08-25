# 罪约预警。没有柱位即无名者。
execute if entity @s[scores={rpg_dm_lord=1}] run return run function rpg:taint/ult1_warn
execute if entity @s[scores={rpg_dm_lord=2}] run return run function rpg:taint/ult2_warn
execute if entity @s[scores={rpg_dm_lord=3}] run return run function rpg:taint/ult3_warn
execute if entity @s[scores={rpg_dm_lord=4}] run return run function rpg:taint/ult4_warn
execute if entity @s[scores={rpg_dm_lord=5}] run return run function rpg:taint/ult5_warn
execute if entity @s[scores={rpg_dm_lord=6}] run return run function rpg:taint/ult6_warn
execute if entity @s[scores={rpg_dm_lord=7}] run return run function rpg:taint/ult7_warn
function rpg:taint/ult0_warn
