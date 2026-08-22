# 6 行原本各自扫一遍全实体表找 @e[tag=rpg.hurt]；现在由上层一次判定后统一进入。
# 行内容与顺序原样保留。
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={holy=0..},tag=rpg.h.holy_weapon_tag1] run particle dust{color:[1.0,1.0,1.0],scale:3} ~0.5 ~1.5 ~0.5 -1 -1 -1 0.2 10
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={holy=0..},tag=rpg.h.holy_weapon_tag1] run particle end_rod ~0.5 ~1.5 ~0.5 -1 -1 -1 0.2 10

execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={holy=0..},tag=rpg.h.holy_weapon_tag2] run particle firework ~0.5 ~1.5 ~0.5 -1 -1 -1 0.2 10
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={holy=0..},tag=rpg.h.holy_weapon_tag2] run particle end_rod ~0.5 ~1.5 ~0.5 -1 -1 -1 0.2 10

execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={holy=0..},tag=rpg.h.holy_weapon_tag3] run particle totem_of_undying ~0.5 ~1.5 ~0.5 -1 -1 -1 0.2 10
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={holy=0..},tag=rpg.h.holy_weapon_tag3] run particle dust{color:[1.0,0.78,0.0],scale:3} ~0.5 ~1.5 ~0.5 -1 -1 -1 0.2 10
