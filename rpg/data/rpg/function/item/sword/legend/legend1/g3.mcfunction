# 4 行原本各自扫一遍全实体表找 @e[tag=rpg.hurt]；现在由上层一次判定后统一进入。
# 行内容与顺序原样保留。
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={blil=0..},tag=rpg.h.blil_tag1] run effect give @e[distance=0..1] minecraft:wither 2 3 true
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={blil=0..},tag=rpg.h.blil_tag1] run effect give @e[distance=0..1] minecraft:glowing 2 3 true
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={blil=0..},tag=rpg.h.blil_tag1] run particle dust_color_transition{from_color:[0.4,0.0,0.6],scale:3,to_color:[0.0,0.0,0.0]} ~0.5 ~1.5 ~0.5 -1 -1 -1 0.1 30

execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[tag=rpg.h.blil_tag1] run particle witch ~0.25 ~1.5 ~0.25 -0.5 -1 -0.5 0 2
