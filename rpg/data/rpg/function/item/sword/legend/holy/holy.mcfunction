execute as @e at @s on attacker if entity @s[scores={holy=0..},tag=rpg.h.holy_weapon_tag1] run particle dust{color:[1.0,1.0,1.0],scale:3} ~0.5 ~1.5 ~0.5 -1 -1 -1 0.2 30
execute as @e at @s on attacker if entity @s[scores={holy=0..},tag=rpg.h.holy_weapon_tag1] run particle end_rod ~0.5 ~1.5 ~0.5 -1 -1 -1 0.2 30

execute as @e at @s on attacker if entity @s[scores={holy=0..},tag=rpg.h.holy_weapon_tag2] run particle firework ~0.5 ~1.5 ~0.5 -1 -1 -1 0.2 30
execute as @e at @s on attacker if entity @s[scores={holy=0..},tag=rpg.h.holy_weapon_tag2] run particle end_rod ~0.5 ~1.5 ~0.5 -1 -1 -1 0.2 30

execute as @e at @s on attacker if entity @s[scores={holy=0..},tag=rpg.h.holy_weapon_tag3] run particle totem_of_undying ~0.5 ~1.5 ~0.5 -1 -1 -1 0.2 30
execute as @e at @s on attacker if entity @s[scores={holy=0..},tag=rpg.h.holy_weapon_tag3] run particle dust{color:[1.0,0.78,0.0],scale:3} ~0.5 ~1.5 ~0.5 -1 -1 -1 0.2 30


scoreboard players reset * holy
