# 幻魔者尖牙：与枪线同路，贴地推进 12 格。
execute positioned ^ ^ ^1 run summon minecraft:evoker_fangs ~ ~ ~ {Warmup:0,Tags:["rpg.luci.fang"]}
execute positioned ^ ^ ^2 run summon minecraft:evoker_fangs ~ ~ ~ {Warmup:2,Tags:["rpg.luci.fang"]}
execute positioned ^ ^ ^3 run summon minecraft:evoker_fangs ~ ~ ~ {Warmup:4,Tags:["rpg.luci.fang"]}
execute positioned ^ ^ ^4 run summon minecraft:evoker_fangs ~ ~ ~ {Warmup:6,Tags:["rpg.luci.fang"]}
execute positioned ^ ^ ^5 run summon minecraft:evoker_fangs ~ ~ ~ {Warmup:8,Tags:["rpg.luci.fang"]}
execute positioned ^ ^ ^6 run summon minecraft:evoker_fangs ~ ~ ~ {Warmup:10,Tags:["rpg.luci.fang"]}
execute positioned ^ ^ ^7 run summon minecraft:evoker_fangs ~ ~ ~ {Warmup:12,Tags:["rpg.luci.fang"]}
execute positioned ^ ^ ^8 run summon minecraft:evoker_fangs ~ ~ ~ {Warmup:14,Tags:["rpg.luci.fang"]}
execute positioned ^ ^ ^9 run summon minecraft:evoker_fangs ~ ~ ~ {Warmup:16,Tags:["rpg.luci.fang"]}
execute positioned ^ ^ ^10 run summon minecraft:evoker_fangs ~ ~ ~ {Warmup:18,Tags:["rpg.luci.fang"]}
execute positioned ^ ^ ^11 run summon minecraft:evoker_fangs ~ ~ ~ {Warmup:20,Tags:["rpg.luci.fang"]}
execute positioned ^ ^ ^12 run summon minecraft:evoker_fangs ~ ~ ~ {Warmup:22,Tags:["rpg.luci.fang"]}

# 认主：不设 Owner 的尖牙会连施法者一起咬
execute as @e[tag=rpg.luci.fang] run data modify entity @s Owner set from entity @a[tag=rpg.luci.cast,limit=1,sort=nearest] UUID
tag @e[tag=rpg.luci.fang] remove rpg.luci.fang
playsound minecraft:entity.evoker_fangs.attack hostile @a[distance=..24] ~ ~ ~ 1 0.6
