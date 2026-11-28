# 战场（as/at 战场中心）。
scoreboard players add #tick rpg_mk 1
execute if score #ghost rpg_mk matches 1.. run return run function rpg:michael_boss/ghost/tick
execute if entity @e[tag=rpg.unit.f,distance=..40] run scoreboard players set #empty rpg_mk 0
execute unless entity @e[tag=rpg.unit.f,distance=..40] run scoreboard players add #empty rpg_mk 1
execute if score #empty rpg_mk matches 1200.. run return run function rpg:michael_boss/lose
execute unless entity @e[type=minecraft:vindicator,tag=rpg.mkb,tag=!rpg.mk.preview,distance=..120] run return run function rpg:michael_boss/lost_unit
bossbar set rpg:michael_boss players @a[distance=..48]
# 守望者：数一数；还有活着的，场上的人就「被看见」（发光）
execute store result score #w rpg_mk if entity @e[type=minecraft:vindicator,tag=rpg.mkb.w,distance=..80]
scoreboard players operation #m rpg_mk = #tick rpg_mk
scoreboard players set #k rpg_mk 10
scoreboard players operation #m rpg_mk %= #k rpg_mk
execute if score #m rpg_mk matches 0 if score #w rpg_mk matches 1.. run effect give @a[distance=..40,gamemode=!spectator,gamemode=!creative] minecraft:glowing 1 0 true
scoreboard players operation #m rpg_mk = #tick rpg_mk
scoreboard players set #k rpg_mk 20
scoreboard players operation #m rpg_mk %= #k rpg_mk
# 守望者全死时，落点招式瞄的是这个标记：每秒挪到玩家那里一次（约 1 秒前的位置）
execute if score #m rpg_mk matches 0 as @e[type=minecraft:marker,tag=rpg.mkb.lag,limit=1,predicate=!rpg:in_prologue] at @e[tag=rpg.unit.f,distance=..40,sort=nearest,limit=1] run tp @s ~ ~ ~
execute as @e[type=minecraft:vindicator,tag=rpg.mkb,tag=!rpg.mk.preview,distance=..120] at @s run function rpg:michael_boss/unit
execute as @e[type=minecraft:vindicator,tag=rpg.mkb.w,distance=..80] at @s run function rpg:michael_boss/watch/tick
execute as @e[tag=rpg.mkb.fx,distance=..120] at @s run function rpg:michael_boss/fx/tick
execute as @e[tag=rpg.unit,tag=rpg.mkb.flamed,predicate=!rpg:in_prologue] at @s run function rpg:michael_boss/flame/tick
execute if score #stage rpg_mk matches 2 as @e[tag=rpg.mkb.pillar,predicate=!rpg:in_prologue] at @s run function rpg:michael_boss/pillar/clock
execute as @e[tag=rpg.unit,tag=rpg.mkb.pend,predicate=!rpg:in_prologue] run function rpg:michael_boss/hit/settle
execute as @e[tag=rpg.unit,predicate=!rpg:in_prologue] run scoreboard players operation @s rpg_mk_dd0 = @s rpg_mk_dd
function rpg:michael_boss/music/tick
