# 4 行原本各自扫一遍全实体表找 @e[tag=rpg.hurt,type=#minecraft:undead]；现在由上层一次判定后统一进入。
# 行内容与顺序原样保留。
execute as @e[tag=rpg.hurt,type=#minecraft:undead] at @s if entity @a[tag=rpg.epic.dawn,distance=..8] run damage @s 6 minecraft:magic by @a[tag=rpg.epic.dawn,limit=1,sort=nearest]
execute as @e[tag=rpg.hurt,type=#minecraft:undead] at @s if entity @a[tag=rpg.epic.dawn,distance=..8] run particle dust_color_transition{from_color:16575098,to_color:8005632,scale:2} ~ ~1 ~ 0.35 0.5 0.35 0.06 26
execute as @e[tag=rpg.hurt,type=#minecraft:undead] at @s if entity @a[tag=rpg.epic.dawn,distance=..8] run particle minecraft:flash{color:16575098} ~ ~1 ~ 0 0 0 0 1
execute as @e[tag=rpg.hurt,type=#minecraft:undead] at @s if entity @a[tag=rpg.epic.dawn,distance=..8] run playsound minecraft:item.firecharge.use hostile @a[distance=..16] ~ ~ ~ 0.7 1.5
