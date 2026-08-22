# 6 行原本各自扫一遍全实体表找 @e[tag=rpg.hurt]；现在由上层一次判定后统一进入。
# 行内容与顺序原样保留。
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={devil_weapon=0..},tag=rpg.h.devil_weapon_tag1] run particle sculk_soul ~0.5 ~1.5 ~0.5 -1 -1 -1 0.2 10
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={devil_weapon=0..},tag=rpg.h.devil_weapon_tag1] run particle soul_fire_flame ~0.5 ~1.5 ~0.5 -1 -1 -1 0.2 10

execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={devil_weapon=0..},tag=rpg.h.devil_weapon_tag2] run particle trial_spawner_detection_ominous ~0.5 ~1.5 ~0.5 -1 -1 -1 0.2 10
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={devil_weapon=0..},tag=rpg.h.devil_weapon_tag2] run particle sonic_boom ~0.5 ~1.5 ~0.5 -1 -1 -1 0.2 5


execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={devil_weapon=0..},tag=rpg.h.devil_weapon_tag3] run particle sculk_soul ~0.5 ~1.5 ~0.5 -1 -1 -1 0.2 10
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={devil_weapon=0..},tag=rpg.h.devil_weapon_tag3] run particle trial_omen ~0.5 ~1.5 ~0.5 -1 -1 -1 0.2 10
