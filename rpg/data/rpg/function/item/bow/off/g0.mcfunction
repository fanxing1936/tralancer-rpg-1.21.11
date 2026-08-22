# 4 行原本各自扫一遍全实体表找 @e[tag=darkness]；现在由上层一次判定后统一进入。
# 行内容与顺序原样保留。
execute as @e[tag=darkness] at @s if entity @e[distance=0..2] unless entity @a[distance=0..2,tag=rpg.h.dark_tag1] at @s run tag @e[distance=0..2,type=!arrow] add darkness
execute as @e[tag=darkness] at @s run particle dust_color_transition{from_color:[0.19,0.05,0.33],to_color:[0.0,0.0,0.0],scale:1} ~0.5 ~ ~0.5 -1 -1 -1 1 20
execute as @e[tag=darkness] at @s run effect give @s wither 1 1 true
execute as @e[tag=darkness] at @s run scoreboard players add @s dark 1
