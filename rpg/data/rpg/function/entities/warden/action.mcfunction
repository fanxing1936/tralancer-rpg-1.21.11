execute as @a[distance=..20] at @s run title @s title {"text":"\ue301\ue302\ue303"}
execute as @a[distance=..20] at @s run title @s subtitle ["",{"text":"堕落的天使","color":"#999999","bold":true},{"text":"\uE012"}," 沙利叶"]
execute as @a[distance=..20] at @s run effect give @s minecraft:blindness 5 10 true
execute as @a[distance=..20] at @s run playsound minecraft:boss3 player @s
execute as @a[distance=..20] at @s run playsound minecraft:entity.generic.explode player @s
summon minecraft:evoker ~ ~ ~ {SpellTicks:0,Health:1000,Silent:1b,Tags:["devil","boss"],active_effects:[{id:speed,duration:-1,amplifier:1,show_particles:0b}],attributes:[{id:"max_health",base:1000f},{id:"armor",base:15f},{id:"scale",base:1.2f},{id:"knockback_resistance",base:0.5f}]}
# `bossbar ... players` 是赋值不是追加 —— 逐个玩家写，等于每人
# 轮流把名单覆盖成自己，最后只有一个人看得见血条。一次设整组。
bossbar set minecraft:devil players @a[distance=..20]
bossbar set minecraft:devil color blue
bossbar set minecraft:devil name {"text":"\ue301\ue302\ue303"}
