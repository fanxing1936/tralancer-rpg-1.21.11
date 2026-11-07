# 破绽：外壳减伤取消，血条转金，体内小人的轮廓透出来。
scoreboard players set #weak rpg_pf 1
scoreboard players set #hudl rpg_pf -1
execute as @e[type=minecraft:armor_stand,tag=rpg.pf.rig,limit=1] on passengers if entity @s[tag=rpg.he.p.inner_body] run data merge entity @s {Glowing:1b,glow_color_override:16767066}
execute as @e[type=minecraft:armor_stand,tag=rpg.pf.rig,limit=1] on passengers if entity @s[tag=rpg.he.p.inner_head] run data merge entity @s {Glowing:1b,glow_color_override:16767066}
execute as @e[type=minecraft:armor_stand,tag=rpg.pf.rig,limit=1] on passengers if entity @s[tag=rpg.he.p.inner_arm_left] run data merge entity @s {Glowing:1b,glow_color_override:16767066}
execute as @e[type=minecraft:armor_stand,tag=rpg.pf.rig,limit=1] on passengers if entity @s[tag=rpg.he.p.inner_arm_right] run data merge entity @s {Glowing:1b,glow_color_override:16767066}
execute as @e[type=minecraft:armor_stand,tag=rpg.pf.rig,limit=1] on passengers if entity @s[tag=rpg.he.p.inner_leg_left] run data merge entity @s {Glowing:1b,glow_color_override:16767066}
execute as @e[type=minecraft:armor_stand,tag=rpg.pf.rig,limit=1] on passengers if entity @s[tag=rpg.he.p.inner_leg_right] run data merge entity @s {Glowing:1b,glow_color_override:16767066}
