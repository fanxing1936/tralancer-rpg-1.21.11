scoreboard players set #weak rpg_pf 0
scoreboard players set #hudl rpg_pf -1
execute as @e[type=minecraft:armor_stand,tag=rpg.pf.rig,limit=1] on passengers if entity @s[tag=rpg.he.p.inner_body] run data merge entity @s {Glowing:0b}
execute as @e[type=minecraft:armor_stand,tag=rpg.pf.rig,limit=1] on passengers if entity @s[tag=rpg.he.p.inner_head] run data merge entity @s {Glowing:0b}
execute as @e[type=minecraft:armor_stand,tag=rpg.pf.rig,limit=1] on passengers if entity @s[tag=rpg.he.p.inner_arm_left] run data merge entity @s {Glowing:0b}
execute as @e[type=minecraft:armor_stand,tag=rpg.pf.rig,limit=1] on passengers if entity @s[tag=rpg.he.p.inner_arm_right] run data merge entity @s {Glowing:0b}
execute as @e[type=minecraft:armor_stand,tag=rpg.pf.rig,limit=1] on passengers if entity @s[tag=rpg.he.p.inner_leg_left] run data merge entity @s {Glowing:0b}
execute as @e[type=minecraft:armor_stand,tag=rpg.pf.rig,limit=1] on passengers if entity @s[tag=rpg.he.p.inner_leg_right] run data merge entity @s {Glowing:0b}
