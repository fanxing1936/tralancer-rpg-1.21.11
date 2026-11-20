# 瞬身（as/at 他）：起点留一个标记，落到最近那人身后 2.5 格；起点到落点画剑痕
summon minecraft:marker ~ ~ ~ {Tags:["rpg.slb.fx","rpg.slb.fxnew","rpg.slb.flasha"]}
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_life 30
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_kd 0
tag @e[tag=rpg.slb.fxnew] remove rpg.slb.fxnew
execute as @e[tag=rpg.slb.flasha,limit=1,sort=nearest] run tp @s ~ ~ ~ ~ 0
execute at @e[tag=rpg.unit.f,distance=..14,sort=nearest,limit=1] facing entity @s feet positioned ^ ^ ^-2.5 if block ~ ~0.5 ~ #minecraft:replaceable if block ~ ~1.5 ~ #minecraft:replaceable unless block ~ ~-0.5 ~ #minecraft:replaceable run tp @s ~ ~ ~
scoreboard players set #d rpg_sl 10
execute as @e[tag=rpg.slb.flasha,limit=1,sort=nearest] at @s facing entity @e[type=minecraft:vindicator,tag=rpg.slb,tag=!rpg.slb.preview,limit=1] feet run function rpg:saul_boss/flash/trail
kill @e[tag=rpg.slb.flasha]
playsound minecraft:entity.breeze.wind_burst hostile @a[distance=..32] ~ ~ ~ 1 1.6
playsound minecraft:item.trident.riptide_2 hostile @a[distance=..32] ~ ~ ~ 1 1.4
