# 4 行原本各自扫一遍全实体表找 @e[tag=rpg.hurt]；现在由上层一次判定后统一进入。
# 行内容与顺序原样保留。
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={sea=0..},tag=rpg.h.sea_tag1] run effect give @e[distance=..1,limit=1] minecraft:wither 2 3 true
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={sea=0..},tag=rpg.h.sea_tag1] run effect give @e[distance=..1,limit=1] minecraft:glowing 2 3 true
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={sea=0..},tag=rpg.h.sea_tag1] run particle dust_color_transition{from_color:[1.0,0.38,0.92],to_color:[1.0,0.78,0.0],scale:3} ~0.5 ~1.5 ~0.5 -1 -1 -1 0.1 30
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[tag=rpg.h.sea_tag1] run particle raid_omen ~0.5 ~1.5 ~0.5 -1 -1 -1 0.1 3
