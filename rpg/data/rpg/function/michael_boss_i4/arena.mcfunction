# 战场（as/at 战场中心）。
scoreboard players add #tick rpg_mk_i4 1
execute if score #ghost rpg_mk_i4 matches 1.. run return run function rpg:michael_boss_i4/ghost/tick
execute if entity @e[tag=rpg.unit.f,distance=..40] run scoreboard players set #empty rpg_mk_i4 0
execute unless entity @e[tag=rpg.unit.f,distance=..40] run scoreboard players add #empty rpg_mk_i4 1
execute if score #empty rpg_mk_i4 matches 1200.. run return run function rpg:michael_boss_i4/lose
execute unless entity @e[type=minecraft:vindicator,tag=rpg.mkb,tag=!rpg.mk.preview,distance=..120] run return run function rpg:michael_boss_i4/lost_unit
bossbar set rpg:michael_boss_i4 players @a[distance=..48]
# 守望者：数一数；还有活着的，场上的人就「被看见」（发光）
execute store result score #w rpg_mk_i4 if entity @e[type=minecraft:vindicator,tag=rpg.mkb.w,distance=..80]
scoreboard players operation #m rpg_mk_i4 = #tick rpg_mk_i4
scoreboard players set #k rpg_mk_i4 10
scoreboard players operation #m rpg_mk_i4 %= #k rpg_mk_i4
execute if score #m rpg_mk_i4 matches 0 if score #w rpg_mk_i4 matches 1.. run effect give @a[distance=..40,gamemode=!spectator,gamemode=!creative] minecraft:glowing 1 0 true
scoreboard players operation #m rpg_mk_i4 = #tick rpg_mk_i4
scoreboard players set #k rpg_mk_i4 20
scoreboard players operation #m rpg_mk_i4 %= #k rpg_mk_i4
# 守望者全死时，落点招式瞄的是这个标记：每秒挪到玩家那里一次（约 1 秒前的位置）
execute if score #m rpg_mk_i4 matches 0 as @e[type=minecraft:marker,tag=rpg.mkb.lag,limit=1,distance=0..] at @e[tag=rpg.unit.f,distance=..40,sort=nearest,limit=1] run tp @s ~ ~ ~
execute as @e[type=minecraft:vindicator,tag=rpg.mkb,tag=!rpg.mk.preview,distance=..120] at @s run function rpg:michael_boss_i4/unit
execute as @e[type=minecraft:vindicator,tag=rpg.mkb.w,distance=..80] at @s run function rpg:michael_boss_i4/watch/tick
execute as @e[tag=rpg.mkb.fx,distance=..120] at @s run function rpg:michael_boss_i4/fx/tick
execute as @e[tag=rpg.unit,tag=rpg.mkb.flamed,distance=0..] at @s run function rpg:michael_boss_i4/flame/tick
execute if score #stage rpg_mk_i4 matches 2 as @e[tag=rpg.mkb.pillar,distance=0..] at @s run function rpg:michael_boss_i4/pillar/clock
execute as @e[tag=rpg.unit,tag=rpg.mkb.pend,distance=0..] run function rpg:michael_boss_i4/hit/settle
execute as @e[tag=rpg.unit,distance=0..] run scoreboard players operation @s rpg_mk_dd0 = @s rpg_mk_dd
function rpg:michael_boss_i4/music/tick
