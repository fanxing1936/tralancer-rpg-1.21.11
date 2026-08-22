# 由 opt_invert.py 内外翻：原本这 6 行每行都自己扫一遍全实体表
# 找 @e[tag=rpg.hurt]。现在上层扫一次，行内一律对 @s 操作。
# 已静态验证过没有反向依赖，所以两种遍历顺序等价。

execute at @s on attacker if entity @s[scores={devil_weapon=0..},tag=rpg.h.devil_weapon_tag1] run particle sculk_soul ~0.5 ~1.5 ~0.5 -1 -1 -1 0.2 10
execute at @s on attacker if entity @s[scores={devil_weapon=0..},tag=rpg.h.devil_weapon_tag1] run particle soul_fire_flame ~0.5 ~1.5 ~0.5 -1 -1 -1 0.2 10
execute at @s on attacker if entity @s[scores={devil_weapon=0..},tag=rpg.h.devil_weapon_tag2] run particle trial_spawner_detection_ominous ~0.5 ~1.5 ~0.5 -1 -1 -1 0.2 10
execute at @s on attacker if entity @s[scores={devil_weapon=0..},tag=rpg.h.devil_weapon_tag2] run particle sonic_boom ~0.5 ~1.5 ~0.5 -1 -1 -1 0.2 5
execute at @s on attacker if entity @s[scores={devil_weapon=0..},tag=rpg.h.devil_weapon_tag3] run particle sculk_soul ~0.5 ~1.5 ~0.5 -1 -1 -1 0.2 10
execute at @s on attacker if entity @s[scores={devil_weapon=0..},tag=rpg.h.devil_weapon_tag3] run particle trial_omen ~0.5 ~1.5 ~0.5 -1 -1 -1 0.2 10
