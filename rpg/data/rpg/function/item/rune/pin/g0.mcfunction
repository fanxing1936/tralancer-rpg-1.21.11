# 6 行原本各自扫一遍全实体表找 @e[tag=rpg.rune.pin]；现在由上层一次判定后统一进入。
# 行内容与顺序原样保留。
execute as @e[tag=rpg.rune.pin] at @s run particle dust_color_transition{from_color:[0.48,0.42,0.66],to_color:[0.20,0.16,0.30],scale:1} ~ ~ ~ 0.08 0.08 0.08 0.02 3
execute as @e[tag=rpg.rune.pin] at @s if entity @e[distance=0.1..1.5,type=!minecraft:arrow] unless entity @a[tag=rpg.h.pin_tag1,distance=..1.5] run effect give @e[distance=..1.5,limit=1,sort=nearest,type=!minecraft:arrow] minecraft:slowness 3 4 true
execute as @e[tag=rpg.rune.pin] at @s if entity @e[distance=0.1..1.5,type=!minecraft:arrow] unless entity @a[tag=rpg.h.pin_tag1,distance=..1.5] run effect give @e[distance=..1.5,limit=1,sort=nearest,type=!minecraft:arrow] minecraft:mining_fatigue 3 2 true
execute as @e[tag=rpg.rune.pin] at @s if entity @e[distance=0.1..1.5,type=!minecraft:arrow] unless entity @a[tag=rpg.h.pin_tag1,distance=..1.5] run particle minecraft:flash{color:8022440} ~ ~0.8 ~ 0 0 0 0 1
execute as @e[tag=rpg.rune.pin] at @s if entity @e[distance=0.1..1.5,type=!minecraft:arrow] unless entity @a[tag=rpg.h.pin_tag1,distance=..1.5] run playsound minecraft:block.anvil.land hostile @a[distance=..14] ~ ~ ~ 0.5 1.8
execute as @e[tag=rpg.rune.pin] at @s unless block ~ ~ ~ air run kill @s
