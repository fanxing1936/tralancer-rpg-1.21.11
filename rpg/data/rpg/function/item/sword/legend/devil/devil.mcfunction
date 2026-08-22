execute as @e at @s on attacker if entity @s[scores={devil_weapon=0..},tag=rpg.h.devil_weapon_tag1] run particle sculk_soul ~0.5 ~1.5 ~0.5 -1 -1 -1 0.2 30
execute as @e at @s on attacker if entity @s[scores={devil_weapon=0..},tag=rpg.h.devil_weapon_tag1] run particle soul_fire_flame ~0.5 ~1.5 ~0.5 -1 -1 -1 0.2 30

execute as @e at @s on attacker if entity @s[scores={devil_weapon=0..},tag=rpg.h.devil_weapon_tag2] run particle trial_spawner_detection_ominous ~0.5 ~1.5 ~0.5 -1 -1 -1 0.2 30
execute as @e at @s on attacker if entity @s[scores={devil_weapon=0..},tag=rpg.h.devil_weapon_tag2] run particle sonic_boom ~0.5 ~1.5 ~0.5 -1 -1 -1 0.2 5


execute as @e at @s on attacker if entity @s[scores={devil_weapon=0..},tag=rpg.h.devil_weapon_tag3] run particle sculk_soul ~0.5 ~1.5 ~0.5 -1 -1 -1 0.2 30
execute as @e at @s on attacker if entity @s[scores={devil_weapon=0..},tag=rpg.h.devil_weapon_tag3] run particle trial_omen ~0.5 ~1.5 ~0.5 -1 -1 -1 0.2 30


scoreboard players reset * devil_weapon
