# 3 行原本各自扫一遍全实体表找 @e[tag=rpg.hurt]；现在由上层一次判定后统一进入。
# 行内容与顺序原样保留。
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={ice=0..},tag=rpg.h.ice_tag1] run effect give @e[distance=..1,limit=1] minecraft:slowness 2 255 true
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[tag=rpg.h.ice_tag1] run damage @e[distance=..1,limit=1] 1 freeze
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={ice=0..},tag=rpg.h.ice_tag1] run particle dust_color_transition{from_color:[0.58,0.92,1.0],to_color:[1.0,1.0,1.0],scale:3} ~0.5 ~1.5 ~0.5 -1 -1 -1 0.1 30
