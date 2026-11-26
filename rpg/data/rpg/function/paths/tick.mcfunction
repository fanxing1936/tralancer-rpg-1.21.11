# 每刻：路径按钮；战车正位的疾跑加速；放技能后的窗口
execute as @a[scores={rpg_pa_do=1..}] at @s run function rpg:paths/press
execute as @a[scores={rpg_ps_18=2},predicate=rpg:paths/sprinting] run attribute @s minecraft:movement_speed modifier add rpg:pa_18s 0.05 add_multiplied_base
execute as @a[scores={rpg_ps_18=2},predicate=!rpg:paths/sprinting] run attribute @s minecraft:movement_speed modifier remove rpg:pa_18s
