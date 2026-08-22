# 3 行原本各自扫一遍全实体表找 @e[tag=rpg.hurt]；现在由上层一次判定后统一进入。
# 行内容与顺序原样保留。
execute as @e[tag=rpg.hurt] at @s if entity @a[tag=rpg.boaz.burst,distance=..7] run particle dust_color_transition{from_color:[0.078,0.510,0.569],to_color:[0.871,0.561,0.949],scale:3} ~ ~1 ~ 0.4 0.5 0.4 0.05 40
execute as @e[tag=rpg.hurt] at @s if entity @a[tag=rpg.boaz.burst,distance=..7] run particle sweep_attack ~ ~1 ~ 0.4 0.3 0.4 0 4
execute as @e[tag=rpg.hurt] at @s if entity @a[tag=rpg.boaz.burst,distance=..7] run particle minecraft:flash{color:14585842} ~ ~1 ~ 0 0 0 0 1
