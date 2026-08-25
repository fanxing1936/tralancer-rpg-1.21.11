# Commit this tick's health snapshot; runs last in #minecraft:tick.
execute as @e[tag=rpg.hurt] run scoreboard players operation @s damage_timing = @s damage_action

# 最后一刻清除圣器持有者的视觉遮蔽。
execute as @a[tag=rpg.holy] run function rpg:command/holy_effects
# 显形阶段在 tick 尾再次清除烟幕续上的隐身；这里只扫正在举行仪式的七柱。
execute as @e[type=minecraft:vindicator,tag=rpg.exorcism.visible] run effect clear @s minecraft:invisibility
