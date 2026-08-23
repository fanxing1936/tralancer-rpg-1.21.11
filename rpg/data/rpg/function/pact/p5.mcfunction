# 毒雾：有毒的光辉使者，吐出来的东西也带光。
particle dust{color:[0.36,0.62,0.16],scale:2} ~ ~1 ~ 0.4 0.4 0.4 0.02 30
playsound minecraft:entity.witch.throw hostile @a[distance=..24] ~ ~ ~ 1 0.6
playsound minecraft:entity.spider.hurt hostile @a[distance=..24] ~ ~ ~ 0.8 0.5
execute at @s anchored eyes run function rpg:pact/p5_fog
